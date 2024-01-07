from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm, ProfileForm, UpdateProfileForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.conf import settings
from userauths.models import Profile, User

#GROUPS
from django.contrib.auth.models import Group

#User = settings.AUTH_USER_MODEL


# Create your views here.
# def register_view(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST or None)
#         if form.is_valid():
#             print("Form is valid")
#             new_user = form.save()
#             username = form.cleaned_data.get("username")

#             #Dennis Ivy 19:20 = Userbased Roles
#             group = Group.objects.get(name='customer')
#             new_user.groups.add(group) #user kay dennis

#             #customer (Profile) to kay Dennis 07:43 User Profile with One to One
#             #Profile.objects.create(
#             #   user=user,
#             # )

#             #Sa version natin tatry natin kabaliktaran
#             #User.objects.create(
#             #   profile=profile,
#             # )
            

#             #

#             print(f"New user created: {username}")
#             messages.success(request, f"Hey {username}, Your account was created successfully.")
#             new_user = authenticate(username=form.cleaned_data['phone_number'],
#                                     password=form.cleaned_data['password1'])
#             if new_user:
#                 print("User authenticated")
#                 login(request, new_user)
#             else:
#                 print("User authentication failed")
#             return redirect("core:index")
#         else:
#             print("Form is invalid")
#             print(form.errors)
#     else:
#         form = UserRegisterForm()

#     context = {
#         'form': form,
#     }
#     return render(request, "userauths/sign-up.html", context)


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        pform = ProfileForm(request.POST)

        if form.is_valid() and pform.is_valid():
            new_user = form.save()

            # Check if a Profile already exists for the user
            profile, created = Profile.objects.get_or_create(user=new_user, defaults={'phone': form.cleaned_data['phone_number']})

            # If a new Profile was created, update its fields
            if not created:
                profile.first_name = pform.cleaned_data['first_name']
                profile.last_name = pform.cleaned_data['last_name']
                profile.phone = form.cleaned_data['phone_number']
                profile.customerType = 'Private'  # Set customerType to 'Private'
                profile.bio = 'Newly created Profile!'  # Set bio to 'Newly created Profile!'
                profile.save()

            username = form.cleaned_data.get("username")

            group = Group.objects.get(name='customer')
            new_user.groups.add(group)

            print(f"New user created: {username}")
            messages.success(request, f"Hey {username}, Your account was created successfully.")

            # Authenticate and log in the new user
            new_user = authenticate(username=form.cleaned_data['phone_number'],
                                    password=form.cleaned_data['password1'])
            if new_user:
                print("User authenticated")
                login(request, new_user)
            else:
                print("User authentication failed")

            return redirect("core:index")
        else:
            print("Form is invalid")
            print(form.errors)
            print(pform.errors)
    else:
        form = UserRegisterForm()
        pform = ProfileForm()

    context = {'form': form, 'pform': pform}
    return render(request, "userauths/sign-up-proto.html", context)



# this one already works
def login_view(request):

    if request.user.is_authenticated:
        return redirect("core:index")
    
    if request.method == "POST":
        phone_number = request.POST.get("phone_number") 
        password = request.POST.get("password")

        try:
            user = User.objects.get(phone_number=phone_number)
            user = authenticate(request, phone_number=phone_number, password=password)
 
            if user is not None:
                login(request,user)
                messages.success(request, "You are now logged-in.")
                return redirect("core:index")
            else:
                messages.warning(request, "User does not exists. Please sign-up first.")
        except:
            messages.warning(request, f"User does not exists, please sign-up first.")

        
    return render(request, "userauths/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You logged out.")
    return redirect("userauths:sign-in")

def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile Updated Successfully.")
            return redirect("core:dashboard")
        
    else: 
        form = UpdateProfileForm(instance=profile)

    context = {"form":form,"profile":profile,}
    return render(request, "userauths/profile-edit.html", context)