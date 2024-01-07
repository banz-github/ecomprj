from django.urls import path
from customorder import views

from customorder.views import custom_order_proto

app_name = "customorder"

urlpatterns = [
        path("custom-order-proto/", custom_order_proto, name="custom-order-proto"), #

]