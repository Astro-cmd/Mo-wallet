"""
Management command to recalculate budget amounts from existing transactions.
Useful for initial setup or fixing budget amounts.
"""
from django.core.management.base import BaseCommand
from django.db.models import Sum, Q
from decimal import Decimal
from transactions.models import Transaction
from budget.models import Budget


class Command(BaseCommand):
    help = 'Recalculate budget amounts based on existing expense transactions'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            help='Recalculate budgets for a specific user ID',
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset all budgets to 0 before recalculating',
        )
    
    def handle(self, *args, **options):
        user_id = options.get('user_id')
        reset = options.get('reset')
        
        # Get all budgets to recalculate
        if user_id:
            budgets = Budget.objects.filter(user_id=user_id)
            self.stdout.write(f'Recalculating budgets for user ID {user_id}')
        else:
            budgets = Budget.objects.all()
            self.stdout.write('Recalculating all budgets')
        
        if reset:
            budgets.update(amount_spent=0)
            self.stdout.write(self.style.WARNING('Reset all budget amounts to 0'))
        
        updated_count = 0
        
        for budget in budgets:
            # Get all expense transactions for this user and category
            total_spent = Transaction.objects.filter(
                user=budget.user,
                category=budget.category,
                transaction_type='expense'
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
            
            # Update the budget if amount changed
            if budget.amount_spent != total_spent:
                budget.amount_spent = total_spent
                budget.save()
                updated_count += 1
                
                self.stdout.write(
                    f'  Updated: {budget.user.username} - {budget.get_category_display()} '
                    f'(Spent: KES {total_spent:,.2f}, Limit: KES {budget.limit:,.2f})'
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully updated {updated_count} budget(s)')
        )
