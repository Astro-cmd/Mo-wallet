from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from .models import Wallet
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
            wallet = form.save(commit=False)
            wallet.user = request.user
            wallet.save()
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
