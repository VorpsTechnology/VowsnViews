from django import forms
from crispy_forms.helper import FormHelper
from listing.models import AddititionalPricing, Area, DraftListing, ListingOffer
from vendors.models import (
    VenueFAQ, MakeupFAQ, BridalWearFAQ, GroomWearFAQ, PhotographerFAQ, DecorFAQ, InvitationFAQ, GiftsFAQ,
)


class ListingForm(forms.ModelForm):
    class Meta:
        model = DraftListing
        exclude = (
            'parent_category', 'category', 'catering_policy', 'decor_policy', 'alcohol_policy', 'dj_policy', 'area',
            'additional_pricing', 'photos', 'videos', 'slug', 'is_approved', 'is_update',
            'decline_reason', 'is_declined', 'is_active', 'is_faq_answered', 'top_trending', 'trending', 'label',
            'review', 'is_verified'
        )


class VenueListingForm(forms.ModelForm):
    class Meta:
        model = DraftListing
        fields = ('title', 'sub_location', 'address', 'description', 'more_info', 'low_price', 'high_price',
                  'pre_low_price_text', 'post_low_price_text', 'pre_high_price_text', 'post_high_price_text',
                  'catering_policy', 'decor_policy', 'alcohol_policy', 'dj_policy', 'location',
                  'image_main', 'image_2', 'image_3', 'image_4', 'image_5', 'video_1', 'short_description')


class AdditionalPricingForm(forms.ModelForm):
    class Meta:
        model = AddititionalPricing
        fields = '__all__'


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'


class VenueFAQForm(forms.ModelForm):
    class Meta:
        model = VenueFAQ
        exclude = (
            'draft_listing', 'listing', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12',
            'Q13',
            'Q14',
        )


class MakeupFAQForm(forms.ModelForm):
    class Meta:
        model = MakeupFAQ
        exclude = ('draft_listing', 'listing', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8')


class BridalWearFAQForm(forms.ModelForm):
    class Meta:
        model = BridalWearFAQ
        exclude = (
            'draft_listing', 'listing', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12',
            'Q13')


class GroomWearFAQForm(forms.ModelForm):
    class Meta:
        model = GroomWearFAQ
        exclude = (
            'draft_listing', 'listing', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12',
            'Q13')


class PhotographerFAQForm(forms.ModelForm):
    class Meta:
        model = PhotographerFAQ
        exclude = (
            'draft_listing', 'listing', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7')


class DecorFAQForm(forms.ModelForm):
    class Meta:
        model = DecorFAQ
        exclude = (
            'draft_listing', 'listing', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9')


class InvitationFAQForm(forms.ModelForm):
    class Meta:
        model = InvitationFAQ
        exclude = (
            'draft_listing', 'listing', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10')


class GiftsFAQForm(forms.ModelForm):
    class Meta:
        model = GiftsFAQ
        exclude = (
            'draft_listing', 'listing', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10')

class ListingOfferForm(forms.ModelForm):
    class Meta:
        model = ListingOffer
        fields = '__all__'
        widgets = {
            'offer_expires': forms.DateInput(format='%d-%m-%Y',
                                               attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                      'type': 'date'}),
        }