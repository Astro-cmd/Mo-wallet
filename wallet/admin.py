from django.contrib import admin
from .models import Wallet, Prediction, PaymentMethod, Invoice, Bill

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'prediction_type', 'predicted_value', 'target_date', 'status')
    list_filter = ('prediction_type', 'status')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_type', 'card_number', 'cardholder_name', 'is_primary', 'is_active')
    list_filter = ('card_type', 'is_primary', 'is_active')
    search_fields = ('user__username', 'cardholder_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'user', 'amount', 'status', 'due_date', 'is_overdue')
    list_filter = ('status', 'due_date')
    search_fields = ('invoice_number', 'user__username')
    readonly_fields = ('invoice_number', 'created_at', 'updated_at')

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'name', 'amount', 'due_date', 'is_paid', 'is_overdue')
    list_filter = ('category', 'is_paid', 'due_date')
    search_fields = ('user__username', 'name')
    readonly_fields = ('created_at', 'updated_at')
