from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Avg
from customorder.models import CustomProduct, ProductType,Swatch,SwatchColor,CustomProduct
from userauths.models import Profile
#from core.forms import

# Create your views here.

def custom_order_proto(request):
    product_types = ProductType.objects.all()
    swatches = Swatch.objects.all()

    service_choices = CustomProduct.SERVICE_CHOICE    
    context = {
        'product_types':product_types,
        'swatches':swatches,
        'service_choices': service_choices,
    }

    return render(request, "customorder/customorder-proto.html", context)

