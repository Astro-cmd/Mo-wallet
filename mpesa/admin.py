from django.contrib import admin
from django.utils.html import format_html
from .models import MpesaTransaction


class MpesaTransactionAdmin(admin.ModelAdmin):
    """Enhanced admin interface for M-Pesa Transaction model."""
    
    list_display = (
        'transaction_id',
        'phone_number_display',
        'amount_display',
        'transaction_type_badge',
        'account_reference_display',
        'transaction_date_display',
    )
    list_filter = (
        'transaction_type',
        'transaction_date',
    )
    search_fields = (
        'transaction_id',
        'phone_number',
        'account_reference',
    )
    readonly_fields = (
        'transaction_id',
        'transaction_date',
        'organization_balance_display',
    )
    
    fieldsets = (
        ('Transaction Details', {
            'fields': (
                'transaction_id',
                'transaction_type',
                'amount',
                'phone_number',
                'account_reference',
            ),
        }),
        ('Description', {
            'fields': (
                'transaction_description',
            ),
        }),
        ('Financial Info', {
            'fields': (
                'organization_balance_display',
            ),
        }),
        ('Metadata', {
            'fields': (
                'transaction_date',
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ('-transaction_date',)
    date_hierarchy = 'transaction_date'
    
    def phone_number_display(self, obj):
        # Mask phone number for privacy
        if len(obj.phone_number) >= 9:
            masked = '***' + obj.phone_number[-4:]
            return masked
        return obj.phone_number
    phone_number_display.short_description = 'Phone Number'
    
    def amount_display(self, obj):
        return format_html(
            '<span style="color: green; font-weight: bold;">KES {:,.2f}</span>',
            obj.amount,
        )
    amount_display.short_description = 'Amount'
    
    def transaction_type_badge(self, obj):
        colors = {
            'C2B': '#007bff',
            'B2C': '#28a745',
            'B2B': '#17a2b8',
        }
        color = colors.get(obj.transaction_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;\">{}</span>',
            color,
            obj.get_transaction_type_display(),
        )
    transaction_type_badge.short_description = 'Type'
    
    def account_reference_display(self, obj):
        if obj.account_reference:
            return obj.account_reference[:30] + ('...' if len(obj.account_reference) > 30 else '')
        return '-'
    account_reference_display.short_description = 'Account Reference'
    
    def transaction_date_display(self, obj):
        return obj.transaction_date.strftime('%Y-%m-%d %H:%M:%S')
    transaction_date_display.short_description = 'Date & Time'
    
    def organization_balance_display(self, obj):
        if obj.organization_balance:
            return format_html(
                '<strong>KES {:,.2f}</strong>',
                obj.organization_balance,
            )
        return '-'
    organization_balance_display.short_description = 'Organization Balance'


admin.site.register(MpesaTransaction, MpesaTransactionAdmin)
