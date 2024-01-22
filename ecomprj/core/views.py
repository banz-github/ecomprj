
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Avg
from taggit.models import Tag
from core.models import CartOrderItems, Product, Category, Vendor, CartOrder, ProductImages, ProductReview, wishlist_model, Address
from userauths.models import ContactUs, Profile
from core.forms import ProductReviewForm
from django.template.loader import  render_to_string
#GROUPS
from django.contrib.auth.models import Group

from django.contrib import messages
from django.core import serializers
import calendar
from django.db.models.functions import ExtractMonth

from customorder.models import ProductType, Swatch, SwatchColor, CustomProduct

#from .decorators import function_name,function_name1, allowed_users
from .decorators import allowed_users
#from pt
#import pdfkit

#trial for customizationorder
from django.db.models.functions import TruncMonth
from customorder_prototype2.models import CustomizationOrder
#trial for customizationorder



##paypal


from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm

# admin dashboard 
#@allowed_users(allowed_roles=['admin'])
@allowed_users(allowed_roles=['admin'])
def admindash(request):
    message_list = ContactUs.objects.all()
    # order_list = CartOrder.objects.filter(profile=request.user.profile).order_by("-id")[:5] #mark, do not change if it works tho
    # order_list = CartOrder.objects.all().order_by("-id")[:5] #mark, do not change if it works tho
    order_list = get_object_or_404(CartOrder, id=id)
    
    context = {
        "order_list":order_list,"message_list":message_list,
    }

    return render(request, 'admindash/main-dash.html',context)

from django.db.models import Count
@allowed_users(allowed_roles=['admin'])
def admindash_orders(request):
    message_list = ContactUs.objects.all()
    # order_list = CartOrder.objects.filter(profile=request.user.profile).order_by("-id") #mark, do not change if it works tho
    
    # order_list = CartOrder.objects.all()
    order_list = CartOrder.objects.all().order_by("-id")#[:10] #NakaCAP LANG

    # Similar analytics as in customer_dashboard
    # orders = CartOrder.objects.filter(profile=request.user.profile).annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    orders = CartOrder.objects.all().annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    month = []
    total_orders = []

    for i in orders:
        month.append(calendar.month_name[i["month"]])
        total_orders.append(i["count"])

    context = {
        "order_list": order_list,
        "message_list": message_list,
        "month": month,
        "total_orders": total_orders,
    }


    # New code for pie chart data
        # New code for pie chart data
    category_orders = CartOrderItems.objects.values('category__title').annotate(count=Count('id'))

    category_labels = []
    category_data = []

    for category_order in category_orders:
        category_labels.append(category_order['category__title'])
        category_data.append(category_order['count'])

    context["category_labels"] = category_labels
    context["category_data"] = category_data

    return render(request, 'admindash/orders-dash.html', context)


from django.shortcuts import render, get_object_or_404
@allowed_users(allowed_roles=['admin'])
def order_detail_maindash(request, id):
    # order = get_object_or_404(CartOrder, profile__user__id=request.user.id, id=id)

    order = get_object_or_404(CartOrder, id=id)

    order_items = CartOrderItems.objects.filter(order=order)
    context = {
        'order': order, "order_items":order_items,
    }

    return render(request, 'admindash/order-detail-maindash.html', context)



# views.py


from django.db.models import Sum

@allowed_users(allowed_roles=['admin'])
def admindash_custom_orders(request):
    custom_order_list = CustomizationOrder.objects.all()
    custom_order_list2 = list(CustomizationOrder.objects.all())
    # Fetch most ordered product types with total quantity
    most_ordered_product_types = get_most_ordered_product_types()
    most_ordered_product_types2 = list(get_most_ordered_product_types())
    context = {
        "custom_order_list": custom_order_list,
        "most_ordered_product_types": most_ordered_product_types,
    }

    return render(request, 'admindash/custom-orders-dash.html', context)

def get_most_ordered_product_types():
    # Returns a queryset of product types with the total quantity
    return CustomizationOrder.objects.values('product_type__name').annotate(
        total_quantity=Sum('qty')
    ).order_by('-total_quantity')[:5]
