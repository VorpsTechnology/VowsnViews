from django.db import models
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import reverse
from ckeditor.fields import RichTextField

WEDDING_DATE_CHOICES = (
    ("Within this month", "Within this month"),
    ("In next 2-3 months", "In next 2-3 months"),
    ("In next 3-6 months", "In next 3-6 months"),
    ("After around 6 months", "After around 6 months"),
)

class NewsLetter(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.email}"

    def get_absolute_url(self):  # Redirect to this link after adding review
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    mobile = models.BigIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    date = models.DateField(default=timezone.now)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name}_{self.mobile}"

    def get_absolute_url(self):  # Redirect to this link after adding review
        return reverse("admin-contact")


class DestinationWedding(models.Model):
    goa = RichTextField(null=True, blank=True)
    jaipur = RichTextField(null=True, blank=True)
    udaipur = RichTextField(null=True, blank=True)
    jim_corbet = RichTextField(null=True, blank=True)
    planning_decor = RichTextField(null=True, blank=True)

    def __str__(self):
        return 'destination_wedding_text'


class TPP(models.Model):
    tand_c = RichTextField(null=True, blank=True)
    t_pp = RichTextField(null=True, blank=True)
    shipping_policy = RichTextField(null=True, blank=True)
    refund_policy = RichTextField(null=True, blank=True)
    vendor_policy = RichTextField(null=True, blank=True)
    contact = RichTextField(null=True, blank=True)

    def __str__(self):
        return 'TPP'


class Landing(models.Model):
    listing_parent_category = models.ManyToManyField('listing.ParentListingCategory', null=True)
    listing_sub_category = models.ManyToManyField('listing.ListingCategory', null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    budget = models.ManyToManyField('ListingCategoryBudget', blank=True)
    mobile = models.BigIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100,blank=True,null=True)
    wedding_date = models.CharField(choices=WEDDING_DATE_CHOICES, max_length=50, null=True, default=None)
    date = models.DateField(default=timezone.now)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name}_{self.mobile}"


class ListingCategoryBudget(models.Model):
    listing_sub_category = models.ForeignKey('listing.ListingCategory', on_delete=models.CASCADE)
    min_price = models.IntegerField(default=0, null=True, blank=True)
    max_price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.listing_sub_category}_{self.min_price} - {self.max_price}"
