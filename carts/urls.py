from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartHomePageView, name = 'cart_home_page'),
    path('add_cart/<int:product_id>', views.add_cart, name = 'add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>', views.remove_cart, name = 'remove_cart'),
    path('remove_cart_items/<int:product_id>', views.remove_cart_items, name = 'remove_cart_items'),
]   