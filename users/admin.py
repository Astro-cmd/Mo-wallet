from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


class UserAdmin(BaseUserAdmin):
    """Enhanced admin interface for User model with profile information."""
    
    list_display = (
        'user_id',
        'username_display',
        'email_display',
        'phone_display',
        'status_badge',
        'account_type_badge',
        'joined_display',
    )
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
        'last_login',
    )
    search_fields = (
        'email',
        'username',
        'first_name',
        'last_name',
        'phone_number',
    )
    readonly_fields = (
        'date_joined',
        'last_login',
        'profile_preview',
        'account_info_display',
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'phone_number',
            ),
        }),
        ('Profile', {
            'fields': (
                'profile_picture',
                'profile_preview',
                'country',
            ),
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        ('Account Information', {
            'fields': (
                'date_joined',
                'last_login',
                'account_info_display',
            ),
            'classes': ('collapse',),
        }),
        ('Password', {
            'fields': (
                'password',
            ),
            'classes': ('collapse',),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    ordering = ('-date_joined',)
    date_hierarchy = 'date_joined'
    
    def user_id(self, obj):
        return f"USR-{obj.id:05d}"
    user_id.short_description = 'User ID'
    
    def username_display(self, obj):
        if obj.get_full_name():
            return format_html(
                '<strong>{}</strong><br/><small style="color: #6c757d;\">{}</small>',
                obj.get_full_name(),
                obj.username,
            )
        return obj.username
    username_display.short_description = 'Name'
    
    def email_display(self, obj):
        return format_html(
            '<a href="mailto:{}\">{}</a>',
            obj.email,
            obj.email,
        )
    email_display.short_description = 'Email'
    
    def phone_display(self, obj):
        if obj.phone_number:
            return format_html(
                '<a href="tel:{}\">{}</a>',
                obj.phone_number,
                obj.phone_number,
            )
        return '-'
    phone_display.short_description = 'Phone'
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-size: 11px; font-weight: bold;\">✓ Active</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-size: 11px; font-weight: bold;\">✗ Inactive</span>'
            )
    status_badge.short_description = 'Status'
    
    def account_type_badge(self, obj):
        if obj.is_superuser:
            return format_html(
                '<span style="background-color: #721c24; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-size: 11px; font-weight: bold;\">👑 Superuser</span>'
            )
        elif obj.is_staff:
            return format_html(
                '<span style="background-color: #856404; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-size: 11px; font-weight: bold;\">👤 Staff</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #17a2b8; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-size: 11px; font-weight: bold;\">👥 User</span>'
            )
    account_type_badge.short_description = 'Type'
    
    def joined_display(self, obj):
        return obj.date_joined.strftime('%Y-%m-%d')
    joined_display.short_description = 'Joined'
    
    def profile_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="200" height="200" style="border-radius: 5px;" />',
                obj.profile_picture.url,
            )
        return '<em>No profile picture</em>'
    profile_preview.short_description = 'Profile Picture Preview'
    
    def account_info_display(self, obj):
        return format_html(
            '<strong>Last Login:</strong> {}<br/><strong>Account Created:</strong> {}',
            obj.last_login or 'Never',
            obj.date_joined.strftime('%Y-%m-%d %H:%M'),
        )
    account_info_display.short_description = 'Account Timeline'


admin.site.register(User, UserAdmin)

