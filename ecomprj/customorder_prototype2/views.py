
# views.py

from django.shortcuts import render, HttpResponse, redirect
from django.http import Http404, HttpResponseServerError
from .models import ProductType, Material, Color,FoamType, CustomizationOrder
from userauths.models import User,Profile
from urllib.parse import unquote
from django.contrib import messages

def choose_product_type(request):
    product_types = ProductType.objects.all()
    return render(request, 'customorder_prototype2/choose_product_type.html', {'product_types': product_types})


#bago
def choose_foam_x(request, product_type):
    product_type = product_type.upper()
    foam_types = FoamType.objects.all()

    return render(request, 'customorder_prototype2/choose_foam_x.html',{'product_type': product_type, 'foam_types': foam_types})


def choose_material(request, product_type, foam_types ):
    foam_types = FoamType.objects.all()
    product_type = product_type.capitalize()  # Capitalize the product type for consistency
    materials = Material.objects.filter(product_type__name=product_type)
    return render(request, 'choose_material.html', {'materials': materials, 'product_type': product_type, 'foam_types': foam_types})

###############HARD WAY. 
# def choose_material_bed(request, product_type):
#     product_type = product_type.capitalize()  # Capitalize the product type for consistency
#     materials = Material.objects.filter(product_type__name=product_type)
#     return render(request, 'choose_material_bed.html', {'materials': materials, 'product_type': product_type})

def choose_material_x(request, product_type, foam_types):
    product_type = product_type.upper()
    foam_types = foam_types.upper()
    print('Product Type:', product_type)
    print('Foam Type:', foam_types)
    # Assuming the product_type is provided as a parameter, capitalize it for consistency
    

    # Get the ProductType instance based on the name
    product_type_instance = ProductType.objects.get(name=product_type)

    foam_type_instance = FoamType.objects.get(name=foam_types)

    # Get all materials related to the specified product type
    materials = Material.objects.filter(product_type=product_type_instance)

    return render(request, 'customorder_prototype2/choose_material_x.html', {'materials': materials, 'product_type': product_type, 'foam_types': foam_types})


######################## CHOOSE COLOR

def choose_color(request, material_id):
    material = Material.objects.get(pk=material_id)
    colors = Color.objects.filter(material=material)
    return render(request, 'choose_color.html', {'colors': colors, 'material': material})

######################################

def choose_color_x(request, product_type, foam_types ,material_name):
    product_type = product_type.upper()
    foam_types = foam_types.upper()
    material_name = material_name.upper()  # Convert material name to uppercase


    material_name = material_name.replace('_', ' ')  # Replace underscores with spaces
    material_name = unquote(material_name)

    print('Reached choose_color_x view')
    print('Received product_type:', product_type)
    print('Received foam_types:', foam_types)
    print('Received material_name:', material_name)

    # Get the ProductType instance based on the name
    product_type_instance = ProductType.objects.get(name=product_type)

    foam_type_instance = FoamType.objects.get(name=foam_types)

    # Get the Material instance based on the name and product type
    material_instance = Material.objects.get(name=material_name, product_type=product_type_instance)

    # Get all colors related to the specified material
    colors = Color.objects.filter(material=material_instance)

    return render(request, 'customorder_prototype2/choose_color_x.html', {'colors': colors, 'product_type': product_type,'foam_types': foam_types, 'material_name': material_name})


#@login_required
def custom_details(request, product_type, foam_types, material_name, color_name):
    product_type = product_type.upper()
    foam_types = foam_types.upper()
    material_name = material_name.upper()
    color_name = color_name.upper()

    material_name = material_name.replace('_', ' ')
    material_name = unquote(material_name)

    color_name = color_name.replace('_', ' ')
    color_name = unquote(color_name)

    print('Reached customorder_details view')
    print('Received product_type:', product_type)
    print('Received foam_types:', foam_types)
    print('Received material_name:', material_name)
    print('Received color_name:', color_name)

    product_type_instance = ProductType.objects.get(name=product_type)
    foam_type_instance = FoamType.objects.get(name=foam_types)
    material_instance = Material.objects.get(name=material_name, product_type=product_type_instance)

    try:
        color_instance = Color.objects.get(name=color_name, material=material_instance)

        # Debugging information
        print('Color Image Path:', color_instance.image.url)

        colors = Color.objects.filter(material=material_instance)

        context = {
            'product_type': product_type,
            'foam_types': foam_types,
            'material_name': material_name,
            'color_name': color_name,
            'color': color_instance,
            'user_profile': request.user.profile,
        }

        return render(request, 'customorder_prototype2/customorder_details.html', context)

    except Color.DoesNotExist:
        raise Http404("Color does not exist")

