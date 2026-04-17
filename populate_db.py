import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mowallet.settings')
django.setup()

from django.contrib.auth.models import User as AuthUser
from users.models import User
from wallet.models import Wallet
from transactions.models import Transaction
from budget.models import Budget
from goals.models import SavingsGoal
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Create or get user 'moses'
user, created = User.objects.get_or_create(
    username='moses',
    defaults={
        'email': 'moses@mowallet.com',
        'first_name': 'Moses',
        'last_name': 'Kipchoge',
        'phone_number': '+254712345678',
        'country': 'Kenya'
    }
)

if created:
    user.set_password('moses123')
    user.save()
    print(f"✓ Created user: {user.username}")
else:
    print(f"✓ User already exists: {user.username}")

# Create or get wallet
wallet, created = Wallet.objects.get_or_create(
    user=user,
    defaults={'balance': Decimal('50000.00')}
)
if created:
    print(f"✓ Created wallet with balance: KES {wallet.balance}")
else:
    print(f"✓ Wallet exists with balance: KES {wallet.balance}")

# Clear existing data for fresh population
Transaction.objects.filter(user=user).delete()
Budget.objects.filter(user=user).delete()
SavingsGoal.objects.filter(user=user).delete()
print("✓ Cleared existing data")

# Sample transaction data (using correct category keys from TRANSACTION_CATEGORIES)
transactions_data = [
    ('salary', 'income', 'mpesa', Decimal('120000'), 'Monthly salary payment'),
    ('housing', 'expense', 'bank', Decimal('15000'), 'House rent - January'),
    ('groceries', 'expense', 'wallet', Decimal('3500'), 'Weekly shopping'),
    ('utilities', 'expense', 'wallet', Decimal('2000'), 'Electric and water bills'),
    ('business_expenses', 'income', 'mpesa', Decimal('25000'), 'Web development project'),
    ('entertainment', 'expense', 'cash', Decimal('1200'), 'Dinner with friends'),
    ('transport', 'expense', 'wallet', Decimal('500'), 'Uber rides'),
    ('subscriptions', 'expense', 'wallet', Decimal('800'), 'Monthly phone subscription'),
    ('gym_membership', 'expense', 'wallet', Decimal('2500'), 'Monthly fitness'),
    ('insurance', 'expense', 'bank', Decimal('5000'), 'Health insurance'),
    ('transportation', 'expense', 'cash', Decimal('3000'), 'Car fuel'),
    ('clothing', 'expense', 'wallet', Decimal('4200'), 'Clothing and accessories'),
    ('business_expenses', 'income', 'mpesa', Decimal('15000'), 'Bonus for completed projects'),
    ('savings', 'income', 'bank', Decimal('2500'), 'Savings account interest'),
]

# Create transactions with varied dates (past 60 days)
base_date = datetime.now()
for i, (category, trans_type, payment_method, amount, description) in enumerate(transactions_data):
    days_ago = random.randint(0, 60)
    trans_date = base_date - timedelta(days=days_ago)
    
    transaction = Transaction.objects.create(
        user=user,
        category=category,
        transaction_type=trans_type,
        payment_method=payment_method,
        amount=amount,
        description=description,
        date=trans_date,
        transaction_date=trans_date
    )

print(f"✓ Created {len(transactions_data)} transactions")

# Update wallet balance
total_income = sum(a for _, t, _, a, _ in transactions_data if t == 'income')
total_expenses = sum(a for _, t, _, a, _ in transactions_data if t == 'expense')
net_balance = Decimal('50000') + total_income - total_expenses
wallet.balance = net_balance
wallet.save()
print(f"✓ Updated wallet balance: KES {wallet.balance}")

# Create budgets for various categories
budgets_data = [
    ('food', Decimal('8000')),
    ('transport', Decimal('5000')),
    ('entertainment', Decimal('3000')),
    ('utilities', Decimal('4000')),
    ('clothing', Decimal('6000')),
    ('health', Decimal('3500')),
    ('insurance', Decimal('5000')),
]

for category, limit in budgets_data:
    budget = Budget.objects.create(
        user=user,
        category=category,
        limit=limit,
        amount_spent=Decimal('0')
    )

print(f"✓ Created {len(budgets_data)} budgets")

# Create savings goals
goals_data = [
    ('Emergency Fund', Decimal('100000'), Decimal('35000'), 180),
    ('Car Purchase', Decimal('500000'), Decimal('50000'), 365),
    ('Vacation to Zanzibar', Decimal('80000'), Decimal('15000'), 120),
    ('Home Renovation', Decimal('200000'), Decimal('20000'), 240),
    ('Education Fund', Decimal('150000'), Decimal('30000'), 300),
]

for goal_name, target, current, days in goals_data:
    goal = SavingsGoal.objects.create(
        user=user,
        goal_name=goal_name,
        target_amount=target,
        current_savings=current,
        deadline=datetime.now().date() + timedelta(days=days)
    )

print(f"✓ Created {len(goals_data)} savings goals")

print("\n" + "="*50)
print("DATABASE POPULATION COMPLETE!")
print("="*50)
print(f"User: {user.username}")
print(f"Email: {user.email}")
print(f"Wallet Balance: KES {wallet.balance}")
print(f"Transactions: {Transaction.objects.filter(user=user).count()}")
print(f"Budgets: {Budget.objects.filter(user=user).count()}")
print(f"Savings Goals: {SavingsGoal.objects.filter(user=user).count()}")
print("="*50)
