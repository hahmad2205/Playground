from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_user(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('logout')
        else:
            return render(request, "users/login.html", {"message": "Invalid username or password"})
    else:
        return render(request, "users/login.html", {})

def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    else:
        return render(request, "users/logout.html", {})
