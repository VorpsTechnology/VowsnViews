from listing.models import Listing, DraftListing, ListingContact
from vendors.models import Vendor


def get_notifications(request):
    context = {}
    user = request.user if request.user.is_authenticated else None
    vendor = Vendor.objects.filter(vendor_user=user).first()
    if vendor:
        if vendor.listing:
            context['contact_count'] = ListingContact.objects.filter(listing=vendor.listing).filter(read=False).count()
            if context['contact_count']:
                context['show_notification'] = True
        else:
            pass
    return context