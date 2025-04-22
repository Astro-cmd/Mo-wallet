from django.shortcuts import render
from users.models import User
from testimonials.models  import Feature, Testimonial
from transactions.models import Transaction
from goals.models import SavingsGoal
from django.db.models import Sum


def features_view(request):
    return render(request, 'features.html')

def help_view(request):
    return render(request, 'help.html')

def home(request):
    context = {
        'user_count': User.objects.count(),
        'features': Feature.objects.filter(active=True)[:3],
        'testimonials': Testimonial.objects.filter(approved=True)[:3],
        'stats': {
            'users': User.objects.count(),
            'transactions': Transaction.objects.aggregate(Sum('amount'))['amount__sum'],
            'goals': SavingsGoal.objects.filter(completed=True).count(),
            'countries': User.objects.values('country').distinct().count()
        }
    }
    return render(request, 'home.html', context)

def dashboard_view(request):
    return render(request, 'dashboard.html')