#The below is working
# def custom_details(request, product_type,foam_types, material_name, color_name):
#     product_type = product_type.upper()
#     foam_types = foam_types.upper()
#     material_name = material_name.upper()  # Convert material name to uppercase
#     color_name = color_name.upper()

#     material_name = material_name.replace('_', ' ')  # Replace underscores with spaces
#     material_name = unquote(material_name)

#     color_name = color_name.replace('_', ' ')  # Replace underscores with spaces
#     color_name = unquote(color_name)

#     print('Reached customorder_details view')
#     print('Received product_type:', product_type)
#     print('Received foam_types:', foam_types)
#     print('Received material_name:', material_name)
#     print('Received color_name:', color_name)

#     product_type_instance = ProductType.objects.get(name=product_type)

#     foam_type_instance = FoamType.objects.get(name=foam_types)

#     # Get the Material instance based on the name and product type
#     material_instance = Material.objects.get(name=material_name, product_type=product_type_instance)

#     # Get the color instance based on the name and material
#     try:
#         color_instance = Color.objects.get(name=color_name, material=material_instance)

#         # Debugging information
#         print('Color Image Path:', color_instance.image.url)

#         # Get all colors related to the specified material
#         colors = Color.objects.filter(material=material_instance)

#         context = {
#             'product_type': product_type,
#             'foam_types': foam_types,
#             'material_name': material_name,
#             'color_name': color_name,
#             'color': color_instance,
#         }

#         return render(request, 'customorder_prototype2/customorder_details.html', context)
    
#     except Color.DoesNotExist:
#         # Handle Color.DoesNotExist exception
#         raise Http404("Color does not exist") ENDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD

# def custom_details(request, product_type, material_name, color_name): 
#     product_type = product_type.upper()

#     # Adjusted material and color names
#     material_name = material_name.replace('_', ' ')
#     material_name = unquote(material_name)

#     color_name = color_name.replace('_', ' ')
#     color_name = unquote(color_name)

#     try:
#         product_type_instance = ProductType.objects.get(name=product_type)
#         material_instance = Material.objects.get(name=material_name, product_type=product_type_instance)
#         color_instance = Color.objects.get(name=color_name, material=material_instance)
#     except Material.DoesNotExist:
#         # Handle the case when the material does not exist
#         return HttpResponse("Material not found", status=404)
#     except Color.DoesNotExist:
#         # Handle the case when the color does not exist
#         return HttpResponse("Color not found", status=404)

#     # If needed, you can still retrieve other colors for the material
#     colors = Color.objects.filter(material=material_instance)

#     context = {
#         "product_type": product_type,
#         "material_name": material_name,
#         "color_name": color_name,
#         "colors": colors,
#     }

#     return render(request, 'customorder_prototype2/customorder_details.html', context)

# def custom_details(request, product_type, material_name, color_name): 
#     product_type = product_type.upper()
#     material_name = material_name.replace('_', ' ')  # Replace underscores with spaces
#     material_name = unquote(material_name)
#     color_name = color_name.replace('_', ' ')  # Replace underscores with spaces
#     color_name = unquote(color_name)

#     try:
#         product_type_instance = ProductType.objects.get(name=product_type)
#         material_instance = Material.objects.get(name=material_name, product_type=product_type_instance)
#         color_instance = Color.objects.get(name=color_name, material=material_instance)
#         colors = Color.objects.filter(material=material_instance)
#     except (ProductType.DoesNotExist, Material.DoesNotExist, Color.DoesNotExist) as e:
#         # Handle the case where either ProductType, Material, or Color does not exist
#         return HttpResponse(f"Error: {e}")

