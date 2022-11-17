from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_price', 'product_stock', 'product_category', 'product_modified_date', 'product_is_available']
    prepopulated_fields = {'product_slug': ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value', 'is_active']
    list_editable = ['is_active']
    list_filter =  ['product', 'variation_category', 'variation_value', 'is_active'] 

admin.site.register(ProductModel, ProductAdmin)
admin.site.register(VariationModel, VariationAdmin)