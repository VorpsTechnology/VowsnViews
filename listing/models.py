from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.db.models import Q
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from users.models import User, Vendor
from vendors.models import VenueFAQ, BridalWearFAQ, GroomWearFAQ, MakeupFAQ, PhotographerFAQ, DecorFAQ, InvitationFAQ, GiftsFAQ
from datetime import datetime

REVIEW_RATING_CHOICES = (
    (1, 1),
    (1.5, 1.5),
    (2, 2),
    (2.5, 2.5),
    (3, 3),
    (3.5, 3.5),
    (4, 4),
    (4.5, 4.5),
    (5, 5),
)

LABEL_CHOICES = (
    ('Elite', 'Elite'),
    ('In Demand', 'In Demand'),
    ('Our Recommendation', 'Our Recommendation'),
    ('Most Booked', 'Most Booked'),
    ('Trending', 'Trending'),
    ('Popular', 'Popular'),
    ('Best Deal', 'Best Deal'),
    ('Best Offer', 'Best Offer'),
)

SEATING_CHOICES = (
    ('Indoor', 'Indoor'),
    ('Outdoor', 'Outdoor'),
)


class ListingReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)
    review_description = models.TextField()
    rating = models.FloatField(choices=REVIEW_RATING_CHOICES, max_length=3)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user}"

    def get_absolute_url(self):  # Redirect to this link after adding review
        return reverse("listing-list-view")

    def to_int(self):
        return int(self.rating)


class ListingLocationQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(slug__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
            return qs


class ListingLocationManager(models.Manager):
    def get_queryset(self):
        return ListingLocationQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class ListingLocation(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='listing_location', null=True, blank=True)  # image of slide ...
    is_active = models.BooleanField(default=True)

    objects = ListingLocationManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # Redirect to this link after adding category , kwargs={'slug': self.slug })
        return reverse("admin-listing-location-list")


class SubListingLocationQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(slug__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
            return qs


class SubListingLocationManager(models.Manager):
    def get_queryset(self):
        return SubListingLocationQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class SubListingLocation(models.Model):
    listing_location = models.ForeignKey(ListingLocation, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='listing_location', null=True, blank=True)  # image of slide ...
    is_active = models.BooleanField(default=True)

    objects = SubListingLocationManager()

    def __str__(self):
        return self.title

    def sub_loc(self):
        return f'sub_location={self.id}'

    def get_absolute_url(self):  # Redirect to this link after adding category , kwargs={'slug': self.slug })
        return reverse("admin-listing-sub-location-list")


class ParentListingCategory(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='parent_listing-category', null=True, blank=True)  # image of slide ...
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # Redirect to this link after adding category , kwargs={'slug': self.slug })
        return reverse("admin-listing-parent-category-list")


class ListingCategoryQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(description__icontains=query) |
                         Q(slug__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
            return qs


class ListingCategoryManager(models.Manager):
    def get_queryset(self):
        return ListingCategoryQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class ListingCategory(models.Model):
    parent_category = models.ForeignKey(ParentListingCategory, on_delete=models.CASCADE)

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='listing_category', null=True, blank=True)  # image of slide ...
    is_active = models.BooleanField(default=True)

    objects = ListingCategoryManager()

    def __str__(self):
        return self.title

    def sub_cat(self):
        return f'category={self.id}'

    def get_absolute_url(self):
        return reverse("admin-listing-category-list")


class ListingQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(description__icontains=query) |
                         Q(slug__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
            return qs


class ListingManager(models.Manager):
    def get_queryset(self):
        return ListingQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class ListingPhoto(models.Model):
    file = models.FileField(upload_to='listing/photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ListingVideo(models.Model):
    file = models.FileField(upload_to='listing/video/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Area(models.Model):
    seating_type = models.CharField(max_length=20, choices=SEATING_CHOICES)
    seating_space = models.IntegerField()
    floating_space = models.IntegerField()
    additional_text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='area', null=True, blank=True)

    def __str__(self):
        return f"{self.id}"


class AddititionalPricing(models.Model):
    pricing_title = models.CharField(max_length=100, default='No Additional Cost')
    cost = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    suffix = models.CharField(max_length=100, null=True, blank=True)


class ListingOffer(models.Model):
    offer_title = models.CharField(max_length=300, default='Offer')
    offer_description = models.TextField(null=True, blank=True)
    offer_expires = models.DateField(null=True, blank=True)
    offer_image = models.ImageField(null=True, blank=True)

    def str(self):
        return self.offer_title

    def is_offer_expired(self):
        now = datetime.date.today()
        if now < self.offer_expires:
            return True
        return False
        

class Listing(models.Model):
    parent_category = models.ForeignKey(ParentListingCategory, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(ListingCategory, on_delete=models.CASCADE, null=True, blank=True)

    location = models.ForeignKey(ListingLocation, on_delete=models.CASCADE)
    sub_location = models.ForeignKey(SubListingLocation, on_delete=models.CASCADE, null=True, blank=True)

    photos = models.ManyToManyField(ListingPhoto, blank=True, null=True)
    videos = models.ManyToManyField(ListingVideo, blank=True, null=True)

    title = models.CharField(max_length=200, unique=True)
    low_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    high_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    pre_low_price_text = models.CharField(max_length=500, blank=True, null=True)
    post_low_price_text = models.CharField(max_length=500, blank=True, null=True)
    pre_high_price_text = models.CharField(max_length=500, blank=True, null=True)
    post_high_price_text = models.CharField(max_length=500, blank=True, null=True)
    additional_text = RichTextField(help_text='To describe product price', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    meta_title = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    short_description = RichTextField(help_text='To describe product in short', null=True, blank=True)
    description = RichTextField(help_text='Overview product', null=True, blank=True)
    more_info = RichTextField(help_text='More Info', null=True, blank=True)

    is_in_house_listing = models.BooleanField(default=False)
    review_id = models.CharField(max_length=500, blank=True, null=True)
    
    offer = models.ManyToManyField(ListingOffer ,null=True, blank=True)

    address = models.TextField(null=True, blank=True, max_length=200)

    image_main = models.ImageField(upload_to='listings', null=True, blank=True)
    image_2 = models.ImageField(upload_to='listings', null=True, blank=True)
    image_3 = models.ImageField(upload_to='listings', null=True, blank=True)
    image_4 = models.ImageField(upload_to='listings', null=True, blank=True)
    image_5 = models.ImageField(upload_to='listings', null=True, blank=True)

    image_main_link = models.URLField(null=True, blank=True)
    image_2_link = models.URLField(null=True, blank=True)
    image_3_link = models.URLField(null=True, blank=True)
    image_4_link = models.URLField(null=True, blank=True)
    image_5_link = models.URLField(null=True, blank=True)

    video_1 = models.URLField(null=True, blank=True)
    video_2 = models.URLField(null=True, blank=True)
    video_3 = models.URLField(null=True, blank=True)
    video_4 = models.URLField(null=True, blank=True)
    video_5 = models.URLField(null=True, blank=True)
    video_6 = models.URLField(null=True, blank=True)
    video_7 = models.URLField(null=True, blank=True)
    video_8 = models.URLField(null=True, blank=True)
    video_9 = models.URLField(null=True, blank=True)
    video_10 = models.URLField(null=True, blank=True)

    review = models.ManyToManyField(ListingReview, blank=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=20, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    top_trending = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    # For Venue Category
    area = models.ManyToManyField(Area, blank=True)
    catering_policy = models.CharField(null=True, blank=True, max_length=200)
    decor_policy = models.CharField(null=True, blank=True, max_length=200)
    alcohol_policy = models.CharField(null=True, blank=True, max_length=200)
    dj_policy = models.CharField(null=True, blank=True, max_length=200)
    additional_pricing = models.ManyToManyField(AddititionalPricing, blank=True)
    objects = ListingManager()

    # FAQ field
    is_faq_answered = models.BooleanField(default=False)

    # For google review
    place_id = models.CharField(null=True, blank=True, max_length=200)

    class Meta:
        db_table = 'listings_listing'
        ordering = ['title']

    def save(self, *args, **kwargs):
        date_time_slug = f"{datetime.now()}"
        date_time_slug = date_time_slug.replace(" ", "@@")
        date_time_slug = date_time_slug.replace("-", "_")
        date_time_slug = date_time_slug.replace(":", "_")
        date_time_slug = date_time_slug.replace(".", "_")
        slug = self.title + date_time_slug
        self.slug = slugify(slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # Redirect to this link after adding product
        return reverse("admin-listing-list")

    def get_search_redirect(self):
        return reverse("listing-detail-view", kwargs={'pk': self.id})

    def get_faq(self):
        if self.is_faq_answered: 
            if self.parent_category.title == 'Venue':
                return VenueFAQ.objects.filter(listing=self).first()
            if self.parent_category.title == 'Bridal Wear':
                return BridalWearFAQ.objects.filter(listing=self).first()
            if self.parent_category.title == 'Groom Wear':
                return GroomWearFAQ.objects.filter(listing=self).first()
            if self.parent_category.title == 'Makeup & Mehndi':
                return MakeupFAQ.objects.filter(listing=self).first()
            if self.parent_category.title == 'Photographer':
                return PhotographerFAQ.objects.filter(listing=self).first()
            if self.parent_category.title == 'Planning & Decor':
                return PhotographerFAQ.objects.filter(listing=self).first()
            if self.parent_category.title == 'Invites':
                return InvitationFAQ.objects.filter(listing=self).first()
            if self.parent_category.title == 'Gifts':
                return GiftsFAQ.objects.filter(listing=self).first()
            return None
        return None    

    def get_image(self):
        if self.image_main:
            return self.image_main.url
        else:
            return self.image_main_link

    def get_vendor(self):
        return Vendor.objects.filter(listing = self).first()


class DraftListing(models.Model):
    parent_category = models.ForeignKey(ParentListingCategory, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(ListingCategory, on_delete=models.CASCADE, null=True, blank=True)

    location = models.ForeignKey(ListingLocation, on_delete=models.CASCADE)
    sub_location = models.ForeignKey(SubListingLocation, on_delete=models.CASCADE, null=True, blank=True)

    photos = models.ManyToManyField(ListingPhoto, blank=True, null=True)
    videos = models.ManyToManyField(ListingVideo, blank=True, null=True)
    
    offer = models.ManyToManyField(ListingOffer ,null=True, blank=True)

    title = models.CharField(max_length=200)
    low_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    high_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    price_for = models.CharField(max_length=500, blank=True, null=True)
    pre_low_price_text = models.CharField(max_length=500, blank=True, null=True)
    post_low_price_text = models.CharField(max_length=500, blank=True, null=True)
    pre_high_price_text = models.CharField(max_length=500, blank=True, null=True)
    post_high_price_text = models.CharField(max_length=500, blank=True, null=True)
    additional_text = RichTextField(help_text='To describe product price', null=True, blank=True)
    slug = models.SlugField(unique=True)

    meta_title = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    short_description = RichTextField(help_text='To describe product in short', null=True, blank=True)
    description = RichTextField(help_text='Overview product', null=True, blank=True)
    more_info = RichTextField(help_text='More Info', null=True, blank=True)

    is_in_house_listing = models.BooleanField(default=False)
    review_id = models.CharField(max_length=200, blank=True, null=True)

    address = models.TextField(null=True, blank=True, max_length=200)

    image_main = models.ImageField(upload_to='listings', null=True, blank=True)
    image_2 = models.ImageField(upload_to='listings', null=True, blank=True)
    image_3 = models.ImageField(upload_to='listings', null=True, blank=True)
    image_4 = models.ImageField(upload_to='listings', null=True, blank=True)
    image_5 = models.ImageField(upload_to='listings', null=True, blank=True)

    image_main_link = models.URLField(null=True, blank=True)
    image_2_link = models.URLField(null=True, blank=True)
    image_3_link = models.URLField(null=True, blank=True)
    image_4_link = models.URLField(null=True, blank=True)
    image_5_link = models.URLField(null=True, blank=True)

    video_1 = models.URLField(null=True, blank=True)
    video_2 = models.URLField(null=True, blank=True)
    video_3 = models.URLField(null=True, blank=True)
    video_4 = models.URLField(null=True, blank=True)
    video_5 = models.URLField(null=True, blank=True)
    video_6 = models.URLField(null=True, blank=True)
    video_7 = models.URLField(null=True, blank=True)
    video_8 = models.URLField(null=True, blank=True)
    video_9 = models.URLField(null=True, blank=True)
    video_10 = models.URLField(null=True, blank=True)

    review = models.ManyToManyField(ListingReview, blank=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=20, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    top_trending = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    # For Venue Category
    area = models.ManyToManyField(Area, blank=True)
    catering_policy = models.CharField(null=True, blank=True, max_length=200)
    decor_policy = models.CharField(null=True, blank=True, max_length=200)
    alcohol_policy = models.CharField(null=True, blank=True, max_length=200)
    dj_policy = models.CharField(null=True, blank=True, max_length=200)
    additional_pricing = models.ManyToManyField(AddititionalPricing, blank=True)
    is_approved = models.BooleanField(default=False)
    is_update = models.BooleanField(default=False)
    objects = ListingManager()

    # FAQ field
    is_faq_answered = models.BooleanField(default=False)

    # For Decline listing
    decline_reason = models.TextField(blank=True, null=True)
    is_declined = models.BooleanField(default=False)

    class Meta:
        db_table = 'listings_draft_listing'
        ordering = ['title']

    def save(self, *args, **kwargs):
        date_time_slug = f"{datetime.now()}"
        date_time_slug = date_time_slug.replace(" ", "@@")
        date_time_slug = date_time_slug.replace("-", "_")
        date_time_slug = date_time_slug.replace(":", "_")
        date_time_slug = date_time_slug.replace(".", "_")
        slug = self.title + date_time_slug
        self.slug = slugify(slug)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    def get_absolute_url(self):  # Redirect to vendor list link after adding product
        return reverse("vendor-home")

    def get_search_redirect(self):
        return reverse("listing-detail-view", kwargs={'pk': self.id})

    def get_faq(self):
        if self.parent_category.title == 'Venue':
            return VenueFAQ.objects.filter(draft_listing=self)
        if self.parent_category.title == 'Bridal Wear':
            return BridalWearFAQ.objects.filter(draft_listing=self)
        if self.parent_category.title == 'Groom Wear':
            return GroomWearFAQ.objects.filter(draft_listing=self)
        if self.parent_category.title == 'Makeup & Mehndi':
            return MakeupFAQ.objects.filter(draft_listing=self)
        if self.parent_category.title == 'Photographer':
            return PhotographerFAQ.objects.filter(draft_listing=self)
        if self.parent_category.title == 'Planning & Decor':
            return PhotographerFAQ.objects.filter(draft_listing=self)
        if self.parent_category.title == 'Invites':
            return InvitationFAQ.objects.filter(draft_listing=self)
        if self.parent_category.title == 'Gifts':
            return GiftsFAQ.objects.filter(draft_listing=self)
        return None

    def get_image(self):
        if self.image_main:
            return self.image_main.url
        else:
            return self.image_main_link


class ListingFavorite(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.listing.title}_{self.user}_favorite'


class ListingContact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    mobile = models.BigIntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    request_call = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name}_{self.mobile}"

    def get_absolute_url(self):  # Redirect to this link after adding review
        return reverse("admin-listing-contact")