from django.contrib import admin
from django.utils.html import format_html
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Transaction model."""
    
    list_display = (
        'transaction_id_display',
        'user_display',
        'amount_display',
        'category_display',
        'transaction_type_badge',
        'payment_method_display',
        'date_display',
    )
    list_filter = (
        'transaction_type',
        'payment_method',
        'category',
        'date',
        'transaction_date',
    )
    search_fields = (
        'user__username',
        'user__email',
        'description',
        'category',
    )
    readonly_fields = (
        'date',
        'transaction_date',
        'created_date_display',
        'amount_display_detail',
    )
    
    fieldsets = (
        ('Transaction Information', {
            'fields': (
                'user',
                'transaction_type',
                'amount',
                'payment_method',
            ),
        }),
        ('Details', {
            'fields': (
                'category',
                'description',
            ),
        }),
        ('Dates', {
            'fields': (
                'date',
                'transaction_date',
                'created_date_display',
            ),
            'classes': ('collapse',),
        }),
    )
    
    date_hierarchy = 'date'
    ordering = ('-date',)
    
    def transaction_id_display(self, obj):
        return f"#{obj.id}"
    transaction_id_display.short_description = 'Transaction ID'
    
    def user_display(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_display.short_description = 'User'
    
    def amount_display(self, obj):
        if obj.transaction_type == 'income':
            color = 'green'
            prefix = '+'
        else:
            color = 'red'
            prefix = '-'
        return format_html(
            '<span style="color: {}; font-weight: bold;\">{}{}</span>',
            color,
            prefix,
            obj.amount,
        )
    amount_display.short_description = 'Amount'
    
    def category_display(self, obj):
        return obj.category.capitalize()
    category_display.short_description = 'Category'
    
    def transaction_type_badge(self, obj):
        colors = {
            'income': 'green',
            'expense': 'red',
            'transfer': 'blue',
        }
        color = colors.get(obj.transaction_type, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;\">{}</span>',
            color,
            obj.transaction_type.upper(),
        )
    transaction_type_badge.short_description = 'Type'
    
    def payment_method_display(self, obj):
        return obj.get_payment_method_display()
    payment_method_display.short_description = 'Payment Method'
    
    def date_display(self, obj):
        return obj.date.strftime('%Y-%m-%d %H:%M') if obj.date else '-'
    date_display.short_description = 'Date'
    
    def created_date_display(self, obj):
        return obj.date
    created_date_display.short_description = 'Created Date'
    
    def amount_display_detail(self, obj):
        return format_html(
            '<strong>KES {}</strong>',
            obj.amount,
        )
    amount_display_detail.short_description = 'Amount (Detail)'


admin.site.register(Transaction, TransactionAdmin)
