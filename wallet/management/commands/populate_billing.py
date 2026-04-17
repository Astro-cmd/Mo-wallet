from django.core.management.base import BaseCommand
from users.models import User
from wallet.models import PaymentMethod, Invoice, Bill
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populate sample billing data for testing'

    def handle(self, *args, **options):
        # Get moses user
        try:
            user = User.objects.get(username='moses')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User "moses" not found'))
            return

        # Clear existing billing data
        PaymentMethod.objects.filter(user=user).delete()
        Invoice.objects.filter(user=user).delete()
        Bill.objects.filter(user=user).delete()

        # Create Payment Methods
        payment_methods_data = [
            {
                'card_type': 'visa',
                'card_number': '**** **** **** 4242',
                'cardholder_name': 'Moses Kipchoge',
                'expiry_month': 12,
                'expiry_year': 2025,
                'is_primary': True,
                'is_active': True,
            },
            {
                'card_type': 'mastercard',
                'card_number': '**** **** **** 5555',
                'cardholder_name': 'Moses Kipchoge',
                'expiry_month': 9,
                'expiry_year': 2026,
                'is_primary': False,
                'is_active': True,
            },
            {
                'card_type': 'amex',
                'card_number': '**** **** **** 3782',
                'cardholder_name': 'Moses Kipchoge',
                'expiry_month': 6,
                'expiry_year': 2024,
                'is_primary': False,
                'is_active': False,
            },
        ]

        payment_methods = []
        for data in payment_methods_data:
            pm = PaymentMethod.objects.create(user=user, **data)
            payment_methods.append(pm)
            self.stdout.write(self.style.SUCCESS(f'Created payment method: {pm.card_type}'))

        # Create Invoices
        invoices_data = [
            {
                'invoice_number': 'INV-2024-001',
                'amount': Decimal('5500.00'),
                'description': 'Monthly subscription - Premium Plan',
                'status': 'paid',
                'due_date': timezone.now().date() - timedelta(days=15),
                'paid_date': timezone.now().date() - timedelta(days=10),
            },
            {
                'invoice_number': 'INV-2024-002',
                'amount': Decimal('12500.00'),
                'description': 'Software License - Annual',
                'status': 'pending',
                'due_date': timezone.now().date() + timedelta(days=7),
                'paid_date': None,
            },
            {
                'invoice_number': 'INV-2024-003',
                'amount': Decimal('3200.00'),
                'description': 'Cloud Services - Q1',
                'status': 'overdue',
                'due_date': timezone.now().date() - timedelta(days=5),
                'paid_date': None,
            },
            {
                'invoice_number': 'INV-2024-004',
                'amount': Decimal('8900.00'),
                'description': 'Consulting Services',
                'status': 'pending',
                'due_date': timezone.now().date() + timedelta(days=30),
                'paid_date': None,
            },
            {
                'invoice_number': 'INV-2024-005',
                'amount': Decimal('2150.00'),
                'description': 'Office Equipment',
                'status': 'paid',
                'due_date': timezone.now().date() - timedelta(days=30),
                'paid_date': timezone.now().date() - timedelta(days=20),
            },
        ]

        for data in invoices_data:
            invoice = Invoice.objects.create(
                user=user,
                payment_method=payment_methods[0] if data['status'] == 'paid' else None,
                **data
            )
            self.stdout.write(self.style.SUCCESS(f'Created invoice: {invoice.invoice_number}'))

        # Create Bills
        bills_data = [
            {
                'name': 'Electricity Bill',
                'category': 'utilities',
                'amount': Decimal('2500.00'),
                'due_date': timezone.now().date() + timedelta(days=5),
                'is_paid': False,
                'recurring': True,
            },
            {
                'name': 'Internet Bill',
                'category': 'utilities',
                'amount': Decimal('1500.00'),
                'due_date': timezone.now().date() + timedelta(days=3),
                'is_paid': False,
                'recurring': True,
            },
            {
                'name': 'Netflix Subscription',
                'category': 'subscriptions',
                'amount': Decimal('500.00'),
                'due_date': timezone.now().date() + timedelta(days=10),
                'is_paid': True,
                'recurring': True,
            },
            {
                'name': 'Car Insurance',
                'category': 'insurance',
                'amount': Decimal('5000.00'),
                'due_date': timezone.now().date() - timedelta(days=2),
                'is_paid': False,
                'recurring': True,
            },
            {
                'name': 'Rent Payment',
                'category': 'rent',
                'amount': Decimal('25000.00'),
                'due_date': timezone.now().date(),
                'is_paid': False,
                'recurring': True,
            },
            {
                'name': 'Property Tax',
                'category': 'taxes',
                'amount': Decimal('8500.00'),
                'due_date': timezone.now().date() + timedelta(days=20),
                'is_paid': False,
                'recurring': False,
            },
        ]

        for data in bills_data:
            bill = Bill.objects.create(user=user, **data)
            self.stdout.write(self.style.SUCCESS(f'Created bill: {bill.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated billing data'))
