from django.shortcuts import render
from store.models import *
def index(request):
    products = ProductModel.objects.filter(product_is_available = True)
    context = {'products':products}
    return render(request, 'index.html', context)