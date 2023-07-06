from django.db.models import Q

from users.forms import CurrencySelectForm
from .forms import NewsLetterForm
from listing.models import ListingLocation, ListingCategory, ParentListingCategory
from users.models import Vendor, UserLocation
import datetime
from geopy.geocoders import Nominatim


def currency_form(request):
    form = CurrencySelectForm()
    return {form: 'form'}


def news_form(request):
    form2 = NewsLetterForm()
    return {form2: 'form2'}


def header_data(request):
    parent_category_list = ParentListingCategory.objects.all()
    category_list = ListingCategory.objects.all()
    lll = ListingLocation.objects.all()
    return {'category_list': category_list, 'parent_category_list': parent_category_list, 'listing_locations': lll}


def get_current_year_to_context(request):
    current_datetime = datetime.datetime.now()
    context = {}
    popup = request.session.get('offer')
    if popup:
        context['offer'] = None
    if not popup:
        request.session['offer'] = 'offer'
        context['offer'] = 'offer'
    print(context['offer'])
    context['current_year'] = current_datetime.year
    user = request.user if request.user.is_authenticated else None
    context['vendor_user'] = Vendor.objects.filter(vendor_user=user)
    return context


def save_user_location(request):
    context = {}
    user = request.user if request.user.is_authenticated else None
    session_key = request.session.session_key
    lat = request.session.get('latitude')
    long = request.session.get('longitude')
    if not user:
        user_location = UserLocation.objects.filter(session_key=session_key).filter(latitude=lat).last()
    else:
        user_location = UserLocation.objects.filter(user=user).filter(latitude=lat).last()
    if not user_location:
        if lat and long:
            try:
                geolocator = Nominatim(user_agent="vowsnviews")
                location = geolocator.reverse(str(lat) + "," + str(long))
                city = location.raw.get('address').get('city')
                district = location.raw.get('address').get('state_district')
                state = location.raw.get('address').get('state')
                user_location = UserLocation()
                user_location.user = user
                user_location.session_key = session_key
                user_location.city = city
                user_location.district = district
                user_location.state = state
                user_location.latitude = lat
                user_location.longitude = long
                user_location.save()
            except:
                pass
        else:
            pass
    else:
        pass
    context['user_location'] = user_location
    return context