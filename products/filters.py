import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="Пошук"
    )
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte", label="Від ціни"
    )
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte", label="До ціни"
    )
    category = django_filters.CharFilter(
        field_name="category__slug", lookup_expr="iexact", label="Категорія"
    )

    class Meta:
        model = Product
        fields = ["q", "category", "min_price", "max_price"]
