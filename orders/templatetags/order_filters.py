from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def sum_total(items):
    """Calculate total sum for order items"""
    try:
        return sum(item.product.price * item.quantity for item in items)
    except (ValueError, TypeError):
        return 0
