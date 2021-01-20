from django.db import models


class ImportSource(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    importsource = models.ForeignKey(ImportSource, models.SET_NULL, null=True, blank=True)
    account = models.CharField(max_length=30)
    date = models.DateField()
    order = models.IntegerField()
    count = models.IntegerField()
    day = models.IntegerField(null=True, blank=True, db_index=True)
    week = models.IntegerField(null=True, blank=True, db_index=True)
    month = models.IntegerField(null=True, blank=True, db_index=True)
    year = models.IntegerField(null=True, blank=True, db_index=True)
    title = models.CharField(max_length=245)
    subcategory = models.ForeignKey('SubCategory', models.SET_NULL, null=True, blank=True)
    ttype = models.CharField(null=True, blank=True, db_index=True, max_length=10)
    value = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        indexes = [
            models.Index(fields=['account', 'date', 'title', 'ttype', 'value', 'count']),
            models.Index(fields=['subcategory']),
        ]
        unique_together = [['account', 'date', 'title', 'ttype', 'value', 'count']]


class Category(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey('Category', models.SET_NULL, blank=True, null=True)
    include_in_budget = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TitleToSubCategoryMap(models.Model):
    title_search_expression = models.CharField(max_length=100, null=True)
    subcategory = models.ForeignKey('SubCategory', null=True, on_delete=models.PROTECT)
    priority = models.IntegerField(null=True)
    min_value = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    max_value = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    type_restriction = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return '(' + self.title_search_expression + ')'

class Stock(models.Model):
    symbol = models.CharField(max_length=30)
    company_overview = models.JSONField(default="{'Name':'none', 'Symbol': 'none' }")
   
    def __str__(self):
        return self.company_overview.Name + ' (' + self.company_overview.Symbol + ')'
    
