from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.shortcuts import (
    get_object_or_404, redirect, render
)
from django.utils import timezone
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from forex_python.converter import CurrencyRates
import datetime
from django.conf import settings
from products.models import Product, Variation
from users.forms import AddressForm
from users.models import Address
from .forms import CouponCustomerForm
from .models import (
    Cart, Order, MiniOrder, Payment, ReturnMiniOrder, CancelMiniOrder, CouponCustomer, Coupon
)
from .filters import OrderFilter
import razorpay
import requests
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from vowsnviews.local_settings import razorpay_api, razorpay_secret


# Cart
# Add to cart # Test Done
@login_required
def add_to_cart(request, slug, buy_now=None):
    product = get_object_or_404(Product, slug=slug)
    cart, created = Cart.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
        # size=size,
        # color=color
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.cart.filter(product=product).exists():
            # and order.cart.filter(color=color) and order.cart.filter(size=size):
            if cart.product.stock_no and cart.quantity >= cart.product.stock_no:
                cart.quantity = cart.product.stock_no
                messages.info(request, "No more stock .")
                if buy_now == 'buy_now':
                    return redirect("order-checkout")
                return redirect("order-view-cart")
            else:
                cart.quantity += 1
                cart.save()
                # m_order = MiniOrder.objects.filter(order_ref_number=order.order_ref_number)
                messages.info(request, "Product quantity was updated.")
                if buy_now == 'buy_now':
                    return redirect("order-checkout")
                return redirect("order-view-cart")
        else:
            order.cart.add(cart)
            # cart.save()
            order.save()

            ordered_date_time = timezone.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            m_order = MiniOrder.objects.create(
                ordered_date_time=ordered_date_time, user=request.user,
                order_ref_number=order.order_ref_number, cart=cart)
            m_order.mini_order_ref_number = f"MORN-{100000 + int(m_order.id)}"
            m_order.save()

            order.mini_order.add(m_order)
            order.save()
            messages.info(request, "product was added to your cart.")
            if buy_now == 'buy_now':
                return redirect("order-checkout")
            return redirect('product-detail-view', pk=product.id)
    else:
        ordered_date_time = timezone.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        order = Order.objects.create(
            user=request.user, ordered_date_time=ordered_date_time)  # vendor=product.sold_by
        ORN = f"ORN-{100000 + int(order.id)}"
        order.order_ref_number = ORN
        order.cart.add(cart)
        order.save()

        m_order = MiniOrder.objects.create(
            ordered_date_time=ordered_date_time, user=request.user,
            order_ref_number=ORN, cart=cart)
        m_order.mini_order_ref_number = f"MORN-{100000 + int(m_order.id)}"
        m_order.save()

        order.mini_order.add(m_order)
        user_address = request.user.address.filter(default=True).first()
        if user_address:
            order.address = user_address
        order.save()

        messages.info(request, "product was added to your cart.")
    if buy_now == 'buy_now':
        return redirect("order-checkout")
    return redirect('product-detail-view', pk=product.id)


