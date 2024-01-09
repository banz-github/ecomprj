
from django.db import models
from userauths.models import Profile
from core.models import Address
from shortuuid.django_fields import ShortUUIDField

from ckeditor_uploader.fields import RichTextUploadingField

class ProductType(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_type/', null=True, blank=True)

    fabric_yard = models.DecimalField(max_digits=10, decimal_places=2) #Not migrated yet
    foam_amount = models.DecimalField(max_digits=10, decimal_places=2) #Not migrated yet

    #Estimated TIme of Arrival
    month_eta = models.DecimalField(max_digits=10, decimal_places=2, default=1)


    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=100)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_type/material', null=True, blank=True)

    fabric_peryard_price = models.DecimalField(max_digits=10, decimal_places=2) #Not migrated yet
    


    def __str__(self):
        return f"{self.name} - {self.product_type.name}"

class Color(models.Model):
    name = models.CharField(max_length=100)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_type/colors', null=True, blank=True)
    def __str__(self):
        return f"{self.name} - {self.material.name} - {self.material.product_type.name}"
    

class FoamType(models.Model):
    name = models.CharField(max_length=100)
    foam_percubicft_price = models.DecimalField(max_digits=10, decimal_places=2) #Foam price per cubic feet (650)  (1 cubic feet is 44W x 80L x1/2H)
    image = models.ImageField(upload_to='foam_type', null=True, blank=True)

    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
class CustomizationOrder(models.Model):
    co_id = ShortUUIDField(unique=True, max_length=25, prefix="CO", alphabet="abcdefgh12345")
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    foam_type = models.ForeignKey(FoamType, on_delete=models.CASCADE)

    qty = models.IntegerField(default=1)
    ##############date

    customer_notes = models.TextField(null=True, blank=True, default="") #check muna ung sa messaging before imigrate
    
    #Make Repair
    make_or_repair = models.CharField(max_length=20, default="MAKE")

    #Progress - Percentage
    percentage_progress = models.CharField(max_length=50, default="0")


    #Down payment status
    with_downpayment = models.BooleanField(default=False)

    #downpayment receipt submission
    receipt_img = models.ImageField(upload_to='receipt/', null=True, blank=True)

    
    #Estimation

    #customer na umorder
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE) #customer na umorder
    #phone = models.ForeignKey(Profile) #
    #address = models.ForeignKey(Address)

    AdminProfile = models.CharField(max_length=100) #Bali dito nalang pass in ng String type na ID nung nagapprove
    #admin notes, igaya dun sa Messaging muna
    admin_notes = RichTextUploadingField(null=True, blank=True, default="")
    #Boolean kung archived yung order , default False
    is_hidden = models.BooleanField(default=False)

class Analytics(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE) # added

    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    foam_type = models.ForeignKey(FoamType, on_delete=models.CASCADE) # added

    selection_count = models.PositiveIntegerField(default=0)

