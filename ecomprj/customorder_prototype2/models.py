
from django.db import models
from userauths.models import Profile
from core.models import Address
from shortuuid.django_fields import ShortUUIDField

from ckeditor_uploader.fields import RichTextUploadingField

MAKE_OR_REPAIR= (
    ("make", "Make"),
    ("repair", "Repair"),

)

STATUS_CHOICE = (
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

ORDER_PURPOSE = (
    ("private", "Private"),
    ("business", "Business"),
    ("government", "Government"),

)

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
        return f"{self.name}" #return f"{self.name} - {self.product_type.name}"

class Color(models.Model):
    name = models.CharField(max_length=100)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_type/colors', null=True, blank=True)
    def __str__(self):
        return f"{self.name}" #return f"{self.name} - {self.material.name} - {self.material.product_type.name}"
    

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
    purpose = models.CharField(choices=ORDER_PURPOSE, max_length=30, default="Private")

    customer_notes = models.TextField(null=True, blank=True, default="") #check muna ung sa messaging before imigrate
    
    #Make Repair
    make_or_repair = models.CharField(choices=MAKE_OR_REPAIR,max_length=20, default="MAKE")

    #Progress - Percentage
    percentage_progress = models.CharField(max_length=50, default="0")
    customization_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="pending")

    order_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    estimated_date_done = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    estimated_total_price = models.DecimalField(max_digits=99999999, decimal_places=2, null=True, blank=True)
    #Down payment status
    with_downpayment = models.BooleanField(default=False)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0) #Magkano ang binayad
    #downpayment receipt submission

    receipt_img = models.ImageField(upload_to='receipt/', null=True, blank=True)
    receipt_submitted = models.BooleanField(default=False)

    date_approved = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    
    #Estimation

    #customer na umorder 
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) #customer na umorder
    #phone = models.ForeignKey(Profile) #
    #address = models.ForeignKey(Address)

    AdminProfile = models.CharField(max_length=30,null=True, blank=True, default="") #Bali dito nalang pass in ng String type na ID nung nagapprove
    #admin notes, igaya dun sa Messaging muna
    admin_notes = RichTextUploadingField(null=True, blank=True, default="")
    #Boolean kung archived yung order , default False
    is_hidden = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Analytics.update_analytics(self)

    def delete(self, *args, **kwargs):
        # Decrement counts in Analytics when a CustomizationOrder instance is deleted
        Analytics.update_analytics_on_deletion(self)
        super().delete(*args, **kwargs)    

    def __str__(self):
        return self.co_id

    
class Analytics(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    foam_type = models.ForeignKey(FoamType, on_delete=models.CASCADE)

    total_orders_per_month = models.JSONField(default=dict)
    make_orders = models.PositiveIntegerField(default=0)
    repair_orders = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['product_type', 'material', 'color', 'foam_type']

    def __str__(self):
        return f"{self.product_type} - {self.material} - {self.color} - {self.foam_type}"

    @classmethod
    def update_analytics(cls, customization_order):
        if customization_order.pk is None:
            raise ValueError("The CustomizationOrder instance must be saved before updating analytics.")
        month_year = customization_order.order_date.strftime('%Y-%m')

        # Get or create Analytics instance for the specific combination
        analytics_instance, created = cls.objects.get_or_create(
            product_type=customization_order.product_type,
            material=customization_order.material,
            color=customization_order.color,
            foam_type=customization_order.foam_type,
        )

        # Initialize total_orders_per_month as an empty dict if it's not set yet
        analytics_instance.total_orders_per_month = analytics_instance.total_orders_per_month or {}

        # Update total_orders based on order date
        if month_year not in analytics_instance.total_orders_per_month:
            analytics_instance.total_orders_per_month[month_year] = 0
        analytics_instance.total_orders_per_month[month_year] += 1

        # Update make_orders and repair_orders based on make_or_repair field
        if customization_order.make_or_repair == 'MAKE':
            analytics_instance.make_orders += 1
        elif customization_order.make_or_repair == 'REPAIR':
            analytics_instance.repair_orders += 1

        # Save the changes only if the Analytics instance is not being created
        if not created:
            analytics_instance.save()

    @property
    def total_orders(self):
        return sum(self.total_orders_per_month.values()) if self.total_orders_per_month else 0
    @classmethod
    def update_analytics_on_deletion(cls, customization_order):
        # Update Analytics counts when a corresponding CustomizationOrder is deleted
        try:
            analytics_instance = cls.objects.get(
                product_type=customization_order.product_type,
                material=customization_order.material,
                color=customization_order.color,
                foam_type=customization_order.foam_type,
            )
            month_year = customization_order.order_date.strftime('%Y-%m')
            if month_year in analytics_instance.total_orders_per_month:
                analytics_instance.total_orders_per_month[month_year] -= 1
                if analytics_instance.total_orders_per_month[month_year] == 0:
                    del analytics_instance.total_orders_per_month[month_year]
            if customization_order.make_or_repair == 'MAKE':
                analytics_instance.make_orders = max(0, analytics_instance.make_orders - 1)
            elif customization_order.make_or_repair == 'REPAIR':
                analytics_instance.repair_orders = max(0, analytics_instance.repair_orders - 1)
            analytics_instance.save()
        except cls.DoesNotExist:
            # Handle the case where Analytics instance does not exist
            pass
    def __str__(self):
        return f"{self.product_type} - {self.material} - {self.color} - {self.foam_type}"        


