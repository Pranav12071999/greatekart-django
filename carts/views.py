from django.shortcuts import render, redirect
from store.models import *
from .models import *
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
# This function is used to fetch or create the session key 
def _cart_id(request):
    # This will try to fetch the session key from browser.
    cart = request.session.session_key
    # If he doesn't found session key then it will try to create new one
    if not cart:
        cart = request.session.create()
    return cart
def add_cart(request, product_id):
    #print(f'Product id ****************************** = {product_id}')
    product = ProductModel.objects.get(id = product_id)
    variation_lst = []
    if request.method == 'POST':
        for item in request.POST:
            key = item # color
            value = request.POST[key] # black
            # This is for checking whether user selected values matches with admin panel or not.
            try:
                variation = VariationModel.objects.get(product = product, variation_category__iexact = key, variation_value = value)
                variation_lst.append(variation)
            except:
                pass
     # Fetching product from product_id
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request)) # getting cart from Cart model.
    # if cart is not registered then then it will create new one.
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    # Then accessing the cart_item from model CartItem
    # Checking that whether there is cart items present inside cart or not
    is_cart_item_exist = CartItem.objects.filter(product = product, cart = cart).exists()
    if is_cart_item_exist:
        cart_items = CartItem.objects.filter(product = product, cart = cart)
        existing_variations = [] # Creating empty existing_variations list for checking which variations available inside cart
        id = [] # this list made for taking id of the items this will help us while increasing quantity of the product which has same variation
        for item in cart_items:
            ex_variations = item.variations.all()
            existing_variations.append(list(ex_variations))
            id.append(item.id)
        if variation_lst in existing_variations:
            index = existing_variations.index(variation_lst)
            item_index = id[index]
            item = CartItem.objects.get(product = product, id = item_index)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product = product, quantity = 1, cart = cart)
            if len(variation_lst) > 0:
                item.variations.clear()
                item.variations.add(*variation_lst) # This will add the variation inside the cart_item model.
            item.save()
    # If any cart_item is not found then it will create new cart_item.
    else:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1
        )
        if len(variation_lst) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*variation_lst) # This will add the variation inside the cart_item model.   
        cart_item.save()
    return redirect ('cart_home_page')

def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = ProductModel.objects.get(id = product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart, id = cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_home_page')

def remove_cart_items(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = ProductModel.objects.get(id = product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)
    cart_item.delete()
    return redirect('cart_home_page')

def CartHomePageView(request, total = 0, quantity = 0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = round(0.02 * total) 
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass # just ignore
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,  
        'grand_total':grand_total
    }
    return render(request, 'store/cart_home.html', context)