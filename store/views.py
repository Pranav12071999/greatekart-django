from django.shortcuts import render, get_object_or_404
from .models import *
from category.models import *
# Create your views here.
def StoreHomePageView(request, category_slug = None):
    if category_slug != None:
        category = get_object_or_404(CategoryModel, category_slug = category_slug)
        products = ProductModel.objects.filter(product_category = category, product_is_available = True)
    else:
        products = ProductModel.objects.all().filter(product_is_available = True)
    product_count = len(products)
    context = {'products':products, 'product_count':product_count}
    return render(request, 'store/storehomepage.html',context)

def DetailProductView(request, category_slug, product_slug):
    try:
        single_product = ProductModel.objects.get(product_category__category_slug = category_slug, product_slug = product_slug) # Here from product_category we can access the category slu inside CategoryModel by ** product_category__category_slug **
        if single_product.product_stock <= 0:
            out_of_stock = True
        else:
            out_of_stock = False
        context = {'single_product':single_product, 'out_of_stock':out_of_stock}

    except Exception as e:
        print(e)
        context = {}
    
    return render(request, 'store/detail_product.html', context)