@login_required
def add_to_cart_variation(request, slug=None, pk=None):
    buy_now = None
    if request.method == 'POST':
        product_var = []
        for item in request.POST:
            key = item  # option data that end user sees
            val = request.POST[key]  # value passed
            print(key, 'key')
            print(val, 'val')
            if val == 'buy_now':
                buy_now = val
            try:
                variation_query = Variation.objects.get(id=val)
                product_var.append(variation_query)
            except:
                pass
        product = get_object_or_404(Product, slug=slug)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            cart_query = order.cart.filter(product=product)
            if cart_query.exists():
                for cart in cart_query:
                    try:
                        if cart.variation.all()[0] in product_var and cart.variation.all()[1] in product_var:
                            # Product with variation in cart
                            if cart.product.stock_no and cart.quantity >= cart.product.stock_no:
                                cart.quantity = cart.product.stock_no
                            else:
                                cart.quantity += 1
                                cart.save()
                            messages.info(request, "Product quantity was increased.")
                            if buy_now == 'buy_now':
                                return redirect("order-checkout")
                            return redirect("order-view-cart")
                    except IndexError:
                        if cart.variation.all()[0] in product_var and cart.variation.all().count() == 1:
                            if cart.product.stock_no and cart.quantity >= cart.product.stock_no:
                                cart.quantity = cart.product.stock_no
                            else:
                                cart.quantity += 1
                                cart.save()
                            messages.info(request, "Product quantity was increased.")
                            if buy_now == 'buy_now':
                                return redirect("order-checkout")
                            return redirect("order-view-cart")
                else:
                    # Product with out variation in cart
                    cart = Cart.objects.create(
                        product=product,
                        user=request.user,
                        ordered=False,
                    )
                    cart.variation.add(*product_var)  # Adding list of variation to cart using *
                    cart.save()

                    order.cart.add(cart)
                    order.save()

                    ordered_date_time = timezone.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    m_order = MiniOrder.objects.create(
                        ordered_date_time=ordered_date_time, user=request.user,
                        order_ref_number=order.order_ref_number, cart=cart)
                    m_order.mini_order_ref_number = f"MORN-{100000 + int(m_order.id)}"
                    m_order.save()

                    order.mini_order.add(m_order)
                    messages.info(request, "Product was added to your cart.")
                    if buy_now == 'buy_now':
                        return redirect("order-checkout")
                    return redirect('product-detail-view', pk=product.id)
            else:
                # Product with out variation in cart
                cart = Cart.objects.create(
                    product=product,
                    user=request.user,
                    ordered=False,
                )
                cart.variation.add(*product_var)  # Adding list of variation to cart using *
                cart.save()

                order.cart.add(cart)
                order.save()

                ordered_date_time = timezone.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                m_order = MiniOrder.objects.create(
                    ordered_date_time=ordered_date_time, user=request.user,
                    order_ref_number=order.order_ref_number, cart=cart)
                m_order.mini_order_ref_number = f"MORN-{100000 + int(m_order.id)}"
                m_order.save()

                order.mini_order.add(m_order)
                order.save()
                messages.info(request, "Product was added to your cart.")
                if buy_now == 'buy_now':
                    return redirect("order-checkout")
                return redirect('product-detail-view', pk=product.id)
        else:
            cart = Cart.objects.create(
                product=product,
                user=request.user,
                ordered=False,
            )
            cart.variation.add(*product_var)  # Adding list of variation to cart using *
            cart.save()

            ordered_date_time = timezone.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            order = Order.objects.create(
                user=request.user, ordered_date_time=ordered_date_time)  # vendor=product.sold_by
            ORN = f"ORN-{100000 + int(order.id)}"
            order.order_ref_number = ORN
            order.cart.add(cart)
            order.save()

            m_order = MiniOrder.objects.create(
                ordered_date_time=ordered_date_time, user=request.user,
                order_ref_number=ORN, cart=cart)
            m_order.mini_order_ref_number = f"MORN-{100000 + int(m_order.id)}"
            m_order.save()

            order.mini_order.add(m_order)
            user_address = request.user.address.filter(default=True).first()
            if user_address:
                order.address = user_address
            order.save()

            messages.info(request, "Product was added to your cart.")
        if buy_now == 'buy_now':
            return redirect("order-checkout")
        return redirect('product-detail-view', pk=product.id)
    else:
        cart = Cart.objects.get(pk=pk)
        if cart.product.stock_no and cart.quantity >= cart.product.stock_no:
            cart.quantity = cart.product.stock_no
        else:
            cart.quantity += 1
            cart.save()
        messages.info(request, "Product quantity was increased.")
        return redirect("order-view-cart")

        
