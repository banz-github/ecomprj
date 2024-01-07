from django.http import HttpResponse
from django.shortcuts import redirect



#=============FORLATERS

#if user is not authenticated (OTP)
#   do not let them order
#elif user is authenticated:
#   can order




#if user is business
#   can bulk order
#if user is private
#   sakto lang
#if user is government
#   strict sa resibo

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not allowed to view this page.')

            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator


#wag ihiwalay sa allowed_users tong comment na to ^^^^^^^^^^^^^^^^^^^^^^^^^
#kapag gusto mo ihide ang isang html, do this
# {% if request.user.is_staff %}
# code like navbar
# {% endif %}

#this is optional and maybe can be used with customer type: private, business, individual
#User role based Permissions by Dennis Ivy #Timestamp 17:16
# def admin_only(view_func):
#     def wrapper_function(request, *args, **kwargs):
#         group = None
#         if request.user.groups.exists():
#             group = request.user.groups.all()[0].name

#         if group == 'customer':
#             return redirect('page-name')
#         if group == 'admin':
#             return view_func(request, *args, **kwargs)
        
#     return wrapper_function 