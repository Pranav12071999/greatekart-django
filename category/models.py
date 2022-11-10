from django.db import models
from django.urls import reverse

# Create your models here.
class CategoryModel(models.Model):
    category_name = models.CharField(max_length = 150, unique = True)
    category_slug = models.SlugField(max_length = 150, unique = True)
    category_description = models.TextField(blank = True)
    category_image = models.ImageField(upload_to = 'photoes/categories/', blank = True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def get_url(self):
        return reverse('sort_by_category', args = [self.category_slug])

    def __str__(self):
        return self.category_name
    