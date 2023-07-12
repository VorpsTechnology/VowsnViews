from django import forms

from .models import NewsLetter, Contact, Landing, ListingCategoryBudget
from listing.models import ParentListingCategory, ListingCategory

CURRENCY = (
    ("INR", "INR"),
    ("USD", "USD"),
    ("EUR", "EUR"),
    ("AUD", "AUD"),
    ("GBP", "GBP"),
)


class CurrencyForm(forms.Form):
    currency = forms.ChoiceField(choices=CURRENCY)


class NewsLetterForm(forms.ModelForm):

    class Meta:
        model = NewsLetter
        fields = ('email',)

class ListingSearchForm(forms.Form):
    category = forms.CharField(max_length=200)
    location = forms.CharField(max_length=200)



class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('name', 'email', 'mobile', 'city','description')



class LandingForm(forms.ModelForm):
    listing_parent_category = forms.ModelMultipleChoiceField(
        queryset=ParentListingCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)
    listing_sub_category = forms.ModelMultipleChoiceField(
        queryset=ListingCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        required=False)

    class Meta:
        model = Landing
        fields = ('name', 'email', 'mobile', 'city', 'wedding_date','listing_parent_category', 'listing_sub_category')


class ListingCategoryBudgetForm(forms.ModelForm):
    class Meta:
        model = ListingCategoryBudget
        fields = ('listing_sub_category', 'min_price', 'max_price')