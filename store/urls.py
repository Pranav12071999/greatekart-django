
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.StoreHomePageView, name = 'store_homepage'),
    path('search/', views.search, name = 'search'),
    path('category/<slug:category_slug>/', views.StoreHomePageView, name = 'sort_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.DetailProductView, name = 'detail_product_view'),
    path('submit_review/<int:product_id>/', views.submit_review, name = 'submit_review'),
    
]