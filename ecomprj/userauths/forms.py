from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile
from phonenumber_field.formfields import PhoneNumberField

#################SAVED######################################
# class UserRegisterForm(UserCreationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
#     phone_number = PhoneNumberField(widget=forms.TextInput(attrs={"placeholder": "Phone Number"}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))
#     class Meta:
#         model = User
#         fields = ['username', 'phone_number','email']


# class ProfileForm(forms.ModelForm):
#     full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Full Name"}))
#     bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio"}))
#     phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone"}))
#     class Meta:
#         model = Profile
#         fields = ['full_name', 'image', 'bio', 'phone']
#################SAVED######################################

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={"placeholder": "Phone Number"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))
    class Meta:
        model = User
        fields = ['username', 'phone_number','email']


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Last Name"}))
    #bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio"}))
    #phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone"}))
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Last Name"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone"}))
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'image', 'bio', 'phone']