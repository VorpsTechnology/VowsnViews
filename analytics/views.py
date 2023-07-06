from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.template.defaultfilters import slugify
from django.shortcuts import redirect, reverse, render
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import JsonResponse, HttpResponse

from listing.filters import DraftListingFilter
from listing.models import DraftListing, Listing, Area, AddititionalPricing, SubListingLocation, ListingCategory
from order.models import (
    MiniOrder, Order, ReturnMiniOrder, CancelMiniOrder, Cart
)
from products.models import (
    Product, Variation, Category, ParentCategory
)
from products.filters import ProductFilter
from home.models import NewsLetter, Contact
from vendors.models import VenueFAQ
from .forms import MiniOrderStatusForm, ReturnMiniOrderStatusForm, CancelMiniOrderStatusForm, SendBulkMailForm, \
    ListingUpdateVendorsAssign
from .filters import CategoryFilter, ReturnFilter, CancelFilter, MiniOrderFilter, ParentCategoryFilter, ContactFilter
from users.models import User, Vendor

# import datetime
from datetime import datetime, timedelta

today = datetime.now().date()
yesterday = today + timedelta(-1)


class AnalyticsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "analytics/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_count = Order.objects.all().count
        contact = Contact.objects.all().count
        order_count_toady = Order.objects.filter(ordered_date_time__gte=yesterday).count
        contact_toady = Contact.objects.filter(date__gte=yesterday).count

        context['order_count'] = order_count
        context['order_count_toady'] = order_count_toady
        context['contact_today'] = contact_toady
        context['contact_count'] = contact
        return context

    def test_func(self):
        return self.request.user.is_superuser is True


