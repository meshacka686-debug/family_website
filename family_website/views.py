from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render

def home(request):
    return render(request, "home.html")

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html')
