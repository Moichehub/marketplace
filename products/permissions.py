from django.core.exceptions import PermissionDenied


def require_seller(user):
    if not user.is_authenticated or not getattr(user, "is_seller", False):
        raise PermissionDenied("Доступ лише для продавців")