def get_most_ordered_product_types():
    # Returns a queryset of product types with the most orders multiplied by quantity
    return CustomizationOrder.objects.values('product_type__name').annotate(
        total_orders=F('qty') * Count('id')
    ).order_by('-total_orders')[:5]
def get_most_ordered_product_types():
    # Returns a queryset of product types with the most orders and total quantity
    return CustomizationOrder.objects.values('product_type__name').annotate(
        total_orders=Count('id'),
        total_quantity=Sum('qty')
    ).order_by('-total_orders')[:5]

###############MOST ORDERED MATERIALS
def most_ordered_materials(request, product_type):
    materials = get_most_ordered_materials(product_type)

    

    context = {
        'product_type': product_type,
        'most_ordered_materials': materials,
    }
    return render(request, 'admindash/most-ordered-materials.html', context)

def get_most_ordered_materials(product_type):
    # Returns a queryset of materials for a specific product type with the total quantity
    return CustomizationOrder.objects.filter(product_type__name=product_type).values('material__name').annotate(
        total_quantity=Sum('qty')
    ).order_by('-total_quantity')[:5]
###############MOST ORDERED MATERIALS


##### MOST ORDERED COLORS IN THE MATERIAL
def most_ordered_colors(request, product_type, material_name):
    colors = get_most_ordered_colors(product_type, material_name)

    context = {
        'product_type': product_type,
        'material_name': material_name,
        'most_ordered_colors': colors,
    }
    return render(request, 'admindash/most-ordered-colors.html', context)

def get_most_ordered_colors(product_type, material_name):
    # Returns a queryset of colors for a specific material with the total quantity
    return CustomizationOrder.objects.filter(
        product_type__name=product_type,
        material__name=material_name
    ).values('color__name').annotate(
        total_quantity=Sum('qty')
    ).order_by('-total_quantity')[:5]
##### MOST ORDERED COLORS IN THE MATERIAL

#This one below is working

from customorder_prototype2.forms import CustomOrderUpdateForm
from django.contrib import messages


# @allowed_users(allowed_roles=['admin'])
# def custom_order_detail_dashboard(request, co_id):


#     coi_details = CustomizationOrder.objects.filter(co_id=co_id)

#     context = {"coi_details":coi_details,}
#     return render(request,'admindash/custom_order_detail_dashboard.html', context)

# @allowed_users(allowed_roles=['admin'])
# def custom_order_detail_dashboard(request, co_id):
#     coi_details = get_object_or_404(CustomizationOrder, co_id=co_id)

#     if request.method == 'POST':
#         form = CustomOrderUpdateForm(request.POST, instance=coi_details)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Custom order details updated successfully.')
#             return redirect('your_redirect_view_name')  # Replace with the appropriate view name
#     else:
#         form = CustomOrderUpdateForm(instance=coi_details)

#     context = {"coi_details": coi_details, "form": form}
#     return render(request, 'admindash/custom_order_detail_dashboard.html', context)

@allowed_users(allowed_roles=['admin'])
def custom_order_detail_dashboard(request, co_id):
    coi_details = CustomizationOrder.objects.filter(co_id=co_id)
    coi_details1 = get_object_or_404(CustomizationOrder, co_id=co_id)

    if request.method == 'POST':
        form = CustomOrderUpdateForm(request.POST, instance=coi_details1)
        if form.is_valid():
            form.save()
            messages.success(request, 'Custom order details updated successfully.')
            return redirect('core:custom-orders-dash')  # Replace with the appropriate view name
    else:
        form = CustomOrderUpdateForm(instance=coi_details1)

    context = {"coi_details": coi_details, "form": form, "coi_details1":coi_details1,}
    return render(request, 'admindash/custom_order_detail_dashboard.html', context)




@allowed_users(allowed_roles=['admin'])
def admindash_customers(request):
    customers = Profile.objects.filter(verified=True)
    
    context = {
        "customers":customers,
    }

    return render(request, 'admindash/customers-dash.html',context)




