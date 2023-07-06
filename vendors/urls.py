from django.urls import path
from . import views

urlpatterns = [

    path('home/', views.VendorHomeView.as_view(), name='vendor-home'),
    path('update/profile/<int:pk>/', views.VendorUpdateView.as_view(), name='vendor-website-update'),
    path('list/details/<int:pk>/', views.VendorListingDetailView.as_view(), name='vendor-listing-detail'),

    path('add/listing/', views.ListingAddView.as_view(), name='add-listing'),
    path('add/area/', views.add_area, name='add-area'),
    path('add/pricing/', views.add_pricing, name='add-pricing'),
    path('add/Additionalpricing/<int:pk>/', views.AdditionalPricingCreateView.as_view(), name='add-additional-pricing'),

    # Update normal Listing pk = draftlisting.pk
    path('list/update/', views.VendorListingUpdateView.as_view(), name='vendor-listing-update'),
    path('check/title/', views.is_title_unique, name='is-title-unique'),
    path('delete/area/', views.area_delete_view, name='delete-area'),
    path('delete/pricing/', views.additional_pricing_delete_view, name='delete-pricing'),

    # Update venue listing
    path('update/venue/<int:pk>/', views.VenueListingUpdate.as_view(), name='update-venue-listing'),


    # FAQ
    path('add/faq/answer/', views.FAQAddView.as_view(), name='faq-answers'),
    path('faq/view/', views.FAQDisplayView.as_view(), name='faq-view'),
    path('faq/update/', views.FAQUpdateView.as_view(), name='faq-update'),

    # Instagram Connect
    path('instagram/connect/', views.InstagramConnectView.as_view(), name='vendor-instagram-connect'),
    path('instagram/disconnect/', views.InstagramDisconnectView.as_view(), name='vendor-instagram-disconnect'),
    path('portfolio/', views.InstagramPortfolioView.as_view(), name='instagram-portfolio'),
    
    path('gallery/<int:pk>/', views.VendorInstagram.as_view(), name='vendor-instagram-gallery'),

    # Listing Contact
    path('listing/contact/list/', views.VendorInquiryListView.as_view(), name='contact-list'),
    path('listing/contact/detail/<int:pk>/', views.VendorInquiryDetailView.as_view(), name='contact-detail'),
    path('listing/contact/seen/update/<int:pk>/', views.ListingContactSeenUpdate.as_view(), name='contact-seen-update'),

    # inquiry
    path('inquiry/', views.VendorInquiryListView.as_view(), name='inquiry'),

# sub listing location
    path('sub/location/', views.get_sub_location, name='get-sub-location'),

# Bulk photo/video
    path('add/media/', views.MediaAddView.as_view(), name='add-media'),
    path('delete/photo/media/', views.delete_photo_media, name='delete-photo'),
    path('delete/video/media/', views.delete_video_media, name='delete-video'),

    path('create/offer/listing/', views.CreateOfferView.as_view(), name='create-offer'),
    path('delete/offer/listing/<int:pk>/', views.DeleteOfferView.as_view(), name='delete-offer'),

    path('user/data/deletion/request/', views.delete_instagram_data, name='instagram-deletion-request'),
    path('user/data/deletion/status/<int:confirmation_code>/', views.InstagramDataDeletionSuccessView.as_view(), name='instagram-deletion-status'),
    
    path('user/deauthorize/request/', views.deauthorize_callback, name='instagram-deauthorize-request'),


]
