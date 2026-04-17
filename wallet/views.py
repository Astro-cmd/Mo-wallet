from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.db.models import Sum, Q
from .models import Wallet, Invoice, PaymentMethod, Bill
from .forms import WalletForm, WalletTransferForm
from decimal import Decimal

@login_required
def wallet_list(request):
    wallets = Wallet.objects.filter(user=request.user)
    main_wallet = wallets.first()
    total_balance = sum(wallet.balance for wallet in wallets)

    context = {
        'wallets': wallets,
        'total_wallets': wallets.count(),
        'total_balance': total_balance,
        'main_wallet_balance': main_wallet.balance if main_wallet else 0,
        'form': WalletForm()
    }
    return render(request, 'wallet.html', context)

@login_required
def create_wallet(request):
    if request.method == 'POST':
        form = WalletForm(request.POST)
        if form.is_valid():
            existing_wallet = Wallet.objects.filter(user=request.user).first()
            if existing_wallet:
                existing_wallet.balance = form.cleaned_data['balance']
                existing_wallet.save(update_fields=['balance', 'updated_at'])
                messages.success(request, 'Wallet balance updated successfully.')
            else:
                wallet = form.save(commit=False)
                wallet.user = request.user
                wallet.save()
                messages.success(request, 'Wallet created successfully.')
            return redirect('wallet:list')
    return redirect('wallet:list')

@login_required
def edit_wallet(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id)
    if wallet.user != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = WalletForm(request.POST, instance=wallet)
        if form.is_valid():
            form.save()
            return redirect('wallet:list')
    else:
        form = WalletForm(instance=wallet)
        return render(request, 'wallet_edit_form.html', {'form': form})


@login_required
def billing_page(request):
    """Display billing page with invoices, bills, and payment methods"""
    
    # Get user's wallet
    wallet = Wallet.objects.filter(user=request.user).first()
    
    # Get all invoices for the user
    invoices = Invoice.objects.filter(user=request.user)
    recent_invoices = invoices[:5]
    
    # Get payment methods
    payment_methods = PaymentMethod.objects.filter(user=request.user, is_active=True)
    primary_payment = payment_methods.filter(is_primary=True).first()
    
    # Get bills
    bills = Bill.objects.filter(user=request.user)
    recent_bills = bills[:5]
    unpaid_bills = bills.filter(is_paid=False)
    
    # Calculate billing statistics
    total_invoiced = invoices.filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    pending_amount = invoices.filter(status__in=['pending', 'overdue']).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    overdue_invoices = invoices.filter(status='overdue').count()
    
    # Calculate bill statistics
    total_bills_amount = bills.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    unpaid_bills_amount = unpaid_bills.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    # Get recent transactions
    from transactions.models import Transaction
    recent_transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')[:5]
    
    context = {
        'wallet': wallet,
        'wallet_balance': wallet.balance if wallet else Decimal('0'),
        'invoices': recent_invoices,
        'all_invoices': invoices,
        'payment_methods': payment_methods,
        'primary_payment': primary_payment,
        'bills': recent_bills,
        'all_bills': bills,
        'unpaid_bills': unpaid_bills,
        'recent_transactions': recent_transactions,
        
        # Statistics
        'total_invoiced': total_invoiced,
        'pending_amount': pending_amount,
        'overdue_invoices': overdue_invoices,
        'total_bills_amount': total_bills_amount,
        'unpaid_bills_amount': unpaid_bills_amount,
        'unpaid_bills_count': unpaid_bills.count(),
    }
    
    return render(request, 'billing.html', context)

@login_required
def delete_wallet(request, wallet_id):
    if request.method == 'POST':
        wallet = get_object_or_404(Wallet, id=wallet_id)
        if wallet.user != request.user:
            raise PermissionDenied
        wallet.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=405)

@login_required
@transaction.atomic
def transfer_funds(request):
    if request.method == 'POST':
        form = WalletTransferForm(request.POST)
        if form.is_valid():
            source_wallet_id = request.POST.get('source_wallet')
            destination_wallet_id = request.POST.get('destination_wallet')
            amount = Decimal(form.cleaned_data['amount'])

            source_wallet = get_object_or_404(Wallet, id=source_wallet_id, user=request.user)
            destination_wallet = get_object_or_404(Wallet, id=destination_wallet_id, user=request.user)

            if source_wallet.balance < amount:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Insufficient funds in source wallet'
                }, status=400)

            source_wallet.balance -= amount
            destination_wallet.balance += amount
            source_wallet.save()
            destination_wallet.save()

            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=405)