@allowed_users(allowed_roles=['admin'])
def admindash_messages(request):
    message_list = ContactUs.objects.all()



 
    context = {
        "message_list":message_list,
    }
    return render(request, 'admindash/messages-dash.html',context)


@allowed_users(allowed_roles=['admin'])
def admindash_products(request):
    product_list = Product.objects.all()



 
    context = {
        "product_list":product_list,
    }
    return render(request, 'admindash/products-dash.html',context)

@allowed_users(allowed_roles=['admin'])
def admindash_analytics(request):


    category_orders = CartOrderItems.objects.values('category__title').annotate(count=Count('id'))

    category_labels = []
    category_data = []

    for category_order in category_orders:
        category_labels.append(category_order['category__title'])
        category_data.append(category_order['count'])


    context = {"category_labels":category_labels,"category_data":category_data,}
    return render(request, 'admindash/analytics-dash.html', context )


# Create your views here.
#@allowed_users(allowed_roles=['customer'])
def index(request):
    #products = Product.objects.all().order_by("-id")
    


    

    products = Product.objects.filter(product_status="published", featured=True)
    latest_product = Product.objects.latest('date')  # Assuming you have a 'created_at' field

    for product in products:
        product.average_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0.0
    
    #top_selling_product = CartOrderItems.objects.annotate(order_count=Sum('item__qty')).order_by('-order_count').first()
    
    context = {
        "products":products, "latest_product":latest_product, #'top_selling_product': top_selling_product, 
    }

    return render(request, 'core/index.html', context)


def category_list_view(request):
    categories = Category.objects.all()
    #categories = Category.objects.all().annotate(product_count=Count("product"))         

    context = {
        "categories":categories
    }
    return render(request, 'core/category-list.html', context)

def product_list_view(request):
    products = Product.objects.filter(product_status="published")

    context = {
        "products":products
    }

    return render(request, 'core/product-list.html', context)

def category_product_list__view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)

    context = {
        "category":category,
        "products":products,
    }
    return render(request, "core/category-product-list.html", context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors":vendors,
    }
    return render(request, "core/vendor-list.html", context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor,product_status="published")
    context = {
        "vendor":vendor,
        "products":products,
    }
    return render(request, "core/vendor-detail.html", context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    p_image = product.p_images.all()
    p_color = product.p_colors.all()
    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    #Getting all reviews
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    #Product Review Form
    review_form = ProductReviewForm()

    make_review = True

    #if request.user.profile.is_authenticated: #try remove then add ulit, ang is_authenticated ay kung bumili naman tlga
    profile_review_count = ProductReview.objects.filter(profile=request.user.profile,product=product).count() #mark

    if profile_review_count > 0:
        make_review = False


    #calculations
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    context={
        "p":product, "p_image":p_image,"p_color":p_color, "products":products, "reviews":reviews, "average_rating":average_rating,
        "review_form":review_form, "make_review":make_review,
    }

    return render(request, "core/product-detail.html", context)

def tag_list(request, tag_slug=None):


    products = Product.objects.filter(product_status="published").order_by("-id")

    tag = None 
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products": products,
        "tag": tag
    }

    return render(request, "core/tag.html", context)

def ajax_add_review(request,pid):
    product = Product.objects.get(pk=pid)
    profile = request.user.profile #mark

    review = ProductReview.objects.create(
        profile=profile,product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        'profile':profile.first_name, 'review':request.POST['review'], 'rating':request.POST['rating'],
    } 

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    return JsonResponse(
        {
        'bool':True, #hiding
        'context':context,
        'avg_reviews':average_reviews
        }
    )


def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        "products":products,
        "query":query,
    }
    return render(request, "core/search.html", context)













def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")

#############################
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
###################

    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

################
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)
################
    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct() #

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()

    data = render_to_string("core/async/product-list.html", {"products":products} )
    return JsonResponse({"data": data})
 






















# def add_to_cart(request):
#     cart_product = {}

