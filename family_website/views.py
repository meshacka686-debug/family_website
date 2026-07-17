from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from firebase_admin import storage

def test_firebase(request):
    bucket = storage.bucket()
    blob = bucket.blob("test_upload.txt")
    blob.upload_from_string("Hello Meshack, Firebase is working!")
    blob.make_public()
    return HttpResponse(f"File uploaded! Public URL: {blob.public_url}")


def home(request):
    return render(request, "home.html")

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html')
