from django.db import models
from category.models import *
from django.urls import reverse
# Create your models here.
class ProductModel(models.Model):
    product_name                = models.CharField(max_length = 100, unique = True)
    product_slug                = models.SlugField(max_length = 100, unique = True)
    product_description         = models.TextField(blank = True)
    product_price               = models.IntegerField()
    product_image               = models.ImageField(upload_to = 'photoes/products')
    product_stock               = models.IntegerField()
    product_is_available        = models.BooleanField(default = True)
    product_category            = models.ForeignKey(CategoryModel, on_delete = models.CASCADE)
    product_created_date        = models.DateTimeField(auto_now_add = True)
    product_modified_date       = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name = 'Product models'
        verbose_name_plural = 'Products'
    
    def get_url(self):
        return reverse ('detail_product_view', args=[self.product_category.category_slug, self.product_slug])
    
    
    def __str__(self):
        return self.product_name
variation_category_choice = (
    ('color', 'color'),
    ('size', 'size')
)
class VariationModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete = models.CASCADE)
    variation_category = models.CharField(max_length = 100, choices = variation_category_choice)
    variation_value = models.CharField(max_length = 100)
    is_active = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return self.variation_value