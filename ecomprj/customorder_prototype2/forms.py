from django import forms
from .models import CustomizationOrder

class CustomOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomizationOrder
        fields = [
            'customer_notes',
            
            'customization_status',
            'estimated_date_done',
            'estimated_total_price', 
            'percentage_progress',
            'with_downpayment',
            'paid_amount',
            'date_approved',
            'AdminProfile',
            'admin_notes',
            'is_hidden',
        ]

