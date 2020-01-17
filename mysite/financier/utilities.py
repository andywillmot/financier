from . import models
import pdb


def map_category(title, value, ttype):

    for m in models.TitleToSubCategoryMap.objects.all().order_by('-priority'):

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
