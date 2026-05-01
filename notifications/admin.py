from django.contrib import admin
from django.utils.html import format_html
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Notification model."""
    
    list_display = (
        'notification_id',
        'user_display',
        'type_badge',
        'title_display',
        'read_status',
        'created_at_display',
    )
    list_filter = (
        'type',
        'is_read',
        'created_at',
    )
    search_fields = (
        'user__username',
        'user__email',
        'title',
        'message',
    )
    readonly_fields = (
        'created_at',
        'message_preview',
        'user_link',
    )
    
    fieldsets = (
        ('Notification Details', {
            'fields': (
                'user_link',
                'type',
                'title',
                'is_read',
            ),
        }),
        ('Message', {
            'fields': (
                'message',
                'message_preview',
            ),
        }),
        ('Action', {
            'fields': (
                'action_url',
            ),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': (
                'created_at',
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    def notification_id(self, obj):
        return f"NOT-{obj.id:05d}"
    notification_id.short_description = 'Notification ID'
    
    def user_display(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_display.short_description = 'User'
    
    def type_badge(self, obj):
        colors = {
            'budget': '#ffc107',
            'goal': '#17a2b8',
            'transaction': '#007bff',
            'security': '#dc3545',
            'system': '#6c757d',
        }
        color = colors.get(obj.type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;\">{}</span>',
            color,
            obj.get_type_display(),
        )
    type_badge.short_description = 'Type'
    
    def title_display(self, obj):
        return obj.title[:50] + ('...' if len(obj.title) > 50 else '')
    title_display.short_description = 'Title'
    
    def read_status(self, obj):
        if obj.is_read:
            return format_html(
                '<span style="color: #6c757d;">✓ Read</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #007bff; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-size: 11px; font-weight: bold;\">📬 Unread</span>'
            )
    read_status.short_description = 'Status'
    
    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_display.short_description = 'Sent'
    
    def message_preview(self, obj):
        return obj.message[:200] + ('...' if len(obj.message) > 200 else '')
    message_preview.short_description = 'Message Preview'
    
    def user_link(self, obj):
        return format_html(
            '<a href="/admin/users/user/{}/change/\">{}</a>',
            obj.user.id,
            obj.user.get_full_name() or obj.user.username,
        )
    user_link.short_description = 'User'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        count = queryset.update(is_read=True)
        self.message_user(request, f'{count} notification(s) marked as read.')
    mark_as_read.short_description = 'Mark selected as read'
    
    def mark_as_unread(self, request, queryset):
        count = queryset.update(is_read=False)
        self.message_user(request, f'{count} notification(s) marked as unread.')
    mark_as_unread.short_description = 'Mark selected as unread'


admin.site.register(Notification, NotificationAdmin)
