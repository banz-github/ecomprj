from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save

CUSTOMERTYPE_CHOICE = (
    ("business", "Business"),
    ("government", "Government"),
    ("private", "Private"),
)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    phone_number = PhoneNumberField(unique=True, null=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Profile(models.Model): #customer kay dennis ivy
    user = models.OneToOneField(User, on_delete=models.CASCADE)  #desphinx , meron din kay dennis
    image = models.ImageField(upload_to="image")
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    customerType = models.CharField(choices=CUSTOMERTYPE_CHOICE, max_length=50, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200)
    verified = models.BooleanField(default=False) #OTP
    active = models.BooleanField(default=True)
    #can add CustomerType - Business, Private, Government

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

#### dito ko pede ibuhos lahat ng request ng panelists
class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200) 
    phone = models.CharField(max_length=200) 
    subject = models.CharField(max_length=200) 
    message = models.TextField()

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return self.full_name
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)