from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "User already exists"}, status=400)

    User.objects.create_user(username=username, password=password)
    return JsonResponse({"message": "Registration successful"}, status=201)


@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    return JsonResponse({
        "message": "Login successful",
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "username": user.username
    }, status=200)

