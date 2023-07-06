from django import forms

from .models import CouponCustomer


class CouponCustomerForm(forms.ModelForm):

    class Meta:
        model = CouponCustomer
        fields = ('code',)

