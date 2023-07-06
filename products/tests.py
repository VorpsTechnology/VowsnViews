# from django.test import TestCase, SimpleTestCase, Client, RequestFactory
# from django.urls import reverse, resolve
# from django.utils import timezone
# from django.template.defaultfilters import slugify
#
# from users.models import User
# from products.models import (
#     Product, Review, Favorite, ParentCategory, Category
# )
# from . import views, filters
# from test_plus.test import CBVTestCase
#
#
# # Model
# class TestAppModels(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             user_full_name='pytest_tests',
#             email='pytest_tests@gmail.com',
#             password='Test@321',
#             phone_number=1230237891,
#             is_active=True
#         )
#         self.review = Review.objects.create(
#             user=self.user,
#             date=timezone.now(),
#             review_description='Good Product',
#             rating=3
#         )
#
#         self.parent_category = ParentCategory.objects.create(
#             title='pytest_tests',
#             slug='pytest_tests',
#             description='pytest_tests desc',
#         )
#
#     def test_model_review_str(self):
#         self.assertEqual(f"{self.review.rating}_user", self.review.__str__())
#
#     def test_review_get_absolute_url_str(self):
#         self.assertEqual('/products/list/', self.review.get_absolute_url())
#
#     def test_to_int(self):
#         self.assertEqual(int(self.review.rating), self.review.to_int())
#
#     def test_model_parent_category_str(self):
#         self.assertEqual(f"{self.parent_category.title}", self.parent_category.__str__())
#
#     def test_parent_category_get_absolute_url_str(self):
#         self.assertEqual('/analytics/parent/category/list-admin/', self.parent_category.get_absolute_url())
#
#
# # Views
# class TestProductsViews(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#
#         self.user = User.objects.create_user(
#             user_full_name='test',
#             email='pytest_tests@gmail.com',
#             password='Test@321',
#             phone_number=1234567890,
#             is_active=True
#         )
#
#         self.parent_category = ParentCategory.objects.create(
#             title='pytest_tests',
#             slug='pytest_tests',
#         )
#
#         self.category = Category.objects.create(
#             parent_category=self.parent_category,
#             title='test category',
#             slug='test_category',
#         )
#
#         self.product = Product.objects.create(
#             category=self.category,
#             title='test product',
#             slug=slugify('test product'),
#             price=50.00,
#             discount_price=40.00,
#             image_main='http://127.0.0.1:8000/media/products/reproductive-health-supplies-coalition-gRRtWpFFMK8-unsplash.jpg',
#         )
#
#         self.product_list_url = reverse('product-list-view')
#         self.product_detail_url = reverse('product-detail-view', kwargs={'pk': 1})
#
#     def test_product_list_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.product_list_url)
#         self.assertEqual(response.status_code, 200)
#
#         # Testing Authenticated User
#         self.client.login(email="pytest_tests@gmail.com", password="Test@321")
#         response = self.client.get(self.product_list_url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_product_detail_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.product_detail_url)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/user/login/?next=' + self.product_detail_url)
#
#         # Testing Authenticated User
#         self.client.login(email="pytest_tests@gmail.com", password="Test@321")
#         response = self.client.get(self.product_detail_url)
#         self.assertEqual(response.status_code, 200)
#



