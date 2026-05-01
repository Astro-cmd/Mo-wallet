from django.contrib import admin
from django.utils.html import format_html
from .models import SavingsGoal


class SavingsGoalAdmin(admin.ModelAdmin):
    """Enhanced admin interface for SavingsGoal model."""
    
    list_display = (
        'goal_id',
        'user_display',
        'goal_name_display',
        'target_amount_display',
        'current_savings_display',
        'progress_bar',
        'days_left_display',
        'status_badge',
    )
    list_filter = (
        'completed',
        'deadline',
        'created_at',
    )
    search_fields = (
        'user__username',
        'user__email',
        'goal_name',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'progress_display',
        'remaining_amount_display',
        'days_left_display_detail',
        'achievability_display',
        'contribution_history',
    )
    
    fieldsets = (
        ('Goal Information', {
            'fields': (
                'user',
                'goal_name',
                'completed',
            ),
        }),
        ('Financial Details', {
            'fields': (
                'target_amount',
                'current_savings',
                'remaining_amount_display',
                'progress_display',
            ),
        }),
        ('Timeline', {
            'fields': (
                'deadline',
                'days_left_display_detail',
                'achievability_display',
            ),
        }),
        ('System Information', {
            'fields': (
                'created_at',
                'updated_at',
                'contribution_history',
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ('-created_at',)
    date_hierarchy = 'deadline'
    
    def goal_id(self, obj):
        return f"GOAL-{obj.id:05d}"
    goal_id.short_description = 'Goal ID'
    
    def user_display(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_display.short_description = 'User'
    
    def goal_name_display(self, obj):
        if obj.completed:
            return format_html(
                '<span style="text-decoration: line-through; color: #6c757d;\">{}</span> ✓',
                obj.goal_name,
            )
        return obj.goal_name
    goal_name_display.short_description = 'Goal Name'
    
    def target_amount_display(self, obj):
        return format_html(
            '<span style="font-weight: bold;">KES {:,.2f}</span>',
            obj.target_amount,
        )
    target_amount_display.short_description = 'Target Amount'
    
    def current_savings_display(self, obj):
        return format_html(
            '<span style="color: green; font-weight: bold;">KES {:,.2f}</span>',
            obj.current_savings,
        )
    current_savings_display.short_description = 'Current Savings'
    
    def progress_bar(self, obj):
        percentage = obj.progress
        color = '#28a745' if percentage < 100 else '#ffc107'
        if obj.completed:
            color = '#28a745'
        
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
    
    def days_left_display(self, obj):
        if obj.completed:
            return format_html('<span style="color: green; font-weight: bold;">Completed</span>')
        
        days = obj.days_left
        if days == 0:
            return format_html('<span style="color: red; font-weight: bold;">Today!</span>')
        elif days < 7:
            return format_html(
                '<span style="color: red; font-weight: bold;\">{} days</span>',
                days,
            )
        else:
            return format_html(
                '<span style="color: green; font-weight: bold;\">{} days</span>',
                days,
            )
    days_left_display.short_description = 'Days Left'
    
    def status_badge(self, obj):
        if obj.completed:
            status_text = '✓ Completed'
            color = '#28a745'
        elif obj.is_achievable:
            status_text = '✓ On Track'
            color = '#17a2b8'
        else:
            status_text = '⚠ At Risk'
            color = '#dc3545'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;\">{}</span>',
            color,
            status_text,
        )
    status_badge.short_description = 'Status'
    
    def progress_display(self, obj):
        return format_html(
            '<strong>{:.1f}%</strong> of goal saved',
            obj.progress,
        )
    progress_display.short_description = 'Progress Percentage'
    
    def remaining_amount_display(self, obj):
        return format_html(
            '<strong>KES {:,.2f}</strong> remaining',
            obj.remaining_amount,
        )
    remaining_amount_display.short_description = 'Remaining Amount'
    
    def days_left_display_detail(self, obj):
        if obj.completed:
            return format_html('<span style="color: green; font-weight: bold;">Goal Completed</span>')
        return format_html(
            '<strong>{} days</strong> until deadline',
            obj.days_left,
        )
    days_left_display_detail.short_description = 'Days Until Deadline'
    
    def achievability_display(self, obj):
        if obj.completed:
            return format_html('<span style="color: green;">✓ Goal Achieved</span>')
        
        if obj.is_achievable:
            return format_html(
                '<span style="color: green;">✓ Goal is achievable with current savings pace</span>'
            )
        else:
            return format_html(
                '<span style="color: red;">⚠ Goal may not be achievable by deadline</span>'
            )
    achievability_display.short_description = 'Achievability'
    
    def contribution_history(self, obj):
        return format_html(
            '<em>View GoalContribution records for {}</em>',
            obj.goal_name,
        )
    contribution_history.short_description = 'Contribution History'


admin.site.register(SavingsGoal, SavingsGoalAdmin)