@login_required
def remove_product_from_cart(request, pk):
    cart = Cart.objects.get(id=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            order.cart.remove(cart)
            cart.delete()
            # Mini Order gets deleted automatic after deleting cart
        messages.info(request, "Product quantity was decreased.")
        return redirect("order-view-cart")
    else:
        messages.info(request, "You don't have any product in your cart.")
        return redirect("/")


@login_required
def delete_cart(request, pk):
    cart = Cart.objects.get(id=pk)
    if cart.user == request.user:
        cart.delete()
        messages.info(request, "Product Removed form cart.")
    else:
        messages.info(request, "Not Authorized.")
    return redirect("order-view-cart")


# Show Products in cart
class CartListView(LoginRequiredMixin, ListView):
    model = Cart
    # Template name cart_list.html
    # object_list variable name

    # Filter queryset to show only login in user's cart and no show ordered product
    def get_queryset(self):
        qs = self.model.objects.filter(ordered=False, user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # form = CouponCustomerForm()
        # context['form'] = form
        context['order'] = Order.objects.filter(user=self.request.user, ordered=False).first()
        return context

    # def post(self, form, **kwargs):
    #     form = CouponCustomerForm(self.request.POST)
    #     if form.is_valid():
    #         try:
    #             coupon_form = form.save(commit=False)
    #             coupon_form.user = self.request.user
    #             coupon_form.save()
    #             coupon = coupon_form
    #         except IntegrityError:
    #             coupon_form = form.save(commit=False)
    #             coupon = CouponCustomer.objects.get(code=coupon_form.code, user=self.request.user)
    #             if coupon.used is True:
    #                 messages.info(self.request, f'Coupon Already Used!')
    #                 return redirect("order-view-cart")
    #         order = Order.objects.get(user=self.request.user, ordered=False)
    #         # coupon.discount_amount = 0
    #         order_amount = order.get_total_without_coupon()
    #         # coupon.save()
    #         vendor_coupon = Coupon.objects.get(code=coupon.code)
    #         if order_amount >= vendor_coupon.minimum_order_amount:
    #             coupon.discount_amount = order_amount * (vendor_coupon.discount_percent / 100)
    #             coupon.coupon = vendor_coupon
    #             coupon.save()
    #
    #             # Adding Coupon to order
    #             order.coupon_customer = coupon
    #             order.coupon_used = True
    #             order.save()
    #             messages.success(self.request, f'Coupon Applied!')
    #     return redirect("order-view-cart")


# Order
# Show all order
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 20
    # Template name order_list.html
    # object_list variable name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['order'] = Order.objects.filter(ordered=True)

        current_query = self.object_list
        # current_query = Order.objects.all()
        order_filter = OrderFilter(self.request.GET, queryset=current_query)
        context['filter'] = order_filter
        if len(order_filter.qs) != current_query.count():
            context['object_list'] = order_filter.qs
            if len(order_filter.qs) < self.paginate_by:
                context['is_paginated'] = False
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user, ordered=True)
        return queryset


# Detail Order
class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Order
    # Template name order_detail.html
    # object_list variable name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # .strftime('%Y-%m-%d %H:%M:%S')
        return context

    def test_func(self):
        model = self.get_object()
        return self.request.user == model.user


# Cancel Mini Order
class CancelMiniOrderView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CancelMiniOrder
    fields = ['cancel_reason', 'review_description']
    # template name cancelminiorder_form.html

    def form_valid(self, form):
        cancel_form = form.instance
        cancel_form.user = self.request.user
        cancel_form.save()

        mini_order = MiniOrder.objects.get(id=self.kwargs.get('pk'))
        mini_order.cancel_requested = True
        mini_order.save()

        cancel_form.cancel_mini_order = mini_order
        cancel_form.save()

        return super().form_valid(form)

    def test_func(self):
        mini_order = MiniOrder.objects.get(id=self.kwargs.get('pk'))
        if not mini_order.user == self.request.user:
            return False
        elif mini_order.order_status not in ['Preparing', 'Shipping']:
            return False
        elif mini_order.cancel_requested is True:
            return False
        elif mini_order.return_requested is True:
            return False
        else:
            return True


# Return Mini Order
class ReturnMiniOrderView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ReturnMiniOrder
    fields = ['return_reason', 'review_description']
    # template name returnminiorder_form.html

    def form_valid(self, form):
        return_form = form.instance
        return_form.user = self.request.user
        return_form.save()

        mini_order = MiniOrder.objects.get(id=self.kwargs.get('pk'))
        mini_order.return_requested = True
        mini_order.save()

        return_form.return_mini_order = mini_order
        return_form.save()
        return super().form_valid(form)

    def test_func(self):
        mini_order = MiniOrder.objects.get(id=self.kwargs.get('pk'))
        if not mini_order.user == self.request.user:
            return False
        elif not mini_order.order_status == 'Delivered':
            return False
        elif mini_order.cancel_requested is True:
            return False
        elif mini_order.return_requested is True:
            return False
        else:
            return True


# Checkout
class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.filter(user=self.request.user, ordered=False)
        order = Order.objects.get(user=self.request.user, ordered=False)
        
        address_form = AddressForm()

        amount = int(order.get_total())
        order_currency = self.request.user.currency
        converter = CurrencyRates()
        try:
            amount = converter.convert('INR', self.request.user.currency, amount)
        except:
            pass
        amount = int(amount) * 100
        client = razorpay.Client(auth=(razorpay_api, razorpay_secret))
        razorpay_payment = client.order.create(
            {
                'amount': amount,
                'currency': order_currency,
                'payment_capture': 0
            }
        )

        context = {
            'cart_query': cart,
            'address_form': address_form,
            'amount': amount,
            'order_currency': order_currency,
            'order_id': razorpay_payment['id'],
            'order': order
        }
        return render(self.request, 'order/checkout.html', context)

    def post(self, *args, **kwargs):
        address_form = AddressForm(self.request.POST)
        order = Order.objects.filter(user=self.request.user, ordered=False).first()
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            if address_form.default is True:
                Address.objects.filter(default=True, user=self.request.user).update(default=False)
            if address_form.default is False:
                add_count = Address.objects.filter(default=True, user=self.request.user).count()
                if add_count == 0:
                    address_form.default = True
            address_form.save()
            self.request.user.address.add(address_form)
            order.address = address_form
            order.save()

            # try:
            address_id = self.request.POST.get('active-address', False)
            if address_id:
                address = Address.objects.get(id=address_id)
                order.address = address
                order.save()
            messages.success(self.request, "Address Updated")
            return redirect('order-checkout')
            # except:
            #     pass
        address_id = self.request.POST.get('active-address', False)
        if address_id:
            try:
                address = Address.objects.get(id=address_id)
                order.address = address
                order.save()
                messages.success(self.request, "Address Updated")
                return redirect('order-checkout')
            except:
                messages.warning(self.request, "Address Error")
                return redirect('order-checkout')

        amount = int(order.get_total())
        order_currency = self.request.user.currency

        converter = CurrencyRates()
        try:
            amount = converter.convert('INR', self.request.user.currency, amount)
        except:
            pass
        amount = int(amount) * 100

        # Convert Currency ..
        payment_id = self.request.POST.get('user_id', False)
        if not payment_id:
            return redirect('order-checkout')

        elif order.address:
            client = razorpay.Client(auth=(razorpay_api, razorpay_secret))
            order_id = self.request.POST.get('payment_id', False)
            razorpay_payment = client.order.fetch(order_id)

            razor_payment_api_url = f'https://api.razorpay.com/v1/orders/{razorpay_payment["id"]}/payments'
            r = requests.get(razor_payment_api_url, auth=(razorpay_api, razorpay_secret))
            payment_details = r.json()

            # raise Exception
            payment = Payment()
            payment.user = self.request.user
            payment.amount = amount
            payment.order_id = razorpay_payment['id']
            payment.payment_id = payment_details['items'][0]['id']
            payment.currency = order_currency
            payment.amount_paid = razorpay_payment['amount_paid']
            payment.payment_method = payment_details['items'][0]['method']
            payment.save()

            cart = order.cart.all()
            for cart_object in cart:
                if cart_object.product.stock_no:
                    cart_object.product.stock_no = int(cart_object.product.stock_no) - cart_object.quantity
                    cart_object.product.save()

            mini_order = order.mini_order.all()
            for m_order in mini_order:
                m_order.cart.ordered = True
                m_order.save()

            ordered_date_time = timezone.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            order.ordered_date_time = ordered_date_time

            # Checking if coupon is applied.
            # if order.coupon_used:
            #     coupon_customer = CouponCustomer.objects.get(id=order.coupon_customer.id)
            #     coupon_customer.used = True
            #     coupon_customer.save()
            cart.update(ordered=True)
            mini_order.update(ordered=True)

            order.payment = payment
            order.ordered = True
            order.save()

            payment.paid = True
            payment.save()
            send_invoice(self.request, order, self.request.user)
            messages.success(self.request, "Your order was successful!")
            return redirect('order-all')
        else:
            messages.warning(self.request, "Please select or add delivery address!")
            return redirect('order-checkout')


@login_required
def payment_pod(request):
    order = Order.objects.filter(user=request.user, ordered=False).first()
    if order.address:

        amount = int(order.get_total())
        order_currency = request.user.currency
    
        converter = CurrencyRates()
        try:
            amount = converter.convert('INR', request.user.currency, amount)
        except:
            pass
        amount = int(amount) * 100
    
        # Convert Currency ..
        # payment_id = self.request.POST.get('payment_id', False)
        # if not payment_id:
        #     return redirect('order-checkout')
    
        # elif self.request.user.address.all().exists():
        # client = razorpay.Client(auth=(razorpay_api, razorpay_secret))
        # razorpay_payment = client.order.create(
        #     {
        #         'amount': amount,
        #         'currency': order_currency,
        #         'payment_capture': 1
        #     }
        # )
        payment = Payment()
        payment.user = request.user
        payment.amount = amount
        payment.order_id = f'{request.user.id}_{timezone.datetime.now()}'
        payment.payment_id = f'{request.user.id}_{timezone.datetime.now()}'
        payment.currency = order_currency
        payment.amount_paid = 0
        payment.payment_method = "Pay on delivery"
        payment.save()

        cart = order.cart.all()
        for cart_object in cart:
            if cart_object.product.stock_no:
                cart_object.product.stock_no = int(cart_object.product.stock_no) - cart_object.quantity
                cart_object.product.save()

        mini_order = order.mini_order.all()
        for m_order in mini_order:
            m_order.cart.ordered = True
            m_order.save()

        ordered_date_time = timezone.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        order.ordered_date_time = ordered_date_time

        # Checking if coupon is applied.
        # if order.coupon_used:
        #     coupon_customer = CouponCustomer.objects.get(id=order.coupon_customer.id)
        #     coupon_customer.used = True
        #     coupon_customer.save()
        cart.update(ordered=True)
        mini_order.update(ordered=True)

        order.payment = payment
        order.ordered = True
        order.order_id = payment.order_id 
        order.save()

        payment.paid = True
        payment.save()

        send_invoice(request, order, request.user)

        messages.success(request, "Your order was successful!")
        return redirect('order-all')
    else:
        messages.warning(request, "Please select or add delivery address!")
        return redirect('order-checkout')


class OrderInvoiceView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs.get('pk'))
        context = {
            'order': order
            }
        return render(self.request, 'order/invoice.html', context)

    def test_func(self):
        order = Order.objects.get(id=self.kwargs.get('pk'))
        return order.user == self.request.user


def send_invoice(request, order, user):
    context = {
        'order': order
    }
    message = get_template('order/invoice.html').render(context)
    email = EmailMessage(
        f'Order Invoice',
        message,
        settings.AUTH_USER_MODEL,
        [user.email],
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)
