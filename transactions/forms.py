from django import forms
from .models import Transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from core.categories import TRANSACTION_CATEGORIES

class TransactionForm(forms.ModelForm):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '0.00'
        })
    )
    
    category = forms.ChoiceField(
        choices=TRANSACTION_CATEGORIES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Transaction
        fields = ['amount', 'category', 'payment_method', 'transaction_type', 'description']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter description'})
        }

class TransactionCSVUploadForm(forms.Form):
    csv_file = forms.FileField()