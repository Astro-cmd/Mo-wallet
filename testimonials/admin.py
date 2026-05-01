from django.contrib import admin
from django.utils.html import format_html
from .models import Feature, Testimonial


class FeatureAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Feature model."""
    
    list_display = (
        'feature_id',
        'title_display',
        'description_preview',
        'icon_display',
        'status_badge',
    )
    list_filter = (
        'active',
    )
    search_fields = (
        'title',
        'description',
    )
    readonly_fields = (
        'icon_preview',
    )
    
    fieldsets = (
        ('Feature Information', {
            'fields': (
                'title',
                'description',
            ),
        }),
        ('Icon', {
            'fields': (
                'icon',
                'icon_preview',
            ),
        }),
        ('Status', {
            'fields': (
                'active',
            ),
        }),
    )
    
    def feature_id(self, obj):
        return f"FT-{obj.id:05d}"
    feature_id.short_description = 'Feature ID'
    
    def title_display(self, obj):
        return obj.title
    title_display.short_description = 'Title'
    
    def description_preview(self, obj):
        return obj.description[:100] + ('...' if len(obj.description) > 100 else '')
    description_preview.short_description = 'Description'
    
    def icon_display(self, obj):
        return format_html(
            '<i class=\"{}\"></i>',
            obj.icon,
        )
    icon_display.short_description = 'Icon'
    
    def status_badge(self, obj):
        if obj.active:
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
    
    def icon_preview(self, obj):
        return format_html(
            '<i class=\"{}\" style=\"font-size: 48px; color: #007bff;\"></i>',
            obj.icon,
        )
    icon_preview.short_description = 'Icon Preview'


class TestimonialAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Testimonial model."""
    
    list_display = (
        'testimonial_id',
        'user_display',
        'content_preview',
        'approval_badge',
        'created_at_display',
    )
    list_filter = (
        'is_approved',
        'created_at',
    )
    search_fields = (
        'user__username',
        'user__email',
        'content',
    )
    readonly_fields = (
        'created_at',
        'user_info',
    )
    
    fieldsets = (
        ('Testimonial Information', {
            'fields': (
                'user',
                'user_info',
                'content',
            ),
        }),
        ('Status', {
            'fields': (
                'is_approved',
            ),
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
    
    def testimonial_id(self, obj):
        return f"TST-{obj.id:05d}"
    testimonial_id.short_description = 'Testimonial ID'
    
    def user_display(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_display.short_description = 'User'
    
    def content_preview(self, obj):
        return obj.content[:80] + ('...' if len(obj.content) > 80 else '')
    content_preview.short_description = 'Content'
    
    def approval_badge(self, obj):
        if obj.is_approved:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-size: 11px; font-weight: bold;\">✓ Approved</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #ffc107; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-size: 11px; font-weight: bold;\">⏳ Pending</span>'
            )
    approval_badge.short_description = 'Status'
    
    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_display.short_description = 'Created'
    
    def user_info(self, obj):
        return format_html(
            '<strong>Email:</strong> {}<br/><strong>Username:</strong> {}',
            obj.user.email,
            obj.user.username,
        )
    user_info.short_description = 'User Information'
    
    actions = ['approve_testimonials', 'unapprove_testimonials']
    
    def approve_testimonials(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, f'{count} testimonial(s) approved.')
    approve_testimonials.short_description = 'Approve selected testimonials'
    
    def unapprove_testimonials(self, request, queryset):
        count = queryset.update(is_approved=False)
        self.message_user(request, f'{count} testimonial(s) unapproved.')
    unapprove_testimonials.short_description = 'Unapprove selected testimonials'


admin.site.register(Feature, FeatureAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
