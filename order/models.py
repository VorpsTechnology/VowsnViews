from django.db import models
from django.utils import timezone
from django.shortcuts import reverse

from users.models import User, Address
from products.models import Product, Variation
from django.contrib.auth.decorators import login_required

import datetime

# Order
ORDER_STATUS = (
    ('Preparing', 'Preparing'),
    ('Shipping', 'Shipping'),
    # ('Picked up from store', 'Picked up from store'),
    # ('Out for delivery', 'Out for delivery'),
    ('Delivered', 'Delivered'),
    ('RETURNED', 'RETURNED'),
    ('CANCELED', 'CANCELED')
)

# Return
RETURN_STATUS = (
    ('Processing Return Request', 'Processing Return Request'),
    ('Item Received by Vendor', 'Item Received by Vendor'),
    ('Return Denied', 'Return Denied'),
    ('Return Granted', 'Return Granted'),
)


RETURN_REASON = (
    ('Damaged', 'Damaged'),
    ('Expired', 'Expired'),
    ('Ordered Wrong Item', 'Ordered Wrong Item'),
    ('Received Wrong Item', 'Received Wrong Item'),
    ('Received Wrong Brand Item', 'Received Wrong Brand Item'),  # may be variation
    ('Other', 'Other')
)


# Cancel
CANCEL_REASON = (
    ('Not Needed', 'Not Needed'),
    ('Ordered Wrong Product', 'Ordered Wrong Product'),
    ('Receiving To Late', 'Receiving To Late'),
    ('Select Different Payment Method', 'Select Different Payment Method'),
    ('Other', 'Other')
)

CANCEL_STATUS = (
    ('Processing Cancel Request', 'Processing Cancel Request'),
    ('CANCEL Denied', 'CANCEL Denied'),
    ('Cancel Granted', 'Cancel Granted'),
)


# Cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    variation = models.ManyToManyField(Variation)
    # variation = models.ForeignKey(Variation, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def get_total_item_price(self):
        if self.variation.all().exists():
            return self.get_variation_price()
        return self.quantity * self.product.price

    def get_total_discount_item_price(self):
        if self.variation.all().exists():
            for var in self.variation.all():
                if var.category == 'size':
                    return self.quantity * var.discount_price
            for var in self.variation.all():
                if var.category == 'color':
                    return self.quantity * var.discount_price
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        discount = self.get_total_item_price() - self.get_total_discount_item_price()
        if discount < 0:
            return 0
        else:
            return discount

    def get_final_price(self):
        return self.get_total_discount_item_price()

    def get_total_quantity(self):
        return self.quantity

    def get_absolute_url(self):  # Redirect to this link after changing quantity in cart  , kwargs={'slug': self.slug })
        return reverse("order-add-to-cart", kwargs={'slug': self.product.slug})

    def get_variation_price(self):
        for var in self.variation.all():
            if var.category == 'size':
                return self.quantity * var.price
        for var in self.variation.all():
            if var.category == 'color':
                return self.quantity * var.price
        return None
        
    def get_tax(self):
        amt = self.get_total_discount_item_price()
        return amt * 18 // 100

# Order

class Coupon(models.Model):
    code = models.CharField(max_length=15, unique=True)
    discount_percent = models.FloatField()
    minimum_order_amount = models.FloatField()

    def __str__(self):
        return self.code


class CouponCustomer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=15)
    discount_amount = models.FloatField(null=True)
    used = models.BooleanField(default=False)
    # applicable = models.BooleanField(default=False)

    class Meta:
        unique_together = ('code', 'user')

    def __str__(self):
        return f"{self.code}_{self.user}"


class MiniOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    order_ref_number = models.CharField(default='ORD-100000', max_length=15)
    mini_order_ref_number = models.CharField(unique=True, default='MORN-100000', max_length=15)

    ordered_date_time = models.DateTimeField(default=timezone.now)
    ordered = models.BooleanField(default=False)
    order_status = models.CharField(choices=ORDER_STATUS, max_length=50, default='Preparing')

    # delivered = models.BooleanField(default=False, blank=True, null=True)
    delivered_time = models.DateTimeField(default=timezone.now)  # 10 days Default

    # Return
    return_window = models.DateTimeField(default=timezone.now)  # 10 days Default
    return_requested = models.BooleanField(default=False)

    # Cancel
    cancel_requested = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    # Payment
    payment_method = models.CharField(default='Online by card', max_length=30)
    
    class Meta:
        ordering = ['-ordered_date_time']

    def __str__(self):
        return f"{self.cart.user} Mini_Order"

    @property
    def is_return_window(self):
        return timezone.now() < self.return_window


class ReturnMiniOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    return_requested = models.BooleanField(default=True)
    return_status = models.CharField(choices=RETURN_STATUS, max_length=50, default='Processing Return Request')
    return_granted = models.BooleanField(default=False)

    return_date = models.DateTimeField(default=timezone.now)
    return_reason = models.CharField(choices=RETURN_REASON, max_length=50, blank=True, null=True)
    review_description = models.TextField(help_text='Please Describe in detail reason of return.')

    return_mini_order = models.ForeignKey(MiniOrder, on_delete=models.SET_NULL, blank=True, null=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['return_date']

    def __str__(self):
        return f"{self.user}_{self.return_reason}_RETURNED"

    def get_absolute_url(self):  # Redirect to this link after filling the form for return order
        return reverse("order-all")


class CancelMiniOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    cancel_requested = models.BooleanField(default=True)
    cancel_status = models.CharField(choices=CANCEL_STATUS, max_length=50, default='Processing Cancel Request')
    cancel_granted = models.BooleanField(default=False)

    cancel_date = models.DateTimeField(default=timezone.now)
    cancel_reason = models.CharField(choices=CANCEL_REASON, max_length=50, blank=True, null=True)
    review_description = models.TextField(help_text='Please Describe in detail reason of cancel.')
    cancel_mini_order = models.ForeignKey(MiniOrder, on_delete=models.SET_NULL, blank=True, null=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}_{self.cancel_reason}_CANCELED"

    def get_absolute_url(self):  # Redirect to this link after filling the form for cancel order
        return reverse("order-all")

    class Meta:
        ordering = ['-cancel_date']


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mini_order = models.ManyToManyField(MiniOrder)
    cart = models.ManyToManyField(Cart)
    order_id = models.CharField(max_length=200, null=True, blank=True)

    coupon_used = models.BooleanField(default=False)
    coupon_customer = models.ForeignKey(CouponCustomer, on_delete=models.CASCADE, null=True, blank=True)

    order_ref_number = models.CharField(unique=True, default='ORD-100000', max_length=15)
    ordered_date_time = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    ordered = models.BooleanField(default=False)

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    received = models.BooleanField(default=False, blank=True, null=True)
    payment_method = models.CharField(default='Online by card', max_length=30)
    taxes = models.FloatField(default=0)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-ordered_date_time']

    def __str__(self):
        return f"{self.user} Order"
        
    def get_total_without_tax_shipping(self):
        total = 0
        for order_item in self.cart.all():
            total += order_item.get_final_price()
        if self.coupon_customer:
            total -= self.get_coupon_total()
        return total

    def get_total(self):
        total = 0
        for order_item in self.cart.all():
            total += order_item.get_final_price()
        if self.coupon_customer:
            total -= self.get_coupon_total()
        shipping = self.get_shipping_total()
        tax = self.get_tax_total()
        return total + shipping + tax
        
    def get_shipping_total(self):
        if self.address:
            if self.address.country.lower() != 'india':
                total = 0
                for order_item in self.cart.all():
                    total += 7000
                return total
        return 0
        
    def get_tax_total(self):
        total = 0
        for order_item in self.cart.all():
            total += order_item.get_tax()
        return total

    def get_total_without_coupon(self):
        total = 0
        for order_item in self.cart.all():
            total += order_item.get_final_price()
        return total

    def get_sub_total(self):
        total = 0
        for order_item in self.cart.all():
            total += order_item.get_total_item_price()
        return total

    def get_discounted_total(self):
        total = 0
        for order_item in self.cart.all():
            total += order_item.get_amount_saved()
        return total

    def get_coupon_total(self):
        vendor_coupon = Coupon.objects.get(code=self.coupon_customer.coupon.code)
        total = self.get_total_without_coupon()
        if total >= vendor_coupon.minimum_order_amount:
            self.coupon_customer.coupon.discount_amount = total * \
                                                          (vendor_coupon.discount_percent / 100)
        try:
            return self.coupon_customer.coupon.discount_amount
        except AttributeError:
            return 0


class Payment(models.Model):
    order_id = models.CharField(max_length=200)
    payment_id = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    amount_paid = models.FloatField()
    currency = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user}_Payment"
