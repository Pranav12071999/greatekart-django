
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.StoreHomePageView, name = 'store_homepage'),
    path('<slug:category_slug>/', views.StoreHomePageView, name = 'sort_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.DetailProductView, name = 'detail_product_view'),
]