from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from home import views

from vendors import views as vendor_view
urlpatterns = [
    path('letsmanagestuff/', admin.site.urls),
    path('user/', include('users.urls')),
    path('products/', include('products.urls')),
    path('order/', include('order.urls')),
    path('listing/', include('listing.urls')),
    path('analytics/', include('analytics.urls')),
    path('listing_analytics/', include('listing_analytics.urls')),
    path('vendors/', include('vendors.urls')),
    path('', include('home.urls')),
    path(r'^$', views.handler404),
    path(r'^$', views.handler500),
    path('auth/', vendor_view.InstagramConnectView.as_view(), name='instagram-from-home-url'),
]

handler404 = 'home.views.handler404'
handler500 = 'home.views.handler500'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)