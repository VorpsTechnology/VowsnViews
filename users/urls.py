from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # Customer
    # Login and Register
    path('profile/', views.DashboardFavoriteListView.as_view(), name='profile'),
    path('account/', TemplateView.as_view(template_name="users/manage_account.html"), name='user-account'),
    path('login/', views.LoginView.as_view(), name='users-login'),
    path('register/', views.SignUpView.as_view(), name='users-register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home/home.html'), name='users-logout'),

    path('checklist/', views.TaskView.as_view(), name='users-checklist'),
    path('checklist/delete/<int:pk>/', views.task_delete, name='users-checklist-delete'),

    path('guest/list/', views.GuestView.as_view(), name='users-guest-list'),
    path('guest/delete/<int:pk>/', views.guest_delete, name='users-guest-delete'),

    path('budget/', views.BudgetView.as_view(), name='users-budget-list'),
    path('budget/delete/<int:pk>/', views.budget_delete, name='users-budget-delete'),

    # Vendor Urls
    path('vendor/register/', views.VendorSignUpView.as_view(), name='vendor-register'),
    path('vendor/parent_listing/', views.get_listing_category, name='get-parent-category'),
    path('vendor/parent_listing/landing/', views.get_listing_category_landing, name='get-parent-category-landing'),
    
    # Update Username
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='users-update'),

    # User Username Verification
    path('resend-confirmation/', views.ResendMailConfirmationView.as_view(),
         name='users-resend-email-confirmation'),
    path('activate/<uidb64>/<token>',
         views.EmailVerificationView.as_view(), name='activate'),

    # Password
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'),
         name='password_change'),
    path('change-password-done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    # Address
    path('address/list/', views.AddressListView.as_view(), name='users-address-list'),
    path('address/add/', views.AddressAddView.as_view(), name='users-address-add'),
    path('address/update/<int:pk>/', views.AddressUpdateView.as_view(), name='users-address-update'),
    path('address/delete/<int:pk>/', views.AddressDeleteView.as_view(), name='users-address-delete'),
    
    
    path('blog/list/', views.BlogListView.as_view(), name='users-blog-list'),
    path('blog/detail/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail-view'),
    path('blog/add/', views.BlogAddView.as_view(), name='users-blog-add'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