#     context = {"product_type": product_type, "material_name": material_name, "color_name": color_name, "colors": colors}
#     return render(request, 'customorder_prototype2/customorder_details.html', context)

# def custom_details(request, product_type, material_name, color_name):
#     try:
#         # Print debug information
#         print("Product Type:", product_type)
#         print("Material Name:", material_name)
#         print("Color Name:", color_name)

#         # Decode URL-encoded material_name and color_name
#         material_name = unquote(material_name)
#         color_name = unquote(color_name)

#         # Get instances from the database
#         product_type_instance = ProductType.objects.get(name__iexact=product_type)

#         material_instance = Material.objects.get(name=material_name, product_type=product_type_instance)
#         color_instance = Color.objects.get(name=color_name, material=material_instance)

#         # Query for related colors
#         colors = Color.objects.filter(material=material_instance)

#         # Your existing logic...
#         context = {"product_type": product_type, "material_name": material_name, "color_name": color_name, "colors": colors}
#         return render(request, 'customorder_prototype2/customorder_details.html', context)

#     except Material.DoesNotExist:
#         # Handle Material.DoesNotExist exception
#         raise Http404("Material does not exist")
def submit_order(request, product_type, foam_types, material_name, color_name):
    try:
        # Retrieve model instances
        product_type_instance = ProductType.objects.get(name=product_type)
        foam_type_instance = FoamType.objects.get(name=foam_types)
        material_instance = Material.objects.get(name=material_name, product_type=product_type_instance)
        color_instance = Color.objects.get(name=color_name, material=material_instance)

        if request.method == 'POST':
            try:
                # Extract form data from the POST request
                quantity = request.POST.get('quantity')
                customer_notes = request.POST.get('customer_notes')

                # Get the user's profile
                profile = request.user.profile

                # Create a new CustomizationOrder instance
                order = CustomizationOrder.objects.create(
                    product_type=product_type_instance,
                    foam_type=foam_type_instance,
                    material=material_instance,
                    color=color_instance,
                    qty=quantity,
                    customer_notes=customer_notes,
                    profile=profile,  # Set the profile associated with the order
                    # Add other fields as needed
                    # ...
                )

                # Additional processing or redirect to success page
                messages.success(request, 'Order submitted successfully!')
                return redirect('success_page')  # Replace 'success_page' with the actual URL name

            except Exception as e:
                # Handle other exceptions
                messages.error(request, f'Error submitting order: {str(e)}')
                return HttpResponseServerError(f'Error submitting order: {str(e)}')
        else:
            # Handle the case where the form is accessed via GET request
            messages.error(request, 'Error submitting order. Please try again.')
            return HttpResponseServerError('Error submitting order. Please try again.')

    except ProductType.DoesNotExist:
        messages.error(request, f'Error submitting order. ProductType {product_type} does not exist.')
        return redirect('error_page')  # Replace 'error_page' with the actual URL name for an error page

def success_page(request):
    return render(request, 'customorder_prototype2/success_page.html')

def error_page(request):
    return render(request, 'customorder_prototype2/error_page.html')



    #trial muna for customization order
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import CustomizationOrder
from django.http import JsonResponse

from django.forms.models import model_to_dict

def customization_order_analytics(request):
    custom_order_list = CustomizationOrder.objects.filter(profile=request.user.profile).order_by("-co_id")

    # Convert QuerySet to a list of dictionaries
    custom_order_data = [model_to_dict(order) for order in custom_order_list]

    # Aggregate CustomizationOrder count per month
    monthly_counts = CustomizationOrder.objects.annotate(month=TruncMonth('order_date')) \
                          .values('month') \
                          .annotate(count=Count('co_id'))

    # Prepare data for the chart
    chart_data = [{'month': entry['month'].strftime('%Y-%m'), 'count': entry['count']} for entry in monthly_counts]

    # Return JSON response
    return JsonResponse({'chart_data': chart_data, 'custom_order_list': custom_order_data})
    #trial muna for customization order 