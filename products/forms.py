from django import forms

from products.models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('review_description', 'rating')

