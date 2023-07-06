from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import View
from django.shortcuts import redirect, render, reverse
from django.contrib import messages
from .filters import ListingFilter
from .forms import ListingReviewForm, ListingContactForm
from .models import (
    Listing, ListingReview, ListingFavorite, SubListingLocation, ListingCategory, ListingLocation
)
from users.models import User, UserLocation
from django.core.mail import EmailMessage
from django.conf import settings
# from geopy.geocoders import Nominatim
from .models import LABEL_CHOICES
from vendors.models import VendorInstagramToken
from users.models import Vendor
from django.contrib.auth.decorators import login_required
from instagram_basic_display.InstagramBasicDisplay import InstagramBasicDisplay
from vowsnviews.local_settings import Instagram_Secret_Key, Instagram_App_Id
import json
from django.conf import settings
import requests


def get_order_listing(request, object_list):
    filter_listing = []
    # listing = []
    LABEL_CHOICES = ['Elite', 'In Demand',
                     'Our Recommendation',
                     'Most Booked',
                     'Trending',
                     'Popular',
                     'Best Deal',
                     'Best Offer',
                     'without_label']
    listing_with_filter = {
        'city_listing': {item: {'is_verified': [], 'normal': []} for item in LABEL_CHOICES},
        'district_listing': {item: {'is_verified': [], 'normal': []} for item in LABEL_CHOICES},
        'state_listing': {item: {'is_verified': [], 'normal': []} for item in LABEL_CHOICES},
        'non_imp_listing': {item: {'is_verified': [], 'normal': []} for item in LABEL_CHOICES}
    }

    if 'latitude' and 'longitude' in request.session:
        lat = request.session.get('latitude')
        long = request.session.get('longitude')
        user = request.user if request.user.is_authenticated else None
        if not user:
            session_key = request.session.session_key
            user_location = UserLocation.objects.filter(session_key=session_key).last()
        else:
            user_location = UserLocation.objects.filter(user=user).last()

        city = None
        district = None
        state = None

        if user_location:
            city = user_location.city
            district = user_location.district
            state = user_location.state
        city_listing_location = ListingLocation.objects.filter(title=city).first()
        district_listing_location =ListingLocation.objects.filter(title=district).first() if not city == district else None
        state_listing_location = ListingLocation.objects.filter(title=state).first() if not state == district or not state == city else None
        if city_listing_location:
            listing = Listing.objects.filter(location=city_listing_location)
            for item in listing:
                filter_listing.append(item)
                if item.label:
                    if item.is_verified:
                        listing_with_filter['city_listing'][item.label]['is_verified'].append(item)
                    else:
                        listing_with_filter['city_listing'][item.label]['normal'].append(item)
                else:
                    if item.is_verified:
                        listing_with_filter['city_listing']['without_label']['is_verified'].append(item)
                    else:
                        listing_with_filter['city_listing']['without_label']['normal'].append(item)
        if district_listing_location:
            listing = Listing.objects.filter(location=district_listing_location)
            for item in listing:
                if filter_listing:
                    if not item in filter_listing:
                        filter_listing.append(item)
                else:
                    filter_listing.append(item)
                if item.label:
                    if item.is_verified:
                        listing_with_filter['district_listing'][item.label]['is_verified'].append(item)
                    else:
                        listing_with_filter['district_listing'][item.label]['normal'].append(item)
                else:
                    if item.is_verified:
                        listing_with_filter['district_listing']['without_label']['is_verified'].append(item)
                    else:
                        listing_with_filter['district_listing']['without_label']['normal'].append(item)

        if state_listing_location:
            listing = Listing.objects.filter(location=state_listing_location)
            for item in listing:
                if filter_listing:
                    if not item in filter_listing:
                        filter_listing.append(item)
                else:
                    filter_listing.append(item)
                if item.label:
                    if item.is_verified:
                        listing_with_filter['state_listing'][item.label]['is_verified'].append(item)
                    else:
                        listing_with_filter['state_listing'][item.label]['normal'].append(item)
                else:
                    if item.is_verified:
                        listing_with_filter['state_listing']['without_label']['is_verified'].append(item)
                    else:
                        listing_with_filter['state_listing']['without_label']['normal'].append(item)

    if not filter_listing:
        filter_listing = object_list
        filter_listing = []
    for item in object_list:
        if not item in filter_listing:
            filter_listing.append(item)
            if item.label:
                if item.is_verified:
                    listing_with_filter['non_imp_listing'][item.label]['is_verified'].append(item)
                else:
                    listing_with_filter['non_imp_listing'][item.label]['normal'].append(item)
            else:
                if item.is_verified:
                    listing_with_filter['non_imp_listing']['without_label']['is_verified'].append(item)
                else:
                    listing_with_filter['non_imp_listing']['without_label']['normal'].append(item)
    filter_listing = []
    new_listing = list()
    for key, value in listing_with_filter.items():
        for key, value in value.items():
            for key, value in value.items():
                for item in value:
                    if item in object_list:
                        filter_listing.append(item)
    return filter_listing


