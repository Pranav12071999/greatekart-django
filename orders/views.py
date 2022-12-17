from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import *
from carts.models import *
import datetime
import json

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.

def payments(request):
    body = json.loads(request.body)
    # Saving data inside PaymentModel
    order = OrderModel.objects.get(user = request.user, is_ordered = False, order_number = body['orderID'])
    payment = PaymentModel(
        user = request.user,
        payment_id = body['transID'],   
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    # Now as OrderModel also has payment foreingkey with PaymentModel so update that also.
    order.payment = payment
    order.is_ordered = True
    order.status = 'COMPLETED'
    order.save()

    # Moving cart_items to OrderProduct model
    cart_items = CartItem.objects.filter(user = request.user)
    print(f'Cart items = {cart_items}')
    for item in cart_items:
        print(f'Items = {item}')
        orderproduct = OrderProductModel()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user = request.user
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.product_price
        orderproduct.ordered = True
        orderproduct.save() # Here we are not saving variations because variations are many to many field and it has saved after saving the object.

        # Setting Varations

        cart_item = CartItem.objects.get(id = item.id)
        orderproduct = OrderProductModel.objects.get(id = orderproduct.id)
        
        product_variations = cart_item.variations.all()
        orderproduct.variation.set(product_variations)
        orderproduct.save()

        # Reducing quantity of Original Product
        product = ProductModel.objects.get(id = orderproduct.product_id)
        product.product_stock -= item.quantity
        product.save()

    # Clear the cart as items are already ordered
    CartItem.objects.filter(user = request.user).delete()

    # Sending Order received email to user
    mail_subject = "Thank you for ordering from GreatCart !!"
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order':order
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to = [to_email])
    send_email.send()

    # Sending data in JSON format to the payment.html
    data = {
        'order_number': order.order_number,
        'transID':payment.payment_id
    }
    return JsonResponse(data) # Sending this data back to payment.html

    return render(request, 'orders/payment.html')
def place_order(request):
    form = OrderForm(request.POST)
    cart_items = CartItem.objects.filter(user = request.user, is_active = True)
    # Checking whether user added atlease sinle component in cart or not, if not then redirect him to store page
    cart_item_count = cart_items.count()
    total = 0
    tax = 0
    grand_total = 0
    quantity = 0
    if cart_item_count <= 0:
        return redirect('store_homepage')
    else:
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = round(0.02 * total) 
        grand_total = total + tax
        if form.is_valid():
            data = OrderModel()
            data.user = request.user
            data.first_name = form.cleaned_data['first_name']
            
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Start Generating order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.datetime(yr,mt,dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            # Fetching order from database for review
            order = OrderModel.objects.get(user = request.user, is_ordered = False, order_number = order_number)
            context = {
                'order':order,
                'cart_items':cart_items,
                'tax':tax,
                'grand_total':grand_total,
                'total':total
            }
            return render(request, 'orders/payment.html', context)
        else:
            return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = OrderModel.objects.get(order_number = order_number, is_ordered = True)
        order_products = OrderProductModel.objects.filter(order_id = order.id)
        payment = PaymentModel.objects.get(payment_id = transID)

        subtotal = 0
        for item in order_products:
            subtotal += item.product_price * item.quantity

        context = {
            'order':order,
            'order_products':order_products,
            'order_number' : order.order_number,
            'transID': payment.payment_id,
            'subtotal':subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (OrderModel.DoesNotExist, PaymentModel.DoesNotExist):
        return redirect ('index')