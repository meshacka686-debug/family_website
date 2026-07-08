from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@login_required
def notification_list(request):
    notifications = request.user.notifications.all().order_by('-timestamp')
    return render(request, "notifications/list.html", {"notifications": notifications})
