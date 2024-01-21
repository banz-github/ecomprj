from django import forms
from .models import CustomizationOrder

class CustomOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomizationOrder
        fields = [
            'customer_notes',
            'make_or_repair',
            'percentage_progress',
            'with_downpayment',
            'paid_amount',
            'date_approved',
            'AdminProfile',
            'admin_notes',
            'is_hidden',
        ]

