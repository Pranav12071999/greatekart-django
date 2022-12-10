from django.db import models
from store.models import *
from accounts.models import *
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length = 250, blank = True)
    cart_date_added = models.DateField(auto_now_add = True)

    def __str__(self) -> str:
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductModel, on_delete = models.CASCADE)
    variations = models.ManyToManyField(VariationModel,blank = True) # Manytomany is because many products have many variations
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default = True)

    def sub_total(self):
        total = self.product.product_price * self.quantity
        return total

    def __unicode__(self):
        return self.product