import django_filters
from django import forms

from products.models import Product, Category, FunctionCategory,ProductBrand,Gender,ProductSize, ProductColor


class ProductFilter(django_filters.FilterSet):
    discount_price = django_filters.RangeFilter(field_name="discount_price")
    note = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    label = django_filters.CharFilter(field_name='label', lookup_expr='iexact')

    variation__product_size = django_filters.ModelMultipleChoiceFilter(queryset=ProductSize.objects.all(),
                                                                       widget=forms.CheckboxSelectMultiple)
                                                                       
    variation__product_color = django_filters.ModelMultipleChoiceFilter(queryset=ProductColor.objects.all(),
                                                                       widget=forms.CheckboxSelectMultiple)
    
    size = django_filters.CharFilter(field_name='variation__title', lookup_expr='iexact')
    
    color = django_filters.CharFilter(field_name='variation__title', lookup_expr='iexact')
    
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple)
    f_category = django_filters.ModelMultipleChoiceFilter(queryset=FunctionCategory.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple)
    gender = django_filters.ModelMultipleChoiceFilter(queryset=Gender.objects.all(),
                                                          widget=forms.CheckboxSelectMultiple)
    brand = django_filters.ModelMultipleChoiceFilter(queryset=ProductBrand.objects.all(),
                                                          widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Product
        fields = ['vendor_name', 'category', 'f_category', 'gender', 'brand'] 
