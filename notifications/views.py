from django.shortcuts import render

from notifications.models import Notification

def notifications_view(request):
    notifications = Notification.objects.filter(target__in=[request.user])[:12]
    return render(request, 'notifications/notifications.html', {'notifications': notifications})


