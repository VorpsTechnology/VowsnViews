from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [

    # Listings
    path('list/', views.ListingListView.as_view(), name='listing-list-view'),
    path('detail/<int:pk>/', views.ListingDetailView.as_view(), name='listing-detail-view'),

    # Favorite
    path('favorite/add/<int:pk>/', views.ListingFavoriteAddView.as_view(), name='listing-favorite-add'),
    path('favorite/remove/<int:pk>/', views.ListingFavoriteRemoveView.as_view(), name='listing-favorite-remove'),
    path('favorite/list/', views.ListingFavoriteListView.as_view(), name='listing-favorite-list'),

    # Review
    path('review/add/<int:pk>/', views.ReviewAddView.as_view(), name='listing-review-add'),
    path('review/update/<int:pk>/', views.ReviewUpdateView.as_view(), name='listing-review-update'),
    path('review/delete/<int:pk>/', views.ReviewDeleteView.as_view(), name='listing-review-delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