#     cart_product[str(request.GET['id'])] = {
#         'title': request.GET['title'],
#         'qty': request.GET['qty'],
#         'price': request.GET['price'],
#         'image':request.GET['image'],
#         'pid':request.GET['pid'],
#     }
#     if 'cart_data_obj' in request.session:
#         if str(request.GET['id']) in request.session['cart_data_obj']:
#             cart_data = request.session['cart_data_obj']
#             cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
#             cart_data.update(cart_data)
#             request.session['cart_data_obj'] = cart_data
#         else:
#             cart_data = request.session['cart_data_obj']
#             cart_data.update(cart_product)
#             request.session['cart_data_obj'] = cart_data

#     else:
#         request.session['cart_data_obj'] = cart_product
#     return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})
def add_to_cart(request):
    cart_product = {
        'title': request.GET.get('title', ''),
        'qty': int(request.GET.get('qty', 0)),
        'price': float(request.GET.get('price', 0.0)),
        'image': request.GET.get('image', ''),
        'pid': str(request.GET['pid']),
        'category': request.GET.get('category', ''),  # newly added
    }

    product_id = str(request.GET.get('id', ''))

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        if product_id in cart_data:
            cart_data[product_id]['qty'] = cart_product['qty']
        else:
            cart_data[product_id] = cart_product

        request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = {product_id: cart_product}

    total_cart_items = len(request.session['cart_data_obj'])
    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': total_cart_items})


def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            item['category'] = Product.objects.get(pid=item['pid']).category.title # newly added code
        return render(request, "core/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")
    
def clear_cart(request):
    if 'cart_data_obj' in request.session:
        del request.session['cart_data_obj']
        request.session.modified = True  # Mark the session as modified after changes

    return JsonResponse({'success': True, 'message': 'Your cart is now empty'})

#//path("add-to-cart", views.add_to_cart, name="add-to-cart"),

# def cart_view(request):
#     cart_total_amount = 0

#     if 'cart_data_obj' in request.session:
#         for p_id, item in request.session['cart_data_obj'].items():
#             cart_total_amount += int(item['qty']) * float(item['price'])
#         return render(request, "core/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
#     else:
#         messages.warning(request, "Your cart is empty")
#         return redirect("core:index")

# def cart_view(request): 
#     cart_total_amount = 0
#     if 'cart_data_obj' in request.session:
#         for p_id, item in request.session['cart_data_obj'].items():
#             cart_total_amount += int(item['qty']) * float(item['price'])
#         return render(request, "core/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
#     else:
#         messages.warning(request, "Your cart is empty")
#         return redirect("core:index")

# #pansamantala
# def cart_view(request):
#     cart_total_amount = 0

#     if 'cart_data_obj' in request.session:
#         for p_id, item in request.session['cart_data_obj'].items():
#             try:
#                 item_price = float(item['price'])
#             except ValueError:
#                 item_price = 0.0  # Provide a default value when 'price' is not a valid float
#             cart_total_amount += int(item['qty']) * item_price

#         return render(request, "core/cart.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
#     else:
#         messages.warning(request, "Your cart is empty")
#         return redirect("core:index")
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist   
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data
            request.session.modified = True  # Mark the session as modified after changes
    
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            try:
                item['category'] = Product.objects.get(pk=int(item['pid'])).category.title
            except (ValueError, Product.DoesNotExist, ObjectDoesNotExist):
                item['category'] = "Unknown Category"

            cart_total_amount += int(item['qty']) * float(item['price']) # newly added code
    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})


# def update_cart(request):
#     product_id = str(request.GET['id'])
#     product_qty = request.GET['qty']

#     if 'cart_data_obj' in request.session:
#         if product_id in request.session['cart_data_obj']:
#             cart_data = request.session['cart_data_obj']
#             cart_data[product_id]['qty'] = product_qty
#             request.session['cart_data_obj'] = cart_data
#             request.session.modified = True  # Mark the session as modified after changes
    
