# from django.test import TestCase, Client, RequestFactory
# from django.urls import reverse
# from django.template.defaultfilters import slugify
# from products.models import (
#     Product, ParentCategory, Category, Variation
# )
#
# from users.models import User
# from home.models import Contact
#
#
# class TestProductsViews(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#
#         self.user = User.objects.create_user(
#             user_full_name='test',
#             email='test@gmail.com',
#             password='Test@321',
#             phone_number=1234567890,
#             is_active=True,
#         )
#
#         self.user_admin = User.objects.create_user(
#             user_full_name='admin',
#             email='admin@gmail.com',
#             password='Test@321',
#             phone_number=1234567890,
#             is_active=True,
#             is_staff=True,
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
#             image_main='http://127.0.0.1:8000/gRRtWpFFMK8-unsplash.jpg',
#         )
#
#         self.variation = Variation.objects.create(
#             product=self.product,
#             title='test category',
#             price=20.30,
#             discount_price=20.00,
#             category='size'
#         )
#
#         self.contact = Contact.objects.create(
#             name='test',
#             mobile=1234567891,
#             description="Some text"
#         )
#
#         self.admin_dashboard = (reverse('admin-dashboard'))
#         self.order_list = (reverse('admin-order-list'))
#         self.order_return = (reverse('admin-order-return'))
#         self.order_cancel = (reverse('admin-order-cancel'))
#         self.product_list = (reverse('admin-product-list'))
#         self.product_detail = (reverse('admin-product-detail', kwargs={'pk': self.product.id}))
#         self.product_add = (reverse('admin-product-add'))
#         self.product_update = (reverse('admin-product-update', kwargs={'pk': self.product.id}))
#         self.product_delete = (reverse('admin-product-delete', kwargs={'pk': self.product.id}))
#         self.category_list = (reverse('admin-category-list'))
#         self.category_add = (reverse('admin-product-category-add'))
#         self.category_update = (reverse('admin-product-category-update', kwargs={'pk': self.category.id}))
#         self.category_delete = (reverse('admin-product-category-delete', kwargs={'pk': self.category.id}))
#         self.parent_category_list = (reverse('admin-parent-category-list'))
#         self.parent_category_add = (reverse('admin-product-parent-category-add'))
#         self.parent_category_update = (reverse('admin-product-parent-category-update', kwargs={'pk': self.category.id}))
#         self.parent_category_delete = (reverse('admin-product-parent-category-delete', kwargs={'pk': self.category.id}))
#         self.product_variation_add = (reverse('admin-variation-add', kwargs={'pk': self.product.id}))
#         self.product_variation_update = (reverse('admin-variation-update', kwargs={'pk': self.variation.id}))
#         self.product_variation_delete = (reverse('admin-variation-delete', kwargs={'product_id': self.product.id,
#                                                                                    'pk': self.variation.id}))
#         self.send_mail = (reverse('admin-send-mail'))
#         self.admin_contact = (reverse('admin-contact'))
#         self.admin_contact_update = (reverse('admin-contact-update', kwargs={'pk': self.contact.id}))
#
#     def test_admin_contact_update_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.admin_contact_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_contact_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_contact_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_admin_contact_update_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.admin_contact_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.admin_contact_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.admin_contact_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_product_variation_delete_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.product_variation_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.product_variation_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.product_variation_delete)
#         self.assertEqual(response.status_code, 200)
#
#     def test_product_variation_delete_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.product_variation_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.product_variation_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.product_variation_delete)
#         self.assertEqual(response.url, self.product_detail)
#         self.assertEqual(response.status_code, 302)
#
#     def test_product_variation_update_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.product_variation_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.product_variation_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.product_variation_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_product_variation_update_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.product_variation_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.product_variation_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.product_variation_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_product_variation_add_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.product_variation_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.product_variation_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.product_variation_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_product_variation_add_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.product_variation_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.product_variation_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.product_variation_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_parent_category_delete_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.parent_category_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.parent_category_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.parent_category_delete)
#         self.assertEqual(response.status_code, 200)
#
#     def test_parent_category_delete_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.parent_category_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.parent_category_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.parent_category_delete)
#         self.assertEqual(response.url, self.parent_category_list)
#         self.assertEqual(response.status_code, 302)
#
#     def test_parent_category_update_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.parent_category_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.parent_category_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.parent_category_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_parent_category_update_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.parent_category_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.parent_category_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.parent_category_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_category_delete_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.category_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.category_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.category_delete)
#         self.assertEqual(response.status_code, 200)
#
#     def test_category_delete_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.category_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.category_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.category_delete)
#         self.assertEqual(response.status_code, 302)
#
#     def test_category_update_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.category_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.category_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.category_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_category_update_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.category_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.category_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.category_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_product_delete_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.product_delete)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/user/login/?next=' + self.product_delete)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.product_delete)
#         self.assertEqual(response.status_code, 403)
#         print(response, 'FORBIDDEN')
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.product_delete)
#         self.assertEqual(response.status_code, 200)
#         # self.assertEqual(response.url, self.product_delete)
#
#     def test_product_delete_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.product_delete)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/user/login/?next=' + self.product_delete)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.product_delete)
#         self.assertEqual(response.status_code, 403)
#         print(response, 'FORBIDDEN')
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.product_delete)
#         self.assertEqual(response.url, self.product_list)
#         self.assertEqual(response.status_code, 302)
#         # self.assertEqual(response.url, self.product_delete)
#
#     def test_product_update_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.product_update)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/user/login/?next=' + self.product_update)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.product_update)
#         self.assertEqual(response.status_code, 403)
#         print(response, 'FORBIDDEN')
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.product_update)
#         self.assertEqual(response.status_code, 200)
#         # self.assertEqual(response.url, self.product_update)
#
#     def test_product_update_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.product_update)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/user/login/?next=' + self.product_update)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.product_update)
#         self.assertEqual(response.status_code, 403)
#         print(response, 'FORBIDDEN')
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.product_update)
#         self.assertEqual(response.status_code, 200)
#         # self.assertEqual(response.url, self.product_update)
#
#     def test_product_detail_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.product_detail)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/user/login/?next=' + self.product_detail)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.product_detail)
#         self.assertEqual(response.status_code, 403)
#         print(response, 'FORBIDDEN')
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.product_detail)
#         self.assertEqual(response.status_code, 200)
#         # self.assertEqual(response.url, self.product_detail)
#
#     def test_admin_dashboard_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.admin_dashboard)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_dashboard)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_dashboard)
#         self.assertEqual(response.status_code, 200)
#
#     def test_order_list_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.order_list)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.order_list)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.order_list)
#         self.assertEqual(response.status_code, 200)
#
#     def test_order_return_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.order_return)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.order_return)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.order_return)
#         self.assertEqual(response.status_code, 200)
#
#     def test_order_cancel_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.order_cancel)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.order_cancel)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.order_cancel)
#         self.assertEqual(response.status_code, 200)
#
#     def test_product_list_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.product_list)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/user/login/?next=' + self.product_list)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.product_list)
#         self.assertEqual(response.status_code, 403)
#         print(response, 'FORBIDDEN')
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.product_list)
#         self.assertEqual(response.status_code, 200)
#         # self.assertEqual(response.url, self.product_list)
#
#     def test_product_add_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.product_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.product_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.product_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_product_add_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.product_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.product_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.product_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_category_list_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.category_list)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.category_list)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.category_list)
#         self.assertEqual(response.status_code, 200)
#
#     def test_category_add_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.category_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.category_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.category_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_category_add_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.category_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.category_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.category_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_parent_category_list_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.parent_category_list)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.parent_category_list)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.parent_category_list)
#         self.assertEqual(response.status_code, 200)
#
#     def test_parent_category_add_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.parent_category_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.parent_category_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.parent_category_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_parent_category_add_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.parent_category_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.parent_category_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.parent_category_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_send_mail_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.send_mail)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.send_mail)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.send_mail)
#         self.assertEqual(response.status_code, 200)
#
#     def test_send_mail_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.send_mail)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.send_mail)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.send_mail)
#         self.assertEqual(response.status_code, 200)
#
#     def test_admin_contact_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.admin_contact)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_contact)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_contact)
#         self.assertEqual(response.status_code, 200)
#
