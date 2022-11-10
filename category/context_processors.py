from . models import *

def menu_links(request):
    links = CategoryModel.objects.all()
    return dict(links = links)