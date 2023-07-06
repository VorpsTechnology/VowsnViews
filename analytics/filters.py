import django_filters

from products.models import Category, ParentCategory
from order.models import (
    MiniOrder, Order, ReturnMiniOrder, CancelMiniOrder
)
from home.models import Contact


class CategoryFilter(django_filters.FilterSet):
    note = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['is_active']


class ParentCategoryFilter(django_filters.FilterSet):
    note = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = ParentCategory
        fields = ['is_active']


class ReturnFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user', lookup_expr='icontains')
    start_date = django_filters.DateFilter(field_name="return_date", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="return_date", lookup_expr='lte')

    class Meta:
        model = ReturnMiniOrder
        fields = ['return_status', 'return_granted', 'return_reason']


class CancelFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user', lookup_expr='icontains')
    start_date = django_filters.DateFilter(field_name="cancel_date", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="cancel_date", lookup_expr='lte')

    class Meta:
        model = CancelMiniOrder
        fields = ['cancel_status', 'cancel_granted', 'cancel_reason']


class MiniOrderFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user', lookup_expr='icontains')
    start_date = django_filters.DateFilter(field_name="ordered_date_time", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="ordered_date_time", lookup_expr='lte')

    class Meta:
        model = MiniOrder
        fields = ['order_status', 'mini_order_ref_number', 'order_ref_number']


class ContactFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = Contact
        fields = ['read']
