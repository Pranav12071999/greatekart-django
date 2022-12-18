from django.db import models
from category.models import *
from django.urls import reverse
from accounts.models import *
from django.db.models import Avg,Count
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
    
    def average_rating(self):
        reviews = ReviewModel.objects.filter(product = self, status = True).aggregate(average = Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    def review_counter(self):
        reviews = ReviewModel.objects.filter(product = self, status = True).aggregate(count = Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = float(reviews['count'])
        return count
    
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

class ReviewModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank = True)
    review = models.TextField(max_length=100, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=100, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.subject