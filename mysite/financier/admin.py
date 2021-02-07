from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from . import models
from . import utilities


def categorise_transaction(modeladmin, request, queryset):
    for q in queryset:
        q.subcategory = utilities.map_category(q.title, q.value, q.ttype)
        q.save()


class TitleToSubCategoryMapResource(resources.ModelResource):
    class Meta:
        model = models.TitleToSubCategoryMap


class TransactionResource(resources.ModelResource):
    class Meta:
        model = models.Transaction


class CategoryResource(resources.ModelResource):
    class Meta:
        model = models.Category


class SubCategoryResource(resources.ModelResource):
    class Meta:
        model = models.SubCategory

# Register your models here.
class TransactionAdmin(ImportExportModelAdmin):
    resource_class = TransactionResource
    actions = [categorise_transaction]
    list_display = (
        'id',
        'account',
        'date',
        'order',
        'title',
        'subcategory',
        'ttype',
        'value',
    )
    ordering = ['date','order']
    list_filter = (
        'date',
        'account',
        'subcategory',
        'ttype',
        'value',
    )


class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('id', 'name', 'description')
    list_filter = ('id', 'name')
    search_fields = ('name',)


class SubCategoryAdmin(ImportExportModelAdmin):
    resource_class = SubCategoryResource
    list_display = ('id', 'name', 'category', 'include_in_budget')
    list_filter = ('category', 'include_in_budget')
    search_fields = ('name','category__name')


class TitleToSubCategoryMapAdmin(ImportExportModelAdmin):
    resource_class = TitleToSubCategoryMapResource
    list_display = (
        'id',
        'title_search_expression',
        'subcategory',
        'priority',
        'min_value',
        'max_value',
        'type_restriction',
    )
    list_filter = (
        'id',
        'title_search_expression',
        'subcategory',
        'priority',
        'min_value',
        'max_value',
        'type_restriction',
    )


class StockAdmin(admin.ModelAdmin):
    pass



def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Transaction, TransactionAdmin)


_register(models.Category, CategoryAdmin)


_register(models.SubCategory, SubCategoryAdmin)


_register(models.TitleToSubCategoryMap, TitleToSubCategoryMapAdmin)


_register(models.Stock,StockAdmin)