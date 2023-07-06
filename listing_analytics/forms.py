from django import forms

from listing.models import Listing, ListingPhoto, ListingVideo


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['category', 'location', 'title', 'short_description', 'description', 'catering_policy',
                  'decor_policy', 'alcohol_policy', 'dj_policy', 'image_main', 'image_2', 'image_3', 'image_4',
                  'image_5', 'is_active', 'address']


class ListingPhotoForm(forms.ModelForm):
    class Meta:
        model = ListingPhoto
        fields = ['file']


class ListingVideoForm(forms.ModelForm):
    class Meta:
        model = ListingVideo
        fields = ['file']
