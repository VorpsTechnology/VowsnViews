import django_filters

from listing.models import ParentListingCategory, ListingCategory, ListingLocation, ListingReview

from home.models import Contact


class ListingReviewFilter(django_filters.FilterSet):
    note = django_filters.CharFilter(field_name='review_description', lookup_expr='icontains')
    start_date = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = ListingReview
        fields = ['is_approved', 'rating']


class CategoryFilter(django_filters.FilterSet):
    note = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = ListingCategory
        fields = ['is_active']


class ParentCategoryFilter(django_filters.FilterSet):
    note = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = ParentListingCategory
        fields = ['is_active']


class ListingLocationFilter(django_filters.FilterSet):
    note = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = ListingLocation
        fields = ['is_active']


class ContactFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = Contact
        fields = ['read']