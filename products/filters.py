import django_filters
from django.db.models import Q
from .models import Product


class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='Search')

    class Meta:
        model = Product
        fields = []

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset

        filters = Q(name__icontains=value) | Q(category__name__icontains=value)

        if value.isdigit():
            filters |= Q(price__gte=value) | Q(price__lte=value)

        return queryset.filter(filters)