from core.models import CartOrderItems, Product, Category, Vendor, CartOrder, ProductImages, ProductReview, wishlist_model, Address, Vendor
from django.db.models import Min, Max
from django.contrib import messages

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    try:
        wishlist = wishlist_model.objects.filter(user=request.user)
    except:
        messages.warning(request, "You need to log in before accessing your wishlist.")        
        wishlist = 0

    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None


    return {
        'categories':categories,'wishlist':wishlist,'address':address,'vendors':vendors,'min_max_price':min_max_price,
    }