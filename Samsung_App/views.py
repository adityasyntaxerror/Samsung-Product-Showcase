from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Category, Product


def _is_valid_email(value):
    try:
        validate_email(value)
    except ValidationError:
        return False
    return True


def home(request):
    products = Product.objects.select_related("category")
    featured = products.filter(is_featured=True)[:3] or products[:3]
    return render(request, "Samsung_App/home.html", {
        "featured": featured,
        "foldable": products.filter(slug="galaxy-z-fold7").first(),
        "watch": products.filter(slug="galaxy-watch8").first(),
    })


def products(request):
    current_category = request.GET.get("category", "").strip()
    query = request.GET.get("q", "").strip()

    items = Product.objects.select_related("category")
    if current_category:
        items = items.filter(category__slug=current_category)
    if query:
        items = items.filter(Q(title__icontains=query) | Q(tagline__icontains=query))

    return render(request, "Samsung_App/products.html", {
        "items": items,
        "categories": Category.objects.all(),
        "current_category": current_category,
        "query": query,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug)
    related = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:3]
    return render(request, "Samsung_App/product_detail.html", {"product": product, "related": related})


def about(request):
    return render(request, "Samsung_App/about.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form_data = {}
    if request.method == "POST":
        identifier = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        form_data = {"username": identifier}
        if not identifier or not password:
            messages.error(request, "Please enter both your username (or email) and password.")
        else:
            if "@" in identifier:  # allow signing in with the email address too
                match = User.objects.filter(email__iexact=identifier).first()
                if match:
                    identifier = match.get_username()
            user = authenticate(request, username=identifier, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect("home")
            messages.error(request, "Invalid username/email or password.")
    return render(request, "Samsung_App/login.html", {"form_data": form_data})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form_data = {}
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm_password", "")
        form_data = {"name": name, "username": username, "email": email}

        if not all([name, username, email, password, confirm]):
            messages.error(request, "Please complete every field.")
        elif not _is_valid_email(email):
            messages.error(request, "Please enter a valid email address.")
        elif password != confirm:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username__iexact=username).exists():
            messages.error(request, "That username is already taken.")
        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, "That email is already registered.")
        else:
            candidate = User(username=username, email=email, first_name=name)
            try:
                validate_password(password, user=candidate)
            except ValidationError as error:
                for message in error.messages:
                    messages.error(request, message)
            else:
                try:
                    user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
                except IntegrityError:
                    messages.error(request, "That username is already taken.")
                else:
                    login(request, user)
                    messages.success(request, "Your account was created successfully.")
                    return redirect("home")
    return render(request, "Samsung_App/signup.html", {"form_data": form_data})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been signed out.")
    return redirect("home")
