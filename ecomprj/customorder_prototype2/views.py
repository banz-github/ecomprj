
# views.py

from django.shortcuts import render, HttpResponse
from django.http import Http404
from .models import ProductType, Material, Color,FoamType
from urllib.parse import unquote

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

def custom_details(request, product_type,foam_types, material_name, color_name):
    product_type = product_type.upper()
    foam_types = foam_types.upper()
    material_name = material_name.upper()  # Convert material name to uppercase
    color_name = color_name.upper()

    material_name = material_name.replace('_', ' ')  # Replace underscores with spaces
    material_name = unquote(material_name)

    color_name = color_name.replace('_', ' ')  # Replace underscores with spaces
    color_name = unquote(color_name)

    print('Reached customorder_details view')
    print('Received product_type:', product_type)
    print('Received foam_types:', foam_types)
    print('Received material_name:', material_name)
    print('Received color_name:', color_name)

    product_type_instance = ProductType.objects.get(name=product_type)

    foam_type_instance = FoamType.objects.get(name=foam_types)

    # Get the Material instance based on the name and product type
    material_instance = Material.objects.get(name=material_name, product_type=product_type_instance)

    # Get the color instance based on the name and material
    try:
        color_instance = Color.objects.get(name=color_name, material=material_instance)

        # Debugging information
        print('Color Image Path:', color_instance.image.url)

        # Get all colors related to the specified material
        colors = Color.objects.filter(material=material_instance)

        context = {
            'product_type': product_type,
            'foam_types': foam_types,
            'material_name': material_name,
            'color_name': color_name,
            'color': color_instance,
        }

        return render(request, 'customorder_prototype2/customorder_details.html', context)
    
    except Color.DoesNotExist:
        # Handle Color.DoesNotExist exception
        raise Http404("Color does not exist")

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