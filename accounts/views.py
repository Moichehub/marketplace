from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SellerProfileForm, SellerRegisterForm, UserRegisterForm
from .models import SellerProfile, User


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
            return redirect("accounts:seller_profile_setup")
    else:
        form = SellerRegisterForm()
    return render(request, "accounts/seller_register.html", {"form": form})


from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm


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


@login_required
def seller_profile_setup(request):
    """Setup seller profile after registration"""
    if not request.user.is_seller:
        messages.error(request, "Ця сторінка доступна тільки для продавців")
        return redirect("products:list")

    try:
        profile = request.user.seller_profile
        messages.info(request, "Профіль магазину вже налаштований")
        return redirect("accounts:seller_profile_edit")
    except SellerProfile.DoesNotExist:
        pass

    if request.method == "POST":
        form = SellerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Профіль магазину успішно створено!")
            return redirect("products:seller_dashboard")
    else:
        form = SellerProfileForm()

    context = {
        "form": form,
        "is_setup": True,
    }
    return render(request, "accounts/seller_profile_form.html", context)


@login_required
def seller_profile_edit(request):
    """Edit seller profile"""
    if not request.user.is_seller:
        messages.error(request, "Ця сторінка доступна тільки для продавців")
        return redirect("products:list")

    try:
        profile = request.user.seller_profile
    except SellerProfile.DoesNotExist:
        messages.error(
            request, "Профіль магазину не знайдено. Будь ласка, створіть його."
        )
        return redirect("accounts:seller_profile_setup")

    if request.method == "POST":
        form = SellerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль магазину успішно оновлено!")
            return redirect("accounts:seller_profile_view")
    else:
        form = SellerProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
        "is_edit": True,
    }
    return render(request, "accounts/seller_profile_form.html", context)


@login_required
def seller_profile_view(request):
    """View seller profile"""
    if not request.user.is_seller:
        messages.error(request, "Ця сторінка доступна тільки для продавців")
        return redirect("products:list")

    try:
        profile = request.user.seller_profile
    except SellerProfile.DoesNotExist:
        messages.error(
            request, "Профіль магазину не знайдено. Будь ласка, створіть його."
        )
        return redirect("accounts:seller_profile_setup")

    total_products = profile.total_products
    total_reviews = profile.total_reviews
    avg_rating = profile.average_rating
    total_sales = profile.total_sales

    context = {
        "profile": profile,
        "total_products": total_products,
        "total_reviews": total_reviews,
        "avg_rating": round(avg_rating, 1) if avg_rating > 0 else 0,
        "total_sales": total_sales,
    }
    return render(request, "accounts/seller_profile_view.html", context)


def seller_store_view(request, store_slug):
    """Public view of a seller's store"""
    profile = get_object_or_404(SellerProfile, store_slug=store_slug, is_active=True)

    products = profile.user.products.filter(is_active=True).order_by("-created_at")

    total_products = products.count()
    total_reviews = profile.total_reviews
    avg_rating = profile.average_rating

    context = {
        "profile": profile,
        "products": products,
        "total_products": total_products,
        "total_reviews": total_reviews,
        "avg_rating": round(avg_rating, 1) if avg_rating > 0 else 0,
    }
    return render(request, "accounts/seller_store_view.html", context)
