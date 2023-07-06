from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [

    # Products
    path('list/', views.ProductListView.as_view(), name='product-list-view'),
    path('in-house-store/', views.InHouseStore.as_view(), name='in-House-Store-view'),
    path('detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail-view'),

    # Favorite
    path('favorite/add/<int:pk>/', views.FavoriteAddView.as_view(), name='product-favorite-add'),
    path('favorite/remove/<int:pk>/', views.FavoriteRemoveView.as_view(), name='product-favorite-remove'),
    path('favorite/list/', views.FavoriteListView.as_view(), name='product-favorite-list'),

    # Review
    path('review/add/<int:pk>/', views.ReviewAddView.as_view(), name='product-review-add'),
    path('review/update/<int:pk>/', views.ReviewUpdateView.as_view(), name='product-review-update'),
    path('review/delete/<int:pk>/', views.ReviewDeleteView.as_view(), name='product-review-delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

