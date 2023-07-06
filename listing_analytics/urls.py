from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views


urlpatterns = [
    path('', views.AnalyticsView.as_view(), name='admin-listing-dashboard'),

    # Listing
    path('listing/list-admin/', views.AdminListingListView.as_view(), name='admin-listing-list'),
    path('listing/add/', views.AdminListingAddView.as_view(), name='admin-listing-add'),
    path('listing/update/<int:pk>/', views.AdminListingUpdateView.as_view(), name='admin-listing-update'),
    path('listing/delete/<int:pk>/', views.AdminListingDeleteView.as_view(), name='admin-listing-delete'),
    path('listing/blog-list-admin/', views.AdminBlogListView.as_view(), name='admin-blog-list'),
    path('listing/blog/add/', views.AdminBlogAddView.as_view(), name='admin-blog-add'),
    path('listing/blog/update/<int:pk>/', views.AdminBlogUpdateView.as_view(), name='admin-blog-update'),
    path('listing/blog/delete/<int:pk>/', views.AdminBlogDeleteView.as_view(), name='admin-blog-delete'),

    # Add Place Id for listing
    path('listing/add/placeid/<int:pk>', views.AdminAddListingPlaceId.as_view(), name='admin-add-placeid'),
    # Listing Approve
    path('listing/approve/<int:pk>/', views.AdminListingApproveView.as_view(), name='admin-listing-approve'),

    # DraftListing
    path('draft/listing/list-admin/', views.AdminDraftListingListView.as_view(), name='admin-draft-listing-list'),
    path('draft/listing/detail-admin/<int:pk>/', views.AdminDraftListingDetailView.as_view(), name='admin-draft'
                                                                                                   '-listing-detail'),
    path('draft/listing/decline/<int:pk>/', views.AdminListingDeclineView.as_view(), name='admin-listing-decline'),
    path('draft/listing/decline/list/', views.AdminDeclineListingListView.as_view(), name='admin-listing-decline-list'),

    # Image
    path('listing/image/add/<int:pk>/', views.ListingPhotosAdd.as_view(), name='analytics-listing-image-add'),
    path('listing/image/delete/<int:listing_id>/<int:pk>/', views.ListingPhotosDelete.as_view(),
         name='analytics-listing-image-delete'),

    # Video
    path('listing/video/add/<int:pk>/', views.ListingVideoAdd.as_view(), name='analytics-listing-video-add'),
    path('listing/video/delete/<int:listing_id>/<int:pk>/', views.ListingVideoDelete.as_view(),
         name='analytics-listing-video-delete'),

    # Category
    path('listing/category/list-admin/', views.AdminCategoryListView.as_view(), name='admin-listing-category-list'),
    path('listing/category/add/', views.AdminCategoryAddView.as_view(), name='admin-listing-category-add'),
    path('listing/category/update/<int:pk>/', views.AdminCategoryUpdateView.as_view(),
         name='admin-listing-category-update'),
    path('listing/category/delete/<int:pk>/', views.AdminCategoryDeleteView.as_view(),
         name='admin-listing-category-delete'),

    # Parent Category
    path('listing/parent/category/list-admin/', views.AdminParentCategoryListView.as_view(),
         name='admin-listing-parent-category-list'),
    path('listing/parent/category/add/', views.AdminParentCategoryAddView.as_view(),
         name='admin-listing-parent-category-add'),
    path('listing/parent/category/update/<int:pk>/', views.AdminParentCategoryUpdateView.as_view(),
         name='admin-listing-parent-category-update'),
    path('listing/parent/category/delete/<int:pk>/', views.AdminParentCategoryDeleteView.as_view(),
         name='admin-listing-parent-category-delete'),

    # Location
    path('listing/location/list-admin/', views.AdminListingLocationListView.as_view(),
         name='admin-listing-location-list'),
    path('listing/location/add/', views.AdminListingLocationAddView.as_view(), name='admin-listing-location-add'),
    path('listing/location/update/<int:pk>/', views.AdminListingLocationUpdateView.as_view(),
         name='admin-listing-location-update'),
    path('listing/location/delete/<int:pk>/', views.AdminListingLocationDeleteView.as_view(),
         name='admin-listing-location-delete'),

    # Sub Location
    path('listing/sub-location/list-admin/', views.AdminListingSubLocationListView.as_view(),
         name='admin-listing-sub-location-list'),
    path('listing/sub-location/add/', views.AdminListingSubLocationAddView.as_view(),
         name='admin-listing-sub-location-add'),
    path('listing/sub-location/update/<int:pk>/', views.AdminListingSubLocationUpdateView.as_view(),
         name='admin-listing-sub-location-update'),
    path('listing/sub-location/delete/<int:pk>/', views.AdminListingSubLocationDeleteView.as_view(),
         name='admin-listing-sub-location-delete'),

    path('listing/review/list-admin/', views.AdminReviewListView.as_view(), name='admin-listing-review-list'),
    path('listing/review/update/<int:pk>/', views.AdminReviewUpdateView.as_view(), name='admin-listing-review-update'),
    path('listing/review/delete/<int:pk>/', views.AdminReviewDeleteView.as_view(), name='admin-listing-review-delete'),

    # Listing Contact
    path('listing/contact/', views.AdminContactListView.as_view(), name='admin-listing-contact'),
    path('listing/contact/update/<int:pk>/', views.AdminContactUpdateView.as_view(),
         name='admin-listing-contact-update'),

    path('landing/list/', views.LandingListView.as_view(), name='landing-list'),
    path('landing/delete/<int:pk>/', views.LandingDeleteView.as_view(), name='landing-delete'),

     # FAQ
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)