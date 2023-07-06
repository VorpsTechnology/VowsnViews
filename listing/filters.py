import django_filters
from django import forms

from .models import Listing, ListingCategory, ParentListingCategory, ListingLocation, SubListingLocation, DraftListing


class ListingFilter(django_filters.FilterSet):
    discount_price = django_filters.RangeFilter(field_name="low_price")
    note = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    category = django_filters.ModelMultipleChoiceFilter(queryset=ListingCategory.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple)

    location = django_filters.ModelMultipleChoiceFilter(queryset=ListingLocation.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple)

    sub_location = django_filters.ModelMultipleChoiceFilter(queryset=SubListingLocation.objects.all(),
                                                            widget=forms.CheckboxSelectMultiple)

    parent_category = django_filters.ModelMultipleChoiceFilter(queryset=ParentListingCategory.objects.all(),
                                                               widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Listing
        fields = ['parent_category', 'category', 'vendor', 'location', 'sub_location']


class DraftListingFilter(django_filters.FilterSet):
    discount_price = django_filters.RangeFilter(field_name="low_price")
    note = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    category = django_filters.ModelMultipleChoiceFilter(queryset=ListingCategory.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple)

    location = django_filters.ModelMultipleChoiceFilter(queryset=ListingLocation.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple)

    sub_location = django_filters.ModelMultipleChoiceFilter(queryset=SubListingLocation.objects.all(),
                                                            widget=forms.CheckboxSelectMultiple)

    parent_category = django_filters.ModelMultipleChoiceFilter(queryset=ParentListingCategory.objects.all(),
                                                               widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = DraftListing
        fields = ['parent_category', 'category', 'vendor', 'location', 'sub_location']