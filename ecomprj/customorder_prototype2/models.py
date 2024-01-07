
from django.db import models
from userauths.models import Profile
class ProductType(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_type/', null=True, blank=True)
    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=100)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_type/material', null=True, blank=True)
    def __str__(self):
        return f"{self.name} - {self.product_type.name}"

class Color(models.Model):
    name = models.CharField(max_length=100)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_type/colors', null=True, blank=True)
    def __str__(self):
        return f"{self.name} - {self.material.name} - {self.material.product_type.name}"

class CustomizationOrder(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Analytics(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    selection_count = models.PositiveIntegerField(default=0)

