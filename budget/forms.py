from django import forms
from .models import Budget
from decimal import Decimal

class BudgetForm(forms.ModelForm):
    limit = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '0.00'
        })
    )
    amount_spent = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0.00'),
        required=False,
        initial=Decimal('0.00'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '0.00'
        })
    )
    
    class Meta:
        model = Budget
        fields = ['category', 'limit', 'amount_spent']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        limit = cleaned_data.get('limit')
        amount_spent = cleaned_data.get('amount_spent') or Decimal('0.00')
        
        if limit and amount_spent > limit:
            self.add_error('amount_spent', 'Amount spent cannot exceed the limit.')