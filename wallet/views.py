from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Wallet
from users.models import User

@login_required
def wallet_detail(request):
    wallet = get_object_or_404(Wallet, user=request.user)
    return render(request, 'wallet/wallet_detail.html', {'wallet': wallet})

@login_required
def create_wallet(request):
    if not hasattr(request.user, 'wallet'):
        Wallet.objects.create(user=request.user)
    return render(request, 'wallet/wallet_created.html')
