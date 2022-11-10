from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_price', 'product_stock', 'product_category', 'product_modified_date', 'product_is_available']
    prepopulated_fields = {'product_slug': ('product_name',)}

    

admin.site.register(ProductModel, ProductAdmin)