from django import forms
from django.utils import timezone
from .models import SavingsGoal
from decimal import Decimal

class GoalForm(forms.ModelForm):
    target_amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '0.00'
        })
    )
    current_savings = forms.DecimalField(
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
    goal_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter goal name'
        })
    )
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    class Meta:
        model = SavingsGoal
        fields = ['goal_name', 'target_amount', 'current_savings', 'deadline']

    def clean(self):
        cleaned_data = super().clean()
        target_amount = cleaned_data.get('target_amount')
        current_savings = cleaned_data.get('current_savings') or Decimal('0.00')
        deadline = cleaned_data.get('deadline')
        
        if current_savings > target_amount:
            self.add_error('current_savings', 'Current savings cannot exceed target amount.')
            
        if deadline and deadline < timezone.now().date():
            self.add_error('deadline', 'Deadline must be in the future.')