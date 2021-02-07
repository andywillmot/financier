from django.http import HttpResponse
from django.conf import settings
from financier.models import TitleToSubCategoryMap
import pdb
from functools import wraps
import jwt
import logging
from urllib.request import urlopen
import json
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend


logger = logging.getLogger(__name__)

def map_category(title, value, ttype):

    for m in TitleToSubCategoryMap.objects.all().order_by('-priority'):

        if m.max_value is None:
            maxvalue = 9999999
        else:
            maxvalue = m.max_value

        if m.min_value is None:
            minvalue = 0
        else:
            minvalue = m.min_value

        if m.type_restriction is None:
            ttypevalue = ""
        else:
            ttypevalue = m.type_restriction

        if m.title_search_expression.upper() in title.upper():
            if minvalue <= abs(float(value)) and maxvalue >= abs(float(value)):
                if ttypevalue == "" or ttypevalue == ttype:
                    return m.subcategory

    return None


def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization')
    if not auth:
        return None, "Authorization header is expected"
    
    parts = auth.split()

    if parts[0].lower() != "bearer":
        return None, "<html><body>Authorization header must start with bearer</html></body>"
    elif len(parts) == 1:
        return None, "<html><body>Token not found</html></body>"
    elif len(parts) > 2:
        return None, "<html><body>Authorization header must be Bearer token</html></body>"

    token = parts[1]
    return token, ""


def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(self, request, *args, **kwargs):

        token, error = get_token_auth_header(request)
        if token is None:
            return HttpResponse("401 Not Authorized: " + error, status=401)

        jsonurl = urlopen(settings.API_ISSUER + ".well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_cert = bytearray("-----BEGIN CERTIFICATE-----\n" + str(key["x5c"][0]) + "\n-----END CERTIFICATE-----", "utf-8")
                rsa_cert_obj = load_pem_x509_certificate(rsa_cert, default_backend())
                rsa_key = rsa_cert_obj.public_key()
#                    "alg": key["alg"],
 #                   "kty": key["kty"],
  #                  "kid": key["kid"],
   #                 "use": key["use"],
    #                "n": key["n"],
     #               "e": key["e"],
      #              "x5c": key["x5c"]
    
        if rsa_key:
            try:
                #logger.warning("rsa_key: " + str(thekey))
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"], # settings.API_ALGORITHMS,
                    audience=settings.API_AUDIENCE,
                    issuer=settings.API_ISSUER
                )
            except jwt.ExpiredSignatureError:
                return HttpResponse("401 Not Authorized: token has expired" + error, status=401)
            except jwt.MissingRequiredClaimError:
                return HttpResponse("401 Not Authorized: incorrect claims, please check the audience and issuer" + error, status=401)
            except jwt.InvalidAlgorithmError:
                logger.error("Invalid algorithm: " + str(token))
                return HttpResponse("401 Not Authorized: Unable to parse authentication token" + error, status=401)                
 #           except Exception:
 #               return HttpResponse("401 Not Authorized: Unable to parse authentication token" + error, status=401)

#            _request_ctx_stack.top.current_user = payload
            return f(self, request, *args, **kwargs)
        return HttpResponse("401 Not Authorized: Unable to find appropriate key" + error, status=401)
    return decorated

def requires_scope(request, required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header(request)
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            for token_scope in token_scopes:
                if token_scope == required_scope:
                    return True
    return False
