from django import forms

from .models import ListingReview, ListingContact


class ListingReviewForm(forms.ModelForm):

    class Meta:
        model = ListingReview
        fields = ('review_description', 'rating')


class ListingContactForm(forms.ModelForm):

    class Meta:
        model = ListingContact
        fields = ['name', 'email', 'mobile', 'description']
