# home/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import json

@csrf_exempt
def api_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"error": "Email and password are required"}, status=400)

            user = authenticate(request, username=email, password=password)
            if user is not None:
                return JsonResponse({"token": "dummy-token-for-now"})
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "POST request required"}, status=405)


# Homepage view
def index(request):
    return render(request, 'home/index.html')


# Registration page view
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not email or not password:
            return render(request, "home/register.html", {"error": "All fields are required"})

        if User.objects.filter(username=username).exists():
            return render(request, "home/register.html", {"error": "Username already exists"})

        if User.objects.filter(email=email).exists():
            return render(request, "home/register.html", {"error": "Email already exists"})

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect("home")

    return render(request, "home/register.html")

def login_view(request):
    return render(request, 'home/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')  

def profile_view(request):
    return render(request, 'home/profile.html')