#     cart_total_amount = 0
#     if 'cart_data_obj' in request.session:
#         for p_id, item in request.session['cart_data_obj'].items():
#             cart_total_amount += int(item['qty']) * float(item['price'])
#             item['category'] = Product.objects.get(pk=item['pid']).category.title  # Add this line

#     context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
#     return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

def update_cart(request):
    product_id = str(request.GET.get('id', ''))
    product_qty = request.GET.get('qty', '')

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        if product_id in cart_data:
            cart_data[product_id]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
            request.session.modified = True  # Mark the session as modified after changes

    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            try:
                item['category'] = Product.objects.get(pk=int(item['pid'])).category.title
            except (ValueError, Product.DoesNotExist, ObjectDoesNotExist):
                item['category'] = "Unknown Category"

            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {
        "cart_data": request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount
    })

    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

# @login_required
# def checkout_view(request):

#     cart_total_amount = 0
#     total_amount = 0 
#     if 'cart_data_obj' in request.session:
#         for p_id, item in request.session['cart_data_obj'].items():
#             total_amount += int(item['qty']) * float(item['price'])
#             item['category'] = Product.objects.get(pid=item['pid']).category.title  # Add this line

#         order = CartOrder.objects.create(
#             profile=request.user.profile, #mark
#             price = total_amount
#         )
#         for p_id, item in request.session['cart_data_obj'].items():
#             cart_total_amount += int(item['qty']) * float(item['price'])
#             #CartOrderProducts kay Desphinx
#             cart_order_products = CartOrderItems.objects.create(
#                 order=order,
#                 invoice_no="INVOICE_NO-" + str(order.id),
#                 item=item['title'],
#                 image=item['image'],
#                 qty=item['qty'],
#                 price=item['price'],
#                 total=float(item['qty']) * float(item['price']),
#                 category=Product.objects.get(pid=item['pid']).category  # newly added code


#             )

#     host = request.get_host()
#     paypal_dict = {
#         'business':settings.PAYPAL_RECEIVER_EMAIL,
#         'amount': cart_total_amount,
#         'item_name': "Order-Item-No-" + str(order.id),
#         'invoice': "INVOICE_NO-" + str(order.id), 
#         'currency_code': "PHP",
#         'notify_url': 'http://{}{}'.format(host,reverse("core:paypal-ipn")),
#         'return_url': 'http://{}{}'.format(host,reverse("core:payment-completed")),
#         'cancel_url': 'http://{}{}'.format(host,reverse("core:payment-failed")),
#     }
#     paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

#     # cart_total_amount = 0
#     # if 'cart_data_obj' in request.session:
#     #     for p_id, item in request.session['cart_data_obj'].items():
#     #         cart_total_amount += int(item['qty']) * float(item['price'])

#     try:
#         active_address = Address.objects.get(profile=request.user.profile, status=True) #Mark one
#     except:
#         messages.warning(request,"There are multiple default addresses, please choose only one default address.")
#         active_address = None

#     return render(request, "core/checkout.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount, 'paypal_payment_button':paypal_payment_button, "active_address":active_address })


#Not working properly
# @login_required
# def checkout_gcash_view(request):
#     # 
    
    

#     cart_total_amount = 0
#     if 'cart_data_obj' in request.session:
#         for p_id, item in request.session['cart_data_obj'].items():
#             cart_total_amount += int(item['qty']) * float(item['price'])




#     context = {'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount}
#     return render(request, "core/gcash-receipt-submission-portal.html",context)

from .forms import ReceiptSubmissionForm

@login_required
def checkout_gcash_view(request,id):
    # Ang kailangan nito iretrieve lang yung Specific order then VIEW the details
    order = CartOrder.objects.get(profile=request.user.profile, id=id) #mark
    order_items = CartOrderItems.objects.filter(order=order)

    for o in order_items:
        o.amount = o.price * o.qty

    
    #################EVERYTHING VIEW RELATED ^^^^^^^^^^^^^^^^
    
    #{% url 'core:order-detail' o.id %}
        
    #BELOW IS EVERYTHING RECEIPT SUBMISSION
    if request.method == 'POST':
        form = ReceiptSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            receipt_image = form.cleaned_data['receipt_image']
            order.receipt_img = receipt_image
            order.receipt_submitted = True
            order.save()
            # Additional logic if needed, e.g., redirect to a success page
            messages.success(request, 'An Order is created.')
            return redirect("core:index")
    else:
        form = ReceiptSubmissionForm()


    context = {"order":order,"order_items":order_items, "form": form}
    return render(request, "core/gcash-receipt-submission-portal.html",context)



