from django.shortcuts import render
from django_filters import FilterSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import HyperlinkedRelatedField
from rest_framework_json_api import filters
from rest_framework import routers, viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from financier.models import Transaction, SubCategory
from financier.utilities import map_category,requires_scope,requires_auth
import logging

logger = logging.getLogger(__name__)

# Serializers
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'description', 'include_in_budget')


class SubCategoryFilter(FilterSet):
    class Meta:
        model = SubCategory
        fields = {
                'id': ['exact','in'],
        }


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filterset_class = SubCategoryFilter


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('account', 'date', 'order', 'count', 'title', 'ttype', 'subcategory_id', 'value')

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

#    @requires_auth
    def list(self, request, *args, **kwargs):
        
        data = super().list(request)
        meta_data = data.data.pop('meta')
        data.data['meta'] = {'total': meta_data['pagination']['count']}
        return(data)


    def create(self, request, *args, **kwargs):

        if isinstance(request.data, list):
            invalid_rows = 0
            serial_list = []
            for row in request.data:

                serializer = self.get_serializer(data=row)
                if serializer.is_valid(raise_exception=False):
                    serial_list.append(serializer)
                else:
                    invalid_rows = invalid_rows + 1

            for validated_serializer in serial_list:
                self.perform_create(validated_serializer)

            return Response("{Response: Multiple rows created. " + str(invalid_rows) + " invalid rows}", status=status.HTTP_201_CREATED, headers="")
        else:
            super(TransactionViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializers):
        subcategory = None
        if serializers.validated_data.get('title') is None:
            print("missing title?")
            print(serializers.validated_data)
            exit(1)

        if self.request:
            subcategory = map_category(serializers.validated_data['title'],
                                       serializers.validated_data['value'],
                                       serializers.validated_data['ttype'])
        serializers.save(subcategory=subcategory)


