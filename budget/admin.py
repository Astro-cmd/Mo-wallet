from django.contrib import admin
from django.utils.html import format_html
from .models import Budget


class BudgetAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Budget model."""
    
    list_display = (
        'budget_id',
        'user_display',
        'category_display',
        'limit_display',
        'spent_display',
        'remaining_display',
        'progress_bar',
        'status_badge',
    )
    list_filter = (
        'category',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'user__username',
        'user__email',
        'category',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'remaining_display_detail',
        'percentage_display',
        'progress_chart',
    )
    
    fieldsets = (
        ('Budget Information', {
            'fields': (
                'user',
                'category',
            ),
        }),
        ('Budget Details', {
            'fields': (
                'limit',
                'amount_spent',
                'remaining_display_detail',
                'percentage_display',
                'progress_chart',
            ),
        }),
        ('Dates', {
            'fields': (
                'start_date',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    def budget_id(self, obj):
        return f"BDG-{obj.id:05d}"
    budget_id.short_description = 'Budget ID'
    
    def user_display(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_display.short_description = 'User'
    
    def category_display(self, obj):
        return obj.get_category_display() if hasattr(obj, 'get_category_display') else obj.category.capitalize()
    category_display.short_description = 'Category'
    
    def limit_display(self, obj):
        return format_html(
            '<span style="font-weight: bold;">KES {:,.2f}</span>',
            obj.limit,
        )
    limit_display.short_description = 'Budget Limit'
    
    def spent_display(self, obj):
        return format_html(
            '<span style="color: orange; font-weight: bold;">KES {:,.2f}</span>',
            obj.amount_spent,
        )
    spent_display.short_description = 'Amount Spent'
    
    def remaining_display(self, obj):
        remaining = obj.remaining
        color = 'green' if remaining > 0 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">KES {:,.2f}</span>',
            color,
            remaining,
        )
    remaining_display.short_description = 'Remaining'
    
    def progress_bar(self, obj):
        percentage = obj.percentage_used
        if percentage <= 50:
            color = '#28a745'  # green
        elif percentage <= 80:
            color = '#ffc107'  # yellow
        else:
            color = '#dc3545'  # red
        
        return format_html(
            '<div style="width: 100%; background-color: #e9ecef; border-radius: 3px; '
            'overflow: hidden;"><div style="width: {}%; background-color: {}; '
            'height: 20px; text-align: center; color: white; font-weight: bold; '
            'font-size: 11px; padding-top: 2px;\">{:.1f}%</div></div>',
            min(percentage, 100),
            color,
            percentage,
        )
    progress_bar.short_description = 'Progress'
    
    def status_badge(self, obj):
        percentage = obj.percentage_used
        if percentage >= 100:
            color = '#dc3545'
            status = '⚠ Over Budget'
        elif percentage >= 80:
            color = '#ffc107'
            status = '⚡ Nearly Full'
        else:
            color = '#28a745'
            status = '✓ OK'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;\">{}</span>',
            color,
            status,
        )
    status_badge.short_description = 'Status'
    
    def remaining_display_detail(self, obj):
        return format_html(
            '<strong>KES {:,.2f}</strong>',
            obj.remaining,
        )
    remaining_display_detail.short_description = 'Remaining Amount'
    
    def percentage_display(self, obj):
        return format_html(
            '<strong>{:.1f}%</strong> of budget used',
            obj.percentage_used,
        )
    percentage_display.short_description = 'Budget Usage'
    
    def progress_chart(self, obj):
        return format_html(
            '<div style="width: 100%; background-color: #e9ecef; border-radius: 3px; '
            'overflow: hidden;"><div style="width: {}%; background-color: #007bff; '
            'height: 25px; text-align: center; color: white; font-weight: bold; '
            'padding-top: 3px;\">{} / KES {:,.2f}</div></div>',
            min((obj.amount_spent / obj.limit * 100) if obj.limit else 0, 100),
            f"KES {obj.amount_spent:,.2f}",
            obj.limit,
        )
    progress_chart.short_description = 'Visual Budget Progress'


admin.site.register(Budget, BudgetAdmin)
