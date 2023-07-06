from django.test import TestCase, SimpleTestCase, Client, RequestFactory
from django.urls import reverse
from django.template.defaultfilters import slugify

from users.models import User, Address
from products.models import (
    Product, Review, Favorite, ParentCategory, Category, Variation
)
from order.models import (
    Cart, Order, MiniOrder, Payment, ReturnMiniOrder, CancelMiniOrder, CouponCustomer, Coupon
)
from . import views, filters


class TestProductsViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            user_full_name='test',
            email='pytest_tests@gmail.com',
            password='Test@321',
            phone_number=1234567890,
            is_active=True
        )

        self.parent_category = ParentCategory.objects.create(
            title='pytest_tests',
            slug='pytest_tests',
        )

        self.category = Category.objects.create(
            parent_category=self.parent_category,
            title='test category',
            slug='test_category',
        )

        self.product = Product.objects.create(
            category=self.category,
            title='test product',
            slug=slugify('test product'),
            price=50.00,
            discount_price=40.00,
            stock_no=5,
            image_main='http://127.0.0.1:8000/MK8-unsplash.jpg',
        )

        self.product_2 = Product.objects.create(
            category=self.category,
            title='test product 2',
            slug=slugify('test product 2'),
            price=20.00,
            discount_price=10.00,
            stock_no=2,
            image_main='http://127.0.0.1:8000/MK8-unsplash.jpg',
        )

        self.product_variation = Product.objects.create(
            category=self.category,
            title='test product var',
            slug=slugify('test product var'),
            price=20.00,
            discount_price=10.00,
            image_main='http://127.0.0.1:8000/MK8-unsplash.jpg',
        )

        self.product_variation_2 = Product.objects.create(
            category=self.category,
            title='test product var2',
            slug=slugify('test product var2'),
            price=20.00,
            discount_price=10.00,
            image_main='http://127.0.0.1:8000/MK8-unsplash.jpg',
        )

        self.product_variation_3 = Product.objects.create(
            category=self.category,
            title='test product var3',
            slug=slugify('test product var3'),
            price=20.00,
            discount_price=10.00,
            image_main='http://127.0.0.1:8000/MK8-unsplash.jpg',
        )

        self.variation_size_s = Variation.objects.create(
            product=self.product_variation,
            title='S',
            price=25,
            discount_price=22.00,
            category='size'
        )

        self.variation_size_l = Variation.objects.create(
            product=self.product_variation,
            title='L',
            price=30,
            discount_price=25.00,
            category='size'
        )

        self.variation_color_blue = Variation.objects.create(
            product=self.product_variation,
            title='blue',
            price=40,
            discount_price=35.00,
            category='color'
        )

        self.variation_size_s_2 = Variation.objects.create(
            product=self.product_variation_2,
            title='S',
            price=25,
            discount_price=22.00,
            category='size'
        )

        self.variation_size_l_2 = Variation.objects.create(
            product=self.product_variation_2,
            title='L',
            price=30,
            discount_price=25.00,
            category='size'
        )

        self.variation_color_red = Variation.objects.create(
            product=self.product_variation_2,
            title='red',
            price=35,
            discount_price=30.00,
            category='color'
        )

        self.variation_color_blue_2 = Variation.objects.create(
            product=self.product_variation_2,
            title='blue',
            price=40,
            discount_price=35.00,
            category='color'
        )

        self.variation_size_s_3 = Variation.objects.create(
            product=self.product_variation_3,
            title='S',
            price=25,
            discount_price=20.00,
            category='size'
        )

        self.variation_size_l_3 = Variation.objects.create(
            product=self.product_variation_3,
            title='L',
            price=30,
            discount_price=25.00,
            category='size'
        )

        self.variation_color_blue_3 = Variation.objects.create(
            product=self.product_variation_3,
            title='blue',
            price=45,
            discount_price=35.00,
            category='color'
        )

        self.variation_color_red_3 = Variation.objects.create(
            product=self.product_variation_3,
            title='red',
            price=40,
            discount_price=30.00,
            category='color'
        )

        self.cart_list = reverse('order-view-cart')

        self.add_to_cart = reverse('order-add-to-cart', kwargs={'slug': self.product.slug})
        self.product_detail = reverse('product-detail-view', kwargs={'pk': self.product.id})

        self.add_to_cart_2 = reverse('order-add-to-cart', kwargs={'slug': self.product_2.slug})
        self.product_detail_2 = reverse('product-detail-view', kwargs={'pk': self.product_2.id})

        self.add_to_cart_variation = reverse('order-add-to-cart-variation',
                                             kwargs={'slug': self.product_variation.slug, 'pk': None})
        self.product_detail_variation = reverse('product-detail-view', kwargs={'pk': self.product_variation.id})

        self.add_to_cart_variation_2 = reverse('order-add-to-cart-variation',
                                               kwargs={'slug': self.product_variation_2.slug, 'pk': None})
        self.product_detail_variation_2 = reverse('product-detail-view', kwargs={'pk': self.product_variation_2.id})

        self.add_to_cart_variation_3 = reverse('order-add-to-cart-variation',
                                               kwargs={'slug': self.product_variation_3.slug, 'pk': None})
        self.product_detail_variation_3 = reverse('product-detail-view', kwargs={'pk': self.product_variation_3.id})

        # TODO add product with variation with and without any products in cart and vice versa

    def test_add_to_cart(self):
        # Testing Anonymous User
        response = self.client.get(self.add_to_cart)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/login/?next=' + self.add_to_cart)

        # Testing Authenticated User add to cart
        self.client.login(email="pytest_tests@gmail.com", password="Test@321")

        # Adds product for first time qty = 1
        response = self.client.get(self.add_to_cart)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().first().cart.product.title, self.product.title)
        self.assertEqual(order.mini_order.all().first().cart.quantity, 1)
        self.assertEqual(order.get_total(), 40)
        self.assertEqual(order.get_sub_total(), 50)
        self.assertRedirects(response, self.product_detail)

        # Adds in cart product for second time qty = 2
        response = self.client.get(self.add_to_cart)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().first().cart.product.title, self.product.title)
        self.assertEqual(order.mini_order.all().first().cart.quantity, 2)
        self.assertEqual(order.get_total(), 80)
        self.assertEqual(order.get_sub_total(), 100)
        self.assertEqual(order.get_discounted_total(), 20)
        self.assertRedirects(response, self.cart_list)

        # Adds product not in cart for 1st time qty = 1
        response = self.client.get(self.add_to_cart_2)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product_2.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 1)
        self.assertEqual(order.get_total(), 90)
        self.assertEqual(order.get_sub_total(), 120)
        self.assertEqual(order.get_discounted_total(), 30)
        self.assertRedirects(response, self.product_detail_2)

        response = self.client.get(self.add_to_cart_2)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product_2.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 2)
        self.assertEqual(order.get_total(), 100)
        self.assertEqual(order.get_sub_total(), 140)
        self.assertEqual(order.get_discounted_total(), 40)
        self.assertRedirects(response, self.cart_list)

        response = self.client.get(self.add_to_cart_2)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product_2.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 2)
        self.assertEqual(order.get_total(), 100)
        self.assertEqual(order.get_sub_total(), 140)
        self.assertEqual(order.get_discounted_total(), 40)
        self.assertRedirects(response, self.cart_list)

    def test_add_to_cart_variation_post(self):
        # Testing Anonymous User
        response = self.client.post(self.add_to_cart_variation)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/login/?next=' + self.add_to_cart_variation)

        # Testing Authenticated User add to cart
        self.client.login(email="pytest_tests@gmail.com", password="Test@321")

        # Adds product for first time qty = 1
        response = self.client.post(self.add_to_cart_variation, {'id_1': self.variation_size_l.id})
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().first().cart.product.title, self.product_variation.title)
        self.assertEqual(order.mini_order.all().first().cart.quantity, 1)
        self.assertEqual(order.mini_order.all().first().cart.variation.all().first().title, "L")
        self.assertEqual(order.get_total(), 25)
        self.assertEqual(order.get_sub_total(), 30)
        self.assertEqual(order.mini_order.all().first().cart.variation.all().first().title, self.variation_size_l.title)
        self.assertRedirects(response, self.product_detail_variation)

        # Adds in cart product for 2nd with same variation time qty = 2
        response = self.client.post(self.add_to_cart_variation, {'id_1': self.variation_size_l.id})
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().first().cart.product.title, self.product_variation.title)
        self.assertEqual(order.mini_order.all().first().cart.quantity, 2)
        self.assertEqual(order.mini_order.all().first().cart.variation.all().first().title, "L")
        self.assertEqual(order.get_total(), 50)
        self.assertEqual(order.get_sub_total(), 60)
        self.assertEqual(order.mini_order.all().first().cart.variation.all().first().title, self.variation_size_l.title)
        self.assertRedirects(response, self.cart_list)

        # Adds in cart product for 3rd time with different variation qty = 1
        response = self.client.post(self.add_to_cart_variation, {'id_1': self.variation_size_s.id})
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product_variation.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 1)
        self.assertEqual(order.mini_order.all().last().cart.variation.all().first().title, "S")
        self.assertEqual(order.get_total(), 72)
        self.assertEqual(order.get_sub_total(), 85)
        self.assertEqual(order.mini_order.all().last().cart.variation.all().first().title, self.variation_size_s.title)
        self.assertRedirects(response, self.product_detail_variation)

        # Adds in cart product for 1st time qty = 1
        response = self.client.post(self.add_to_cart_variation_2, {'id_1': self.variation_color_blue_2.id})
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product_variation_2.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 1)
        self.assertEqual(order.mini_order.all().last().cart.variation.all().first().title, "blue")
        self.assertEqual(order.get_total(), 107)
        self.assertEqual(order.get_sub_total(), 125)
        self.assertEqual(order.mini_order.all().last().cart.variation.all().first().title,
                         self.variation_color_blue_2.title)
        self.assertRedirects(response, self.product_detail_variation_2)

        # Adds in cart product for 1st time qty = 1
        response = self.client.post(self.add_to_cart_variation_2, {'id_1': self.variation_color_blue_2.id})
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product_variation_2.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 2)
        self.assertEqual(order.mini_order.all().last().cart.variation.all().first().title, "blue")
        self.assertEqual(order.get_total(), 142)
        self.assertEqual(order.get_sub_total(), 165)
        self.assertEqual(order.mini_order.all().last().cart.variation.all().first().title,
                         self.variation_color_blue_2.title)
        self.assertRedirects(response, self.cart_list)

        # Adds product 1st time with multi variation = 1
        response = self.client.post(self.add_to_cart_variation_3, {'id_1': self.variation_size_l_3.id,
                                                                   'id_2': self.variation_color_blue_3.id})
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product_variation_3.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 1)
        self.assertEqual(order.mini_order.all().last().cart.variation.all().first().title, "L")
        self.assertEqual(order.mini_order.all().last().cart.variation.all().last().title, "blue")
        self.assertEqual(order.get_total(), 167)
        self.assertEqual(order.get_sub_total(), 195)
        self.assertEqual(order.mini_order.all().last().cart.variation.all().first().title,
                         self.variation_size_l_3.title)
        self.assertRedirects(response, self.product_detail_variation_3)

        # Adds in cart product for 2nd with same variation time qty = 2
        response = self.client.post(self.add_to_cart_variation_3, {'id_1': self.variation_size_l_3.id,
                                                                   'id_2': self.variation_color_blue_3.id})
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product_variation_3.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 2)
        self.assertEqual(order.mini_order.all().last().cart.variation.all().first().title, "L")
        self.assertEqual(order.mini_order.all().last().cart.variation.all().last().title, "blue")
        self.assertEqual(order.get_total(), 192)
        self.assertEqual(order.get_sub_total(), 225)
        self.assertEqual(order.mini_order.all().last().cart.variation.all().first().title,
                         self.variation_size_l_3.title)
        self.assertRedirects(response, self.cart_list)

    # add and remove products in cart
    def test_add_to_cart_variation_get(self):
        # Testing Anonymous User
        response = self.client.get(self.add_to_cart_variation)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/login/?next=' + self.add_to_cart_variation)

        # Testing Authenticated User add to cart
        self.client.login(email="pytest_tests@gmail.com", password="Test@321")

        # Adds product 1st time with multi variation = 1
        response = self.client.post(self.add_to_cart_variation_3, {'id_1': self.variation_size_l_3.id,
                                                                   'id_2': self.variation_color_blue_3.id})
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product_variation_3.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 1)
        self.assertEqual(order.mini_order.all().last().cart.variation.all().first().title, "L")
        self.assertEqual(order.mini_order.all().last().cart.variation.all().last().title, "blue")
        self.assertEqual(order.get_total(), 25)
        self.assertEqual(order.get_sub_total(), 30)
        self.assertEqual(order.mini_order.all().last().cart.variation.all().first().title,
                         self.variation_size_l_3.title)
        self.assertRedirects(response, self.product_detail_variation_3)

        cart = Cart.objects.first()
        self.add_to_cart_get = reverse('order-add-to-cart-variation', kwargs={'slug': None, 'pk': cart.pk})

        response = self.client.get(self.add_to_cart_get)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product_variation_3.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 2)
        self.assertEqual(order.mini_order.all().last().cart.variation.all().first().title, "L")
        self.assertEqual(order.mini_order.all().last().cart.variation.all().last().title, "blue")
        self.assertEqual(order.get_total(), 50)
        self.assertEqual(order.get_sub_total(), 60)
        self.assertEqual(order.mini_order.all().last().cart.variation.all().first().title,
                         self.variation_size_l_3.title)
        self.assertRedirects(response, self.cart_list)

        response = self.client.post(self.add_to_cart)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 1)
        self.assertEqual(order.get_total(), 40 + 50)
        self.assertEqual(order.get_sub_total(), 50 + 60)
        self.assertRedirects(response, self.product_detail)

        cart = Cart.objects.last()
        self.add_to_cart_get = reverse('order-add-to-cart-variation', kwargs={'slug': None, 'pk': cart.pk})

        response = self.client.get(self.add_to_cart_get)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 2)
        self.assertEqual(order.get_total(), 80 + 50)
        self.assertEqual(order.get_sub_total(), 100 + 60)
        self.assertRedirects(response, self.cart_list)

        response = self.client.get(self.add_to_cart_get)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 3)
        self.assertEqual(order.get_total(), 120 + 50)
        self.assertEqual(order.get_sub_total(), 150 + 60)
        self.assertRedirects(response, self.cart_list)

        response = self.client.get(self.add_to_cart_get)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 4)
        self.assertEqual(order.get_total(), 160 + 50)
        self.assertEqual(order.get_sub_total(), 200 + 60)
        self.assertRedirects(response, self.cart_list)

        response = self.client.get(self.add_to_cart_get)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 5)
        self.assertEqual(order.get_total(), 200 + 50)
        self.assertEqual(order.get_sub_total(), 250 + 60)
        self.assertRedirects(response, self.cart_list)

        response = self.client.get(self.add_to_cart_get)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 5)
        self.assertEqual(order.get_total(), 200 + 50)
        self.assertEqual(order.get_sub_total(), 250 + 60)
        self.assertRedirects(response, self.cart_list)

    def test_cart_remove(self):
        # Testing Anonymous User
        response = self.client.get(self.add_to_cart)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/login/?next=' + self.add_to_cart)

        # Testing Authenticated User add to cart
        self.client.login(email="pytest_tests@gmail.com", password="Test@321")
        response = self.client.post(self.add_to_cart)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 1)
        self.assertEqual(order.get_total(), 40)
        self.assertEqual(order.get_sub_total(), 50)
        self.assertRedirects(response, self.product_detail)

        cart = Cart.objects.all().last()
        self.add_to_cart_get = reverse('order-add-to-cart-variation', kwargs={'slug': None, 'pk': cart.pk})

        # Remove / Decrease qty from cart
        response = self.client.get(self.add_to_cart_get)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 2)
        self.assertEqual(order.get_total(), 80)
        self.assertEqual(order.get_sub_total(), 100)
        self.assertRedirects(response, self.cart_list)
        order.user = self.user
        order.save()

        cart = Cart.objects.first()
        self.assertEqual(cart.quantity, 2)
        self.remove_from_cart = reverse('remove-product-from-cart', kwargs={'pk': cart.pk})
        response = self.client.get(self.remove_from_cart)
        cart = Cart.objects.first()

        self.assertEqual(cart.quantity, 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.cart_list)

        self.remove_from_cart = reverse('remove-product-from-cart', kwargs={'pk': cart.pk})
        response = self.client.get(self.remove_from_cart)

        self.assertEqual(Cart.objects.count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.cart_list)

        self.remove_from_cart = reverse('remove-product-from-cart', kwargs={'pk': cart.pk})
        self.assertRedirects(response, self.cart_list)

        self.remove_from_cart = reverse('remove-product-from-cart', kwargs={'pk': cart.pk})
        self.assertRedirects(response, self.cart_list)

    def test_delete_remove(self):
        # Testing Anonymous User
        response = self.client.get(self.add_to_cart)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/login/?next=' + self.add_to_cart)

        # Testing Authenticated User add to cart
        self.client.login(email="pytest_tests@gmail.com", password="Test@321")
        response = self.client.post(self.add_to_cart)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 1)
        self.assertEqual(order.get_total(), 40)
        self.assertEqual(order.get_sub_total(), 50)
        self.assertRedirects(response, self.product_detail)

        cart = Cart.objects.last()
        self.add_to_cart_get = reverse('order-add-to-cart-variation', kwargs={'slug': None, 'pk': cart.pk})

        # Delete product  from cart
        response = self.client.get(self.add_to_cart_get)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 2)
        self.assertEqual(order.get_total(), 80)
        self.assertEqual(order.get_sub_total(), 100)
        self.assertRedirects(response, self.cart_list)
        order.user = self.user
        order.save()

        cart = Cart.objects.first()
        self.assertEqual(cart.quantity, 2)
        self.assertEqual(Cart.objects.count(), 1)
        self.remove_from_cart = reverse('delete-cart', kwargs={'pk': cart.pk})
        response = self.client.get(self.remove_from_cart)

        self.assertEqual(Cart.objects.count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.cart_list)


class TestOrderViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.address = Address.objects.create(
            street_address='test',
            pin_code=12345,
            city='JALGAON',
            state='MAH',
            default=True
        )

        self.user = User.objects.create_user(
            user_full_name='test',
            email='pytest_tests@gmail.com',
            password='Test@321',
            phone_number=1234567890,
            is_active=True
        )
        self.user.address.add(self.address)
        self.user.save()

        self.parent_category = ParentCategory.objects.create(
            title='pytest_tests',
            slug='pytest_tests',
        )

        self.category = Category.objects.create(
            parent_category=self.parent_category,
            title='test category',
            slug='test_category',
        )

        self.product = Product.objects.create(
            category=self.category,
            title='test product',
            slug=slugify('test product'),
            price=50.00,
            discount_price=40.00,
            stock_no=5,
            image_main='http://127.0.0.1:8000/MK8-unsplash.jpg',
        )

        self.product_variation = Product.objects.create(
            category=self.category,
            title='test product var',
            slug=slugify('test product var'),
            price=60.00,
            discount_price=50.00,
            image_main='http://127.0.0.1:8000/MK8-unsplash.jpg',
        )

        self.variation_size_s = Variation.objects.create(
            product=self.product_variation,
            title='S',
            price=25,
            discount_price=20.00,
            category='size'
        )

        self.variation_size_l = Variation.objects.create(
            product=self.product_variation,
            title='L',
            price=30,
            discount_price=25.00,
            category='size'
        )

        self.variation_color_blue = Variation.objects.create(
            product=self.product_variation,
            title='blue',
            price=40,
            discount_price=35.00,
            category='color'
        )

        self.variation_color_red = Variation.objects.create(
            product=self.product_variation,
            title='red',
            price=45,
            discount_price=30.00,
            category='color'
        )

        self.cart_list = reverse('order-view-cart')
        self.add_to_cart = reverse('order-add-to-cart', kwargs={'slug': self.product.slug})
        self.product_detail = reverse('product-detail-view', kwargs={'pk': self.product.id})

        self.client.login(email="pytest_tests@gmail.com", password="Test@321")
        # Adds product for first time qty = 1
        response = self.client.get(self.add_to_cart)
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().first().cart.product.title, self.product.title)
        self.assertEqual(order.mini_order.all().first().cart.quantity, 1)
        self.assertEqual(order.get_total(), 40)
        self.assertEqual(order.get_sub_total(), 50)
        self.assertRedirects(response, self.product_detail)

        self.add_to_cart_variation = reverse('order-add-to-cart-variation', kwargs={'slug': self.product_variation.slug,
                                                                                    "pk": None})
        self.product_detail_variation = reverse('product-detail-view', kwargs={'pk': self.product_variation.id})

        # Adds product for first time qty = 1
        response = self.client.post(self.add_to_cart_variation, {'id_2': self.variation_size_l.id,
                                                                 'id_1': self.variation_color_blue.id})
        order = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.mini_order.all().last().cart.product.title, self.product_variation.title)
        self.assertEqual(order.mini_order.all().last().cart.quantity, 1)
        self.assertEqual(order.get_total(), 65)  # 50
        self.assertEqual(order.get_sub_total(), 80)  # 60
        self.assertRedirects(response, self.product_detail_variation)

        self.cart_list = reverse('order-view-cart')
        self.order_list = reverse('order-all')
        self.checkout = reverse('order-checkout')

        # self.cart = Cart.objects.create(
        #     user=self.user,
        #     product=self.product,
        #     ordered=False,
        #     quantity=2
        # )
        #
        # self.cart_var = Cart.objects.create(
        #     user=self.user,
        #     product=self.product_variation,
        #     ordered=False,
        #     quantity=2
        # )
        #
        # self.cart_var.variation.add(self.variation_size_l)
        # self.cart_var.variation.add(self.variation_color_blue)
        # self.cart_var.save()

    def test_payment(self):
        # Testing Anonymous User
        self.client = Client()
        response = self.client.get(self.checkout)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/login/?next=' + self.checkout)

        # Testing Authenticated User add to cart
        self.client.login(email="pytest_tests@gmail.com", password="Test@321")

        order = Order.objects.filter(ordered=False, user=self.user)
        self.assertEqual(order.count(), 1)

        # Testing the get method
        response = self.client.get(self.checkout)
        order = Order.objects.filter(ordered=False, user=self.user)
        self.assertEqual(order.count(), 1)
        self.assertEqual(response.context['amount'], 6500)

        # Testing the post method address form
        self.assertEqual(self.user.address.count(), 1)
        response = self.client.post(self.checkout, {'street_address': 'ring road', 'state': 'MAHA', 'city': 'jalgaon',
                                                    'pin_code': 425001})
        order = Order.objects.filter(ordered=False, user=self.user)
        self.assertEqual(order.count(), 1)
        order = order.first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.address.count(), 2)
        self.assertEqual(order.address.state, self.user.address.all().first().state)
        self.assertEqual(order.address, self.user.address.all().first())
        self.assertEqual(order.address.state, 'MAHA')

        # Testing the post method active address
        self.assertNotEqual(self.user.address.all().last().id, order.address.id)
        response = self.client.post(self.checkout, {'active-address': self.user.address.all().last().id})
        order = Order.objects.filter(ordered=False, user=self.user)
        self.assertEqual(order.count(), 1)
        order = order.first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.address.count(), 2)
        self.assertEqual(order.address.state, self.user.address.all().last().state)
        self.assertEqual(order.address, self.user.address.all().last())
        self.assertEqual(order.address.state, 'MAH')

        # Testing the post method payment without payment id
        response = self.client.post(self.checkout)
        order = Order.objects.filter(ordered=True, user=self.user)
        self.assertEqual(order.count(), 0)
        order = order.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order, None)

        # Testing the post method payment
        response = self.client.post(self.checkout, {'payment_id': 1})
        order = Order.objects.filter(ordered=True, user=self.user)
        self.assertEqual(order.count(), 1)
        order = order.first()
        payment = Payment.objects.all().first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.get_sub_total(), 80)
        self.assertEqual(order.get_total(), 65)
        self.assertEqual(order.payment.amount, payment.amount)
        self.assertEqual(order.payment.amount, 6500)
        self.assertEqual(order.payment.paid, True)

    # def test_order_cancel(self):
    #     # Testing Anonymous User
    #     self.client = Client()
    #     response = self.client.get(self.checkout)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, '/user/login/?next=' + self.checkout)
    #
    #     # Testing Authenticated User add to cart
    #     self.client.login(email="pytest_tests@gmail.com", password="Test@321")
    #     self.client.post(self.checkout, {'payment_id': 1})
    #
    #     # Order Status Preparing
    #     order = Order.objects.filter(ordered=True, user=self.user).first()
    #     self.return_url = reverse('order-mini-return', kwargs={'pk': order.mini_order.first().id})
    #     self.cancel_url = reverse('order-mini-cancel', kwargs={'pk': order.mini_order.last().id})
    #
    #     response = self.client.post(self.cancel_url, {'cancel_reason': 'TEST', 'review_description': 'TEST DESC'})
    #     print(order.mini_order.all(), 'MINI ORDERS')
    #     # self.assertEqual(order.mini_order.last().cancel_requested, True)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(order.mini_order.last().cancelminiorder_set.all().first().cancel_reason, 'TEST')
    #
    #     response = self.client.post(self.return_url)
    #     self.assertEqual(response.status_code, 403)