#Before chat
# @login_required
# def checkout_view(request):

#     cart_total_amount = 0
#     total_amount = 0 
#     if 'cart_data_obj' in request.session:
#         for p_id, item in request.session['cart_data_obj'].items():
#             total_amount += int(item['qty']) * float(item['price'])
#             item['category'] = Product.objects.get(pid=item['pid']).category.title  # Add this line

#         order = CartOrder.objects.create(
#             profile=request.user.profile, #mark
#             price = total_amount
#         )
#         for p_id, item in request.session['cart_data_obj'].items():
#             cart_total_amount += int(item['qty']) * float(item['price'])
#             #CartOrderProducts kay Desphinx
#             cart_order_products = CartOrderItems.objects.create(
#                 order=order,
#                 invoice_no="INVOICE_NO-" + str(order.id),
#                 item=item['title'],
#                 image=item['image'],
#                 qty=item['qty'],
#                 price=item['price'],
#                 total=float(item['qty']) * float(item['price']),
#                 category=Product.objects.get(pid=item['pid']).category  # newly added code


#             )



#     try:
#         active_address = Address.objects.get(profile=request.user.profile, status=True) #Mark one
#     except:
#         messages.warning(request,"There are multiple default addresses, please choose only one default address.")
#         active_address = None

#     return render(request, "core/checkout.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount, "active_address":active_address })
@login_required
def checkout_check(request):
    

     # Fetch and display order details without creating a new order
    if 'cart_data_obj' in request.session:
        cart_total_amount = sum(int(item['qty']) * float(item['price']) for item in request.session['cart_data_obj'].values())

        try:
            active_address = Address.objects.get(profile=request.user.profile, status=True)
        except Address.DoesNotExist:
            messages.warning(request, "There are multiple default addresses, please choose only one default address.")
            active_address = None

        return render(request, "core/checkout_check.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount,'active_address': active_address,})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")
    
    


from django.db import transaction
from decimal import Decimal
@login_required #MUST BE SYNCHRONIZED WITH GCASH VIEW
def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0 

    if 'cart_data_obj' in request.session:
        # Use transaction.atomic to ensure atomicity of the database operations
        with transaction.atomic():
            # Check if an order already exists for the user
            existing_order = CartOrder.objects.filter(profile=request.user.profile, paid_status=False, is_completed=False).first()

            if existing_order:
                order = existing_order
            else:
                # Create a new order if one doesn't exist
                order = CartOrder.objects.create(
                    profile=request.user.profile,
                    price=Decimal('0'),  # Use Decimal for money values
                )

            for p_id, item in request.session['cart_data_obj'].items():
                total_amount += int(item['qty']) * float(item['price'])
                item['category'] = Product.objects.get(pid=item['pid']).category.title

                # Update the order's price as you go through the items
                order.price += Decimal(item['qty']) * Decimal(item['price'])
                order.save()

                # Check if a CartOrderItems instance already exists for this order and item
                existing_item = CartOrderItems.objects.filter(order=order, item=item['title']).first()

                if existing_item:
                    # Update the existing item if it already exists
                    existing_item.qty += int(item['qty'])
                    existing_item.total += Decimal(item['qty']) * Decimal(item['price'])
                    existing_item.save()
                else:
                    # Create a new CartOrderItems instance if it doesn't exist
                    cart_order_products = CartOrderItems.objects.create(
                        order=order,
                        invoice_no="INVOICE_NO-" + str(order.id),
                        item=item['title'],
                        image=item['image'],
                        qty=int(item['qty']),
                        price=Decimal(item['price']),
                        total=Decimal(item['qty']) * Decimal(item['price']),
                        category=Product.objects.get(pid=item['pid']).category
                    )

            # Update the total price of the order after processing all items
            order.price = total_amount
            order.is_completed = True  # Mark the order as completed
            order.save()
            
            # Clear the cart
            del request.session['cart_data_obj']
            request.session.modified = True 
            

            messages.success(request, 'An Order is created.')

    try:
        active_address = Address.objects.get(profile=request.user.profile, status=True)
    except Address.DoesNotExist:
        messages.warning(request, "There are multiple default addresses, please choose only one default address.")
        active_address = None

    #if gcash, go to gcash - 
    #if pay later , go to home


    #return render(request, "core/checkout.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, "active_address": active_address })
    return redirect("core:index")


