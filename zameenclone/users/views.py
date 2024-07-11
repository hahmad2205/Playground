from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_user(request):
    if request.user.is_authenticated:
        response = redirect('properties/marketplace')
    elif request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            response = redirect('properties/marketplace')
        else:
            response = render(request, "users/login.html", {"message": "Invalid username or password"})
    elif request.method == "GET":
        response = render(request, "users/login.html", {})
        
    return response

def logout_user(request):
    if request.method == "POST":
        logout(request)
        response = redirect('login')
    elif request.method == "GET":
        response = redirect('properties/marketplace')
    
    return response
