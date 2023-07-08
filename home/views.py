from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.contrib import messages
from itertools import chain

from users.forms import CurrencySelectForm
from home.forms import NewsLetterForm
from home.models import Contact, DestinationWedding, TPP, Landing, ListingCategoryBudget
from .forms import ListingSearchForm, ContactForm, LandingForm, ListingCategoryBudgetForm
from django.http import HttpResponse

from users.models import (
    User, Address, Task, Budget, GuestList, Blog
)
from itertools import chain
from products.models import Product, Category
from listing.models import Listing, ListingLocation, ListingCategory, ParentListingCategory
from django.urls import reverse_lazy



def handler404(request, *args, **kwargs):
    return render(request, 'home/error.html')


def handler500(request, *args, **kwargs):
    return render(request, 'home/error.html')


# TEST DONE
class Home(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            form = CurrencySelectForm(instance=self.request.user)
        else:
            form = CurrencySelectForm()

        list_location = ListingLocation.objects.filter(is_active=True)
        blog = Blog.objects.filter(is_active=True)
        category = ListingCategory.objects.filter(is_active=True)
        return render(self.request, 'home/home.html', {'form': form, 'list_location': list_location,
                                                       'category': category, 'blog': blog})

    def post(self, *args, **kwargs):
        try:
            if self.request.user.is_authenticated:
                form = CurrencySelectForm(self.request.POST, instance=self.request.user)
            else:
                form = CurrencySelectForm(self.request.POST)
            currency = self.request.POST.get('currency')
            self.request.session['currency'] = currency

            if self.request.user.is_authenticated:
                self.request.user.currency = currency
                self.request.user.save()
        except:
            pass
        search_form = ListingSearchForm(self.request.POST)
        if search_form.is_valid():
            location = search_form.cleaned_data['location']
            location_id = ListingLocation.objects.get(title=location)
            category = search_form.cleaned_data['category']
            category_id = ListingCategory.objects.get(title=category)

            url = f'https://vowsnviews.com/listing/list/?note=&discount_price_min=&discount_price_max=&category={category_id.id}&location={location_id.id}&vendor_name='
            return redirect(url)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class listVendor(View):
    def get(self, *args, **kwargs):
        LABEL_CHOICES = ['Elite', 'In Demand',
                         'Our Recommendation',
                         'Most Booked',
                         'Trending',
                         'Popular',
                         'Best Deal',
                         'Best Offer',
                         'without_label']
        listing_with_filter = {
            'listing': {item: {'is_verified': [], 'normal': []} for item in LABEL_CHOICES},
            'top_photograher': {item: {'is_verified': [], 'normal': []} for item in LABEL_CHOICES},
            'top_venue': {item: {'is_verified': [], 'normal': []} for item in LABEL_CHOICES},
            'food': {item: {'is_verified': [], 'normal': []} for item in LABEL_CHOICES},
            'planning_decor': {item: {'is_verified': [], 'normal': []} for item in LABEL_CHOICES},
            'music': {item: {'is_verified': [], 'normal': []} for item in LABEL_CHOICES},
            'invites': {item: {'is_verified': [], 'normal': []} for item in LABEL_CHOICES},
        }

        # elite_listing = Listing.objects.filter(parent_category="5", label="Elite")
        # recommend = Listing.objects.filter(parent_category=5, label="Our Recommendation")
        listing = Listing.objects.filter(parent_category="5")
        top_photograher = Listing.objects.filter(parent_category="4")
        top_venue = Listing.objects.filter(parent_category="1")
        food = Listing.objects.filter(parent_category="7")
        planning_decor = Listing.objects.filter(parent_category="6")
        music = Listing.objects.filter(parent_category="9")
        invites = Listing.objects.filter(parent_category="8")

        for item in listing:
            if item.label:
                if item.is_verified:
                    listing_with_filter['listing'][item.label]['is_verified'].append(item)
                else:
                    listing_with_filter['listing'][item.label]['normal'].append(item)
            else:
                if item.is_verified:
                    listing_with_filter['listing']['without_label']['is_verified'].append(item)
                else:
                    listing_with_filter['listing']['without_label']['normal'].append(item)

        for item in top_photograher:
            if item.label:
                if item.is_verified:
                    listing_with_filter['top_photograher'][item.label]['is_verified'].append(item)
                else:
                    listing_with_filter['top_photograher'][item.label]['normal'].append(item)
            else:
                if item.is_verified:
                    listing_with_filter['top_photograher']['without_label']['is_verified'].append(item)
                else:
                    listing_with_filter['top_photograher']['without_label']['normal'].append(item)

        for item in top_venue:
            if item.label:
                if item.is_verified:
                    listing_with_filter['top_venue'][item.label]['is_verified'].append(item)
                else:
                    listing_with_filter['top_venue'][item.label]['normal'].append(item)
            else:
                if item.is_verified:
                    listing_with_filter['top_venue']['without_label']['is_verified'].append(item)
                else:
                    listing_with_filter['top_venue']['without_label']['normal'].append(item)

        for item in food:
            if item.label:
                if item.is_verified:
                    listing_with_filter['food'][item.label]['is_verified'].append(item)
                else:
                    listing_with_filter['food'][item.label]['normal'].append(item)
            else:
                if item.is_verified:
                    listing_with_filter['food']['without_label']['is_verified'].append(item)
                else:
                    listing_with_filter['food']['without_label']['normal'].append(item)

        for item in planning_decor:
            if item.label:
                if item.is_verified:
                    listing_with_filter['planning_decor'][item.label]['is_verified'].append(item)
                else:
                    listing_with_filter['planning_decor'][item.label]['normal'].append(item)
            else:
                if item.is_verified:
                    listing_with_filter['planning_decor']['without_label']['is_verified'].append(item)
                else:
                    listing_with_filter['planning_decor']['without_label']['normal'].append(item)


        for item in music:
            if item.label:
                if item.is_verified:
                    listing_with_filter['music'][item.label]['is_verified'].append(item)
                else:
                    listing_with_filter['music'][item.label]['normal'].append(item)
            else:
                if item.is_verified:
                    listing_with_filter['music']['without_label']['is_verified'].append(item)
                else:
                    listing_with_filter['music']['without_label']['normal'].append(item)

        for item in invites:
            if item.label:
                if item.is_verified:
                    listing_with_filter['invites'][item.label]['is_verified'].append(item)
                else:
                    listing_with_filter['invites'][item.label]['normal'].append(item)
            else:
                if item.is_verified:
                    listing_with_filter['invites']['without_label']['is_Verified'].append(item)
                else:
                    listing_with_filter['invites']['without_label']['normal'].append(item)

        makeup_list = []
        top_photograher_list = []
        top_venue_list = []
        food_list = []
        planning_decor_list = []
        music_list = []
        invites_list = []

        print("Aniket",listing_with_filter['listing'].values())
        for item in listing_with_filter['listing'].values():
            for item1 in item.values():
                for item in item1:
                    makeup_list.append(item)

        for item in listing_with_filter['top_photograher'].values():
            for item1 in item.values():
                for item in item1:
                    top_photograher_list.append(item)

        for item in listing_with_filter['top_venue'].values():
            for item1 in item.values():
                for item in item1:
                    top_venue_list.append(item)

        for item in listing_with_filter['food'].values():
            for item1 in item.values():
                for item in item1:
                    food_list.append(item)

        for item in listing_with_filter['planning_decor'].values():
            for item1 in item.values():
                for item in item1:
                    planning_decor_list.append(item)

        for item in listing_with_filter['music'].values():
            for item1 in item.values():
                for item in item1:
                    music_list.append(item)

        for item in listing_with_filter['invites'].values():
            for item1 in item.values():
                for item in item1:
                    invites_list.append(item)

        return render(self.request, 'home/vendors.html',
                      {
                          'makeup_list': makeup_list,
                          'photographer': top_photograher_list,
                          'choreographer': top_venue_list,
                          'food': food_list,
                          'planning_decor': planning_decor_list,
                          'music': music_list,
                          'invites': invites_list,
                      })


class Popup(View):
    def post(self, *args, **kwargs):
        search_form = ContactForm(self.request.POST)
        if search_form.is_valid():
            search_form.save()
            self.request.session['offer'] = 'viewed'
            messages.success(self.request, 'Registration successful for the lucky draw.')
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        messages.warning(self.request, 'Registration Unsuccessful for the lucky draw. Please fill details properly!')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class ClosePopup(View):
    def get(self, *args, **kwargs):
        self.request.session['offer'] = 'viewed'
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


# TEST DONE
class NewsLetterCreateView(View):
    def get(self, *args, **kwargs):
        form2 = NewsLetterForm()
        return render(self.request, 'home/home.html', {'form2': form2})

    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            form = NewsLetterForm(self.request.POST)
            if form.is_valid:
                form.save()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class ContactView(CreateView):
    model = Contact
    fields = ['name', 'email', 'mobile', 'description']
    template_name = "home/contact.html"
    success_url = '/contact/'

    def form_valid(self, form):
        phone_number = form.cleaned_data['mobile']
        if len(str(phone_number)) != 10:
            messages.warning(self.request, 'Invalid mobile number')
            return redirect('contact')
        messages.success(self.request, 'Message sent you will be contact soon!')
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        tpp = TPP.objects.all().first()
        context['tpp'] = tpp
        return context


class SearchView(ListView):
    template_name = "home/search.html"
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            product_results = Product.objects.search(query).filter(is_active=True)
            listing_results = Listing.objects.search(query).filter(is_active=True)
            # profile_results = Profile.objects.search(query)

            # combine querysets

            queryset_chain = chain(
                product_results,
                listing_results,
                # profile_results
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)  # since qs is actually a list
            return qs
        return Product.objects.none()


# TEST DONE
class DestinationWeddingView(View):
    def get(self, *args, **kwargs):
        destination_wedding = DestinationWedding.objects.all().first()
        object_list = ListingLocation.objects.all()
        return render(self.request, 'home/destination_wedding.html', {'destination_wedding': destination_wedding,
                                                                      'object_list': object_list})


class PlanningDecorView(CreateView):
    model = Contact
    fields = ['name', 'email', 'mobile', 'description']
    template_name = "home/planning_decor.html"
    success_url = '/planning-decor'

    def form_valid(self, form):
        phone_number = form.cleaned_data['mobile']
        if len(str(phone_number)) != 10:
            messages.warning(self.request, 'Invalid mobile number')
            return redirect('contact')
        messages.success(self.request, 'Message sent you will be contact soon!')
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        destination_wedding = DestinationWedding.objects.all().first()
        context['destination_wedding'] = destination_wedding
        return context


class InHouseServiceListView(CreateView):
    model = Contact
    fields = ['name', 'email', 'mobile', 'description']
    template_name = "home/house_service.html"
    success_url = '/in-house-services/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        list = Listing.objects.filter(is_in_house_listing=True)
        context['list_location'] = list
        return context

    def form_valid(self, form):
        phone_number = form.cleaned_data['mobile']
        if len(str(phone_number)) != 10:
            messages.warning(self.request, 'Invalid mobile number')
            return redirect('contact')
        messages.success(self.request, 'Message sent you will be contact soon!')
        return super().form_valid(form)


# TEST DONE
class TPCView(View):
    def get(self, *args, **kwargs):
        tpp = TPP.objects.all().first()
        return render(self.request, 'home/terms_and_condition.html', {'tpp': tpp})


class TPPView(View):
    def get(self, *args, **kwargs):
        tpp = TPP.objects.all().first()
        return render(self.request, 'home/privacy_policy.html', {'tpp': tpp})


class SPView(View):
    def get(self, *args, **kwargs):
        tpp = TPP.objects.all().first()
        return render(self.request, 'home/shipping_policy.html', {'tpp': tpp})


class RPView(View):
    def get(self, *args, **kwargs):
        tpp = TPP.objects.all().first()
        return render(self.request, 'home/refund_policy.html', {'tpp': tpp})


class SomeView(View):
    def get(self, *args, **kwargs):
        tpp = TPP.objects.all().first()
        return render(self.request, 'home/vendor_policy.html', {'tpp': tpp})


def save_location(request):
    lat = request.GET.get('lat', None)
    long = request.GET.get('long', None)

    if lat and long:
        request.session['latitude'] = lat
        request.session['longitude'] = long

    return JsonResponse({
        'status': 'saved'
    })


class LandingView(CreateView):
    model = Landing
    form_class = LandingForm
    template_name = "home/landings.html"
    # success_url = '/landing/'
    success_url = reverse_lazy('users-register')  

    def form_valid(self, form):
        phone_number = form.cleaned_data['mobile']
        if len(str(phone_number)) != 10:
            messages.warning(self.request, 'Invalid mobile number')
            return redirect('contact')
        landing_model = form.instance
        landing_model.save()

        # saving budgets
        prefix_arr = self.request.POST.getlist('prefix_array')
        try:
            for prefix in prefix_arr:
                budget_form = ListingCategoryBudgetForm(self.request.POST, prefix=prefix)
                if budget_form.is_valid():
                    budget_model = budget_form.instance
                    budget_model.save()
                    landing_model.budget.add(budget_model)
        except Exception as e:
            print(e)
        messages.success(self.request, 'You will be get in touch shortly.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # messages.error(self.request, 'Invalid details.')
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        list = ParentListingCategory.objects.all()
        context['parent_listing'] = list
        return context
    


    # def download_file(request):
    #     file_url = 'https://vowsnviews.com/landing/path/to/file.js'
    #     local_path = 'http://127.0.0.1:8000/landings/'  # Specify the local path where you want to save the file
        
    #     # Download the file
    #     urllib.request.urlretrieve(file_url, local_path)
        
    #     # Once downloaded, you can use the file locally as needed
        
    #     # Example: Read the contents of the file
    #     with open(local_path, 'r') as file:
    #         file_contents = file.read()
        
    #     # Example: Perform operations on the file contents or use it in your Django application
        
    #     return HttpResponse('File downloaded successfully.')



