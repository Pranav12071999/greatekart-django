from django.contrib import admin
from .models import *

# This class is used to make OrderProductModel come inside OrderModel Table by matching order_number
class OrderProductModelInline(admin.TabularInline):
    model = OrderProductModel
    readonly_fields = ['payment', 'user', 'product', 'quantity', 'product_price', 'ordered']
    extra = 0 # This extra means at every table there are 3 extra rows automatically added there so that to remove that we nedd to make it 0.
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['user','order_number','full_name','phone','email','order_total','tax','status','created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number','first_name','last_name','phone','email']
    list_per_page = 20
    inlines = [OrderProductModelInline]
# Register your models here.
admin.site.register(PaymentModel)
admin.site.register(OrderModel, OrderModelAdmin)
admin.site.register(OrderProductModel)