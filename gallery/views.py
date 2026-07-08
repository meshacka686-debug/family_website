from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PhotoForm
from .models import Photo

from notifications.models import Notification

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from notifications.models import Notification


@login_required
def gallery_view(request):
    """Show only the logged-in user's gallery, with inline upload form"""
    photos = Photo.objects.filter(user=request.user)
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            # Optional: notify user of upload
            Notification.objects.create(
                message=f"{request.user.username} uploaded a new photo!"
            )
            return redirect("accounts:gallery_view")
    else:
        form = PhotoForm()
    return render(request, "accounts/gallery.html", {"photos": photos, "form": form})


@login_required
def edit_photo(request, photo_id):
    """Allow editing only if the photo belongs to the logged-in user"""
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect("accounts:gallery_view")
    else:
        form = PhotoForm(instance=photo)
    return render(request, "accounts/edit_photo.html", {"form": form, "photo": photo})


@login_required
def delete_photo(request, photo_id):
    """Allow deletion only if the photo belongs to the logged-in user"""
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)
    photo.delete()
    return redirect("accounts:gallery_view")


@login_required
def user_gallery(request, user_id):
    """View another user's gallery (read-only)"""
    other_user = get_object_or_404(User, id=user_id)
    photos = Photo.objects.filter(user=other_user)
    return render(request, "accounts/user_gallery.html", {
        "other_user": other_user,
        "photos": photos
    })



@login_required
def upload_photo(request):
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

            return redirect("accounts:my_gallery")
    else:
        form = PhotoForm()
    return render(request, "gallery/upload_photo.html", {"form": form})




@login_required
def gallery_view(request):
    photos = Photo.objects.all().order_by('-uploaded_at')
    return render(request, "accounts/gallery.html", {"photos": photos})

