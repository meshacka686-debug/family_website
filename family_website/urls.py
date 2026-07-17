from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from . import views
def dashboard_view(request):
    return render(request, "dashboard.html")  # 👈 create this template

urlpatterns = [
    path('', dashboard_view, name='dashboard'),   # ✅ root URL
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('gallery/', include('gallery.urls')),
  path("notifications/", include("notifications.urls")),
    path('chat/', include('chat.urls')),
     path("test-firebase/", views.test_firebase, name="test_firebase"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