# Orders
# Return View
class AdminReturnListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ReturnMiniOrder
    template_name = 'analytics/return_morder_list_admin.html'
    paginate_by = 20

    # object_list variable name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = self.object_list
        return_filter = ReturnFilter(self.request.GET, queryset=current_query)
        context['filter'] = return_filter
        if len(return_filter.qs) != len(current_query):
            context['object_list'] = return_filter.qs
            if len(return_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def test_func(self):
        return self.request.user.is_superuser is True


# Order Detail View Admin
class AdminReturnDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MiniOrder
    context_object_name = 'mini_order'
    template_name = "analytics/return_detail_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReturnMiniOrderStatusForm(instance=self.object.returnminiorder_set.all().first())
        return context

    def post(self, form, **kwargs):
        mini_order = MiniOrder.objects.get(pk=self.kwargs.get('pk'))
        form = ReturnMiniOrderStatusForm(self.request.POST, instance=mini_order.returnminiorder_set.all().first())
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            if form.return_status == 'Return Granted':
                mini_order.order_status = 'RETURNED'
                mini_order.save()
        return redirect("admin-order-return-detail", pk=self.kwargs.get('pk'))

    def test_func(self):
        return self.request.user.is_superuser is True


# Cancel View
class AdminCancelListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CancelMiniOrder
    paginate_by = 20
    template_name = 'analytics/cancel_morder_list_admin.html'

    # object_list variable name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = self.object_list
        cancel_filter = CancelFilter(self.request.GET, queryset=current_query)
        context['filter'] = cancel_filter
        if len(cancel_filter.qs) != len(current_query):
            context['object_list'] = cancel_filter.qs
            if len(cancel_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def test_func(self):
        return self.request.user.is_superuser is True


# Order Detail View Admin
class AdminCancelDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MiniOrder
    context_object_name = 'mini_order'
    template_name = "analytics/cancel_detail_admin.html"

    # Template name order_detail.html
    # object_list variable name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CancelMiniOrderStatusForm(instance=self.object.cancelminiorder_set.all().first())

        return context

    def post(self, form, **kwargs):
        mini_order = MiniOrder.objects.get(pk=self.kwargs.get('pk'))
        form = CancelMiniOrderStatusForm(self.request.POST, instance=mini_order.cancelminiorder_set.all().first())
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            if form.cancel_status == 'Cancel Granted':
                mini_order.order_status = 'CANCELED'
                mini_order.save()
        return redirect("admin-order-cancel-detail", pk=self.kwargs.get('pk'))

    def test_func(self):
        return self.request.user.is_superuser is True


class AdminNotOrderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Cart
    paginate_by = 20
    queryset = Cart.objects.filter(ordered=False)
    template_name = "analytics/cart_list_admin.html"

    def test_func(self):
        return self.request.user.is_superuser is True


class AdminOrderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = MiniOrder
    paginate_by = 20
    queryset = MiniOrder.objects.filter(ordered=True)
    context_object_name = 'mini_order'
    template_name = "analytics/order_list_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['order'] = Order.objects.filter(ordered=True)

        current_query = self.object_list
        # current_query = Order.objects.all()
        order_filter = MiniOrderFilter(self.request.GET, queryset=current_query)
        context['filter'] = order_filter
        if len(order_filter.qs) != len(current_query):
            context['object_list'] = order_filter.qs
            if len(order_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def test_func(self):
        return self.request.user.is_superuser is True


# Order Detail View Admin
class AdminOrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MiniOrder
    context_object_name = 'mini_order'
    template_name = "analytics/order_detail_admin.html"

    # Template name order_detail.html
    # object_list variable name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(mini_order=self.object)
        context['now'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        context['form'] = MiniOrderStatusForm(instance=self.object)
        return context

    def post(self, form, **kwargs):
        mini_order = MiniOrder.objects.get(pk=self.kwargs.get('pk'))
        form = MiniOrderStatusForm(self.request.POST, instance=mini_order)
        if form.is_valid():
            m_form = form.save(commit=False)
            if m_form.order_status == 'Delivered':
                time = datetime.now() + timedelta(days=10)  # adding 10 days for return
                mini_order.return_window = time.strftime('%Y-%m-%d %H:%M:%S')
                mini_order.save()
            m_form.save()
        return redirect("admin-order-detail", pk=self.kwargs.get('pk'))

    def test_func(self):
        return self.request.user.is_superuser is True


# ----------------------------------------------------------------------------------------------------------------------
# Add Variation
class AdminVariationAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Variation
    fields = ['title', 'category', 'color_code', 'product_size', 'price', 'discount_price']
    template_name = "analytics/variation_add_update_admin.html"

    def form_valid(self, form):
        product = Product.objects.get(id=self.kwargs['pk'])
        form.instance.product = product
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser is True


# Update ParentCategory
class AdminVariationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Variation
    fields = ['title', 'category', 'color_code', 'product_size', 'price', 'discount_price']
    template_name = "analytics/variation_add_update_admin.html"

    def test_func(self):
        return self.request.user.is_superuser is True


# Delete ParentCategory
class AdminVariationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Variation
    fields = ['title', 'category', 'color_code', 'product_size', 'price', 'discount_price']
    template_name = "analytics/variation_confirm_delete.html"

    def get_success_url(self):
        return reverse("admin-product-detail", kwargs={'pk': self.kwargs['product_id']})

    def test_func(self):
        return self.request.user.is_superuser is True


# Products
class AdminProductListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    paginate_by = 40
    template_name = "analytics/product_list_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = Product.objects.all()
        product_filter = ProductFilter(self.request.GET, queryset=current_query)
        context['filter'] = product_filter

        if len(product_filter.qs) != len(current_query):
            context['object_list'] = product_filter.qs
            if len(product_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def test_func(self):
        return self.request.user.is_superuser is True


# Product Detail View
class AdminProductDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Product
    template_name = "analytics/product_detail_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs.get('pk'))

        price = product.price
        discount_price = product.discount_price

        context['object'] = product
        context['discount_percent'] = int(100 - ((discount_price / price) * 100))
        return context

    def test_func(self):
        return self.request.user.is_superuser is True


# Add Products
class AdminProductAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    fields = ['title', 'price', 'discount_price', 'category', 'f_category', 'gender', 'brand', 'label', 'stock_no',
              'short_description', 'description', 'image_main', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6',
              'image_7', 'image_8', 'image_9', 'image_10', 'image_main_link', 'image_2_link', 'image_3_link',
              'image_4_link', 'image_5_link', 'image_6_link', 'image_7_link', 'image_8_link', 'image_9_link',
              'image_10_link', 'video_1', 'video_2', 'video_3', 'video_4', 'video_5', 'video_6', 'video_7', 'video_8',
              'video_9', 'video_10', 'is_active', 'luxury_couture', 'trending', 'vendor_name']
    template_name = "analytics/product_add_update_admin.html"

    def form_valid(self, form):
        product = form.save(commit=False)
        product.slug = slugify(product.title)
        product.save()
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser is True


# Update Products
class AdminProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title', 'price', 'discount_price', 'category', 'f_category', 'gender', 'brand', 'label', 'stock_no',
              'short_description', 'description', 'image_main', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6',
              'image_7', 'image_8', 'image_9', 'image_10', 'image_main_link', 'image_2_link', 'image_3_link',
              'image_4_link', 'image_5_link', 'image_6_link', 'image_7_link', 'image_8_link', 'image_9_link',
              'image_10_link', 'video_1', 'video_2', 'video_3', 'video_4', 'video_5', 'video_6', 'video_7', 'video_8',
              'video_9', 'video_10', 'is_active', 'luxury_couture', 'trending', 'vendor_name']
    template_name = "analytics/product_add_update_admin.html"

    def test_func(self):
        return self.request.user.is_superuser is True


# Delete Products
class AdminProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    fields = ['title', 'price', 'discount_price', 'category', 'f_category', 'gender', 'brand', 'label', 'stock_no',
              'short_description', 'description', 'image_main', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6',
              'image_7', 'image_8', 'image_9', 'image_10', 'image_main_link', 'image_2_link', 'image_3_link',
              'image_4_link', 'image_5_link', 'image_6_link', 'image_7_link', 'image_8_link', 'image_9_link',
              'image_10_link', 'video_1', 'video_2', 'video_3', 'video_4', 'video_5', 'video_6', 'video_7', 'video_8',
              'video_9', 'video_10', 'is_active', 'vendor_name']
    success_url = '/analytics/product/list-admin/'
    template_name = "analytics/product_confirm_delete.html"

    def test_func(self):
        return self.request.user.is_superuser is True


# Category
# Show all Category
class AdminCategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Category
    paginate_by = 10
    template_name = "analytics/category_list_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = Category.objects.all()
        category_filter = CategoryFilter(self.request.GET, queryset=current_query)
        context['filter'] = category_filter
        if len(category_filter.qs) != len(current_query):
            context['object_list'] = category_filter.qs
            if len(category_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def test_func(self):
        return self.request.user.is_superuser is True


# Add Category
class AdminCategoryAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    fields = ['title', 'parent_category', 'description', 'image']
    template_name = "analytics/category_add_update_admin.html"

    # template name category_form

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser is True


# Update Category
class AdminCategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['title', 'parent_category', 'description', 'image']
    template_name = "analytics/category_add_update_admin.html"

    # template name category_form

    def test_func(self):
        return self.request.user.is_superuser is True


# Delete Category
class AdminCategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    fields = ['title', 'parent_category', 'description', 'image']
    success_url = '/analytics/category/list-admin/'
    template_name = "analytics/category_confirm_delete.html"

    def test_func(self):
        return self.request.user.is_superuser is True


# Show all ParentCategory
class AdminParentCategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ParentCategory
    paginate_by = 10
    template_name = "analytics/parent_category_list_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = ParentCategory.objects.all()
        category_filter = ParentCategoryFilter(self.request.GET, queryset=current_query)
        context['filter'] = category_filter
        if len(category_filter.qs) != len(current_query):
            context['object_list'] = category_filter.qs
            if len(category_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def test_func(self):
        return self.request.user.is_superuser is True


# Add ParentCategory
class AdminParentCategoryAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ParentCategory
    fields = ['title', 'description', 'image']
    template_name = "analytics/parent_category_add_update_admin.html"

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser is True


# Update ParentCategory
class AdminParentCategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ParentCategory
    fields = ['title', 'description', 'image']
    template_name = "analytics/parent_category_add_update_admin.html"

    def test_func(self):
        return self.request.user.is_superuser is True


# Delete ParentCategory
class AdminParentCategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ParentCategory
    fields = ['title', 'description', 'image']
    success_url = '/analytics/parent/category/list-admin/'
    template_name = "analytics/parent_category_confirm_delete.html"

    def test_func(self):
        return self.request.user.is_superuser is True


# SEND BULK MAIL
class SendMail(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = SendBulkMailForm
    template_name = 'analytics/send_bulk_mail.html'
    success_url = '/'

    def form_valid(self, form):
        form = form.cleaned_data
        email_subject = form['title']
        email_body = form['body']
        email = NewsLetter.objects.all()
        email_2 = User.objects.all()
        email_3 = Contact.objects.all()

        email = [e.email for e in email]
        email_2 = [e.email for e in email_2]
        email_3 = [e.email for e in email_3]
        email += email_2 + email_3
        email = list(set(email))

        email = EmailMessage(
            email_subject,
            email_body,
            settings.AUTH_USER_MODEL,
            email,
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
        return redirect('admin-dashboard')

    def test_func(self):
        return self.request.user.is_superuser is True


class AdminContactListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Contact
    paginate_by = 40
    # Template name category_list_admin.html
    # object_list variable name
    template_name = "analytics/contact_list_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_query = Contact.objects.all()
        category_filter = ContactFilter(self.request.GET, queryset=current_query)
        context['filter'] = category_filter
        if len(category_filter.qs) != len(current_query):
            context['object_list'] = category_filter.qs
            if len(category_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def test_func(self):
        return self.request.user.is_superuser is True


class AdminContactUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Contact
    fields = ['name', 'email', 'mobile', 'description', 'city', 'read']
    template_name = "analytics/contact_update_admin.html"

    # template name category_form

    def test_func(self):
        return self.request.user.is_superuser is True


class AdminContactSeenUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, *args, **kwargs):
        contact = Contact.objects.filter(id=kwargs.get('pk')).first()
        if contact:
            contact.read = True
            contact.save()
            return redirect('admin-contact')

    def test_func(self):
        return self.request.user.is_superuser is True


class AdminReturnSeenUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, *args, **kwargs):
        return_mini = ReturnMiniOrder.objects.filter(id=kwargs.get('pk')).first()
        if return_mini:
            return_mini.read = True
            return_mini.save()
            return redirect('admin-order-return')

    def test_func(self):
        return self.request.user.is_superuser is True


class AdminCancelSeenUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, *args, **kwargs):
        cancel = CancelMiniOrder.objects.filter(id=kwargs.get('pk')).first()
        if cancel:
            cancel.read = True
            cancel.save()
            return redirect('admin-order-cancel')

    def test_func(self):
        return self.request.user.is_superuser is True


class MiniOrderSeenUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, *args, **kwargs):
        cancel = MiniOrder.objects.filter(id=kwargs.get('pk')).first()
        if cancel:
            cancel.read = True
            cancel.save()
            return redirect('admin-order-cancel')

    def test_func(self):
        return self.request.user.is_superuser is True


class ListingCopyView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, *args, **kwargs):
        listing_all = Listing.objects.all()

        for listing in listing_all:
            draft_listing = DraftListing()
            if not DraftListing.objects.filter(slug=listing.slug).first():
                for field in listing._meta.fields:
                    setattr(draft_listing, field.name, getattr(listing, field.name))
                draft_listing.save()
                for item in listing.photos.all():
                    draft_listing.photos.add(item)
                for item in listing.videos.all():
                    draft_listing.videos.add(item)
                for item in listing.review.all():
                    draft_listing.review.add(item)
                for item in listing.area.all():
                    draft_listing.area.add(item)
                for item in listing.additional_pricing.all():
                    draft_listing.additional_pricing.add(item)
                draft_listing.save()
            else:
                pass
        return render(self.request, 'analytics/copy_listing.html')

    def test_func(self):
        return self.request.user.is_superuser is True


class BlankDraftListingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = DraftListing
    template_name = 'analytics/blank_listing.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft_listing = DraftListing.objects.all()
        context['draft_listing'] = draft_listing
        vendors = Vendor.objects.all()
        context['vendors'] = vendors
        listing_present = []
        for vendor in vendors:
            if vendor.draft_listing:
                listing_present.append(vendor.draft_listing.id)
        context['listing_present'] = listing_present
        current_query = DraftListing.objects.all()
        listing_filter = DraftListingFilter(self.request.GET, queryset=current_query)
        context['filter'] = listing_filter
        if len(listing_filter.qs) != len(current_query):
            context['object_list'] = listing_filter.qs
            if len(listing_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        sub_locations = SubListingLocation.objects.all()
        sub_category = ListingCategory.objects.all()
        context['sub_locations'] = sub_locations
        context['sub_categorys'] = sub_category
        return context

    def test_func(self):
        return self.request.user.is_superuser is True


class BlankListingUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DraftListing
    form_class = ListingUpdateVendorsAssign
    template_name = 'analytics/assign_vendors_to_listing.html'

    def form_valid(self, form):
        path = self.request.POST.get('path', None)

        draft_listing = form.instance
        draft_listing.save()

        if path and '/assign/vendors/' in path:
            return redirect('vendor-assign-to-listing', pk=draft_listing.id)
        else:
            return HttpResponse("Draft Listing Updated")

    def form_invalid(self, form):
        draft_listing = self.object
        form = form
        vendors = Vendor.objects.all()
        return redirect('vendor-assign-to-listing', pk=draft_listing.id)

    def test_func(self):
        return self.request.user.is_superuser is True


class AssignVendorToListing(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, *args, **kwargs):
        id = self.kwargs.get('pk')
        draft_listing = DraftListing.objects.filter(id=id).first()

        form = ListingUpdateVendorsAssign(instance=draft_listing)
        vendors = Vendor.objects.all()
        for vendor in vendors:
            if vendor.draft_listing:
                if vendor.draft_listing.id == draft_listing.id:
                    messages.success(self.request, "Sorry, Listing already assigned to another vendor!")
                    return redirect('blank-listing-list')
                else:
                    pass
            else:
                pass

        return render(self.request, 'analytics/assign_vendors_to_listing.html',
                      {'draft_listing': draft_listing, 'vendors': vendors, 'form': form})

    def post(self, *args, **kwargs):
        listing_id = self.request.POST.get('post_listing_id')
        vendor_id = self.request.POST.get('post_vendor_id')

        draft_listing = DraftListing.objects.filter(id=int(listing_id)).first()
        vendor = Vendor.objects.filter(id=int(vendor_id)).first()
        if draft_listing and vendor:
            if not vendor.draft_listing:
                vendor.draft_listing = draft_listing
                listing = Listing.objects.filter(slug=draft_listing.slug).first()
                if not listing:
                    listing = copy_draftlisting_to_listing(self.request, draft_listing)
                if listing:
                    listing.is_active = True
                    listing.is_verified = True
                    listing.save()
                    vendor.listing = listing
                    draft_listing.is_faq_answered = False
                    draft_listing.is_approved = True
                    draft_listing.is_active = True
                    draft_listing.is_verified = True
                    draft_listing.save()
                    vendor.is_listing_on = False
                    vendor.save()
        messages.success(self.request, "Vendor Assigned Successfully!")
        return redirect('blank-listing-list')

    def test_func(self):
        return self.request.user.is_superuser is True


def copy_draftlisting_to_listing(request, draft_listing):
    listing = Listing()
    for field in draft_listing._meta.fields:
        setattr(listing, field.name, getattr(draft_listing, field.name))
    listing.save()
    area = draft_listing.area.all()
    if area:
        for item in area:
            single_area = Area.objects.get(id=item.id)
            listing.area.add(single_area)
        venueFaq = VenueFAQ(listing=listing)
        venueFaq.save()
    additional_pricing = draft_listing.additional_pricing.all()
    if additional_pricing:
        for item in additional_pricing:
            single_pricing = AddititionalPricing.objects.get(id=item.id)
            listing.additional_pricing.add(single_pricing)
    listing.save()
    for item in draft_listing.photos.all():
        listing.photos.add(item)
    for item in draft_listing.videos.all():
        listing.videos.add(item)
    for item in draft_listing.review.all():
        listing.review.add(item)
    listing.save()
    return listing


def get_vendor_detail(request):
    id = request.GET.get('id')
    vendor = Vendor.objects.get(id=int(id))
    return JsonResponse({
        'id': vendor.id,
        'name': vendor.vendor_user.user_full_name,
        'email': vendor.vendor_user.email,
        'phone_number': vendor.vendor_user.phone_number,
        'brand_name': vendor.brand_name,
        'website_link': vendor.website_link,
        'listing_parent_category': vendor.listing_parent_category.title,
        'listing_sub_category': vendor.listing_sub_category.title,
    })


def make_all_active_listing(request):
    listing = Listing.objects.all()
    for object in listing:
        object.is_active = True
        object.save()
        print("listing activated")
    products = Product.objects.all()
    for object in products:
        object.save()
        print("product activated")
    return HttpResponse("All Listing and Product are active now")
