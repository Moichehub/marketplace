from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Order, OrderItem
from products.models import Product

def add_to_cart(request, product_id):
    """Add a product to the user's cart"""
    if not request.user.is_authenticated:
        messages.error(request, "Будь ласка, увійдіть в систему для додавання товарів до кошика.")
        return redirect('accounts:login')
    
    if request.user.is_seller:
        messages.error(request, "Продавці не можуть додавати товари до кошика.")
        return redirect('products:list')
    
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        messages.error(request, "Кількість повинна бути більше 0.")
        return redirect('products:detail', slug=product.slug)
    
    if quantity > product.stock:
        messages.error(request, f"На складі доступно лише {product.stock} одиниць цього товару.")
        return redirect('products:detail', slug=product.slug)
    
    # Get or create a pending order (cart)
    order, created = Order.objects.get_or_create(
        customer=request.user,
        status='pending',
        defaults={'status': 'pending'}
    )
    
    # Check if product is already in cart
    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # Product already in cart, update quantity
        new_quantity = order_item.quantity + quantity
        if new_quantity > product.stock:
            messages.error(request, f"Загальна кількість не може перевищувати {product.stock} одиниць.")
            return redirect('products:detail', slug=product.slug)
        order_item.quantity = new_quantity
        order_item.save()
        messages.success(request, f"Кількість товару '{product.name}' оновлено в кошику.")
    else:
        messages.success(request, f"Товар '{product.name}' додано до кошика.")
    
    return redirect('orders:cart')

@login_required
def cart_view(request):
    """Display the user's shopping cart"""
    if request.user.is_seller:
        messages.error(request, "Продавці не можуть мати кошик.")
        return redirect('products:list')
    
    try:
        order = Order.objects.get(customer=request.user, status='pending')
        items = order.items.all()
        total = sum(item.product.price * item.quantity for item in items)
    except Order.DoesNotExist:
        order = None
        items = []
        total = 0
    
    context = {
        'order': order,
        'items': items,
        'total': total,
    }
    return render(request, 'orders/cart.html', context)

@login_required
def update_cart_item(request, item_id):
    """Update quantity of an item in the cart"""
    if request.user.is_seller:
        return JsonResponse({'error': 'Продавці не можуть мати кошик.'}, status=403)
    
    item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user, order__status='pending')
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        item.delete()
        messages.success(request, f"Товар '{item.product.name}' видалено з кошика.")
    elif quantity > item.product.stock:
        messages.error(request, f"На складі доступно лише {item.product.stock} одиниць цього товару.")
    else:
        item.quantity = quantity
        item.save()
        messages.success(request, f"Кількість товару '{item.product.name}' оновлено.")
    
    return redirect('orders:cart')

@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the cart"""
    if request.user.is_seller:
        return JsonResponse({'error': 'Продавці не можуть мати кошик.'}, status=403)
    
    item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user, order__status='pending')
    product_name = item.product.name
    item.delete()
    messages.success(request, f"Товар '{product_name}' видалено з кошика.")
    
    return redirect('orders:cart')

@login_required
def checkout(request):
    """Process the checkout"""
    if request.user.is_seller:
        messages.error(request, "Продавці не можуть робити замовлення.")
        return redirect('products:list')
    
    try:
        order = Order.objects.get(customer=request.user, status='pending')
        items = order.items.all()
        
        if not items:
            messages.error(request, "Ваш кошик порожній.")
            return redirect('orders:cart')
        
        # Check stock availability
        for item in items:
            if item.quantity > item.product.stock:
                messages.error(request, f"Товар '{item.product.name}' недоступний у такій кількості.")
                return redirect('orders:cart')
        
        # Update stock
        for item in items:
            item.product.stock -= item.quantity
            item.product.save()
        
        # Mark order as paid
        order.status = 'paid'
        order.save()
        
        total = sum(item.product.price * item.quantity for item in items)
        messages.success(request, f"Замовлення на суму {total:.2f} грн успішно оформлено!")
        
        return redirect('orders:order_detail', order_id=order.id)
        
    except Order.DoesNotExist:
        messages.error(request, "Ваш кошик порожній.")
        return redirect('orders:cart')

@login_required
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    items = order.items.all()
    total = sum(item.product.price * item.quantity for item in items)
    
    context = {
        'order': order,
        'items': items,
        'total': total,
    }
    return render(request, 'orders/order_detail.html', context)

@login_required
def order_history(request):
    """Display user's order history"""
    if request.user.is_seller:
        messages.error(request, "Ця функція доступна тільки для покупців.")
        return redirect('products:list')
    
    orders = Order.objects.filter(customer=request.user).exclude(status='pending').order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_history.html', context)
