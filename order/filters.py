import django_filters

from .models import Order


class OrderFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="ordered_date_time", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="ordered_date_time", lookup_expr='lte')

    class Meta:
        model = Order
        fields = []
