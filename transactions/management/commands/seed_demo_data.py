from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from transactions.models import Transaction
from budget.models import Budget
from goals.models import SavingsGoal
from core import categories
from django.utils import timezone
from datetime import timedelta, date
import random

class Command(BaseCommand):
    help = 'Seed the database with demo transactions, budgets, and saving goals for a specified user.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to create demo data for')

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} not found.'))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching user: {e}'))
            return

        # Seed Budgets
        budgets_data = [
            {'category': 'food', 'limit': 5000, 'amount_spent': 4200},
            {'category': 'transport', 'limit': 5000, 'amount_spent': 3500},
            {'category': 'housing', 'limit': 10000, 'amount_spent': 5000},
            {'category': 'entertainment', 'limit': 5000, 'amount_spent': 1200},
        ]
        Budget.objects.filter(user=user).delete()
        for b in budgets_data:
            Budget.objects.create(user=user, **b)

        # Seed Savings Goals
        goal_data = [
            {'goal_name': 'New Laptop', 'target_amount': 45000, 'current_savings': 12500, 'deadline': date(2025, 7, 1)},
            {'goal_name': 'Vacation', 'target_amount': 30000, 'current_savings': 18000, 'deadline': date(2025, 12, 15)},
        ]
        SavingsGoal.objects.filter(user=user).delete()
        for g in goal_data:
            SavingsGoal.objects.create(user=user, **g)

        # Seed Transactions
        Transaction.objects.filter(user=user).delete()

        categories_list = [c[0] for c in categories.TRANSACTION_CATEGORIES]
        payment_methods = ['cash', 'card', 'bank']
        transaction_types = ['income', 'expense']
        descriptions = [
            'Grocery shopping', 'Bus fare', 'Electricity bill', 'Movie night', 'Dinner out',
            'Monthly salary', 'Freelance project', 'Gift received', 'Coffee', 'Gym membership',
            'Online subscription', 'Book purchase', 'Pharmacy', 'Taxi ride', 'Lunch',
            'Mobile airtime', 'Water bill', 'Clothing', 'Home supplies', 'Petrol', 'Snacks'
        ]
        now = timezone.now()
        transaction_data = []
        for i in range(100):
            t_type = random.choice(transaction_types)
            category = random.choice(categories_list)
            payment_method = random.choice(payment_methods)
            days_ago = random.randint(0, 90)
            t_date = now - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
            amount = round(random.uniform(200, 50000) if t_type == 'income' else random.uniform(100, 5000), 2)
            description = random.choice(descriptions)
            transaction_data.append({
                'amount': amount,
                'category': category,
                'payment_method': payment_method,
                'transaction_date': t_date,
                'transaction_type': t_type,
                'description': description,
            })
        for t in transaction_data:
            Transaction.objects.create(user=user, **t)

        self.stdout.write(self.style.SUCCESS(f'Demo data seeded for user {username}.'))
