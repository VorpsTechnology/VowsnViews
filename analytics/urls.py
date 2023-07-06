from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from . import views


urlpatterns = [
    path('', views.AnalyticsView.as_view(), name='admin-dashboard'),

    # Order
    
    path('order/cart/list-admin/', views.AdminNotOrderListView.as_view(), name='admin-not-order-list'),
    
    path('order/list-admin/', views.AdminOrderListView.as_view(), name='admin-order-list'),
    path('order/detail-admin/<int:pk>/', views.AdminOrderDetailView.as_view(), name='admin-order-detail'),

    # Return
    path('list-return-admin/', views.AdminReturnListView.as_view(), name='admin-order-return'),
    path('detail-return-admin/<int:pk>/', views.AdminReturnDetailView.as_view(), name='admin-order-return-detail'),

    # Cancel
    path('list-cancel-admin/', views.AdminCancelListView.as_view(), name='admin-order-cancel'),
    path('detail-cancel-admin/<int:pk>/', views.AdminCancelDetailView.as_view(), name='admin-order-cancel-detail'),

    # Products
    path('product/list-admin/', views.AdminProductListView.as_view(), name='admin-product-list'),
    path('product/detail-admin/<int:pk>/', views.AdminProductDetailView.as_view(), name='admin-product-detail'),
    path('product/add/', views.AdminProductAddView.as_view(), name='admin-product-add'),
    path('product/update/<int:pk>/', views.AdminProductUpdateView.as_view(), name='admin-product-update'),
    path('product/delete/<int:pk>/', views.AdminProductDeleteView.as_view(), name='admin-product-delete'),

    # Variation
    path('variation/add/<int:pk>/', views.AdminVariationAddView.as_view(), name='admin-variation-add'),
    path('variation/update/<int:pk>/', views.AdminVariationUpdateView.as_view(), name='admin-variation-update'),
    path('variation/delete/<int:product_id>/<int:pk>/', views.AdminVariationDeleteView.as_view(),
         name='admin-variation-delete'),

    # Category
    path('category/list-admin/', views.AdminCategoryListView.as_view(), name='admin-category-list'),
    path('category/add/', views.AdminCategoryAddView.as_view(), name='admin-product-category-add'),
    path('category/update/<int:pk>/', views.AdminCategoryUpdateView.as_view(), name='admin-product-category-update'),
    path('category/delete/<int:pk>/', views.AdminCategoryDeleteView.as_view(), name='admin-product-category-delete'),

    path('parent/category/list-admin/', views.AdminParentCategoryListView.as_view(), name='admin-parent-category-list'),
    path('parent/category/add/', views.AdminParentCategoryAddView.as_view(), name='admin-product-parent-category-add'),
    path('parent/category/update/<int:pk>/', views.AdminParentCategoryUpdateView.as_view(),
         name='admin-product-parent-category-update'),
    path('parent/category/delete/<int:pk>/', views.AdminParentCategoryDeleteView.as_view(),
         name='admin-product-parent-category-delete'),

    # Mail
    path('send/mail/', views.SendMail.as_view(), name='admin-send-mail'),

    # Contact
    path('contact/', views.AdminContactListView.as_view(), name='admin-contact'),
    path('contact/update/<int:pk>/', views.AdminContactUpdateView.as_view(), name='admin-contact-update'),

    path('contact/read/update/<int:pk>/', views.AdminContactSeenUpdateView.as_view(), name='admin-contact-read'),
    path('return/read/update/<int:pk>/', views.AdminReturnSeenUpdateView.as_view(), name='admin-return-read'),
    path('cancellation/read/update/<int:pk>/', views.AdminCancelSeenUpdateView.as_view(), name='admin-cancel-read'),
    path('order/read/update/<int:pk>/', views.MiniOrderSeenUpdateView.as_view(), name='admin-order-read'),

    # Data Copy
    path('listing/blank/list/', views.BlankDraftListingListView.as_view(), name='blank-listing-list'),
    path('listing/copy/all/', views.ListingCopyView.as_view(), name='copy-all-listing'),
    path('listing/vendors/assign/<int:pk>/', views.AssignVendorToListing.as_view(), name='vendor-assign-to-listing'),
    path('get/vendor/detail/', views.get_vendor_detail, name='get-vendor-detail'),

    path('blank/listing/update/<int:pk>/', views.BlankListingUpdate.as_view(), name='blank-listing-update'),

    path('make/active/', views.make_all_active_listing, name='make-active'),
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