# Listings
# Show all Listings
class ListingListView(ListView):
    model = Listing
    paginate_by = 39
    template_name = 'listing/listing_list.html'

    # queryset = Listing.objects.filter(is_active=True)
    # Template name listing_list.html
    # object_list variable name

    def get_queryset(self,*args, **kwargs):
        object_list = Listing.objects.filter(is_active=True)
        object_list = get_order_listing(self.request, object_list)
        print(self.request.GET)
        # listing_filter = ListingFilter(self.request.GET, queryset=object_list)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = Listing.objects.filter(is_active=True)
        listing_filter = ListingFilter(self.request.GET, queryset=current_query)
        print(self.request.GET)
        context['filter'] = listing_filter
        print("FIlter query", listing_filter.qs)
        if len(listing_filter.qs) != len(current_query):
            context['object_list'] = listing_filter.qs
            if len(listing_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        context['object_list'] = get_order_listing(self.request, listing_filter.qs)
        sub_locations = SubListingLocation.objects.all()
        sub_category = ListingCategory.objects.all()
        context['sub_locations'] = sub_locations
        context['sub_categorys'] = sub_category

        # if 'latitude' and 'longitude' in self.request.session:
        #     lat = self.request.session.get('latitude')
        #     long = self.request.session.get('longitude')
        #     geolocator = Nominatim(user_agent="vowsnviews")
        #     location = geolocator.reverse(str(lat) + "," + str(long))
        #     context['location'] = location
        return context


class ListingDetailView(View):
    def get(self, *args, **kwargs):
        context = {}
        review = None

        listing = Listing.objects.get(id=self.kwargs.get('pk'))
        if not listing.is_active:
            return redirect('listing-list-view')
        # Faq for listing item
        context['faq'] = listing.get_faq()
        if self.request.user.is_authenticated:
            len_wishlist = ListingFavorite.objects.filter(user=self.request.user).count()
            review = listing.review.filter(user=self.request.user, is_approved=True)

            context['review_count'] = review.count()
            context['len_wishlist'] = len_wishlist

        reviews = listing.review.filter(is_approved=True)
        if reviews:
            review_rating_list = [float(review.rating) for review in reviews]  # list of review's rating
            review_rating_total = sum(review_rating_list)  # total of review rating
            average_review = review_rating_total / review.count()

            context['average_review'] = round(average_review * 2) / 2  # Round to nearest .5
            context['int_average_review'] = int(context['average_review'])  # Making it int
            context['reviews'] = reviews
        context['review_form'] = ListingReviewForm()
        context['reviewed'] = 'False'

        if review:
            context['reviewed'] = 'True'

        context['object'] = listing
        context['similar_listing'] = Listing.objects.filter(category=listing.category)
        context['form'] = ListingContactForm()
        context['photo_list'] = Listing.objects.all()


        # Media from Instagram
        vendor = Vendor.objects.filter(listing=listing).last()
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
                while len(media_urls) < 30 or len(video_urls) < 30:
                    print(len(media_urls), len(video_urls))
                    if len(media_urls) > 30 or len(video_urls) > 30:
                        break
                    for data in media['data']:
                        if data['media_type'] == "IMAGE":
                            media_urls.append(data['media_url'])
                        elif data['media_type'] == "VIDEO":
                            video_urls.append(data['media_url'])
                    media = instagram_basic_display.pagination(media)
                    if not media:
                        break
                context['media_urls'] = media_urls  # it has urls of all media from instagram in the list
                context['video_urls'] = video_urls
        context['vendor'] = vendor
        return render(self.request, 'listing/listing_detail_v2 -2.html', context)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            review_form = ListingReviewForm(self.request.POST)
            if review_form.is_valid():
                form = review_form.save(commit=False)
                form.user = self.request.user
                form.save()


                listing = Listing.objects.get(id=self.kwargs.get('pk'))
                listing.review.add(form)
                listing.save()
                messages.success(self.request, "Review Posted!")
                return redirect('listing-detail-view', pk=self.kwargs.get('pk'))
            form = ListingContactForm(self.request.POST)
            if form.is_valid():
                contact = form.instance
                phone_number = contact.mobile
                if len(str(phone_number)) != 10:
                    messages.warning(self.request, 'Invalid mobile number')
                    return redirect('listing-detail-view', pk=self.kwargs.get('pk'))
                listing = Listing.objects.get(id=self.kwargs.get('pk'))
                contact.listing = listing
                contact.save()
                request_call = self.request.POST.get("request_call")
                if request_call == "Yes":
                    contact.request_call = True
                    contact.save()
                messages.success(self.request, 'Message sent, we will contact you soon!')
                send_inquiry_mail(self.request, listing.get_vendor(), contact.description)
                return redirect('listing-detail-view', pk=self.kwargs.get('pk'))
            messages.warning(self.request, 'Please enter valid data!')
            return redirect('listing-detail-view', pk=self.kwargs.get('pk'))
        else:
            messages.warning(self.request, 'Please login to post review!')
            return redirect(f'/user/login/?next=detail/{self.kwargs.get("pk")}/')
            

class ListingInDetailView(View):
    def get(self, *args, **kwargs):
        context = {}
        review = None

        listing = Listing.objects.get(id=self.kwargs.get('pk'))
        if not listing.is_active:
            return redirect('listing-list-view')
        # Faq for listing item
        context['faq'] = listing.get_faq()
        if self.request.user.is_authenticated:
            len_wishlist = ListingFavorite.objects.filter(user=self.request.user).count()
            review = listing.review.filter(user=self.request.user, is_approved=True)

            context['review_count'] = review.count()
            context['len_wishlist'] = len_wishlist

        reviews = listing.review.filter(is_approved=True)
        if reviews:
            review_rating_list = [float(review.rating) for review in reviews]  # list of review's rating
            review_rating_total = sum(review_rating_list)  # total of review rating
            average_review = review_rating_total / review.count()

            context['average_review'] = round(average_review * 2) / 2  # Round to nearest .5
            context['int_average_review'] = int(context['average_review'])  # Making it int
            context['reviews'] = reviews
        context['review_form'] = ListingReviewForm()
        context['reviewed'] = 'False'

        if review:
            context['reviewed'] = 'True'

        context['object'] = listing
        context['similar_listing'] = Listing.objects.filter(category=listing.category)
        context['form'] = ListingContactForm()
        context['photo_list'] = Listing.objects.all()


        # Media from Instagram
        vendor = Vendor.objects.filter(listing=listing).last()
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
                while len(media_urls) < 30 or len(video_urls) < 30:
                    for data in media['data']:
                        if data['media_type'] == "IMAGE":
                            media_urls.append(data['media_url'])
                        elif data['media_type'] == "VIDEO":
                            video_urls.append(data['media_url'])
                    media = instagram_basic_display.pagination(media)
                    if not media:
                        break
                context['media_urls'] = media_urls  # it has urls of all media from instagram in the list
                context['video_urls'] = video_urls

        return render(self.request, 'listing/listing_detail_v2 -2.html', context)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            review_form = ListingReviewForm(self.request.POST)
            if review_form.is_valid():
                form = review_form.save(commit=False)
                form.user = self.request.user
                form.save()


                listing = Listing.objects.get(id=self.kwargs.get('pk'))
                listing.review.add(form)
                listing.save()
                messages.success(self.request, "Review Posted!")
                return redirect('listing-detail-view', pk=self.kwargs.get('pk'))
            form = ListingContactForm(self.request.POST)
            if form.is_valid():
                contact = form.instance
                phone_number = contact.mobile
                if len(str(phone_number)) != 10:
                    messages.warning(self.request, 'Invalid mobile number')
                    return redirect('listing-detail-view', pk=self.kwargs.get('pk'))
                listing = Listing.objects.get(id=self.kwargs.get('pk'))
                contact.listing = listing
                contact.save()
                request_call = self.request.POST.get("request_call")
                if request_call == "Yes":
                    contact.request_call = True
                    contact.save()
                messages.success(self.request, 'Message sent you will be contact soon!')
                send_inquiry_mail(self.request, listing.get_vendor(), contact.description)
                return redirect('listing-detail-view', pk=self.kwargs.get('pk'))
            messages.warning(self.request, 'Please enter valid data!')
            return redirect('listing-detail-view', pk=self.kwargs.get('pk'))
        else:
            messages.warning(self.request, 'Please login to post review!')
            return redirect(f'/user/login/?next=detail/{self.kwargs.get("pk")}/')


# Show all ListingFavorite
class ListingFavoriteListView(LoginRequiredMixin, ListView):
    model = ListingFavorite
    paginate_by = 10

    # object_list variable name

    def get_queryset(self):
        queryset = ListingFavorite.objects.filter(user=self.request.user)
        return queryset


class ListingFavoriteAddView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        listing = Listing.objects.filter(id=self.kwargs.get('pk')).first()
        if not listing:
            messages.warning(self.request, "Listing not exist!")
            return redirect('listing-list-view')
        if listing.is_active:
            fav_item = ListingFavorite.objects.filter(user=self.request.user, listing=listing).first()
            if not fav_item:
                ListingFavorite.objects.create(user=self.request.user, listing=listing)
                messages.success(self.request, "Listing added to wishlist!")
                return redirect('listing-detail-view', pk=listing.id)
            messages.success(self.request, "Listing already in wishlist!")
        return redirect('listing-detail-view', pk=listing.id)


class ListingFavoriteRemoveView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            ListingFavorite.objects.get(id=self.kwargs.get('pk')).delete()
            messages.success(self.request, "Listing removed from wishlist!")
        except:
            pass
        return redirect('listing-favorite-list')


class ReviewAddView(LoginRequiredMixin, CreateView):
    model = ListingReview
    fields = ['review_description', 'rating']

    # template name review_form.html
    # TODO Pass form button and heading data
    # TODO add pytest_tests case

    def post(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = self.request.user
        listing = Listing.objects.filter(id=pk).first()
        if not listing:
            messages.warning(self.request, "Sorry, Listing not Exist.")
            return redirect('listing-list-view')
        review = ListingReview.objects.filter(
            user=user).filter(listing=listing).first()
        if not review:
            review = ListingReview(user=user)
            review.review_description = self.request.POST.get('review_description')
            review.rating = self.request.POST.get('rating')
            review.save()
            listing.review.add(review)
            listing.save()
            messages.success(self.request, "Review Added Successfully.")
            return redirect('listing-detail-view', pk=pk)
        messages.warning(self.request, "Sorry, Review already Exist.")
        return redirect('listing-detail-view', pk=pk)

    # def form_valid(self, form):
    #     review = form.instance
    #     review.user = self.request.user
    #     review.save()
    #
    #     listing = Listing.objects.get(id=self.kwargs.get('pk'))
    #     listing.review.add(review)
    #     listing.save()
    #     # return super().form_valid(form)
    #     return redirect('listing-detail-view', pk=self.kwargs.get('pk'))

    # def test_func(self):
    #     return self.request.user.is_staff is True


# Update Review
class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ListingReview
    fields = ['review_description', 'rating']

    # template name review_form

    def test_func(self):
        model = self.get_object()
        return self.request.user == model.user


# Delete Review
class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ListingReview
    fields = ['review_description', 'rating']
    success_url = '/'

    # template name review_confirm_delete.html

    def test_func(self):
        model = self.get_object()
        return self.request.user == model.user


def send_inquiry_mail(request, vendor, message):
    if vendor:
        user = vendor.vendor_user
    else:
        user = User.objects.filter(is_superuser=True, is_active=True, is_verified=True).last()
    if user:
        email = EmailMessage(
            f'Inquiry',
            message,
            settings.AUTH_USER_MODEL,
            [user.email, settings.EMAIL_HOST_USER],
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)



