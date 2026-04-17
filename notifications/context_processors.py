from .models import Notification


def notifications_context(request):
    """Expose notification data globally for navbar components."""
    if not request.user.is_authenticated:
        return {
            'unread_notifications': 0,
            'recent_notifications': [],
        }

    recent_notifications = Notification.objects.filter(user=request.user).only(
        'id', 'type', 'title', 'created_at', 'is_read', 'action_url'
    )[:5]
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()

    return {
        'unread_notifications': unread_notifications,
        'recent_notifications': recent_notifications,
    }
