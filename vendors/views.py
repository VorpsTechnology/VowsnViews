import datetime
from datetime import date

import requests
from django.shortcuts import render, reverse, redirect
from django.views import View
from django.views.generic.edit import FormView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from listing.models import (Listing, ParentListingCategory, ListingCategory, DraftListing,
                            Area, AddititionalPricing, ListingContact, ListingLocation, SubListingLocation,
                            ListingPhoto, ListingVideo, ListingOffer
                            )
from users.models import Vendor
from .models import (VenueFAQ, BridalWearFAQ, GroomWearFAQ, MakeupFAQ, PhotographerFAQ,
                     DecorFAQ, InvitationFAQ, GiftsFAQ, VendorInstagramToken
                     )
from .forms import (ListingForm, AreaForm, AdditionalPricingForm, VenueListingForm,
                    VenueFAQForm, BridalWearFAQForm, GroomWearFAQForm, MakeupFAQForm,
                    PhotographerFAQForm, DecorFAQForm, InvitationFAQForm, GiftsFAQForm, ListingOfferForm
                    )

from instagram_basic_display.InstagramBasicDisplay import InstagramBasicDisplay
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
import json
from datetime import date
from itertools import zip_longest
from vowsnviews.local_settings import Instagram_App_Id, Instagram_Secret_Key
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from facepy import SignedRequest


class IsVendor:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active and request.user.is_vendor:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def is_listing_assign(request):
    user = request.user
    vendor = Vendor.objects.get(vendor_user=user)
    return vendor.is_listing_on


class IsListingNotAssign:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        vendor = Vendor.objects.get(vendor_user=user)
        if vendor.is_listing_on:
            return redirect('vendor-home')
        else:
            return super().dispatch(request, *args, **kwargs)


# Redirect to add liting view if not one
class IsListingPresent:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        vendor = Vendor.objects.get(vendor_user=user)
        if vendor.get_listing():
            return super().dispatch(request, *args, **kwargs)
        if not vendor.is_listing_on:
            return redirect('add-listing')
        else:
            return super().dispatch(request, *args, **kwargs)


def is_instagram_connect(request):
    user = request.user
    vendor = Vendor.objects.get(vendor_user=user)
    vendor_token = VendorInstagramToken.objects.filter(vendor=vendor).first()
    if vendor_token:
        return vendor_token
    return False


class VendorHomeView(LoginRequiredMixin, IsVendor, IsListingPresent, View):
    model = Vendor

    template_name = 'vendors/vendor_home.html'

    def get(self, *args, **kwargs):
        context = {}
        user = self.request.user
        context['vendor'] = vendor = self.model.objects.get(vendor_user=user)
        context['object'] = vendor.get_listing()
        context['is_listing_assign'] = is_listing_assign(self.request)
        # Inquiry List of Customer
        context['inquiry_list'] = ListingContact.objects.filter(read=False, listing=vendor.listing)

        # For instagram Connect
        vendor_token = is_instagram_connect(self.request)
        if not vendor_token:
            url = 'https://hospitalsystemmanagement25.pythonanywhere.com/panel/dashboard.view/'
            view_url = reverse('vendor-instagram-connect')

            url = self.request.build_absolute_uri(url)  # full path of our app to redirect insta user
            instagram_basic_display = InstagramBasicDisplay(app_id='549315439403500',
                                                        app_secret='0c3fd79c822b212973bbd2f63d523137',
                                                        redirect_url='https://vowsnviews.com/auth/')
            print("Anikety url",instagram_basic_display.get_login_url())
            context['instagram_connect_url'] = instagram_basic_display.get_login_url()
        else:

            insta_obj = vendor_token
            if insta_obj.days_remaining() < 1:
                result = refreshInstagramToken(self.request, insta_obj.id)
                if result:
                    messages.success(self.request, "Instagram Token refreshed successfully")
                context['instagram_profile'] = insta_obj
        return render(self.request, self.template_name, context)


class VendorUpdateView(LoginRequiredMixin, IsVendor, IsListingPresent, SuccessMessageMixin, View):
    def post(self, request, *args, **kwargs):
        website_link = request.POST.get('website_link', None)
        name = request.POST.get('user_full_name', None)
        email = request.POST.get('email', None)
        phone_number = request.POST.get('phone_number', None)
        user = request.user
        vendor = Vendor.objects.filter(vendor_user=user).first()
        if vendor:
            if website_link:
                vendor.website_link = website_link
                vendor.save()
            if name:
                user.user_full_name = name
            if email:
                user.email = email
            if phone_number:
                user.phone_number = phone_number
            user.save()
            messages.success(request, "Profile updated successfully")
            return redirect('vendor-home')
        else:
            messages.warning(request, "Vendor not found")
            return redirect('home')


def parse_signed_request(signed_request):
    signed_data = SignedRequest.parse(signed_request, Instagram_Secret_Key)
    return signed_data

@method_decorator(csrf_exempt)
def deauthorize_callback(request):
    try:
        signed_request = request.POST.get('signed_request')
        signed_data = parse_signed_request(signed_request)

        user_id = signed_data['user_id']
        user_token = VendorInstagramToken.objects.filter(instagram_user_id=user_id).first()
        if user_token:
            confirmation_code = 200
        else:
            confirmation_code = 403
    except:
        confirmation_code = 403
    return JsonResponse({
        'confirmation_code': confirmation_code,
    })


