# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def home(request):
    return render(request, 'home.html')  # Replace 'home.html' with your template name

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')  # Replace 'dashboard.html' with your template name

def logout_view(request):
    logout(request)
    return redirect('/')
