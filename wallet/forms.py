from django import forms
from .models import Wallet

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['balance']
        widgets = {
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class WalletTransferForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    description = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )