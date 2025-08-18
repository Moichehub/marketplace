from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm, SellerRegisterForm
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Реєстрація успішна!")
            return redirect("products:list")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def seller_register(request):
    if request.method == "POST":
        form = SellerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Реєстрація продавця успішна!")
            return redirect("products:list")
    else:
        form = SellerRegisterForm()
    return render(request, "accounts/seller_register.html", {"form": form})

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("products:list")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("products:list")





































