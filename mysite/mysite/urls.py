"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from financier.models import Transaction, SubCategory
from rest_framework import routers, serializers, viewsets, status
from rest_framework.response import Response
from financier.utilities import map_category


# Serializers define the API representation.


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name']


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta(object):
        model = Transaction
        fields = ['account', 'date', 'order', 'count', 'title', 'ttype', 'value', 'subcategory', 'importsource']
        read_only_fields = ['subcategory', 'importsource']


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):

        if isinstance(request.data, list):
            serial_list = []
            for row in request.data:
                serializer = self.get_serializer(data=row)
                serializer.is_valid(raise_exception=True)
                serial_list.append(serializer)

            for validated_serializer in serial_list:
                self.perform_create(validated_serializer)

            return Response("{Response: Multiple rows created}", status=status.HTTP_201_CREATED, headers="")
        else:
            super(TransactionViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializers):
        subcategory = None
        if self.request:
            subcategory = map_category(serializers.validated_data['title'],
                                       serializers.validated_data['value'],
                                       serializers.validated_data['ttype'])
        serializers.save(subcategory=subcategory)


router = routers.DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register(r'subcategorys', SubCategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
]
