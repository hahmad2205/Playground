from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_user(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            response = redirect('logout')
        else:
            response = render(request, "users/login.html", {"message": "Invalid username or password"})
    else:
        response = render(request, "users/login.html", {})
        
    return response

def logout_user(request):
    if request.method == "POST":
        logout(request)
        response = redirect('login')
    else:
        response = render(request, "users/logout.html", {})
    
    return response