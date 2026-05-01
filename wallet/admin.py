from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Wallet, Prediction, PaymentMethod, Invoice, Bill


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Wallet model."""
    
    list_display = ('wallet_id', 'user_display', 'balance_display', 'status_indicator', 'last_updated')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'user_info')
    
    fieldsets = (
        ('Wallet Information', {
            'fields': ('user', 'user_info', 'balance'),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def wallet_id(self, obj):
        return f"WAL-{obj.id:05d}"
    wallet_id.short_description = 'Wallet ID'
    
    def user_display(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_display.short_description = 'User'
    
    def balance_display(self, obj):
        return format_html(
            '<strong style="color: green; font-size: 14px;\">KES {:,.2f}</strong>',
            obj.balance,
        )
    balance_display.short_description = 'Balance'
    
    def status_indicator(self, obj):
        if obj.balance > 0:
            icon = '✓'
            color = 'green'
        else:
            icon = '⚠'
            color = 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold; font-size: 16px;\">{}</span>',
            color,
            icon,
        )
    status_indicator.short_description = 'Status'
    
    def last_updated(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M')
    last_updated.short_description = 'Last Updated'
    
    def user_info(self, obj):
        return format_html(
            '<strong>Email:</strong> {}<br/><strong>Username:</strong> {}',
            obj.user.email,
            obj.user.username,
        )
    user_info.short_description = 'User Information'


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Prediction model."""
    
    list_display = ('prediction_id', 'user_display', 'type_badge', 'predicted_value_display', 'target_date_display', 'status_badge')
    list_filter = ('prediction_type', 'status', 'target_date')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'prediction_date_display')
    
    fieldsets = (
        ('Prediction Details', {
            'fields': ('user', 'prediction_type', 'predicted_value'),
        }),
        ('Related Objects', {
            'fields': ('budget', 'goal'),
        }),
        ('Timeline', {
            'fields': ('prediction_date_display', 'target_date', 'status'),
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def prediction_id(self, obj):
        return f"PRED-{obj.id:05d}"
    prediction_id.short_description = 'Prediction ID'
    
    def user_display(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_display.short_description = 'User'
    
    def type_badge(self, obj):
        colors = {'budget': '#ffc107', 'goal': '#17a2b8'}
        color = colors.get(obj.prediction_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;\">{}</span>',
            color,
            obj.get_prediction_type_display(),
        )
    type_badge.short_description = 'Type'
    
    def predicted_value_display(self, obj):
        return format_html('<strong>KES {:,.2f}</strong>', obj.predicted_value)
    predicted_value_display.short_description = 'Predicted Value'
    
    def target_date_display(self, obj):
        return obj.target_date.strftime('%Y-%m-%d')
    target_date_display.short_description = 'Target Date'
    
    def status_badge(self, obj):
        colors = {'pending': '#ffc107', 'achieved': '#28a745', 'failed': '#dc3545'}
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;\">{}</span>',
            color,
            obj.status.upper(),
        )
    status_badge.short_description = 'Status'
    
    def prediction_date_display(self, obj):
        return obj.prediction_date.strftime('%Y-%m-%d')
    prediction_date_display.short_description = 'Prediction Date'


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    """Enhanced admin interface for PaymentMethod model."""
    
    list_display = ('payment_id', 'user_display', 'card_type_badge', 'masked_card', 'cardholder_name', 'expiry_display', 'primary_badge', 'active_badge')
    list_filter = ('card_type', 'is_primary', 'is_active')
    search_fields = ('user__username', 'user__email', 'cardholder_name', 'card_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Payment Method', {
            'fields': ('user', 'card_type', 'card_number', 'cardholder_name'),
        }),
        ('Expiry', {
            'fields': ('expiry_month', 'expiry_year'),
        }),
        ('Settings', {
            'fields': ('is_primary', 'is_active'),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def payment_id(self, obj):
        return f"PM-{obj.id:05d}"
    payment_id.short_description = 'Payment ID'
    
    def user_display(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_display.short_description = 'User'
    
    def card_type_badge(self, obj):
        colors = {'visa': '#1A1F71', 'mastercard': '#FF5F00', 'amex': '#006FCF', 'discover': '#FF6000'}
        color = colors.get(obj.card_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;\">{}</span>',
            color,
            obj.get_card_type_display(),
        )
    card_type_badge.short_description = 'Card Type'
    
    def masked_card(self, obj):
        if len(obj.card_number) >= 4:
            return f"**** **** **** {obj.card_number[-4:]}"
        return obj.card_number
    masked_card.short_description = 'Card Number'
    
    def expiry_display(self, obj):
        return f"{obj.expiry_month:02d}/{obj.expiry_year}"
    expiry_display.short_description = 'Expiry'
    
    def primary_badge(self, obj):
        if obj.is_primary:
            return format_html('<span style="color: gold; font-weight: bold;">★ Primary</span>')
        return '-'
    primary_badge.short_description = 'Primary'
    
    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ Active</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;\">✗ Inactive</span>')
    active_badge.short_description = 'Active'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Invoice model."""
    
    list_display = ('invoice_id', 'user_display', 'amount_display', 'status_badge', 'due_date_display', 'days_until_due_display', 'overdue_indicator')
    list_filter = ('status', 'due_date', 'issue_date')
    search_fields = ('invoice_number', 'user__username', 'user__email', 'description')
    readonly_fields = ('invoice_number', 'created_at', 'updated_at', 'days_until_due')
    
    fieldsets = (
        ('Invoice Details', {
            'fields': ('invoice_number', 'user', 'amount', 'description'),
        }),
        ('Status', {
            'fields': ('status',),
        }),
        ('Dates', {
            'fields': ('issue_date', 'due_date', 'paid_date', 'days_until_due'),
        }),
        ('Payment', {
            'fields': ('payment_method',),
        }),
        ('Notes', {
            'fields': ('notes',),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    date_hierarchy = 'due_date'
    
    def invoice_id(self, obj):
        return f"INV-{obj.id:05d}"
    invoice_id.short_description = 'Invoice ID'
    
    def user_display(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_display.short_description = 'User'
    
    def amount_display(self, obj):
        return format_html('<strong>KES {:,.2f}</strong>', obj.amount)
    amount_display.short_description = 'Amount'
    
    def status_badge(self, obj):
        colors = {'draft': '#6c757d', 'pending': '#ffc107', 'paid': '#28a745', 'overdue': '#dc3545', 'cancelled': '#999'}
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;\">{}</span>',
            color,
            obj.get_status_display(),
        )
    status_badge.short_description = 'Status'
    
    def due_date_display(self, obj):
        return obj.due_date.strftime('%Y-%m-%d')
    due_date_display.short_description = 'Due Date'
    
    def days_until_due_display(self, obj):
        days = obj.days_until_due
        if obj.status == 'paid':
            return format_html('<span style="color: green;">Paid</span>')
        elif obj.is_overdue:
            return format_html('<span style="color: red; font-weight: bold;\">{} days overdue</span>', abs(days))
        else:
            return format_html('<span style="color: green;\">{} days left</span>', days)
    days_until_due_display.short_description = 'Days Until Due'
    
    def overdue_indicator(self, obj):
        if obj.is_overdue:
            return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 8px; '
                             'border-radius: 3px; font-weight: bold;\">⚠ OVERDUE</span>')
        return '-'
    overdue_indicator.short_description = 'Overdue'


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Bill model."""
    
    list_display = ('bill_id', 'user_display', 'bill_name', 'category_display', 'amount_display', 'due_date_display', 'paid_badge', 'overdue_badge')
    list_filter = ('category', 'is_paid', 'due_date')
    search_fields = ('user__username', 'user__email', 'name')
    readonly_fields = ('created_at', 'updated_at', 'days_until_due_display')
    
    fieldsets = (
        ('Bill Information', {
            'fields': ('user', 'name', 'category', 'amount'),
        }),
        ('Schedule', {
            'fields': ('due_date', 'days_until_due_display'),
        }),
        ('Payment Status', {
            'fields': ('is_paid',),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    date_hierarchy = 'due_date'
    
    def bill_id(self, obj):
        return f"BILL-{obj.id:05d}"
    bill_id.short_description = 'Bill ID'
    
    def user_display(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_display.short_description = 'User'
    
    def bill_name(self, obj):
        return obj.name[:30] + ('...' if len(obj.name) > 30 else '')
    bill_name.short_description = 'Bill Name'
    
    def category_display(self, obj):
        return obj.get_category_display() if hasattr(obj, 'get_category_display') else obj.category.capitalize()
    category_display.short_description = 'Category'
    
    def amount_display(self, obj):
        return format_html('<strong>KES {:,.2f}</strong>', obj.amount)
    amount_display.short_description = 'Amount'
    
    def due_date_display(self, obj):
        return obj.due_date.strftime('%Y-%m-%d')
    due_date_display.short_description = 'Due Date'
    
    def paid_badge(self, obj):
        if obj.is_paid:
            return format_html('<span style="color: green; font-weight: bold;\">✓ Paid</span>')
        else:
            return format_html('<span style="color: orange; font-weight: bold;\">⏳ Pending</span>')
    paid_badge.short_description = 'Payment Status'
    
    def overdue_badge(self, obj):
        if obj.is_overdue:
            return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 8px; '
                             'border-radius: 3px; font-weight: bold;\">⚠ OVERDUE</span>')
        return '-'
    overdue_badge.short_description = 'Overdue'
    
    def days_until_due_display(self, obj):
        days = (obj.due_date - timezone.now().date()).days
        if obj.is_overdue:
            return format_html('<span style="color: red; font-weight: bold;\">{} days overdue</span>', abs(days))
        else:
            return format_html('<span style="color: green;\">{} days left</span>', days)
    days_until_due_display.short_description = 'Days Until Due'
