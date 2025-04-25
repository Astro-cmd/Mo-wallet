from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from .forms import TransactionForm, TransactionCSVUploadForm
from .models import Transaction
import csv
from io import TextIOWrapper

@login_required
def transactions_view(request):
    # Initialize forms
    form = TransactionForm()
    csv_form = TransactionCSVUploadForm()
    
    if request.method == 'POST':
        if 'manual_entry' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                messages.success(request, "Transaction added successfully.")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success'})
                return redirect('transactions:transactions')
            elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                }, status=400)
        elif 'csv_upload' in request.POST:
            csv_form = TransactionCSVUploadForm(request.POST, request.FILES)
            if csv_form.is_valid():
                try:
                    csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        Transaction.objects.create(
                            user=request.user,
                            amount=row['amount'],
                            category=row['category'],
                            payment_method=row['payment_method'],
                            transaction_date=row['transaction_date'],
                            transaction_type=row['transaction_type'],
                            description=row['description']
                        )
                    messages.success(request, "Transactions uploaded successfully.")
                    return redirect('transactions:transactions')
                except Exception as e:
                    messages.error(request, f"Error uploading CSV: {str(e)}")
            else:
                messages.error(request, "Please correct the errors in the form.")

    # Get all transactions for the user
    transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')
    return render(request, 'transactions.html', {
        'form': form,
        'csv_form': csv_form,
        'transactions': transactions
    })

@login_required
def transaction_edit(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if transaction.user != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully.")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('transactions:transactions')
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
    else:
        form = TransactionForm(instance=transaction)
    
    context = {
        'form': form,
        'transaction': transaction
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('transaction_edit_form.html', context, request=request)
        return HttpResponse(html)
    return render(request, 'transaction_edit_form.html', context)

@login_required
def transaction_delete(request, transaction_id):
    if request.method == 'POST':
        transaction = get_object_or_404(Transaction, id=transaction_id)
        if transaction.user != request.user:
            raise PermissionDenied
        transaction.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=405)
