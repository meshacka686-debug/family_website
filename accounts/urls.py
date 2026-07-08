from django.urls import path
from . import views
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
  path("gallery/", views.gallery_view, name="gallery_view"),
    path("gallery/<int:photo_id>/edit/", views.edit_photo, name="edit_photo"),
    path("gallery/<int:photo_id>/delete/", views.delete_photo, name="delete_photo"),
    path("gallery/user/<int:user_id>/", views.user_gallery, name="user_gallery"),
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('upload-photo/', views.upload_photo, name='upload_photo'),
]

