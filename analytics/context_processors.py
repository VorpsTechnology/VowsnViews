from order.models import Order, MiniOrder, ReturnMiniOrder, CancelMiniOrder
from listing.models import DraftListing, Listing
from home.models import Contact


def analytics_data(request):
    order_count = Order.objects.filter(ordered=True, read=False).count()
    mini_order_count = MiniOrder.objects.filter(ordered=True, read=False).count()
    return_count = ReturnMiniOrder.objects.filter(return_requested=True, read=False).count()
    cancel_count = CancelMiniOrder.objects.filter(cancel_requested=True, read=False).count()
    normal_contact = Contact.objects.filter(read=False).count()
    context = {
        'order_count': order_count,
        'mini_order_count': mini_order_count,
        'return_count': return_count,
        'cancel_count': cancel_count,
        'normal_contact': normal_contact,
    }
    if order_count or mini_order_count or return_count or cancel_count or normal_contact:
        context['show_order_notification'] = True
    return context


def get_listing_analytics_data(request):
    context = {}
    new_listing_list_count = DraftListing.objects.filter(is_approved=False).filter(is_declined=False).count()
    updated_listing_count = DraftListing.objects.filter(is_update=True).count()
    context['draft_listing_count'] = new_listing_list_count + updated_listing_count

    if context['new_listing_list_count'] or context['updated_listing_count']:
        context['listing_notification'] = True

    return context