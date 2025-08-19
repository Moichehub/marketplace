from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import JsonResponse

from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm
from .filters import ProductFilter
from .permissions import require_seller
from orders.models import PaymentMethod


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
    try:
        product = get_object_or_404(Product.objects.select_related("category", "seller"), slug=slug, is_active=True)
    except Exception as e:
        print(f"Error getting product: {e}")
        messages.error(request, "Помилка при завантаженні товару")
        return redirect('products:list')
    
    # Get reviews for the product (only those with valid users)
    try:
        # Use a simple approach with select_related but handle errors gracefully
        reviews = product.reviews.filter(user__isnull=False).select_related('user').order_by('-created_at')
    except Exception as e:
        print(f"Error getting reviews: {e}")
        # Fallback to simple query without select_related
        reviews = product.reviews.filter(user__isnull=False).order_by('-created_at')
    
    # Check if user has already reviewed this product
    user_review = None
    if request.user.is_authenticated and not request.user.is_seller:
        try:
            user_review = product.reviews.filter(user=request.user).first()
        except Exception as e:
            # Log the error and continue without user_review
            print(f"Error getting user review: {e}")
            user_review = None
    
    # Initialize form as None
    form = None
    
    # Handle review submission
    if request.method == "POST" and request.user.is_authenticated and not request.user.is_seller:
        form = ReviewForm(request.POST, user=request.user, product=product)
        
        if form.is_valid():
            try:
                review = form.save(commit=False)
                review.user = request.user
                review.product = product
                review.save()
                messages.success(request, "Ваш відгук успішно додано!")
                return redirect("products:detail", slug=product.slug)
            except Exception as e:
                print(f"Error saving review: {e}")
                messages.error(request, "Помилка при збереженні відгуку. Спробуйте ще раз.")
    elif request.user.is_authenticated and not request.user.is_seller:
        # Only create form for authenticated non-seller users
        form = ReviewForm(user=request.user, product=product)
    
    # Get available payment methods for the add to cart form
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    
    context = {
        "product": product,
        "reviews": reviews,
        "user_review": user_review,
        "review_form": form,
        "payment_methods": payment_methods,
    }
    
    # Debug: Print context information (only for development)
    # print(f"Debug - User authenticated: {request.user.is_authenticated}")
    # print(f"Debug - User is seller: {getattr(request.user, 'is_seller', False)}")
    # print(f"Debug - User review exists: {user_review is not None}")
    # print(f"Debug - Form exists: {form is not None}")
    # if form:
    #     print(f"Debug - Form fields: {list(form.fields.keys())}")
    #     if form.errors:
    #         print(f"Debug - Form errors: {form.errors}")
    
    # Debug: Check if any reviews have issues
    try:
        for review in reviews:
            if review.user is None:
                print(f"Warning: Review {review.id} has no user")
    except Exception as e:
        print(f"Error checking reviews: {e}")
    
    try:
        return render(request, "products/product_detail.html", context)
    except Exception as e:
        print(f"Error rendering template: {e}")
        messages.error(request, "Помилка при відображенні сторінки")
        return redirect('products:list')


@login_required
def add_review(request, slug):
    """Add a review to a product"""
    if request.user.is_seller:
        messages.error(request, "Продавці не можуть залишати відгуки")
        return redirect('products:detail', slug=slug)
    
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Check if user already reviewed this product
    if product.reviews.filter(user=request.user).exists():
        messages.error(request, "Ви вже залишили відгук для цього товару")
        return redirect('products:detail', slug=slug)
    
    if request.method == "POST":
        form = ReviewForm(request.POST, user=request.user, product=product)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Ваш відгук успішно додано!")
            return redirect('products:detail', slug=slug)
    else:
        form = ReviewForm(user=request.user, product=product)
    
    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'products/add_review.html', context)


@login_required
def edit_review(request, review_id):
    """Edit an existing review"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review, user=request.user, product=review.product)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш відгук успішно оновлено!")
            return redirect('products:detail', slug=review.product.slug)
    else:
        form = ReviewForm(instance=review, user=request.user, product=review.product)
    
    context = {
        'form': form,
        'review': review,
        'product': review.product,
    }
    return render(request, 'products/edit_review.html', context)


@login_required
def delete_review(request, review_id):
    """Delete a review"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    
    if request.method == "POST":
        review.delete()
        messages.success(request, "Ваш відгук успішно видалено!")
        return redirect('products:detail', slug=product_slug)
    
    context = {
        'review': review,
        'product': review.product,
    }
    return render(request, 'products/delete_review.html', context)


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
            
            # Check if slug was generated properly
            if prod.slug:
                messages.success(request, f"Товар '{prod.name}' успішно створено!")
                return redirect("products:detail", slug=prod.slug)
            else:
                # If slug is empty, redirect to seller dashboard
                messages.success(request, f"Товар '{prod.name}' успішно створено!")
                return redirect("products:seller_dashboard")
    else:
        form = ProductForm()
    return render(request, "products/product_form.html", {"form": form, "mode": "create"})


@login_required
@require_http_methods(["GET", "POST"])
def product_update(request, slug):
    require_seller(request.user)
    
    try:
        product = get_object_or_404(Product, slug=slug, seller=request.user)
    except:
        messages.error(request, f"Товар з URL '{slug}' не знайдено або у вас немає прав для його редагування.")
        return redirect("products:seller_dashboard")
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            prod = form.save()
            messages.success(request, f"Товар '{prod.name}' успішно оновлено!")
            return redirect("products:detail", slug=prod.slug)
        else:
            messages.error(request, "Будь ласка, виправте помилки в формі.")
            # Log form errors for debugging
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Form error in {field}: {error}")
    else:
        form = ProductForm(instance=product)
    
    return render(request, "products/product_form.html", {"form": form, "mode": "update", "product": product})


@login_required
def product_delete(request, slug):
    """Delete a product (only for the product's seller)"""
    require_seller(request.user)
    
    try:
        product = get_object_or_404(Product, slug=slug, seller=request.user)
    except:
        messages.error(request, f"Товар з URL '{slug}' не знайдено або у вас немає прав для його видалення.")
        return redirect("products:seller_dashboard")
    
    if request.method == "POST":
        product_name = product.name
        product.delete()
        messages.success(request, f'Товар "{product_name}" успішно видалено.')
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
    
    # Get seller profile
    try:
        seller_profile = request.user.seller_profile
    except Exception:
        seller_profile = None
    
    # Get statistics
    total_products = products.count()
    active_products = products.filter(is_active=True).count()
    
    # Calculate reviews and ratings safely
    total_reviews = 0
    total_rating = 0
    product_count = 0
    
    for product in products:
        try:
            total_reviews += product.review_count
            total_rating += product.average_rating
            product_count += 1
        except Exception as e:
            print(f"Error calculating stats for product {product.name}: {e}")
    
    avg_rating = total_rating / product_count if product_count > 0 else 0
    
    context = {
        'products': products,
        'seller_profile': seller_profile,
        'total_products': total_products,
        'active_products': active_products,
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating, 1),
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
