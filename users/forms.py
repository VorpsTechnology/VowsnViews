from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from .models import (
    User, Address, Task, Budget, GuestList, Vendor
)
# from store.models import CustomerAddress
import re


class LoginForm(forms.Form):
    email = forms.CharField(label='email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class EmailForm(forms.Form):
    email = forms.CharField(label='email')


class CurrencySelectForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('currency',)


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'user_full_name', 'phone_number', 'password1', 'password2')

    def clean(self):
        super(RegistrationForm, self).clean()
        phone_number = self.cleaned_data.get('phone_number')
        if len(str(phone_number)) != 10:
            raise ValidationError(
                _(f'{phone_number} is not an valid mobile number'))


# if inherit form UserChangeForm then user fields are working but also getting password reset form
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # TODO email should be not editable or require Confirmation
        # TODO show phone number filed is email is not phone number
        fields = ('email', 'user_full_name', 'partner_full_name', 'user_bride_groom', 'wedding_date', 'wedding_venue')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(
                _(f'{email} is not an valid email'))

        try:
            email = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('email "%s" is already in use.' % email)


# if inherit form UserChangeForm then user fields are working but also getting password reset form
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('street_address', 'pin_code', 'city', 'state', 'country', 'default')



class TaskAddForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'category')


class BudgetAddForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ('name', 'amount')


class GuestAddForm(forms.ModelForm):
    class Meta:
        model = GuestList
        fields = ('name', 'people')

class VendorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'






