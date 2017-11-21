# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from django.contrib.admin import SimpleListFilter

# Register your models here.

class ProductFilter(SimpleListFilter):
    title = ('Product Stock')
    parameter_name = 'stock'
    # Set the displaying options
    def lookups(self, request, model_admin):
        return (
            ('100', ('Less than 100 numbers')),
            ('20', ('Less than 20 numbers')),
            ('0', ('Out od Stock')),
        )
    # Assign a query for each option
    def queryset(self, request, queryset):
        queryset = Product.objects.all()
        if self.value() == '100':
            return queryset.filter(quantity__lte = 100)
        elif self.value() == '20':
        	return queryset.filter(quantity__lte =  20)
        elif self.value() == '0':
        	return queryset.filter(quantity = 0)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
        list_display = ('name','product_code', 'availability', 'manufacturer', 'price', 'quantity','product_rating')
        readonly_fields = ('slug','product_code', 'availability')
        search_fields = ('name', 'product_code')
        list_filter = [ProductFilter,]

        fieldsets = (
        ('General', {
            'fields': ('name','product_code', 'product_type','slug', 'description', 'manufacturer', 'photo')
        }),
        ('Variables', {
            'fields': ('price','availability','quantity')
        }),
    )

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
        list_display = ('name','manufacturer_code')
        search_fields = ('name','manufacturer_code')
        
@admin.register(ProductRating)
class RatingAdmin(admin.ModelAdmin):
	pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	pass