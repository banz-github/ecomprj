from django.urls import path, include
from core.views import index
from core.views import checkout_gcash_view,admindash_analytics,admindash_products,admindash_customers,admindash_messages,admindash_orders,admindash,get_product_type_image,custom_order,ajax_contact_form,product_list_view, category_list_view, category_product_list__view,vendor_list_view,vendor_detail_view,product_detail_view,tag_list,ajax_add_review,search_view,filter_product,clear_cart,add_to_cart,cart_view,delete_item_from_cart,update_cart,checkout_view,payment_failed_view,payment_completed_view,customer_dashboard,order_detail,make_address_default,wishlist_view,add_to_wishlist,remove_wishlist,contact
app_name = "core"

urlpatterns = [
    #admin dash
    path("main-dash/", admindash, name="main-dash"),

    path("main-dash/orders/", admindash_orders, name="order-dash"),

    path("main-dash/messages/", admindash_messages, name="message-dash"),

    path("main-dash/customers/", admindash_customers, name="customers-dash"),

    path("main-dash/products/", admindash_products, name="products-dash"),
    path("main-dash/analytics/", admindash_analytics, name="analytics-dash"),
    
    

    #homepage
    path("", index, name="index"),
    path("products/", product_list_view, name="product-list"),
    path("product/<pid>/", product_detail_view, name="product-detail"),
    
    #category
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list__view, name="category-product-list"),

    #vendor
    path("vendors/", vendor_list_view, name="vendor-list"),
    path("vendor/<vid>/", vendor_detail_view, name="vendor-detail"),

    path("products/tag/<slug:tag_slug>/", tag_list, name="tags"),

    #add review
    path("ajax-add-review/<int:pid>/", ajax_add_review, name="ajax-add-review"),

    #search
    path("search/", search_view, name="search"),

    #filter
    path("filter-products/", filter_product, name="filter-product"),

    #add to cart
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    #cart page url
    path("cart/", cart_view, name="cart"),
    #lear cart page url
    path('clear-cart/', clear_cart, name='clear-cart'),
    #delete
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),
    #update
    path("update-cart/", update_cart, name="update-cart"),
    #checkout
    path("checkout/", checkout_view, name="checkout"),
    #gcash
     path("checkout-gcash-receipt-submission-portal/", checkout_gcash_view, name="checkout-gcash"),
    
    #paypal
    path('paypal/', include('paypal.standard.ipn.urls')),

    path("payment-completed/", payment_completed_view, name="payment-completed"),

    path("payment-failed/", payment_failed_view, name="payment-failed"),

    #from pt
    #path('generate_pdf/', generate_pdf, name='generate_pdf'),

    #customer dashboard
    path("dashboard/", customer_dashboard, name="dashboard"),

    #Order Detail
    path("dashboard/order/<int:id>", order_detail, name="order-detail"),
    path("make-default-address/", make_address_default, name="make-default-address"),

    path("wishlist/", wishlist_view, name="wishlist"),

    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),

    path("remove-from-wishlist/", remove_wishlist, name="remove-from-wishlist"),

    path("contact/", contact, name="contact"),

    
    path("ajax-contact-form/", ajax_contact_form, name="ajax-contact-form"),


    #Custom Order

    path("custom-order/", custom_order, name="custom-order"),


    path('get_product_type_image/', get_product_type_image, name='get_product_type_image'),

]
