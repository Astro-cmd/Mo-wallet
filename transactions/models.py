from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from users.models import User
from core import categories

class Transaction(models.Model):
    TRANSACTION_CATEGORIES = (
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('housing', 'Housing'),
        ('entertainment', 'Entertainment'),
        ('health', 'Health'),
        ('education', 'Education'),
        ('other', 'Other'),
        ('savings', 'Savings'),
        ('investments', 'Investments'),
        ('utilities', 'Utilities'),
        ('clothing', 'Clothing'),
        ('gifts', 'Gifts'),
        ('travel', 'Travel'),
        ('groceries', 'Groceries'),
        ('subscriptions', 'Subscriptions'),
        ('bills', 'Bills'),
        ('miscellaneous', 'Miscellaneous'),
        ('debt_repayment', 'Debt Repayment'),
        ('insurance', 'Insurance'),
        ('charity', 'Charity'),
        ('home_improvement', 'Home Improvement'),
        ('furniture', 'Furniture'),
        ('electronics', 'Electronics'),
        ('toys', 'Toys'),
        ('sports', 'Sports'),
        ('hobbies', 'Hobbies'),
        ('pets', 'Pets'),
        ('vacation', 'Vacation'),
        ('events', 'Events'),
        ('personal_care', 'Personal Care'),
        ('transportation', 'Transportation'),
        ('home_services', 'Home Services'),
        ('legal', 'Legal'),
        ('professional_services', 'Professional Services'),
        ('business_expenses', 'Business Expenses'),
        ('marketing', 'Marketing'),
        ('software', 'Software'),
        ('website', 'Website'),
        ('advertising', 'Advertising'),
        ('consulting', 'Consulting'),
        ('training', 'Training'),
        ('education_tuition', 'Education Tuition'),
        ('childcare', 'Childcare'),
        ('eldercare', 'Eldercare'),
        ('medical', 'Medical'),
        ('dental', 'Dental'),
        ('vision', 'Vision'),
        
    )
    
    TRANSACTION_TYPE = (
        ('income', 'Income'),
        ('expense', 'Expense')
    )
    PAYMENT_METHODS = (
        ('mpesa', 'M-Pesa'),
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank', 'Bank Transfer'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_date = models.DateTimeField(default=timezone.now)
    transaction_type = models.CharField(max_length=20, choices = TRANSACTION_TYPE)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-transaction_date']
    
    def __str__(self):
        return f"{self.amount} - {self.category} ({self.user.username})"

@receiver(pre_save, sender=Transaction)
def add_category_if_not_exists(sender, instance, **kwargs):
    if instance.category not in dict(categories.TRANSACTION_CATEGORIES).keys():
        Transaction.TRANSACTION_CATEGORIES += ((instance.category, instance.category.capitalize()),)