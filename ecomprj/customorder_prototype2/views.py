
# views.py

from django.shortcuts import render
from .models import ProductType, Material, Color
from urllib.parse import unquote

def choose_product_type(request):
    product_types = ProductType.objects.all()
    return render(request, 'customorder_prototype2/choose_product_type.html', {'product_types': product_types})

def choose_material(request, product_type):
    product_type = product_type.capitalize()  # Capitalize the product type for consistency
    materials = Material.objects.filter(product_type__name=product_type)
    return render(request, 'choose_material.html', {'materials': materials, 'product_type': product_type})

###############HARD WAY. 
# def choose_material_bed(request, product_type):
#     product_type = product_type.capitalize()  # Capitalize the product type for consistency
#     materials = Material.objects.filter(product_type__name=product_type)
#     return render(request, 'choose_material_bed.html', {'materials': materials, 'product_type': product_type})

def choose_material_x(request, product_type):
    product_type = product_type.upper()
    print('Product Type:', product_type)
    # Assuming the product_type is provided as a parameter, capitalize it for consistency
    

    # Get the ProductType instance based on the name
    product_type_instance = ProductType.objects.get(name=product_type)

    # Get all materials related to the specified product type
    materials = Material.objects.filter(product_type=product_type_instance)

    return render(request, 'customorder_prototype2/choose_material_x.html', {'materials': materials, 'product_type': product_type})


######################## CHOOSE COLOR

def choose_color(request, material_id):
    material = Material.objects.get(pk=material_id)
    colors = Color.objects.filter(material=material)
    return render(request, 'choose_color.html', {'colors': colors, 'material': material})

######################################

def choose_color_x(request, product_type, material_name):
    product_type = product_type.upper()
    material_name = material_name.upper()  # Convert material name to uppercase


    material_name = material_name.replace('_', ' ')  # Replace underscores with spaces
    material_name = unquote(material_name)

    print('Reached choose_color_x view')
    print('Received product_type:', product_type)
    print('Received material_name:', material_name)

    # Get the ProductType instance based on the name
    product_type_instance = ProductType.objects.get(name=product_type)

    # Get the Material instance based on the name and product type
    material_instance = Material.objects.get(name=material_name, product_type=product_type_instance)

    # Get all colors related to the specified material
    colors = Color.objects.filter(material=material_instance)

    return render(request, 'customorder_prototype2/choose_color_x.html', {'colors': colors, 'product_type': product_type, 'material_name': material_name})
