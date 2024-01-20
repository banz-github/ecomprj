from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User, Profile
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)


STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)



RATING = (
    ( 1,  "★☆☆☆☆"),
    ( 2,  "★★☆☆☆"),
    ( 3,  "★★★☆☆"),
    ( 4,  "★★★★☆"),
    ( 5,  "★★★★★"),
)


# Create your models here.

# def user_directory_path(instance, filename):
#     return 'user_{0}/{1}'.format(instance.user.id, filename)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.profile.user, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, max_length=25, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Upholstery/Furniture")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories" 

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title


class Tags(models.Model):
    pass

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Ataiza") #Title, Heading #############
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    cover_image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    #description = models.TextField(null=True, blank=True, default="Providing top-notch upholstery solutions.")
    description = RichTextUploadingField(null=True, blank=True, default="Providing top-notch upholstery solutions.")
    
    address = models.CharField(max_length=100, default="123 Main Street, Philippines.") #Title, Heading #############
    contact = models.CharField(max_length=100, default="+63 ") #Title, Heading #############
    chat_resp_time = models.CharField(max_length=100, default="100") #Title, Heading #############
    shipping_on_time = models.CharField(max_length=100, default="100") #Title, Heading #############
    authentic_rating = models.CharField(max_length=100, default="100") #Title, Heading #############
    days_return = models.CharField(max_length=100, default="100") #Title, Heading #############
    warranty_period = models.CharField(max_length=100, default="100") #Title, Heading #############


    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Vendors" 
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            return total_rating / len(reviews)
        return 0  # Return 0 if there are no reviews
    
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345") #
    
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True, related_name="category")
    
    title = models.CharField(max_length=100, default="Ataiza's") #Title, Heading #############
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    color = models.ImageField(upload_to=user_directory_path, default="color.jpg") #initial color

    description = RichTextUploadingField(null=True, blank=True, default="Hand-made")

    price = models.DecimalField(max_digits=99999999, decimal_places=2, default="500.00") 
    old_price = models.DecimalField(max_digits=99999999, decimal_places=2, default="1000.00")

    specifications = RichTextUploadingField(null=True, blank=True, default=" w x d x h") #can be details

    type = models.CharField(max_length=100, default="Furniture", null=True, blank=True) #I don't think this is needed
    stock_count = models.IntegerField(default=1) #I do not think this is needed
    color_count = models.IntegerField(default=5) #Originally Life #############

    tags = TaggableManager(blank=True)
    
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL,null=True, related_name="product")
    status = models.BooleanField(default=True) 
    in_stock = models.BooleanField(default=True) #I do not think this is needed
    featured = models.BooleanField(default=False) 


    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890") #
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products" 
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        display_price = 100 - new_price
        return display_price

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, related_name="p_images", on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images" 

class ProductColors(models.Model):
    colors = models.ImageField(upload_to="product-colors", default="color1.jpg")
    product = models.ForeignKey(Product, related_name="p_colors", on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Colors" 

############################### Card, Order, OrderItems, and Address    

class CartOrder(models.Model):
    cartorder_id = ShortUUIDField(unique=True, length=5, max_length=17, prefix="cart_order_", alphabet="abcdefgh12345")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=99999999, decimal_places=2, default="500.00")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    receipt_img = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    receipt_submitted = models.BooleanField(default=False) #newly added

    #newly added 
    is_completed = models.BooleanField(default=False)  # New field to track order completion status


    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)

    #newly added
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Add this line

    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999999, decimal_places=2, default="500.00")
    total = models.DecimalField(max_digits=99999999, decimal_places=2, default="500.00")

    order_completed = models.BooleanField(default=False)  # New field to track order item completion status

    class Meta:
        verbose_name_plural = "Cart Order Items"
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))
    

############################################################################################


class ProductReview(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING , default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews" 
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
class wishlist_model(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists" 
    def __str__(self):
        return self.product.title
    
class Address(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True, related_name='addresses')
    mobile = models.CharField(max_length=300, null=True)
    address = models.CharField(max_length=500, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses" 
        
    def __str__(self):
        return self.address
    