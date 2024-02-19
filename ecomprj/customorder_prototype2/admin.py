from django.contrib import admin
from customorder_prototype2.models import ProductType, Material, Color, CustomizationOrder,Analytics, FoamType, ProductTypeSizes

class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1

class ColorInline(admin.TabularInline):
    model = Color
    extra = 1


class SizeInline(admin.TabularInline):
    model = ProductTypeSizes
    extra = 1


class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [MaterialInline, SizeInline]

class MaterialAdmin(admin.ModelAdmin):
    inlines = [ColorInline]

admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Color)
admin.site.register(CustomizationOrder)
admin.site.register(Analytics)
admin.site.register(FoamType)

admin.site.register(ProductTypeSizes)