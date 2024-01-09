from django.urls import path
from customorder_prototype2.views import choose_product_type,choose_foam_x, choose_material, choose_color, choose_material_x, choose_color_x,custom_details

product_types = ['bed', 'chair', 'sofa']  

urlpatterns = [
    path('choose-product-type/', choose_product_type, name='choose_product_type'),

    path('choose_foam_x/', choose_foam_x, name='choose_foam_x' ),


    path('choose-material/<slug:product_type>/', choose_material, name='choose_material'),
    path('choose-color/<int:material_id>/', choose_color, name='choose_color'),


    #HARDWAY
    # path('choose-material/<slug:product_type>/', choose_material, name='choose_material'),
    path('choose_material_<slug:product_type>/', choose_material_x, name='choose_material_x'),
    path('choose_color_x/<slug:product_type>/<slug:material_name>/', choose_color_x, name='choose_color_x'),
    path('custom_order_details/<str:product_type>/<str:material_name>/<str:color_name>/', custom_details, name='custom_details'),


]