@login_required #MUST BE SYNCHRONIZED WITH GCASH VIEW
def if_checkout_to_gcash(request):
    cart_total_amount = 0
    total_amount = 0 

    if 'cart_data_obj' in request.session:
        # Use transaction.atomic to ensure atomicity of the database operations
        with transaction.atomic():
            # Check if an order already exists for the user
            existing_order = CartOrder.objects.filter(profile=request.user.profile, paid_status=False, is_completed=False).first()

            if existing_order:
                order = existing_order
            else:
                # Create a new order if one doesn't exist
                order = CartOrder.objects.create(
                    profile=request.user.profile,
                    price=Decimal('0'),  # Use Decimal for money values
                )

            for p_id, item in request.session['cart_data_obj'].items():
                total_amount += int(item['qty']) * float(item['price'])
                item['category'] = Product.objects.get(pid=item['pid']).category.title

                # Update the order's price as you go through the items
                order.price += Decimal(item['qty']) * Decimal(item['price'])
                order.save()

                # Check if a CartOrderItems instance already exists for this order and item
                existing_item = CartOrderItems.objects.filter(order=order, item=item['title']).first()

                if existing_item:
                    # Update the existing item if it already exists
                    existing_item.qty += int(item['qty'])
                    existing_item.total += Decimal(item['qty']) * Decimal(item['price'])
                    existing_item.save()
                else:
                    # Create a new CartOrderItems instance if it doesn't exist
                    cart_order_products = CartOrderItems.objects.create(
                        order=order,
                        invoice_no="INVOICE_NO-" + str(order.id),
                        item=item['title'],
                        image=item['image'],
                        qty=int(item['qty']),
                        price=Decimal(item['price']),
                        total=Decimal(item['qty']) * Decimal(item['price']),
                        category=Product.objects.get(pid=item['pid']).category
                    )

            # Update the total price of the order after processing all items
            order.price = total_amount
            order.is_completed = True  # Mark the order as completed
            order.save()

            
            
            # Clear the cart
            del request.session['cart_data_obj']
            request.session.modified = True 
            
            order_id = order.id # the only diff

            messages.success(request, 'An Order is created.')

    try:
        active_address = Address.objects.get(profile=request.user.profile, status=True)
    except Address.DoesNotExist:
        messages.warning(request, "There are multiple default addresses, please choose only one default address.")
        active_address = None

    #if gcash, go to gcash - 
    #if pay later , go to home


    #return render(request, "core/checkout.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, "active_address": active_address })
    return redirect("core:checkout-gcash", id=order_id)



@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    return render(request, 'core/payment-completed.html',{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})

@login_required
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')

