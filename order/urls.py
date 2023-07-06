from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [

    # Cart
    path('cart/', views.CartListView.as_view(), name='order-view-cart'),  # TD
    path('cart/add/<slug>/<str:buy_now>/', views.add_to_cart, name='order-add-to-cart'),  # TD
    path('cart/remove/<pk>/', views.remove_product_from_cart, name='remove-product-from-cart'),  # TD
    path('cart/delete/<pk>/', views.delete_cart, name='delete-cart'),  # TD
    path('cart/add/variation/<slug>/<pk>/', views.add_to_cart_variation, name='order-add-to-cart-variation'),  # TD
    

    # Order
    path('list/', views.OrderListView.as_view(), name='order-all'),
    path('detail/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('invoice/<int:pk>/', views.OrderInvoiceView.as_view(), name='order-invoice'),

    # Order Return
    path('mini/return/<int:pk>/', views.ReturnMiniOrderView.as_view(), name='order-mini-return'),
    path('mini/cancel/<int:pk>/', views.CancelMiniOrderView.as_view(), name='order-mini-cancel'),

    # Payment
    path('checkout/', views.CheckoutView.as_view(), name='order-checkout'),
    path('checkout/pod/', views.payment_pod, name='order-pod'), 


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
