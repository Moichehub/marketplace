from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .models import Product, Category
from .forms import ProductForm
from .filters import ProductFilter
from .permissions import require_seller


def product_list(request):
    qs = Product.objects.select_related("category", "seller").filter(is_active=True).order_by("-created_at")
    paginator = Paginator(qs, 12)
    q = request.GET.get("q")
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    filt = ProductFilter(request.GET, queryset=qs)
    qs = filt.qs

    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    ctx = {
        "filter": filt,
        "page_obj": page_obj,
        "categories": Category.objects.all(),
    }


    if request.headers.get("HX-Request"):
        return render(request, "products/product_grid.html", ctx)

    return render(request, "products/product_list.html", ctx)


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category", "seller"), slug=slug, is_active=True)
    return render(request, "products/product_detail.html", {"product": product})


@login_required
@require_http_methods(["GET", "POST"])
def product_create(request):
    require_seller(request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.seller = request.user
            prod.save()
            return redirect("products:detail", slug=prod.slug)
    else:
        form = ProductForm()
    return render(request, "products/product_form.html", {"form": form, "mode": "create"})


@login_required
@require_http_methods(["GET", "POST"])
def product_update(request, slug):
    require_seller(request.user)
    product = get_object_or_404(Product, slug=slug, seller=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            prod = form.save()
            return redirect("products:detail", slug=prod.slug)
    else:
        form = ProductForm(instance=product)
    return render(request, "products/product_form.html", {"form": form, "mode": "update", "product": product})


@login_required
def product_delete(request, slug):
    """Delete a product (only for the product's seller)"""
    require_seller(request.user)
    product = get_object_or_404(Product, slug=slug, seller=request.user)
    
    if request.method == "POST":
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" has been deleted successfully.')
        return redirect("products:seller_dashboard")
    
    return render(request, "products/product_confirm_delete.html", {"product": product})


@login_required
def seller_dashboard(request):
    """Dashboard for sellers to manage their products"""
    require_seller(request.user)
    
    # Get all products by the seller
    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    
    # Apply filters if provided
    q = request.GET.get("q")
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    
    category_filter = request.GET.get("category")
    if category_filter:
        products = products.filter(category__slug=category_filter)
    
    status_filter = request.GET.get("status")
    if status_filter == "active":
        products = products.filter(is_active=True)
    elif status_filter == "inactive":
        products = products.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    
    context = {
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "total_products": products.count(),
        "active_products": products.filter(is_active=True).count(),
        "inactive_products": products.filter(is_active=False).count(),
    }
    
    return render(request, "products/seller_dashboard.html", context)


def create_sample_data(request):
    """Create sample products and sellers for the marketplace"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Create categories
    categories = {}
    for cat_name in ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports']:
        cat, created = Category.objects.get_or_create(name=cat_name)
        categories[cat_name] = cat
    
    # Create sellers
    sellers = {}
    for username, email in [
        ('techstore', 'tech@example.com'), 
        ('fashion', 'fashion@example.com'), 
        ('books', 'books@example.com'),
        ('home', 'home@example.com'),
        ('sports', 'sports@example.com')
    ]:
        seller, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_seller': True}
        )
        if created:
            seller.set_password('pass123')
            seller.save()
        sellers[username] = seller
    
    # Add products
    products_data = [
        # TechStore products
        ('techstore', 'iPhone 15 Pro', 'Latest iPhone with advanced features', 999.99, 'Electronics'),
        ('techstore', 'MacBook Air M2', 'Lightweight laptop with M2 chip', 1199.99, 'Electronics'),
        ('techstore', 'Sony Headphones', 'Premium noise-cancelling headphones', 349.99, 'Electronics'),
        ('techstore', 'Samsung Galaxy S24', 'Android flagship with AI features', 899.99, 'Electronics'),
        ('techstore', 'iPad Pro', 'Professional tablet with M2 chip', 1099.99, 'Electronics'),
        
        # Fashion products
        ('fashion', 'Denim Jacket', 'Classic denim jacket for any occasion', 89.99, 'Clothing'),
        ('fashion', 'Premium T-Shirt', 'Soft, breathable cotton t-shirt', 24.99, 'Clothing'),
        ('fashion', 'Leather Bag', 'Stylish leather crossbody bag', 129.99, 'Clothing'),
        ('fashion', 'Running Shoes', 'Comfortable running shoes', 79.99, 'Clothing'),
        ('fashion', 'Sunglasses', 'Trendy sunglasses with UV protection', 159.99, 'Clothing'),
        
        # BookWorld products
        ('books', 'The Great Gatsby', 'F. Scott Fitzgerald classic novel', 12.99, 'Books'),
        ('books', 'Python Programming Guide', 'Complete guide to Python programming', 29.99, 'Books'),
        ('books', 'The Art of War', 'Sun Tzu military treatise', 9.99, 'Books'),
        ('books', 'Harry Potter Book 1', 'J.K. Rowling magical first book', 15.99, 'Books'),
        ('books', 'The Hobbit', 'J.R.R. Tolkien fantasy adventure', 13.99, 'Books'),
        
        # Home Improvement products
        ('home', 'LED Desk Lamp', 'Adjustable LED lamp with multiple levels', 49.99, 'Home & Garden'),
        ('home', 'Garden Tool Set', 'Complete set of gardening tools', 89.99, 'Home & Garden'),
        ('home', 'Kitchen Mixer', 'Professional stand mixer for baking', 199.99, 'Home & Garden'),
        ('home', 'Smart Thermostat', 'WiFi-enabled thermostat', 149.99, 'Home & Garden'),
        ('home', 'Cordless Drill', 'Powerful cordless drill', 129.99, 'Home & Garden'),
        
        # Sports World products
        ('sports', 'Basketball', 'Official size basketball', 29.99, 'Sports'),
        ('sports', 'Yoga Mat', 'Non-slip yoga mat for workouts', 34.99, 'Sports'),
        ('sports', 'Tennis Racket', 'Professional tennis racket', 89.99, 'Sports'),
        ('sports', 'Running Shorts', 'Comfortable running shorts', 24.99, 'Sports'),
        ('sports', 'Dumbbell Set', 'Adjustable dumbbell set', 199.99, 'Sports'),
    ]
    
    created_count = 0
    for seller_username, name, desc, price, cat_name in products_data:
        product, created = Product.objects.get_or_create(
            name=name,
            seller=sellers[seller_username],
            defaults={
                'description': desc,
                'price': price,
                'category': categories[cat_name],
                'stock': 10,
                'is_active': True
            }
        )
        if created:
            created_count += 1
    
    messages.success(request, f'Successfully created {created_count} new products!')
    messages.info(request, 'Seller accounts created: techstore, fashion, books, home, sports (password: pass123)')
    return redirect('products:list')
