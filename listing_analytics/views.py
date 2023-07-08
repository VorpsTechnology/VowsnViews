import json

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template.defaultfilters import slugify
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib import messages
from instagram_basic_display.InstagramBasicDisplay import InstagramBasicDisplay

from listing.models import (
    ListingLocation, ListingCategory, Listing, ParentListingCategory, ListingContact, ListingPhoto, ListingReview,
    ListingVideo, SubListingLocation, DraftListing, Area, AddititionalPricing
)
from vendors.models import VenueFAQ, Vendor, VendorInstagramToken
from users.models import (
    Blog
)
from home.models import Landing
from listing.filters import ListingFilter, DraftListingFilter
from .filters import CategoryFilter, ParentCategoryFilter, ContactFilter, ListingLocationFilter, ListingReviewFilter
from .forms import ListingPhotoForm, ListingVideoForm

from datetime import datetime, timedelta

today = datetime.now().date()
yesterday = today + timedelta(-1)


class ListingPhotosAdd(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, **kwargs):
        listing_pk = self.kwargs['pk']
        listing = Listing.objects.get(id=listing_pk)
        photos_list = listing.photos.all()
        return render(self.request, 'listing_analytics/multi-image.html', {'photos': photos_list,
                                                                           'listing_pk': listing_pk})

    def post(self, request, **kwargs):
        form = ListingPhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            listing = Listing.objects.get(id=self.kwargs['pk'])
            listing.photos.add(form)
            listing.save()
            data = {'is_valid': True, 'name': form.file.name, 'url': form.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

    def test_func(self):
        return self.request.user.is_staff is True


class ListingPhotosDelete(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, **kwargs):
        ListingPhoto.objects.get(id=self.kwargs['pk']).delete()
        return redirect('analytics-listing-image-add', pk=self.kwargs['listing_id'])

    def test_func(self):
        return self.request.user.is_staff is True


class ListingVideoAdd(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, **kwargs):
        listing_pk = self.kwargs['pk']
        listing = Listing.objects.get(id=listing_pk)
        photos_list = listing.videos.all()
        return render(self.request, 'listing_analytics/multi-video.html', {'photos': photos_list,
                                                                           'listing_pk': listing_pk})

    def post(self, request, **kwargs):
        form = ListingVideoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            listing = Listing.objects.get(id=self.kwargs['pk'])
            listing.videos.add(form)
            listing.save()
            data = {'is_valid': True, 'name': form.file.name, 'url': form.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

    def test_func(self):
        return self.request.user.is_staff is True


class ListingVideoDelete(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, **kwargs):
        ListingVideo.objects.get(id=self.kwargs['pk']).delete()
        return redirect('analytics-listing-video-add', pk=self.kwargs['listing_id'])

    def test_func(self):
        return self.request.user.is_staff is True


class AnalyticsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "listing_analytics/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contact_total = ListingContact.objects.all().count
        contact_today = ListingContact.objects.filter(date__gte=yesterday).count

        context['contact_today'] = contact_today
        context['contact_total'] = contact_total
        return context

    def test_func(self):
        return self.request.user.is_staff is True


# Listings
class AdminListingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Listing
    paginate_by = 20
    template_name = "listing_analytics/listing_list_admin.html"

    # queryset = Listing.objects.filter(is_active=True)
    # Template name listing_list.html
    # object_list variable name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = Listing.objects.all()
        listing_filter = ListingFilter(self.request.GET, queryset=current_query)

        context['filter'] = listing_filter
        if len(listing_filter.qs) != len(current_query):
            context['object_list'] = listing_filter.qs
            if len(listing_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


# Add Listings
class AdminListingAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Listing
    fields = ['parent_category', 'category', 'location', 'sub_location', 'title', 'low_price', 'high_price',
              'pre_low_price_text', 'post_low_price_text', 'pre_high_price_text', 'post_high_price_text',
              'additional_text', 'meta_title', 'meta_description', 'short_description', 'description', 'review_id',
              'more_info', 'catering_policy', 'decor_policy', 'alcohol_policy', 'dj_policy', 'video_1', 'video_2',
              'video_3', 'video_4', 'video_5', 'video_6', 'video_7', 'video_8', 'video_9', 'video_10',
              'image_main', 'image_2', 'image_3', 'image_4', 'image_5', 'image_main_link', 'image_2_link',
              'image_3_link', 'image_4_link', 'image_5_link', 'is_active', 'is_verified', 'is_in_house_listing',  'is_faq_answered',
              'address', 'trending', 'label']
    template_name = "listing_analytics/listing_add_update_admin.html"

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.slug = slugify(listing.title)
        listing.save()

        draft_listing = DraftListing()
        if not DraftListing.objects.filter(slug=listing.slug).first():
            for field in listing._meta.fields:
                setattr(draft_listing, field.name, getattr(listing, field.name))
            draft_listing.save()
            for item in listing.photos.all():
                draft_listing.photos.add(item)
            for item in listing.videos.all():
                draft_listing.videos.add(item)
            for item in listing.review.all():
                draft_listing.review.add(item)
            for item in listing.area.all():
                draft_listing.area.add(item)
            for item in listing.additional_pricing.all():
                draft_listing.additional_pricing.add(item)
            draft_listing.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponse(form.errors.as_json())

    def test_func(self):
        return self.request.user.is_staff is True


# Update Listings
class AdminListingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Listing
    fields = ['parent_category', 'category', 'location', 'sub_location', 'title', 'low_price', 'high_price',
              'pre_low_price_text', 'post_low_price_text', 'pre_high_price_text', 'post_high_price_text',
              'additional_text', 'meta_title', 'meta_description', 'short_description', 'description', 'review_id',
              'more_info', 'catering_policy', 'decor_policy', 'alcohol_policy', 'dj_policy', 'video_1', 'video_2',
              'video_3', 'video_4', 'video_5', 'video_6', 'video_7', 'video_8', 'video_9', 'video_10',
              'image_main', 'image_2', 'image_3', 'image_4', 'image_5', 'image_main_link', 'image_2_link',
              'image_3_link', 'image_4_link', 'image_5_link', 'is_active', 'is_verified', 'is_in_house_listing',  'is_faq_answered',
              'address', 'trending', 'label']
    template_name = "listing_analytics/listing_add_update_admin.html"

    def form_valid(self, form):
        listing = form.instance
        listing_backup = Listing.objects.get(id = listing.id)
        draft_listing = DraftListing.objects.filter(slug = listing_backup.slug).first()
        listing.save()
        if draft_listing:
            for field in listing._meta.fields:
                setattr(draft_listing, field.name, getattr(listing, field.name))
            draft_listing.save()
            for item in listing.photos.all():
                draft_listing.photos.add(item)
            for item in listing.videos.all():
                draft_listing.videos.add(item)
            for item in listing.review.all():
                draft_listing.review.add(item)
            for item in listing.area.all():
                draft_listing.area.add(item)
            for item in listing.additional_pricing.all():
                draft_listing.additional_pricing.add(item)
            draft_listing.save()
        messages.success(self.request, "Listing updated successfully")
        return redirect('admin-listing-list')

    # template name listing_form
    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


# Delete Listings
class AdminListingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Listing
    fields = ['parent_category', 'category', 'location', 'sub_location', 'title', 'low_price', 'high_price',
              'pre_low_price_text', 'post_low_price_text', 'pre_high_price_text', 'post_high_price_text',
              'additional_text', 'meta_title', 'meta_description', 'short_description', 'description', 'review_id',
              'more_info', 'catering_policy', 'decor_policy', 'alcohol_policy', 'dj_policy', 'video_1', 'video_2',
              'video_3', 'video_4', 'video_5', 'video_6', 'video_7', 'video_8', 'video_9', 'video_10',
              'image_main', 'image_2', 'image_3', 'image_4', 'image_5', 'image_main_link', 'image_2_link',
              'image_3_link', 'image_4_link', 'image_5_link', 'is_active', 'is_verified', 'is_in_house_listing',  'is_faq_answered',
              'address', 'trending', 'label']
    template_name = "listing_analytics/listing_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        listing = self.get_object()
        draft_listing = DraftListing.objects.filter(slug=listing.slug).first()
        if draft_listing:
            draft_listing.is_approved = False
            draft_listing.save()
        listing.delete()
        messages.success(self.request, "Listing deleted successfully.")
        return redirect('admin-listing-list')

    def test_func(self):
        return self.request.user.is_staff is True


class AdminBlogListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Blog
    paginate_by = 20
    template_name = "listing_analytics/blog_list_admin.html"

    # queryset = Listing.objects.filter(is_active=True)
    # Template name listing_list.html
    # object_list variable name

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


class AdminBlogAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Blog
    fields = ['title', 'image', 'youtube_embed_link', 'meta_title', 'meta_description', 'description', 'short_description', 'is_vnv',
              'is_active']
    template_name = "listing_analytics/blog_add_update_admin.html"

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.user = self.request.user
        listing.save()
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff is True


# Update Listings
class AdminBlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'image', 'youtube_embed_link', 'meta_title', 'meta_description', 'description', 'short_description', 'is_vnv',
              'is_active']
    template_name = "listing_analytics/blog_add_update_admin.html"

    # template name listing_form

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


# Delete Listings
class AdminBlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    fields = ['title', 'image', 'youtube_embed_link', 'meta_title', 'meta_description', 'description', 'short_description', 'is_vnv',
              'is_active']
    success_url = '/listing_analytics/listing/blog-list-admin/'
    template_name = "listing_analytics/blog_confirm_delete.html"

    def test_func(self):
        return self.request.user.is_staff is True


# Show all Review List
class AdminReviewListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ListingReview
    paginate_by = 20
    template_name = "listing_analytics/review_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = ListingReview.objects.all()
        category_filter = ListingReviewFilter(self.request.GET, queryset=current_query)
        context['filter'] = category_filter
        if len(category_filter.qs) != len(current_query):
            context['object_list'] = category_filter.qs
            if len(category_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def test_func(self):
        return self.request.user.is_staff is True


# Update Review
class AdminReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ListingReview
    fields = ['user', 'review_description', 'rating', 'is_approved']
    template_name = "listing_analytics/review_update.html"
    success_url = '/listing_analytics/listing/review/list-admin/'

    def test_func(self):
        return self.request.user.is_staff is True


# Delete Review
class AdminReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ListingReview
    success_url = '/listing_analytics/listing/review/list-admin/'
    template_name = "listing_analytics/review_confirm_delete.html"

    def test_func(self):
        return self.request.user.is_staff is True


# Location
# Show all Location
class AdminListingLocationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ListingLocation
    paginate_by = 20
    template_name = "listing_analytics/listing_location_list_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = ListingLocation.objects.all()
        category_filter = ListingLocationFilter(self.request.GET, queryset=current_query)
        context['filter'] = category_filter
        if len(category_filter.qs) != len(current_query):
            context['object_list'] = category_filter.qs
            if len(category_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


class AdminListingLocationAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ListingLocation
    fields = ['title', 'image']
    template_name = "listing_analytics/listing_location_add_update_admin.html"

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff is True


class AdminListingLocationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ListingLocation
    fields = ['title', 'image', 'is_active']
    template_name = "listing_analytics/listing_location_add_update_admin.html"

    def test_func(self):
        return self.request.user.is_staff is True


class AdminListingLocationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ListingLocation
    fields = ['title', 'image', 'is_active']
    success_url = '/listing_analytics/listing/location/list-admin/'
    template_name = "listing_analytics/listing_location_confirm_delete.html"

    def test_func(self):
        return self.request.user.is_staff is True


# Sub Location
class AdminListingSubLocationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = SubListingLocation
    paginate_by = 20
    template_name = "listing_analytics/listing_sub_location_list_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = ListingLocation.objects.all()
        category_filter = ListingLocationFilter(self.request.GET, queryset=current_query)
        context['filter'] = category_filter
        if len(category_filter.qs) != len(current_query):
            context['object_list'] = category_filter.qs
            if len(category_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


class AdminListingSubLocationAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = SubListingLocation
    fields = ['title', 'listing_location', 'image']
    template_name = "listing_analytics/listing_sub_location_add_update_admin.html"

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff is True


class AdminListingSubLocationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SubListingLocation
    fields = ['title', 'listing_location', 'image', 'is_active']
    template_name = "listing_analytics/listing_sub_location_add_update_admin.html"

    def test_func(self):
        return self.request.user.is_staff is True


class AdminListingSubLocationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SubListingLocation
    fields = ['title', 'listing_location', 'image', 'is_active']
    success_url = '/listing_analytics/listing/sub-location/list-admin/'
    template_name = "listing_analytics/listing_sub_location_confirm_delete.html"

    def test_func(self):
        return self.request.user.is_staff is True


# Category
# Show all Category
class AdminCategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ListingCategory
    paginate_by = 20
    # Template name category_list_admin.html
    # object_list variable name
    template_name = "listing_analytics/listing_category_list_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = ListingCategory.objects.all()
        category_filter = CategoryFilter(self.request.GET, queryset=current_query)
        context['filter'] = category_filter
        if len(category_filter.qs) != len(current_query):
            context['object_list'] = category_filter.qs
            if len(category_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


# Add Category
class AdminCategoryAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ListingCategory
    fields = ['title', 'parent_category', 'description', 'image']
    template_name = "listing_analytics/listing_category_add_update_admin.html"

    # template name category_form

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


# Update Category
class AdminCategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ListingCategory
    fields = ['title', 'parent_category', 'description', 'image', 'is_active']
    template_name = "listing_analytics/listing_category_add_update_admin.html"

    # template name category_form

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


# Delete Category
class AdminCategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ListingCategory
    fields = ['title', 'parent_category', 'description', 'image', 'is_active']
    success_url = 'admin-listing-category-list'
    template_name = "listing_analytics/listing_category_confirm_delete.html"

    # template name category_confirm_delete.html
    # TODO Pass form button and heading data

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


# Show all ParentCategory
class AdminParentCategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ParentListingCategory
    paginate_by = 20
    # Template name category_list_admin.html
    # object_list variable name
    template_name = "listing_analytics/listing_parent_category_list_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = ParentListingCategory.objects.all()
        category_filter = ParentCategoryFilter(self.request.GET, queryset=current_query)
        context['filter'] = category_filter
        if len(category_filter.qs) != len(current_query):
            context['object_list'] = category_filter.qs
            if len(category_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


# Add Category
class AdminParentCategoryAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ParentListingCategory
    fields = ['title', 'description', 'image']
    template_name = "listing_analytics/listing_parent_category_add_update_admin.html"

    # template name category_form

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


# Update Category
class AdminParentCategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ParentListingCategory
    fields = ['title', 'description', 'image', 'is_active']
    template_name = "listing_analytics/listing_parent_category_add_update_admin.html"

    # template name category_form
    # TODO Pass form button and heading data

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


# Delete Category
class AdminParentCategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ParentListingCategory
    fields = ['title', 'description', 'image', 'is_active']
    success_url = 'admin-listing-parent-category-list'
    template_name = "listing_analytics/listing_parent_category_confirm_delete.html"

    # template name category_confirm_delete.html
    # TODO Pass form button and heading data

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


class AdminContactListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ListingContact
    paginate_by = 20
    template_name = "listing_analytics/listing_contact_list_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = ListingContact.objects.all()
        category_filter = ContactFilter(self.request.GET, queryset=current_query)
        context['filter'] = category_filter
        if len(category_filter.qs) != len(current_query):
            context['object_list'] = category_filter.qs
            if len(category_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


class AdminContactUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ListingContact
    fields = ['name', 'email', 'mobile', 'description']
    template_name = "listing_analytics/listing_contact_update_admin.html"

    # template name category_form
    # TODO Pass form button and heading data

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True



class AdminDraftListingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = DraftListing
    paginate_by = 20
    template_name = "listing_analytics/draftlisting_list_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = DraftListing.objects.all()
        listing_filter = DraftListingFilter(self.request.GET, queryset=current_query)

        context['filter'] = listing_filter
        if len(listing_filter.qs) != len(current_query):
            context['object_list'] = listing_filter.qs
            if len(listing_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    # List out only those list which are not approved yet!
    def get_queryset(self):
        qs = self.model.objects.filter(is_approved=False, is_declined=False)
        vendors = Vendor.objects.all()
        listing_present = []
        for vendor in vendors:
            if vendor.draft_listing:
                listing_present.append(vendor.draft_listing.id)
        new_listing_list = []
        for listing in qs:
            if listing.id in listing_present:
                new_listing_list.append(listing)
        return new_listing_list

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


# DraftListing DetailView

class AdminDraftListingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = DraftListing
    template_name = 'listing_analytics/draft_listing_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AdminDraftListingDetailView, self).get_context_data(**kwargs)
        listing = self.get_object()
        vendor = Vendor.objects.filter(draft_listing=listing).last()
        if vendor:
            instagram_token = VendorInstagramToken.objects.filter(vendor=vendor).first()
            if instagram_token:
                token_json = instagram_token.token
                token = json.loads(token_json)
                url = reverse('vendor-instagram-connect')
                url = self.request.build_absolute_uri(url)
                instagram_basic_display = InstagramBasicDisplay(app_id='549315439403500',
                                                                app_secret='0c3fd79c822b212973bbd2f63d523137',
                                                                redirect_url='https://vowsnviews.com/auth/')
                instagram_basic_display.set_access_token(token['access_token'])
                profile = instagram_basic_display.get_user_profile()
                media = instagram_basic_display.get_user_media()
                media_data = media['data']
                media_urls = []
                video_urls = []
                for data in media_data:
                    if data['media_type'] == "IMAGE":
                        media_urls.append(data['media_url'])
                    elif data['media_type'] == "VIDEO":
                        video_urls.append(data['media_url'])
                context['media_urls'] = media_urls  # it has urls of all media from instagram in the list
                context['video_urls'] = video_urls
        context['vendor'] = vendor        
        return context

    def test_func(self, *args, **kwargs):
        listing = DraftListing.objects.filter(id=kwargs.get('pk'))
        vendor = Vendor.objects.filter(vendor_user=self.request.user, draft_listing=listing).first
        if vendor or self.request.user.is_staff:
            return True
        return False


class AdminListingApproveView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = DraftListing

    def post(self, *args, **kwargs):
        draft_listing = self.model.objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        vendor = Vendor.objects.get(draft_listing=draft_listing)
        old_listing = Listing.objects.filter(slug=draft_listing.slug).first()
        
        if draft_listing.is_update:
            if old_listing:
                old_listing.delete()
                
            listing = Listing()
            for field in draft_listing._meta.fields:
                setattr(listing, field.name, getattr(draft_listing, field.name))
            listing.save()
            vendor.listing = listing
            vendor.save()
        else:
            listing = Listing()
            for field in draft_listing._meta.fields:
                setattr(listing, field.name, getattr(draft_listing, field.name))
            listing.save()
            vendor.listing = listing
            vendor.save()
        
        area = draft_listing.area.all()
        if area:
            for item in area:
                single_area = Area.objects.get(id=item.id)
                listing.area.add(single_area)
                
        # Rest of the code...
        
        draft_listing.is_approved = True
        draft_listing.is_update = False
        draft_listing.save()
        listing.save()
        
        messages.success(self.request, "Listing Approved Successfully")
        return redirect('admin-draft-listing-list')

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


class AdminListingDeclineView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = DraftListing

    def post(self, request, *args, **kwargs):
        draft_listing = self.model.objects.get(id=self.kwargs.get('pk'))
        decline_reason = request.POST.get('reason', None)
        if decline_reason:
            draft_listing.decline_reason = decline_reason
            draft_listing.is_declined = True
            draft_listing.save()
            messages.success(self.request, "Listing Declined Successfully")
            return redirect('admin-draft-listing-list')
        messages.warning(self.request, "Please, specify the reason for decline the list")
        return redirect('admin-draft-listing-list')

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


# Decline Listing List View
class AdminDeclineListingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = DraftListing
    paginate_by = 20
    template_name = "listing_analytics/dummy_draft_listing.html"

    # List out only those list which are decline.
    def get_queryset(self):
        qs = self.model.objects.filter(is_declined=True)
        return qs

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True


# Add place id for google review
class AdminAddListingPlaceId(LoginRequiredMixin, UserPassesTestMixin, View):

    def post(self, request, *args, **kwargs):
        listing = Listing.objects.get(id=self.kwargs.get('pk'))
        place_id = request.POST.get('place_id')
        listing.place_id = place_id
        listing.save()
        messages.success(self.request, "Place Id for Listing added.")
        return redirect('admin-listing-list')

    def test_func(self):  # Giving only staff the permission to add Category
        return self.request.user.is_staff is True
        
        
class LandingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Landing
    paginate_by = 40
    # Template name category_list_admin.html
    # object_list variable name
    template_name = "listing_analytics/landing_list.html"


    def test_func(self):
        return self.request.user.is_superuser is True
        
        
class LandingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Landing
    success_url = '/listing_analytics/landing/list/'
    template_name = "analytics/parent_category_confirm_delete.html"

    def test_func(self):
        return self.request.user.is_superuser is True