@login_required
def customer_dashboard(request):
    #orders = request.user.customer.order_set.all() #profile?

    order_list = CartOrder.objects.filter(profile=request.user.profile).order_by("-id") #raw

    order_list_rfalse = CartOrder.objects.filter(profile=request.user.profile, receipt_submitted=False).order_by("-id")

    order_list_rtrue = CartOrder.objects.filter(profile=request.user.profile, receipt_submitted=True, paid_status=False).order_by("-id")
    
    order_list_paid = CartOrder.objects.filter(profile=request.user.profile, receipt_submitted=True, paid_status=True).order_by("-id")

    address = Address.objects.filter(profile=request.user.profile) #mark 2
    
    profile = Profile.objects.get(user=request.user) #mark


    #ang didisplay dapat dito ay kanya kanyang user , not all user
    orders = CartOrder.objects.filter(profile=request.user.profile).annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count") #mark
    month = []
    total_orders = []

    for i in orders:
        month.append(calendar.month_name[i["month"]])
        total_orders.append(i["count"])


    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        new_address = Address.objects.create(
            profile = request.user.profile, #mark 3
            address=address,

            mobile=mobile,
        )
        messages.success(request, "Address Added Successfully")
        return redirect("core:dashboard")
    
    context = {
        "profile" : profile,"orders" : orders,"order_list":order_list, "address":address,"month":month,"total_orders":total_orders, "order_list_rfalse":order_list_rfalse,
        "order_list_rtrue":order_list_rtrue, "order_list_paid":order_list_paid, 
    }
    return render(request, 'core/dashboard.html',context)
    


    

@login_required
def order_detail(request, id):
    order = CartOrder.objects.get(profile=request.user.profile, id=id) #mark
    order_items = CartOrderItems.objects.filter(order=order)
    context = {
        "order":order,"order_items":order_items,
    }
    return render(request, 'core/order-detail.html',context)
### TRY LANG FROM pt 
# def generate_pdf(request):
#     html_content = f"""`
    
#     """
#     pdf = pdfkit.from_string(html_content, False)
#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
#     return response


#This one make other Profile's Address FALSE
# def make_address_default(request):
#     id = request.GET['id']
#     Address.objects.update(status=False)
#     Address.objects.filter(id=id).update(status=True)
#     return JsonResponse({"boolean": True})



def make_address_default(request):
    address_id = request.GET.get('id')

    try:
        address_to_make_default = Address.objects.get(id=address_id, profile=request.user.profile)
        Address.objects.filter(profile=request.user.profile).exclude(id=address_id).update(status=False)
        address_to_make_default.status = True
        address_to_make_default.save()

        return JsonResponse({"boolean": True})
    except Address.DoesNotExist:
        return JsonResponse({"boolean": False, "error": "Address not found or doesn't belong to the current user's profile"})



@login_required
def wishlist_view(request):
    wishlist = wishlist_model.objects.filter(profile=request.user.profile) #IS AUTHENTICATED?

    context = {
    "w": wishlist
    }
    return render(request, 'core/wishlist.html', context)

def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    context = {}

    wishlist_count = wishlist_model.objects.filter(product=product , profile=request.user.profile).count() #mark
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = wishlist_model.objects.create(
            product = product,
            profile = request.user.profile #mark
        )
        context = {
            "bool":True
        }
    return JsonResponse(context)




def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = wishlist_model.objects.filter(profile=request.user.profile) #mark

    product = wishlist_model.objects.get(id=pid)
    product.delete()

    context = {
        "bool":True,
        "wishlist":wishlist
    }
    wishlist_json = serializers.serialize('json', wishlist)
    t = render_to_string('core/async/wishlist-list.html', context)
    return JsonResponse({"data":t,"w":wishlist_json})

def contact(request):
    return render(request, "core/contact.html")

def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {
        "bool":True,
        "message":"Message sent successfully"
    }
    return JsonResponse({"data":data})


####

def custom_order(request):
    product_types = ProductType.objects.all()
    swatches = Swatch.objects.all()

    service_choices = CustomProduct.SERVICE_CHOICE    
    context = {
        'product_types':product_types,
        'swatches':swatches,
        'service_choices': service_choices,
    }

    return render(request, "core/customorder.html", context)



# Replace this with your actual view function for getting product type image URL
def get_product_type_image(request):
    product_type_id = request.GET.get('product_type_id')
    try:
        product_type = ProductType.objects.get(id=product_type_id)
        image_url = product_type.image.url
        return JsonResponse({'image_url': image_url})
    except ProductType.DoesNotExist:
        return JsonResponse({'error': 'Product Type not found'}, status=400)
    
