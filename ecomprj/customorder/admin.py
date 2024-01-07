from django.contrib import admin
from customorder.models import ProductType,Swatch,SwatchColor,CustomProduct


class SwatchColorInline(admin.TabularInline):
    model = SwatchColor

@admin.register(Swatch)
class SwatchAdmin(admin.ModelAdmin):
    list_display = ('title', 'base_price', 'image')
    inlines = [SwatchColorInline]


# Register your models here.
admin.site.register(ProductType)
#admin.site.register(Swatch)
admin.site.register(SwatchColor)
admin.site.register(CustomProduct)