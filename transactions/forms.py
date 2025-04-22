from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'category', 'payment_method', 'transaction_date', 'transaction_type', 'description']

class TransactionCSVUploadForm(forms.Form):
    csv_file = forms.FileField()