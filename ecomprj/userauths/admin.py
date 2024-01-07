from django.contrib import admin
from userauths.models import User, ContactUs, Profile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number']

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'subject']

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user','full_name', 'bio', 'phone']


admin.site.register(User, UserAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Profile)