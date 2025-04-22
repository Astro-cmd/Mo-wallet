from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TransactionForm, TransactionCSVUploadForm
from .models import Transaction
import csv
from io import TextIOWrapper

def transactions_view(request):
    if request.method == 'POST':
        if 'manual_entry' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Transaction added successfully.")
                return redirect('transactions:transactions')
        elif 'csv_upload' in request.POST:
            csv_form = TransactionCSVUploadForm(request.POST, request.FILES)
            if csv_form.is_valid():
                csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
                reader = csv.DictReader(csv_file)
                for row in reader:
                    Transaction.objects.create(
                        amount=row['amount'],
                        category=row['category'],
                        payment_method=row['payment_method'],
                        transaction_date=row['transaction_date'],
                        transaction_type=row['transaction_type'],
                        description=row['description']
                    )
                messages.success(request, "Transactions uploaded successfully.")
                return redirect('transactions:transactions')
    else:
        form = TransactionForm()
        csv_form = TransactionCSVUploadForm()

    transactions = Transaction.objects.all()
    return render(request, 'transactions.html', {
        'form': form,
        'csv_form': csv_form,
        'transactions': transactions
    })
