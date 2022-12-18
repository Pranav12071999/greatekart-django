from django.shortcuts import render, get_object_or_404
from .models import *
from category.models import *
from carts.views import *
from carts.views import _cart_id
from carts.models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from store.models import *
from .forms import *
from django.contrib import messages
from orders.models import *
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
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProductModel.objects.filter(user = request.user, product__product_slug = product_slug).exists()
        except OrderProductModel.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Printing reviews for this product
    try:
        reviews = ReviewModel.objects.filter(product__product_slug = product_slug, status = True) # This status is true filter is for let us say admin wants to not show any comment then he will make status = False from backend.
    except ReviewModel.DoesNotExist:
        reviews = None
    context = {'single_product':single_product, 
    'out_of_stock':out_of_stock, 
    'in_cart':in_cart,
    'color_variations':color_variations,
    'size_variations':size_variations,
    'orderproduct':orderproduct,
    'reviews':reviews,
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

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER') # This will give us current url
    try:
        # This try block is for if that user gives review for this product previously then it will update the review.
        review = ReviewModel.objects.get(user__id = request.user.id, product__id = product_id)
        form = ReviewForm(request.POST, instance=review)
        form.save()
        messages.success(request, 'Your Review is updated successfully !!')
        return redirect(url)
    except ReviewModel.DoesNotExist:
        # If review is not there before then create new review
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = ReviewModel()
            data.subject = form.cleaned_data['subject']
            data.review = form.cleaned_data['review']
            data.rating = form.cleaned_data['rating']
            data.ip = request.META.get('REMOTE_ADDR') # This will sae an ip address of your computer
            data.product_id = product_id
            data.user_id = request.user.id
            data.save()
            messages.success(request, 'Your review added successfully')
            return redirect(url)
    
