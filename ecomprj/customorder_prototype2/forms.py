from django import forms
from .models import CustomizationOrder
from tempus_dominus.widgets import DatePicker

class CustomOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomizationOrder
        fields = [
            'customer_notes',
            
            'customization_status',
            # 'estimated_date_done',
            'estimated_total_price', 
            'percentage_progress',
            'with_downpayment',
            'paid_amount',
            # 'date_approved',
            'AdminProfile',
            'admin_notes',
            'is_hidden',
        ]
        # widgets = {
        #     'estimated_date_done': DatePicker(),
        #     'date_approved': DatePicker(),
        # }

