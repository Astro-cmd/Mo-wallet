"""
Tests for transaction-budget synchronization signals.
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from transactions.models import Transaction
from budget.models import Budget


User = get_user_model()


class TransactionBudgetSyncTestCase(TestCase):
    """Test cases for automatic budget updates when transactions are created/updated."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create budgets for testing
        self.food_budget = Budget.objects.create(
            user=self.user,
            category='food',
            limit=Decimal('5000.00'),
            amount_spent=Decimal('0.00')
        )
        
        self.transport_budget = Budget.objects.create(
            user=self.user,
            category='transport',
            limit=Decimal('2000.00'),
            amount_spent=Decimal('0.00')
        )
    
    def test_create_expense_transaction_updates_budget(self):
        """Test that creating an expense transaction updates the budget amount_spent."""
        # Create an expense transaction
        transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('500.00'),
            category='food',
            description='Groceries',
            payment_method='wallet',
            transaction_type='expense'
        )
        
        # Refresh budget from database
        self.food_budget.refresh_from_db()
        
        # Check that budget amount_spent was updated
        self.assertEqual(self.food_budget.amount_spent, Decimal('500.00'))
    
    def test_create_multiple_expenses_accumulates(self):
        """Test that multiple expense transactions accumulate in the budget."""
        # Create first transaction
        Transaction.objects.create(
            user=self.user,
            amount=Decimal('300.00'),
            category='food',
            payment_method='wallet',
            transaction_type='expense'
        )
        
        # Create second transaction
        Transaction.objects.create(
            user=self.user,
            amount=Decimal('200.00'),
            category='food',
            payment_method='wallet',
            transaction_type='expense'
        )
        
        # Refresh budget
        self.food_budget.refresh_from_db()
        
        # Check that both amounts accumulated
        self.assertEqual(self.food_budget.amount_spent, Decimal('500.00'))
    
    def test_income_transaction_does_not_affect_budget(self):
        """Test that income transactions don't affect budget amount_spent."""
        # Create an income transaction
        Transaction.objects.create(
            user=self.user,
            amount=Decimal('1000.00'),
            category='food',
            payment_method='wallet',
            transaction_type='income'
        )
        
        # Refresh budget
        self.food_budget.refresh_from_db()
        
        # Budget should remain unchanged
        self.assertEqual(self.food_budget.amount_spent, Decimal('0.00'))
    
    def test_update_transaction_amount_updates_budget(self):
        """Test that updating a transaction amount updates the budget."""
        # Create initial transaction
        transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('500.00'),
            category='food',
            payment_method='wallet',
            transaction_type='expense'
        )
        
        self.food_budget.refresh_from_db()
        self.assertEqual(self.food_budget.amount_spent, Decimal('500.00'))
        
        # Update transaction amount
        transaction.amount = Decimal('750.00')
        transaction.save()
        
        # Refresh budget
        self.food_budget.refresh_from_db()
        
        # Budget should be updated with the new amount
        self.assertEqual(self.food_budget.amount_spent, Decimal('750.00'))
    
    def test_change_transaction_type_from_expense_to_income(self):
        """Test that changing transaction type from expense to income removes it from budget."""
        # Create expense transaction
        transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('500.00'),
            category='food',
            payment_method='wallet',
            transaction_type='expense'
        )
        
        self.food_budget.refresh_from_db()
        self.assertEqual(self.food_budget.amount_spent, Decimal('500.00'))
        
        # Change to income
        transaction.transaction_type = 'income'
        transaction.save()
        
        # Refresh budget
        self.food_budget.refresh_from_db()
        
        # Budget amount should be removed
        self.assertEqual(self.food_budget.amount_spent, Decimal('0.00'))
    
    def test_change_transaction_type_from_income_to_expense(self):
        """Test that changing transaction type from income to expense adds it to budget."""
        # Create income transaction
        transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('500.00'),
            category='food',
            payment_method='wallet',
            transaction_type='income'
        )
        
        self.food_budget.refresh_from_db()
        self.assertEqual(self.food_budget.amount_spent, Decimal('0.00'))
        
        # Change to expense
        transaction.transaction_type = 'expense'
        transaction.save()
        
        # Refresh budget
        self.food_budget.refresh_from_db()
        
        # Budget amount should be added
        self.assertEqual(self.food_budget.amount_spent, Decimal('500.00'))
    
    def test_change_transaction_category_updates_budgets(self):
        """Test that changing transaction category updates both old and new budgets."""
        # Create expense in food category
        transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('500.00'),
            category='food',
            payment_method='wallet',
            transaction_type='expense'
        )
        
        self.food_budget.refresh_from_db()
        self.transport_budget.refresh_from_db()
        
        self.assertEqual(self.food_budget.amount_spent, Decimal('500.00'))
        self.assertEqual(self.transport_budget.amount_spent, Decimal('0.00'))
        
        # Change to transport category
        transaction.category = 'transport'
        transaction.save()
        
        # Refresh both budgets
        self.food_budget.refresh_from_db()
        self.transport_budget.refresh_from_db()
        
        # Food budget should be reduced, transport should be increased
        self.assertEqual(self.food_budget.amount_spent, Decimal('0.00'))
        self.assertEqual(self.transport_budget.amount_spent, Decimal('500.00'))
    
    def test_delete_transaction_removes_from_budget(self):
        """Test that deleting a transaction removes it from budget."""
        # Create transaction
        transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('500.00'),
            category='food',
            payment_method='wallet',
            transaction_type='expense'
        )
        
        self.food_budget.refresh_from_db()
        self.assertEqual(self.food_budget.amount_spent, Decimal('500.00'))
        
        # Delete transaction
        transaction.delete()
        
        # Refresh budget
        self.food_budget.refresh_from_db()
        
        # Budget should be back to 0
        self.assertEqual(self.food_budget.amount_spent, Decimal('0.00'))
    
    def test_transaction_for_non_existent_budget_category(self):
        """Test that transaction for non-existent budget is handled gracefully."""
        # Create transaction for category without budget
        transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('500.00'),
            category='utilities',  # No budget for this
            payment_method='wallet',
            transaction_type='expense'
        )
        
        # Should not raise an error, and should complete successfully
        self.assertIsNotNone(transaction.id)
