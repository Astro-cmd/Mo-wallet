from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Notification

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()
    total_count = notifications.count()
    type_counts = {
        'budget': notifications.filter(type='budget').count(),
        'goal': notifications.filter(type='goal').count(),
        'transaction': notifications.filter(type='transaction').count(),
        'security': notifications.filter(type='security').count(),
        'system': notifications.filter(type='system').count(),
    }
    return render(request, 'notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
        'total_count': total_count,
        'type_counts': type_counts,
    })

@login_required
def mark_all_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=405)


@login_required
def mark_read(request, notification_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save(update_fields=['is_read'])
    return JsonResponse({'status': 'success'})
