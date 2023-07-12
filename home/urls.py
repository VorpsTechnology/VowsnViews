from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from .views import Home, NewsLetterCreateView, ContactView, SearchView, DestinationWeddingView, PlanningDecorView, \
                   InHouseServiceListView, TPPView, TPCView, Popup, RPView, SPView, SomeView, listVendor, ClosePopup, save_location, LandingView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('newsletter', NewsLetterCreateView.as_view(), name='news-letter'),
    path('wedding-stylist/', TemplateView.as_view(template_name='home/wedding_stylist.html'), name='wedding-stylist'),
    path('pricing/', TemplateView.as_view(template_name='home/pricing.html'), name='pricing'),
    path('landing/', LandingView.as_view(), name='landing'), #--recent change
    path('planning-decor/', PlanningDecorView.as_view(), name='planning-decor'),
    path('destination-wedding/', DestinationWeddingView.as_view(), name='destination-wedding'),
    path('in-house-services/', InHouseServiceListView.as_view(), name='in-house-service'),
    path('terms-and-condition/', TPCView.as_view(), name='terms-and-condition'),
    path('privacy-policy/', TPPView.as_view(), name='privacy-policy'),
    path('shipping-policy/', SPView.as_view(), name='shipping-policy'),
    path('refund-poliicy/', RPView.as_view(), name='refund-policy'),
    path('vendor-poliicy/', SomeView.as_view(), name='vendor-policy'),
    path('about/', TemplateView.as_view(template_name='home/about.html'), name='about'),
    path('sitemap.xml/', TemplateView.as_view(template_name='home/sitemap.html'), name='sitemap'),
    path('robots.txt/', TemplateView.as_view(template_name='home/robots.html'), name='robots'),

    path('popup/', Popup.as_view(), name='popup'),
    path('close_popup/', ClosePopup.as_view(), name='close-popup'),
    path('vendor/', listVendor.as_view() , name='vendor'),

    path('save/location/', save_location, name='save-location')
   
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
