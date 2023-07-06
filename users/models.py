from __future__ import unicode_literals
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from .managers import UserManager

BG = [
    ('Bride', 'Bride'),
    ('Groom', 'Groom'),
]

CURRENCY = (
    ("INR", "INR"),
    ("USD", "USD"),
    ("EUR", "EUR"),
    ("AUD", "AUD"),
    ("GBP", "GBP"),
)


# Address
class Address(models.Model):
    street_address = models.TextField()
    pin_code = models.IntegerField(null=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    default = models.BooleanField(default=False)

    class Meta:
        ordering = ['default']

    def __str__(self):
        return self.city

    def get_absolute_url(self):  # Redirect to this link after adding address
        return reverse("users-address-list")

    # def save(self, *args, **kwargs):
    #     if self.default is True:
    #         # try:
    #         a = Address.objects.get(default=True, user=self.request.user)
    #         a.default = False
    #         a.save()
    #         # except:
    #             # pass
    #     # else:
    #     #     try:
    #     #         a = Address.objects.filter(default=True, user=self.request.user).count()
    #     #         if 0 == a:
    #     #           self.default = True
    #     #     except:
    #     #         pass
    #     super().save(*args, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'), unique=True, max_length=320, help_text='Provide an email for registration')

    # User Details
    user_full_name = models.CharField(_('name'), max_length=70)
    user_bride_groom = models.CharField(choices=BG, max_length=20, blank=True, null=True)
    user_profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)

    # Partner Details
    partner_full_name = models.CharField(_("Partner name"), max_length=70, blank=True, null=True)
    partner_bride_groom = models.CharField(choices=BG, max_length=20, blank=True, null=True)
    # partner_profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)

    # Wedding
    wedding_date = models.DateField(_('wedding date'), blank=True, null=True)
    wedding_venue = models.CharField(_('wedding venue'), max_length=70, blank=True, null=True)

    # Contact Info
    phone_number = models.BigIntegerField(help_text='Provide an mobile number without +91')

    # Django
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_verified = models.BooleanField(_('verified'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_vendor = models.BooleanField(_('vendor'), default=False)
    currency = models.CharField(choices=CURRENCY, max_length=70, default='INR')

    address = models.ManyToManyField(Address, blank=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("profile")

    def get_full_name(self):
        full_name = '%s %s' % (self.user_full_name)
        return full_name.strip()

    def get_short_name(self):
        return self.user_full_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


# Task
class Task(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}_{self.user}'

    def get_absolute_url(self):
        return reverse("users-checklist")


# Budget
class Budget(models.Model):
    name = models.CharField(max_length=200)
    amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}_{self.user}'

    def get_absolute_url(self):
        return reverse("users-budget-list")

    def get_total(self):
        budget_list = Budget.objects.filter(user=self.user)
        total = 0
        for budget in budget_list:
            total += budget.amount
        return total


# GuestList
class GuestList(models.Model):
    name = models.CharField(max_length=200)
    people = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}_{self.user}'

    def get_absolute_url(self):
        return reverse("users-guest-list")

    def get_total_people_count(self):
        guest_list = GuestList.objects.filter(user=self.user)
        total = 0
        for guest in guest_list:
            total += guest.people
        return total


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(default='default.jpg', blank=True)
    youtube_embed_link = models.URLField(null=True, blank=True)
    description = RichTextField(help_text='Description')
    short_description = models.TextField(help_text='Short Description', blank=True, null=True)
    meta_title = models.TextField(help_text='Meta title', blank=True, null=True)
    meta_description = models.TextField(help_text='Meta desription', blank=True, null=True)
    is_vnv = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def _str_(self):
        return f'{self.title}'

    def get_absolute_url(self):  # Redirect to this link after adding address
        return reverse("users-blog-list")


# Vendor User
class Vendor(models.Model):
    vendor_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    brand_name = models.CharField(max_length=200)
    description = models.TextField()
    website_link = models.URLField(null=True, blank=True)
    listing_parent_category = models.ForeignKey('listing.ParentListingCategory', on_delete=models.SET_NULL, null=True)
    listing_sub_category = models.ForeignKey('listing.ListingCategory', on_delete=models.SET_NULL, null=True)
    listing = models.OneToOneField('listing.Listing', on_delete=models.SET_NULL, null=True, blank=True)
    draft_listing = models.OneToOneField('listing.DraftListing', on_delete=models.SET_NULL, null=True, blank=True)

    # Field for data transfer
    is_listing_on = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.brand_name}"

    def get_listing(self):
        if self.draft_listing:
            if self.draft_listing.is_approved:
                return self.listing
            else:
                return self.draft_listing
        else:
            return None

class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return f"{self.id}"