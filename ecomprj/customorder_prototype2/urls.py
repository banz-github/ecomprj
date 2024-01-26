from django.urls import path
from customorder_prototype2.views import submit_receipt_image,custom_order_receipt_submission,customization_order_analytics, choose_product_type,choose_foam_x, error_page, success_page, choose_material_x, choose_color_x,custom_details, submit_order

product_types = ['bed', 'chair', 'sofa']  

urlpatterns = [
    #path('choose-material/<slug:product_type>/', choose_material, name='choose_material'),
    #path('choose-color/<int:material_id>/', choose_color, name='choose_color'),

    path('choose-product-type/', choose_product_type, name='choose_product_type'),

    path('choose_foam_<slug:product_type>/', choose_foam_x, name='choose_foam_x' ),

    path('choose_material_<slug:product_type>/<slug:foam_types>/', choose_material_x, name='choose_material_x'),
    path('choose_color_x/<slug:product_type>/<slug:foam_types>/<slug:material_name>/', choose_color_x, name='choose_color_x'),
    path('custom_order_details/<str:product_type>/<slug:foam_types>/<str:material_name>/<str:color_name>/', custom_details, name='custom_details'),

    path('submit_order/<str:product_type>/<str:foam_types>/<str:material_name>/<str:color_name>/', submit_order, name='submit_order'),

    path('custom_order_receipt_submission/<str:co_id>/', custom_order_receipt_submission, name='custom_order_receipt_submission'),
    path('submit_receipt_image/<str:co_id>/', submit_receipt_image, name='submit_receipt_image'),



    #result pages
    path('success-page/', success_page, name='success_page'),
    path('error-page/', error_page, name='error_page'),

    #trial analytics
    path('trial-analytics/', customization_order_analytics, name='trial_analytics'),
    
]
