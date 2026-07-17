from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from notifications.models import Notification

from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, PhotoForm, UserForm
from gallery.models import Photo


# ------------------ GALLERY ------------------


@login_required
def gallery_view(request):
    """Show only the logged-in user's own gallery"""
    photos = request.user.gallery_photos.all()  # 👈 use related_name
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            # 👇 Create a notification for all users
            note = Notification.objects.create(
                message=f"{request.user.username} uploaded a new photo!"
            )
            for u in User.objects.all():
                note.users.add(u)
            return redirect("accounts:gallery_view")
    else:
        form = PhotoForm()
    return render(request, "gallery/gallery.html", {"photos": photos, "form": form})

@login_required
def upload_photo(request):
    """Allow logged-in user to upload a new photo"""
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            # 👇 Create a notification for all users
            messages.success(request, "Photo uploaded successfully.")
            return redirect("accounts:gallery_view")
    else:
        form = PhotoForm()
    return render(request, "accounts/upload_photo.html", {"form": form})


@login_required
def edit_photo(request, photo_id):
    """Allow editing only if the photo belongs to the logged-in user"""
    photo = get_object_or_404(Photo, id=photo_id)
    if photo.user != request.user:
        raise PermissionDenied("You cannot edit another user's photo.")

    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            # 👇 Create a notification for all users
            note = Notification.objects.create(
                message=f"{request.user.username} edited a photo!"
            )
            for u in User.objects.all():
                note.users.add(u)

            messages.success(request, "Photo updated successfully.")
            return redirect("accounts:gallery_view")
    else:
        form = PhotoForm(instance=photo)
    return render(request, "accounts/edit_photo.html", {"form": form, "photo": photo})


@login_required
def delete_photo(request, photo_id):
    """Allow deletion only if the photo belongs to the logged-in user"""
    photo = get_object_or_404(Photo, id=photo_id)
    if photo.user != request.user:
        raise PermissionDenied("You cannot delete another user's photo.")

    photo.delete()
    messages.success(request, "Photo deleted successfully.")
    return redirect("accounts:gallery_view")


@login_required
def user_gallery(request, user_id):
    """View another user's gallery (read-only)"""
    other_user = get_object_or_404(User, id=user_id)
    photos = other_user.gallery_photos.all()  # 👈 use related_name
    return render(request, "accounts/user_gallery.html", {
        "other_user": other_user,
        "photos": photos
    })


# ------------------ PROFILE ------------------

@login_required
def profile_view(request):
    """Display logged-in user's profile"""
    return render(request, "accounts/profile.html")


@login_required
def edit_profile(request):
    """Allow logged-in user to edit their profile"""
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
         # 👇 Create a notification for all users
            note = Notification.objects.create(
                message=f"{request.user.username} edited their profile!"
            )
            for u in User.objects.all():
                note.users.add(u)

            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, "accounts/edit_profile.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })


# ------------------ AUTH ------------------

def register_view(request):
    """Register a new user"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
                  # 👇 Create a notification for all users
            note = Notification.objects.create(
                message=f"{request.user.username} registered a new account!"
            )
            for u in User.objects.all():
                note.users.add(u)

            login(request, user)  # log the user in immediately
            return redirect("dashboard")  # send them to dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"


class CustomLogoutView(LogoutView):
    """Ensure logout works and redirects to login page"""
    next_page = "accounts:login"