@method_decorator(csrf_exempt)
def delete_instagram_data(request):
    try:
        signed_request = request.POST.get('signed_request')
        signed_data = parse_signed_request(signed_request)

        user_id = signed_data['user_id']
        user_token = VendorInstagramToken.objects.filter(instagram_user_id=user_id).first()
        if user_token:
            user_token.delete()
            confirmation_code = 200
        else:
            confirmation_code = 403
    except:
        confirmation_code = 403

    status_url = reverse('instagram-deletion-status', kwargs={'confirmation_code': confirmation_code})
    status_url = request.build_absolute_uri(status_url)
    return JsonResponse({
        'url': status_url,
        'confirmation_code': confirmation_code,
    })


class InstagramDataDeletionSuccessView(LoginRequiredMixin, IsVendor, IsListingPresent, IsListingNotAssign, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        vendor = Vendor.objects.filter(vendor_user=user).first()
        token = Vendor.objects.filter(vendor=vendor)
        context = {}
        if not token:
            context['status'] = "Your data is deleted successfully"
        else:
            context['status'] = "Your data is not deleted! please try again"
        return render(self.request, 'vendors/instagram_delete_status.html', context)


# This view is a for handling return url from instagram view
class InstagramConnectView(IsListingPresent, IsListingNotAssign, View):
    def get(self, *args, **kwargs):
        '''
        Api return url like this
        https://hospitalsystemmanagement25.pythonanywhere.com/panel/
        dashboard.view/?code=AQBShYmhYJg7f4Ewdpkf1I9iPmtEsqd2-rH4NQnFv8yq7gg9h4mm7
        NXhVw3wFnlTHLnD6UpxLFQrcHN7s7AkH1F8hDLxPc1Y5pDpTNPQl5svw38VVjtcLedurCv
        dNaN4m6NiajZCnFZUQhcmXILOGFSnBD2uAuG3tEdVBMxAdN3yKfkgfG5QSu7nDrs-C
        71FjItmhkiZWbGbmARFd74lBgv0lIo6nwqh6TdEfakASKbADQ#_
        '''
        instagram_basic_display = InstagramBasicDisplay(app_id='549315439403500',
                                                        app_secret='0c3fd79c822b212973bbd2f63d523137',
                                                        redirect_url='https://vowsnviews.com/auth/')

        code = self.request.GET.get('code', None)
        if code:
            short_token = instagram_basic_display.get_o_auth_token(code)
            '''
            get_o_auth_toekn return dict object like 
            {'access_token': 'IGQVJXZA3BCdkVOU0htSFlxbkE4cnY5QVdzUExHNkljanZAPelgxbzlod1p1MnR5dFZAndDFDRFRkSGRPVlBJMXRLYVBVWlBnbGJUWEZAKLWRZAZAUdfeWxqTjBteHp1M1NOR0tyMmp1NzJDcG1OMEg3UWJQeV
            puaGxqRTVhaW5F', 'user_id': 17841446045166165}
            '''
            instagram_user_id = short_token.get('user_id')
            long_token = instagram_basic_display.get_long_lived_token(short_token.get('access_token'))
            long_token = json.dumps(long_token)
            user = self.request.user
            vendor = Vendor.objects.get(vendor_user=user)
            '''
            Save token receive from api for future use
            '''
            vendor_token = VendorInstagramToken(vendor=vendor, token=long_token)
            vendor_token.date_added = date.today()
            vendor_token.instagram_user_id = instagram_user_id
            vendor_token.save()
            messages.success(self.request, "Your instagram Account Added Successfully")
            return redirect('instagram-portfolio')
        else:
            raise HttpResponseBadRequest


def refreshInstagramToken(request, id):
    obj = VendorInstagramToken.objects.get(id=id)
    token_json = obj.token
    token = json.loads(token_json)
    access_token = token.access_token
    url = reverse('vendor-instagram-connect')
    url = request.build_absolute_uri(url)
    instagram_basic_display = InstagramBasicDisplay(app_id='549315439403500',
                                                        app_secret='0c3fd79c822b212973bbd2f63d523137',
                                                        redirect_url='https://vowsnviews.com/auth/')
    token = instagram_basic_display.refresh_token(access_token)
    token_json = json.dumps(token)
    obj.token = token_json
    obj.date_added = date.today()
    return True


class InstagramDisconnectView(LoginRequiredMixin, IsVendor, IsListingPresent, IsListingNotAssign, View):
    def get(self, *args, **kwargs):
        vendor = Vendor.objects.get(vendor_user=self.request.user)
        vendor_token = VendorInstagramToken.objects.filter(vendor=vendor).first()
        if vendor_token:
            vendor_token.delete()
            messages.success(self.request, "Instagram Disconnect Successfully.")
        else:
            messages.warning(self.request, "Sorry! Instagram Not connected yet.")
        return redirect('instagram-portfolio')


class VendorInstagram(View):
    def get(self, *args, **kwargs):
        vendor_id = self.kwargs.get('pk')
        redirect_url = self.request.META.get('HTTP_REFERER')
        vendor = Vendor.objects.filter(id=vendor_id).last()
        if not vendor:
            messages.warning(self.request, "Vendor not found")
            if redirect_url:
                return redirect(redirect_url)
            return redirect('listing-list-view')
        instagram_token = VendorInstagramToken.objects.filter(vendor=vendor).first()
        context = {}
        if instagram_token:
            token_json = instagram_token.token
            token = json.loads(token_json)
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

        listing = vendor.draft_listing
        if listing:
            context['photos'] = listing.photos.all()
            context['videos'] = listing.videos.all()
            context['object'] = vendor
        return render(self.request, 'vendors/instagram.html', context)


class VendorListingDetailView(LoginRequiredMixin, IsVendor, IsListingPresent, IsListingNotAssign, UserPassesTestMixin,DetailView):
    model = Listing
    template_name = 'vendors/list_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def test_func(self):
        user = self.request.user
        vendor = Vendor.objects.filter(vendor_user = user).first()
        listing = self.get_object()
        if not vendor.listing == listing:
            return False
        return True



class ListingAddView(LoginRequiredMixin, IsVendor, IsListingNotAssign, View):
    context = {}

    def get(self, *args, **kwargs):
        user = self.request.user
        vendor = Vendor.objects.get(vendor_user=user)
        if vendor.get_listing():
            return redirect('vendor-home')
        listing_category = vendor.listing_parent_category
        if listing_category.title == "Venue":
            context = {}
            context['form'] = VenueListingForm(None)
            context['area_form'] = AreaForm(None)
            context['pricing_form'] = AdditionalPricingForm(None)
            '''
            Note: put one hidden field in both venue_listing & listing_add template
            <input type="hidden" name="form_name" value="VenueForm"> or
            <input type="hidden" name="form_name" value="ListingForm">
            '''
            return render(self.request, 'vendors/venue_listing_add.html', context)
        else:
            self.context['form'] = ListingForm(None)
            return render(self.request, 'vendors/listing_add_update.html', self.context)

    def post(self, *args, **kwargs):
        form_name = self.request.POST.get('form_name', None)
        user = self.request.user
        vendor = Vendor.objects.get(vendor_user=user)
        parent_category = ParentListingCategory.objects.get(title=vendor.listing_parent_category.title)
        listing_category = ListingCategory.objects.get(title=vendor.listing_sub_category.title)
        if form_name == 'VenueForm':
            draft_listing = VenueListingForm(self.request.POST, self.request.FILES)
            area_form = AreaForm(self.request.POST, self.request.FILES)
            pricing_form = AdditionalPricingForm(self.request.POST)
            if draft_listing.is_valid():
                listing_obj = draft_listing.instance
                listing_obj.category = listing_category
                listing_obj.parent_category = parent_category
                listing_obj.meta_title = listing_obj.title
                listing_obj.meta_description = listing_obj.short_description
                listing_obj.save()

                area_items = self.request.POST.getlist("area_data[]")
                pricing_items = self.request.POST.getlist("pricing_data[]")

                for item in area_items:
                    area = Area.objects.get(id=item)
                    listing_obj.area.add(area)
                    listing_obj.save()

                for item in pricing_items:
                    pricing = AddititionalPricing.objects.get(id=item)
                    listing_obj.additional_pricing.add(pricing)
                    listing_obj.save()

                listing_obj.save()
                vendor.draft_listing = listing_obj
                vendor.save()
                messages.success(self.request, "Listing Created Successfully")
                return redirect('faq-answers')
            else:
                context = {}
                context['form'] = VenueListingForm(self.request.POST, self.request.FILES)
                context['area_form'] = AreaForm(self.request.POST, self.request.FILES)
                context['pricing_form'] = AdditionalPricingForm(self.request.POST)
                '''
                Note: put one hidden field in both venue_listing & listing_add template
                <input type="hidden" name="form_name" value="VenueForm"> or
                <input type="hidden" name="form_name" value="ListingForm">
                '''
                return render(self.request, 'vendors/venue_listing_add.html', context)



        elif form_name == 'ListingForm':
            listing = ListingForm(self.request.POST, self.request.FILES)
            if listing.is_valid():
                listing_obj = listing.instance
                listing_obj.meta_title = listing_obj.title
                listing_obj.meta_description = listing_obj.short_description
                listing_obj.parent_category = parent_category
                listing_obj.category = listing_category
                listing_obj.save()
                vendor.draft_listing = listing_obj
                vendor.save()
                messages.success(self.request, "Listing Created Successfully")
                return redirect('vendor-home')
            else:
                messages.error(self.request, "Data is not valid")
                return redirect('add-listing')


class FAQAddView(LoginRequiredMixin, IsVendor, IsListingPresent, IsListingNotAssign, View):

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        vendor = Vendor.objects.get(vendor_user=user)
        if vendor.draft_listing:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.warning(self.request, "Please Add Listing before adding faq.")
            return redirect('add-listing')

    def get(self, request, *args, **kwargs):
        user = request.user
        vendor = Vendor.objects.get(vendor_user=user)
        listing = vendor.draft_listing
        if not listing.is_faq_answered:
            if listing.parent_category.title == "Venue":
                faq = VenueFAQ()
                form = VenueFAQForm(None)
                return render(self.request, 'vendors/venue_faq_add.html', {'faq': faq, 'form': form})
            elif listing.parent_category.title == "Bridal Wear":
                faq = BridalWearFAQ()
                form = BridalWearFAQForm(None)
                return render(self.request, 'vendors/bridal_faq_add.html', {'faq': faq, 'form': form})
            elif listing.parent_category.title == 'Groom Wear':
                faq = GroomWearFAQ()
                form = GroomWearFAQForm(None)
                return render(self.request, 'vendors/groom_faq_add.html', {'faq': faq, 'form': form})
            elif listing.parent_category.title == 'Makeup & Mehndi':
                faq = MakeupFAQ()
                form = MakeupFAQForm(None)
                return render(self.request, 'vendors/makeup_faq_add.html', {'faq': faq, 'form': form})
            elif listing.parent_category.title == 'Photographer':
                faq = PhotographerFAQ()
                form = PhotographerFAQForm(None)
                return render(self.request, 'vendors/photographer_faq_add.html', {'faq': faq, 'form': form})
            elif listing.parent_category.title == 'Planning & Decor':
                faq = DecorFAQ()
                form = DecorFAQForm(None)
                return render(self.request, 'vendors/planning_faq_add.html', {'faq': faq, 'form': form})
            elif listing.parent_category.title == 'Invites':
                faq = InvitationFAQ()
                form = InvitationFAQForm(None)
                return render(self.request, 'vendors/invites_faq_add.html', {'faq': faq, 'form': form})
            elif listing.parent_category.title == 'Gifts':
                faq = GiftsFAQ()
                form = GiftsFAQForm(None)
                return render(self.request, 'vendors/gifts_faq_add.html', {'faq': faq, 'form': form})
            else:
                messages.warning(self.request, "Listing not found")
                return redirect('add-listing')
        else:
            messages.warning(self.request, "FAQ already Answered")
            return redirect('vendor-home')

    def post(self, request, *args, **kwargs):
        user = request.user
        vendor = Vendor.objects.get(vendor_user=user)
        listing = vendor.draft_listing
        category = listing.parent_category.title
        if category == "Venue":
            form = VenueFAQForm(request.POST)
        elif category == "Bridal Wear":
            form = BridalWearFAQForm(request.POST)
        elif category == 'Groom Wear':
            form = GroomWearFAQForm(request.POST)
        elif category == 'Makeup & Mehndi':
            form = MakeupFAQForm(request.POST)
        elif category == 'Photographer':
            form = PhotographerFAQForm(request.POST)
        elif category == 'Planning & Decor':
            form = DecorFAQForm(request.POST)
        elif category == 'Invites':
            form = InvitationFAQForm(request.POST)
        elif category == 'Gifts':
            form = GiftsFAQForm(request.POST)
        else:
            form = VenueFAQForm(None)

        if form.is_valid():
            if id:

                draft_listing = vendor.draft_listing
                faq_object = form.save()
                faq_object.draft_listing = draft_listing
                if vendor.listing:
                    faq_object.listing = vendor.listing
                faq_object.save()
                draft_listing.is_faq_answered = True
                draft_listing.save()
                messages.success(self.request, "FAQ Added Successfully")
                if not is_instagram_connect(request):
                    return redirect('instagram-portfolio')
                return redirect('vendor-home')
            else:
                messages.error(self.request, "Error")
                return HttpResponseBadRequest
        else:
            messages.error(self.request, "Form not valid")
            return redirect('faq-answers')


class FAQUpdateView(LoginRequiredMixin, IsVendor, IsListingPresent, IsListingNotAssign, View):

    def get(self, *args, **kwargs):
        user = self.request.user
        vendor = Vendor.objects.get(vendor_user=user)
        listing = vendor.draft_listing
        category = listing.parent_category.title
        if category == "Venue":
            faq = VenueFAQ.objects.get(draft_listing=listing)
            form = VenueFAQForm(instance=faq)
            return render(self.request, 'vendors/venue_faq_add.html', {'faq': faq, 'form': form})

        elif category == "Bridal Wear":
            faq = BridalWearFAQ.objects.get(draft_listing=listing)
            form = BridalWearFAQForm(instance=faq)
            return render(self.request, 'vendors/bridal_faq_add.html', {'faq': faq, 'form': form})

        elif category == 'Groom Wear':
            faq = GroomWearFAQ.objects.get(draft_listing=listing)
            form = GroomWearFAQForm(instance=faq)
            return render(self.request, 'vendors/groom_faq_add.html', {'faq': faq, 'form': form})
        elif category == 'Makeup & Mehndi':
            faq = MakeupFAQ.objects.get(draft_listing=listing)
            form = MakeupFAQForm(instance=faq)
            return render(self.request, 'vendors/makeup_faq_add.html', {'faq': faq, 'form': form})

        elif category == 'Photographer':
            faq = PhotographerFAQ.objects.get(draft_listing=listing)
            form = PhotographerFAQForm(instance=faq)
            return render(self.request, 'vendors/photographer_faq_add.html', {'faq': faq, 'form': form})

        elif category == 'Planning & Decor':
            faq = DecorFAQ.objects.get(draft_listing=listing)
            form = DecorFAQForm(instance=faq)
            return render(self.request, 'vendors/planning_faq_add.html', {'faq': faq, 'form': form})

        elif category == 'Invites':
            faq = InvitationFAQ.objects.get(draft_listing=listing)
            form = InvitationFAQForm(instance=faq)
            return render(self.request, 'vendors/invites_faq_add.html', {'faq': faq, 'form': form})
        elif category == 'Gifts':
            faq = GiftsFAQ.objects.get(draft_listing=listing)
            form = GiftsFAQForm(instance=faq)
            return render(self.request, 'vendors/gifts_faq_add.html', {'faq': faq, 'form': form})
        else:
            messages.warning(self.request, "Lisitng not found")
            return redirect('vendor-home')

    def post(self, request, *args, **kwargs):
        user = request.user
        vendor = Vendor.objects.get(vendor_user=user)
        listing = vendor.draft_listing
        category = listing.parent_category.title
        if category == "Venue":
            form = VenueFAQForm(request.POST)
        elif category == "Bridal Wear":
            form = BridalWearFAQForm(request.POST)
        elif category == 'Groom Wear':
            form = GroomWearFAQForm(request.POST)
        elif category == 'Makeup & Mehndi':
            form = MakeupFAQForm(request.POST)
        elif category == 'Photographer':
            form = PhotographerFAQForm(request.POST)
        elif category == 'Planning & Decor':
            form = DecorFAQForm(request.POST)
        elif category == 'Invites':
            form = InvitationFAQForm(request.POST)
        elif category == 'Gifts':
            form = GiftsFAQForm(request.POST)
        else:
            form = VenueFAQForm(None)

        if form.is_valid():
            if id:
                draft_listing = vendor.draft_listing
                old_faq = draft_listing.get_faq()
                try:
                    old_faq.delete()
                except:
                    messages.warning(self.request, "FAQ not present, first add FAQ")
                    return redirect('faq-answers')
                faq_object = form.save()
                faq_object.draft_listing = draft_listing
                if vendor.listing:
                    faq_object.listing = vendor.listing
                faq_object.save()
                draft_listing.is_faq_answered = True
                draft_listing.save()
                messages.success(self.request, "FAQ Updated Successfully")
                return redirect('vendor-home')
            else:
                messages.error(self.request, "Error")
                return HttpResponseBadRequest
        else:
            messages.error(self.request, "Form not valid")
            return redirect('faq-update')


class AdditionalPricingCreateView(LoginRequiredMixin, IsVendor, IsListingPresent, IsListingNotAssign,
                                  SuccessMessageMixin, CreateView):
    model = AddititionalPricing
    form_class = AdditionalPricingForm
    template_name = 'vendors/form.html'
    success_message = 'Additional Pricing added successfully to your listing'

    def form_valid(self, form):
        pricing = form.instance
        pricing.save()
        draft_listing = DraftListing.objects.get(pk=self.kwargs.get('pk'))
        draft_listing.additional_pricing.add(pricing)
        draft_listing.is_update = True
        draft_listing.is_approved = False
        draft_listing.save()
        return redirect('vendor-home')


class VendorListingUpdateView(LoginRequiredMixin, IsVendor, IsListingPresent, IsListingNotAssign, SuccessMessageMixin,
                              View):

    def get(self, request, *args, **kwargs):
        user = request.user
        vendor = Vendor.objects.filter(vendor_user=user).first()
        context = {}
        draft_listing = vendor.draft_listing
        context['draft_listing'] = draft_listing
        if draft_listing:
            if draft_listing.parent_category.title == "Venue":
                area = draft_listing.area.all()
                additional_pricing = draft_listing.additional_pricing.all()
                context['area'] = area
                context['area_form'] = AreaForm(None)
                context['additional_pricing'] = additional_pricing
                context['listing'] = draft_listing
                context['form'] = VenueListingForm(instance=draft_listing)
                context['locations'] = ListingLocation.objects.all()
                context['sub_locations'] = SubListingLocation.objects.all()
                return render(self.request, 'vendors/venue_listing_update.html', context)
            else:
                listing = draft_listing
                context['listing'] = draft_listing
                context['form'] = ListingForm(instance=listing)
                return render(self.request, 'vendors/listing_add_update.html', context)
        else:
            messages.warning(self.request, "Listing not Found")
            return redirect('vendor-home')

    def post(self, request):
        user = request.user
        vendor = Vendor.objects.filter(vendor_user=user).first()
        draft_listing = vendor.draft_listing
        parent_category = vendor.listing_parent_category
        category = vendor.listing_sub_category
        context = {}
        old_is_approved = draft_listing.is_approved
        if vendor.listing_parent_category.title == "Venue":
            venue_form = VenueListingForm(request.POST, request.FILES)
            area_form = AreaForm(request.POST)
            pricing_form = AdditionalPricingForm(request.POST)
            if venue_form.is_valid():
                listing = listing_backup = draft_listing
                # area_list = listing.area.all()
                # for item in area_list:
                #     item.delete()
                # pricing_list = listing.additional_pricing.all()
                # for item in pricing_list:
                #     item.delete()
                listing.delete()
                venue_listing = venue_form.instance
                venue_listing.save()

                # Image
                image_main = request.FILES.get('image_main')
                image_2 = request.FILES.get('image_2')
                image_3 = request.FILES.get('image_3')
                image_4 = request.FILES.get('image_4')
                image_5 = request.FILES.get('image_5')

                image_main_clear = request.POST.get('image_main-clear', None)
                image_2_clear = request.POST.get('image_2-clear', None)
                image_3_clear = request.POST.get('image_3-clear', None)
                image_4_clear = request.POST.get('image_4-clear', None)
                image_5_clear = request.POST.get('image_5-clear', None)

                if image_main is None:
                    venue_listing.image_main = listing_backup.image_main
                if image_2 is None:
                    venue_listing.image_2 = listing_backup.image_2
                if image_3 is None:
                    venue_listing.image_3 = listing_backup.image_3
                if image_4 is None:
                    venue_listing.image_4 = listing_backup.image_4
                if image_5 is None:
                    venue_listing.image_5 = listing_backup.image_5

                if image_main_clear == "on":
                    venue_listing.image_main = None
                if image_2_clear == "on":
                    venue_listing.image_2 = None
                if image_3_clear == "on":
                    venue_listing.image_3 = None
                if image_4_clear == "on":
                    venue_listing.image_4 = None
                if image_5_clear == "on":
                    venue_listing.image_5 = None

                venue_listing.parent_category = ParentListingCategory.objects.get(title='Venue')

                area_items = self.request.POST.getlist("area_data[]")
                pricing_items = self.request.POST.getlist("pricing_data[]")

                for item in area_items:
                    area = Area.objects.get(id=item)
                    if area:
                        venue_listing.area.add(area)
                        venue_listing.save()

                for item in pricing_items:
                    pricing = AddititionalPricing.objects.get(id=item)
                    if pricing:
                        venue_listing.additional_pricing.add(pricing)
                        venue_listing.save()


                if old_is_approved:
                    venue_listing.is_approved = False
                    venue_listing.is_update = True
                    venue_listing.is_declined = False
                else:
                    venue_listing.is_declined = False

                venue_listing.parent_category = parent_category
                venue_listing.category = category
                venue_listing.save()
                vendor.draft_listing = venue_listing

                vendor.save()
                messages.success(request, "Listing Updated Successfully")
                return redirect('vendor-home')
            else:
                messages.error(self.request, "Listing Form is not valid")
                context['form'] = VenueListingForm(self.request.POST, self.request.FILES)
                context['area_form'] = AreaForm(self.request.POST, self.request.FILES)
                context['pricing_form'] = AdditionalPricingForm(self.request.POST)
                return render(self.request, 'vendors/venue_listing_update.html', context)
        else:
            listing_form = ListingForm(request.POST, request.FILES)
            if listing_form.is_valid():
                listing = vendor.draft_listing
                listing_backup = listing
                # Image field
                image_main = request.FILES.get('image_main')
                image_2 = request.FILES.get('image_2')
                image_3 = request.FILES.get('image_3')
                image_4 = request.FILES.get('image_4')
                image_5 = request.FILES.get('image_5')

                image_main_clear = request.POST.get('image_main-clear', None)
                image_2_clear = request.POST.get('image_2-clear', None)
                image_3_clear = request.POST.get('image_3-clear', None)
                image_4_clear = request.POST.get('image_4-clear', None)
                image_5_clear = request.POST.get('image_5-clear', None)

                listing.delete()
                listing = listing_form.instance
                if image_main is None:
                    listing.image_main = listing_backup.image_main
                if image_2 is None:
                    listing.image_2 = listing_backup.image_2
                if image_3 is None:
                    listing.image_3 = listing_backup.image_3
                if image_4 is None:
                    listing.image_4 = listing_backup.image_4
                if image_5 is None:
                    listing.image_5 = listing_backup.image_5

                if image_main_clear == "on":
                    listing.image_main = None
                if image_2_clear == "on":
                    listing.image_2 = None
                if image_3_clear == "on":
                    listing.image_3 = None
                if image_4_clear == "on":
                    listing.image_4 = None
                if image_5_clear == "on":
                    listing.image_5 = None
                listing.save()
                listing.is_approved = False
                listing.is_update = True
                listing.is_declined = False
                listing.parent_category = parent_category
                listing.category = category
                listing.save()
                vendor.draft_listing = listing
                vendor.save()
                messages.success(request, "Listing Updated Successfully")
                return redirect('vendor-home')
            else:
                return redirect('vendor-listing-update')


class VenueListingUpdate(LoginRequiredMixin, IsVendor, IsListingPresent, IsListingNotAssign, SuccessMessageMixin,
                         UpdateView):
    model = DraftListing
    fields = ('catering_policy', 'decor_policy', 'dj_policy')
    template_name = 'vendors/update.html'
    success_message = 'Listing Updated Successfully'

    def form_valid(self, form):
        draft_listing = form.instance
        if draft_listing.is_approved:
            draft_listing.is_update = True
            draft_listing.is_approved = False
        
        draft_listing.save()
        return redirect('vendor-home')


@method_decorator(csrf_exempt, name='dispatch')
class InstagramPortfolioView(LoginRequiredMixin, IsVendor, IsListingPresent, IsListingNotAssign, View):
    model = Vendor

    def get(self, *args, **kwargs):
        context = {}
        user = self.request.user
        vendor = self.model.objects.get(vendor_user=user)
        listing = vendor.draft_listing
        instagram_token = VendorInstagramToken.objects.filter(vendor=vendor).first()
        short_url = reverse('vendor-instagram-connect')
        full_url = self.request.build_absolute_uri(short_url)
        if instagram_token:

            token_json = instagram_token.token
            token = json.loads(token_json)

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
        elif listing.photos:
            context['photos'] = listing.photos.all()
            context['videos'] = listing.videos.all()
            context['photos_len'] = len(listing.photos.all())
            context['videos_len'] = len(listing.videos.all())
            context['listing'] = listing
            instagram_basic_display = InstagramBasicDisplay(app_id='549315439403500',
                                                        app_secret='0c3fd79c822b212973bbd2f63d523137',
                                                        redirect_url='https://vowsnviews.com/auth/')
            context['instagram_connect_url'] = instagram_basic_display.get_login_url()
        else:
            instagram_basic_display = InstagramBasicDisplay(app_id='549315439403500',
                                                        app_secret='0c3fd79c822b212973bbd2f63d523137',
                                                        redirect_url='https://vowsnviews.com/auth/')
            context['instagram_connect_url'] = instagram_basic_display.get_login_url()

        if listing.photos.all():
            context['photos'] = listing.photos.all()
        if listing.videos.all():
            context['videos'] = listing.videos.all()
        context['object'] = vendor
        return render(self.request, 'vendors/portfolio.html', context)

    def post(self, request, *args, **kwargs):
        # data from ajax
        img_media = request.FILES.getlist('images[]', None)
        video_media = request.FILES.getlist('videos[]', None)
        user = self.request.user
        vendor = Vendor.objects.filter(vendor_user=user).first()
        listing = vendor.draft_listing

        # data from database to check if already media present
        photos = listing.photos.all()
        videos = listing.videos.all()
        if len(photos) > 15:
            messages.warning(request, "Only 15 images should be uploaded")
            return redirect('instagram-portfolio')
        if len(videos) > 5:
            messages.warning(request, "Only 5 videos should be uploaded")
            return redirect('instagram-portfolio')
        if len(img_media) + len(photos) > 15:
            messages.warning(request, "Only 15 images are allowed")
            return redirect('add-media')
        if len(video_media) + len(videos) > 5:
            messages.warning(request, "Only 5 videos are allowed")
            return redirect('add-media')
        if vendor:
            if vendor.draft_listing and vendor.listing:
                listing = vendor.listing
                draft_listing = vendor.draft_listing
                for item in img_media:
                    obj = ListingPhoto.objects.create(file=item)
                    obj.save()
                    draft_listing.photos.add(obj)
                    listing.photos.add(obj)
                    listing.save()
                    draft_listing.save()

                for item in video_media:
                    obj = ListingVideo.objects.create(file=item)
                    obj.save()
                    draft_listing.videos.add(obj)
                    listing.videos.add(obj)
                    listing.save()
                    draft_listing.save()

                messages.success(request, "Media added successfully")
                return redirect('vendor-home')
            elif vendor.draft_listing:
                draft_listing = vendor.draft_listing
                for item in img_media:
                    obj = ListingPhoto.objects.create(file=item)
                    obj.save()
                    draft_listing.photos.add(obj)
                    draft_listing.save()

                for item in video_media:
                    obj = ListingVideo.objects.create(file=item)
                    obj.save()
                    draft_listing.videos.add(obj)
                    draft_listing.save()

                messages.success(request, "Media added successfully")
                return redirect('vendor-home')
            else:
                messages.warning(request, "Listing not exist, first add listing")
                return redirect('add-listing')
        else:
            messages.warning(request, "Vendor does not exist")
            return redirect('home')


class FAQDisplayView(LoginRequiredMixin, IsVendor, IsListingNotAssign, View):

    def get(self, *args, **kwargs):
        user = self.request.user
        vendor = Vendor.objects.get(vendor_user=user)
        context = {}
        if vendor.draft_listing:
            if vendor.draft_listing.is_faq_answered:
                context['faq'] = vendor.draft_listing.get_faq()
                return render(self.request, 'vendors/faq.html', context)
            else:
                messages.warning(self.request, "FAQ not answered yet! please answer FAQ")
                return redirect('faq-answers')
        else:
            messages.warning(self.request, "Please add Listing")
            return redirect('add-listing')


class ListingContactSeenUpdate(LoginRequiredMixin, IsVendor, IsListingNotAssign, View):
    def get(self, *args, **kwargs):
        listing_contact = ListingContact.objects.filter(id=kwargs.get('pk')).first()
        if listing_contact:
            listing_contact.read = True
            listing_contact.save()
            if self.request.META.get('HTTP_REFERER'):
                return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
            return redirect('contact-list')
        else:
            messages.warning(self.request, "Contact does not exist!")
            if self.request.META.get('HTTP_REFERER'):
                return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
            return redirect('contact-list')


class VendorInquiryListView(LoginRequiredMixin, IsVendor, IsListingPresent, IsListingNotAssign, View):
    template_name = 'vendors/inquiry_list.html'

    def get(self, *args, **kwargs):
        context = {}
        user = self.request.user
        vendor = Vendor.objects.get(vendor_user=user)
        if not vendor.listing:
            messages.warning(self.request, "Your listing is not approved yet!")
            return redirect('vendor-home')
        context['contact_list'] = ListingContact.objects.filter(listing=vendor.listing)
        return render(self.request, self.template_name, context)


class VendorInquiryDetailView(LoginRequiredMixin, IsVendor, IsListingPresent, IsListingNotAssign, DetailView):
    template_name = 'vendors/inquiry_detail.html'
    model = ListingContact


@method_decorator(csrf_exempt, name='dispatch')
class MediaAddView(LoginRequiredMixin, IsVendor, IsListingPresent, IsListingNotAssign, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        vendor = Vendor.objects.filter(vendor_user=user).first()
        # Condtition
        # if is_instagram_connect(self.request):
        #    messages.success(self.request, "Media already added from instagram")
        #    return redirect('vendor-home')
        #
        # if vendor.draft_listing:
        #     photos = vendor.draft_listing.photos.all()
        #     if photos:
        #         messages.warning(self.request, "Media already present")
        #         return redirect('vendor-home')
        return render(self.request, 'vendors/bulk_photo_video.html')

    def post(self, request, *args, **kwargs):
        img_media = request.FILES.getlist('images[]', None)
        video_media = request.FILES.getlist('videos[]')
        user = self.request.user
        vendor = Vendor.objects.filter(vendor_user=user).first()

        if len(img_media) > 15:
            messages.warning(request, "Only 15 images are allowed")
            return redirect('add-media')
        if len(video_media) > 5:
            messages.warning(request, "Only 5 videos are allowed")
            return redirect('add-media')

        if vendor:

            if vendor.draft_listing and vendor.listing:
                listing = vendor.listing
                draft_listing = vendor.draft_listing
                for item in img_media:
                    obj = ListingPhoto.objects.create(file=item)
                    obj.save()
                    draft_listing.photos.add(obj)
                    listing.photos.add(obj)
                    listing.save()
                    draft_listing.save()

                for item in video_media:
                    obj = ListingVideo.objects.create(file=item)
                    obj.save()
                    draft_listing.videos.add(obj)
                    listing.videos.add(obj)
                    listing.save()
                    draft_listing.save()

                messages.success(request, "Media added successfully")
                return redirect('vendor-home')
            elif vendor.draft_listing:
                draft_listing = vendor.draft_listing
                for item in img_media:
                    obj = ListingPhoto.objects.create(file=item)
                    obj.save()
                    draft_listing.photos.add(obj)
                    draft_listing.save()

                for item in video_media:
                    obj = ListingVideo.objects.create(file=item)
                    obj.save()
                    draft_listing.videos.add(obj)
                    draft_listing.save()

                messages.success(request, "Media added successfully")
                return redirect('vendor-home')
            else:
                messages.warning(request, "Listing not exist, first add listing")
                return redirect('add-listing')
        else:
            messages.warning(request, "Vendor does not exist")
            return redirect('home')


class CreateOfferView(LoginRequiredMixin, IsVendor, IsListingNotAssign, UserPassesTestMixin, CreateView):
    model = ListingOffer
    template_name = 'vendors/create_offer.html'
    form_class = ListingOfferForm

    def form_valid(self, form):
        listing_offer = form.instance
        listing_offer.save()
        vendor = Vendor.objects.filter(vendor_user=self.request.user).first()
        vendor.listing.offer.add(listing_offer)
        vendor.draft_listing.offer.add(listing_offer)
        messages.success(self.request, "Offer applied to listing")
        return redirect('vendor-home')

    def test_func(self):
        vendor = Vendor.objects.filter(vendor_user=self.request.user).first()
        if vendor.draft_listing.is_approved:
            return True
        return False


class DeleteOfferView(LoginRequiredMixin, IsVendor, IsListingNotAssign, UserPassesTestMixin, DeleteView):
    model = ListingOffer
    template_name = 'vendors/delete_offer.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "Your listing offer is deleted!")
        return redirect('vendor-home')

    def test_func(self):
        offer = ListingOffer.objects.filter(id=int(self.kwargs.get('pk'))).first()
        if not offer:
            return False
        vendor = Vendor.objects.filter(vendor_user=self.request.user).first()
        if offer in vendor.listing.offer.all():
            return True
        return False


# ajax method to check is title of updated listing is unique or not
def is_title_unique(request):
    title = request.GET.get('title')
    id = int(request.GET.get('id'))
    listing = DraftListing.objects.filter(title=title)
    if len(listing) > 2:
        return JsonResponse({'status': 'false', 'case': 'first'})
    if len(listing) > -1:
        if len(listing) == 1:
            if listing[0].id == id:
                return JsonResponse({'status': 'true', 'case': 'second'})
            else:
                return JsonResponse({'status': 'false', 'case': 'first'})
    if len(listing) < 1:
        return JsonResponse({'status': 'true', 'case': 'second'})


# ajax method to delete area
def area_delete_view(request):
    id = int(request.GET.get('id'))
    print(id)
    area = Area.objects.filter(id=id).first()
    print(area)
    area.delete()
    return JsonResponse({'status': 'true'})


# ajax method to delete pricing
def additional_pricing_delete_view(request):
    id = int(request.GET.get('id'))
    pricing = AddititionalPricing.objects.filter(id=id).first()
    pricing.delete()
    return JsonResponse({'status': 'true'})


# ajax method to add area
@csrf_exempt
def add_area(request):
    area = Area.objects.create(seating_type=request.POST.get('seating_type'),
                               seating_space=request.POST.get('seating_space'),
                               floating_space=request.POST.get('floating_space'),
                               additional_text=request.POST.get('additional_info'),
                               image=request.FILES.get('image'))
    area.save()
    return JsonResponse({
        'area_id': area.id,
        'seating_type': area.seating_type,
        'seating_space': area.seating_space,
        'floating_space': area.floating_space,
        'additional_text': area.additional_text,
        'image': area.image.url if area.image else "",
    })


# ajax method to add additional pricing
def add_pricing(request):
    pricing = AddititionalPricing.objects.create(
        pricing_title=request.GET.get('pricing_title'),
        cost=request.GET.get('cost'),
        suffix=request.GET.get('suffix'),
    )
    pricing.save()
    return JsonResponse({
        'pricing_id': pricing.id,
        'pricing_title': pricing.pricing_title,
        'cost': pricing.cost,
        'suffix': pricing.suffix,
    })


# ajax method to get sub location listing
def get_sub_location(request):
    id = request.GET.get('id', None)
    if id:
        location = ListingLocation.objects.filter(id=int(id)).first()
        if location:
            listing_sub_location = SubListingLocation.objects.filter(listing_location=location)
            export_data = {}
            for item in listing_sub_location:
                export_data[item.id] = item.title
            return JsonResponse({
                'sub_location': export_data
            })
        else:
            return JsonResponse({
                'status': 'fail'
            })
    else:
        return JsonResponse({
            'status': 'fail1'
        })


def delete_photo_media(request):
    id = int(request.GET.get("id"))
    photo = ListingPhoto.objects.filter(id=id).first()
    vendor = Vendor.objects.get(vendor_user=request.user)
    listing = vendor.draft_listing
    if photo:
        photo.delete()
    return JsonResponse({
        'status': 'success',
        'photos_len': len(listing.photos.all())
    })


def delete_video_media(request):
    id = int(request.GET.get("id"))
    video = ListingVideo.objects.filter(id=id).first()
    vendor = Vendor.objects.get(vendor_user=request.user)
    listing = vendor.draft_listing
    if video:
        video.delete()
    return JsonResponse({
        'status': 'success',
        'videos_len': len(listing.videos.all())
    })
