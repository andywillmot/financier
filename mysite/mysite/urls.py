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
import pdb
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from financier.models import Transaction, SubCategory
from rest_framework import routers, serializers, viewsets
from financier.utilities import map_category

from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)

from rest_framework_bulk.routes import BulkRouter

# Serializers define the API representation.


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name']


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class TransactionSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta(object):
        model = Transaction
        list_serializer_class = BulkListSerializer
        fields = ['account', 'date', 'order', 'title', 'ttype', 'value', 'subcategory']
        read_only_fields = ['subcategory']

# ViewSets define the view behavior.
#class TransactionViewSet(viewsets.ModelViewSet):
#    queryset = Transaction.objects.all()
#    serializer_class = TransactionSerializer
#    def perform_create(self, serializers):
#        subcategory = None
#        if self.request:
#            subcategory = map_category(serializers.validated_data['title'],
#                                       serializers.validated_data['value'],
#                                       serializers.validated_data['ttype'])
#        serializers.save(subcategory=subcategory)

class TransactionView(ListBulkCreateUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializers):
        subcategory = None
        if self.request:
            subcategory = map_category(serializers.validated_data['title'],
                                       serializers.validated_data['value'],
                                       serializers.validated_data['ttype'])
        serializers.save(subcategory=subcategory)

class TransactionViewSet(BulkModelViewSet):
    model = Transaction

    def allow_bulk_destroy(self, qs, filtered):
        """Don't forget to fine-grain this method"""
        pass
    
    def perform_create(self, serializers):
        subcategory = None
        if self.request:
            subcategory = map_category(serializers.validated_data['title'],
                                       serializers.validated_data['value'],
                                       serializers.validated_data['ttype'])
        serializers.save(subcategory=subcategory)

router = BulkRouter()
router.register(r'transactions', TransactionViewSet)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
#router.register(r'transactions', TransactionViewSet)
router.register(r'subcategorys', SubCategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
]
