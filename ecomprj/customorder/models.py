from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from core.models import *
# Create your models here.


#All the models below is WHAT makes the CustomProduct

class ProductType(models.Model):
    title = models.CharField(max_length=100)
    estimated_delivery_days = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_type_images/', null=True, blank=True)

    base_price = models.FloatField()


    def __str__(self):
        return self.title
    

class Swatch(models.Model):
    title = models.CharField(max_length=100)
    base_price = models.FloatField()
    image = models.ImageField(upload_to='swatch_images/', null=True, blank=True)


    def __str__(self):
        return self.title

class SwatchColor(models.Model):
    swatch = models.ForeignKey(Swatch, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.swatch.title} - {self.color}"


#This Model (CustomProduct) is like the summary of everything above, it is like a receipt

class CustomProduct(models.Model):
    customprd_id = ShortUUIDField(unique=True, max_length=45, prefix="customed_", alphabet="abcdefghijklmnopqrstuv123456789")

    SERVICE_CHOICE = (
        ("make", "Make"),
        ("repair", "Repair"),
    )
    service_type = models.CharField(max_length=10, choices=SERVICE_CHOICE)
    
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    swatch = models.ForeignKey(Swatch, on_delete=models.SET_NULL, null=True)
    swatch_color = models.ForeignKey(SwatchColor, on_delete=models.SET_NULL, null=True)

    # New fields
    note = models.TextField(null=True, blank=True)  # Additional notes or comments

    PROGRESS_CHOICE = (
        ("in_progress", "In Progress"),
        ("done", "Done"),
    )
    progress = models.CharField(max_length=12, choices=PROGRESS_CHOICE)

    def __str__(self):
        return f"{self.customprd_id} | {self.service_type} | {self.category.title} | {self.swatch.title} | {self.swatch_color.color} | {self.progress}"
        #return self.product_type.title
