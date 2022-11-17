from django.shortcuts import render, get_object_or_404
from .models import *
from category.models import *
from carts.views import *
from carts.views import _cart_id
from carts.models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from store.models import *
# Create your views here.
def StoreHomePageView(request, category_slug = None):
    if category_slug != None:
        category = get_object_or_404(CategoryModel, category_slug = category_slug)
        products = ProductModel.objects.filter(product_category = category, product_is_available = True)
        paginator = Paginator(products, 2) # Among all products it will choose first 2 of them
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = ProductModel.objects.all().filter(product_is_available = True).order_by('id')
        paginator = Paginator(products, 6) # Among all products it will choose first 6 of them
        page = request.GET.get('page')
        paged_products = paginator.get_page(page) # This will get page number from url of browser.
    product_count = len(products)
    context = {'products':paged_products, 'product_count':product_count}
    return render(request, 'store/storehomepage.html',context)

def DetailProductView(request, category_slug, product_slug):
    
    try:
        single_product = ProductModel.objects.get(product_category__category_slug = category_slug, product_slug = product_slug) # Here from product_category we can access the category slu inside CategoryModel by ** product_category__category_slug **
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = single_product).exists()
        color_variations = VariationModel.objects.all().filter(product = single_product, variation_category = 'color')
        size_variations = VariationModel.objects.all().filter(product = single_product, variation_category = 'size')
        if single_product.product_stock <= 0:
            out_of_stock = True
        else:
            out_of_stock = False
        

    except Exception as e:
        raise e
    context = {'single_product':single_product, 
    'out_of_stock':out_of_stock, 
    'in_cart':in_cart,
    'color_variations':color_variations,
    'size_variations':size_variations
    } 
    
    return render(request, 'store/detail_product.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        print(f'keyword is {keyword}')
        if keyword:
            products = ProductModel.objects.order_by('-product_created_date').filter(Q(product_description__icontains = keyword) | Q(product_name__icontains = keyword))
            product_count = products.count()
    context = {'products':products, 'product_count':product_count}
    return render(request, 'store/storehomepage.html', context)