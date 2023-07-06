# from django.test import TestCase, Client, RequestFactory
# from django.urls import reverse
#
# from django.template.defaultfilters import slugify
# from products.models import (
#     Product, ParentCategory, Category, Variation
# )
# from listing.models import (
#     ListingLocation, ListingCategory, Listing, ParentListingCategory, ListingContact, ListingPhoto, ListingReview
# )
# from users.models import User
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
#         self.parent_category = ParentListingCategory.objects.create(
#             title='pytest_tests',
#             slug='pytest_tests',
#         )
#
#         self.category = ListingCategory.objects.create(
#             parent_category=self.parent_category,
#             title='test category',
#             slug='test_category',
#         )
#
#         self.location = ListingLocation.objects.create(
#             title='test location',
#             slug='test_location',
#         )
#
#         self.listing = Listing.objects.create(
#             category=self.category,
#             location=self.location,
#             title='test product',
#             slug=slugify('test product'),
#             low_price=50.00,
#             high_price=40.00,
#             image_main='http://127.0.0.1:8000/gRRtWpFFMK8-unsplash.jpg',
#         )
#
#         self.contact = ListingContact.objects.create(
#             name='test',
#             mobile=1234567891,
#             listing=self.listing
#         )
#
#         self.listing_image = ListingPhoto.objects.create(
#             file='http://127.0.0.1:8000/gRRtWpFFMK8-unsplash.jpg',
#         )
#
#         self.review = ListingReview.objects.create(
#             review_description='test',
#             rating=5,
#             user=self.user
#         )
#
#         self.listing.photos.add(self.listing_image)
#         self.listing.save()
#         self.admin_listing_detail = (reverse('listing-detail-view', kwargs={'pk': self.listing.id}))
#
#         self.admin_listing_dashboard = (reverse('admin-listing-dashboard'))
#         self.admin_listing_list = (reverse('admin-listing-list'))
#         self.admin_listing_add = (reverse('admin-listing-add'))
#         self.admin_listing_image_add = (reverse('analytics-listing-image-add', kwargs={'pk': self.listing.id}))
#         self.admin_listing_image_delete = (reverse('analytics-listing-image-delete',
#                                                    kwargs={'listing_id': self.listing.id, 'pk': self.listing_image.id}))
#         self.admin_listing_update = (reverse('admin-listing-update', kwargs={'pk': self.listing.id}))
#         self.admin_listing_delete = (reverse('admin-listing-delete', kwargs={'pk': self.listing.id}))
#
#         self.listing_category_list = (reverse('admin-listing-category-list'))
#         self.listing_category_add = (reverse('admin-listing-category-add'))
#         self.listing_category_update = (reverse('admin-listing-category-update', kwargs={'pk': self.category.id}))
#         self.listing_category_delete = (reverse('admin-listing-category-delete', kwargs={'pk': self.category.id}))
#         self.listing_parent_category_list = (reverse('admin-listing-parent-category-list'))
#         self.listing_parent_category_add = (reverse('admin-listing-parent-category-add'))
#         self.listing_parent_category_update = (reverse('admin-listing-parent-category-update',
#                                                        kwargs={'pk': self.parent_category.id}))
#         self.listing_parent_category_delete = (reverse('admin-listing-parent-category-delete',
#                                                        kwargs={'pk': self.parent_category.id}))
#
#         self.listing_location_list = (reverse('admin-listing-location-list'))
#         self.listing_location_add = (reverse('admin-listing-location-add'))
#         self.listing_location_update = (reverse('admin-listing-location-update', kwargs={'pk': self.location.id}))
#         self.listing_location_delete = (reverse('admin-listing-location-delete', kwargs={'pk': self.location.id}))
#
#         self.listing_review_list = (reverse('admin-listing-review-list'))
#         self.listing_review_update = (reverse('admin-listing-review-update', kwargs={'pk': self.review.id}))
#         self.listing_review_delete = (reverse('admin-listing-review-delete', kwargs={'pk': self.review.id}))
#
#         self.listing_contact = (reverse('admin-listing-contact'))
#         self.listing_contact_update = (reverse('admin-listing-contact-update', kwargs={'pk': self.contact.id}))
#
#     def test_listing_contact_update_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_contact_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_contact_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_contact_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_contact_update_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.listing_contact_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_contact_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_contact_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_contact_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_contact)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_contact)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_contact)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_review_delete_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_review_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_review_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_review_delete)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_review_delete_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.listing_review_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_review_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_review_delete)
#         self.assertEqual(response.status_code, 302)
#
#     def test_listing_review_update_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_review_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_review_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_review_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_review_update_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.listing_review_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_review_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_review_update)
#         self.assertEqual(response.status_code, 200)
#
#     # def test_listing_review_list_get(self):
#     #     # Testing Anonymous User
#     #     response = self.client.get(self.listing_review_list)
#     #     self.assertEqual(response.status_code, 302)
#     #
#     #     # Testing Authenticated User
#     #     self.client.login(email="test@gmail.com", password="Test@321")
#     #     response = self.client.get(self.listing_review_list)
#     #     self.assertEqual(response.status_code, 403)
#     #
#     #     # Testing Authenticated  Staff
#     #     self.client.login(email="admin@gmail.com", password="Test@321")
#     #     response = self.client.get(self.listing_review_list)
#     #     self.assertEqual(response.status_code, 200)
#
#     def test_listing_location_delete_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_location_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_location_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_location_delete)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_location_delete_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.listing_location_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_location_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_location_delete)
#         self.assertEqual(response.status_code, 302)
#
#     def test_listing_location_update_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_location_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_location_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_location_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_location_update_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.listing_location_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_location_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_location_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_location_add_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_location_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_location_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_location_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_location_add_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.listing_location_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_location_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_location_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_location_list_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_location_list)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_location_list)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_location_list)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_parent_category_delete_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_parent_category_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_parent_category_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_parent_category_delete)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_parent_category_delete_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.listing_parent_category_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_parent_category_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_parent_category_delete)
#         self.assertEqual(response.status_code, 302)
#
#     def test_listing_parent_category_update_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_parent_category_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_parent_category_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_parent_category_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_parent_category_update_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.listing_parent_category_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_parent_category_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_parent_category_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_parent_category_add_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_parent_category_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_parent_category_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_parent_category_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_parent_category_add_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.listing_parent_category_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_parent_category_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_parent_category_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_parent_category_list_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_parent_category_list)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_parent_category_list)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_parent_category_list)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_category_delete_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_category_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_category_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_category_delete)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_category_delete_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.listing_category_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_category_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_category_delete)
#         self.assertEqual(response.status_code, 302)
#
#     def test_listing_category_update_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_category_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_category_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_category_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_category_update_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.listing_category_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_category_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_category_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_category_add_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_category_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_category_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_category_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_category_add_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.listing_category_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_category_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.listing_category_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_listing_category_list_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.listing_category_list)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_category_list)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.listing_category_list)
#         self.assertEqual(response.status_code, 200)
#
#     def test_admin_listing_delete_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.admin_listing_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_listing_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_listing_delete)
#         self.assertEqual(response.status_code, 200)
#
#     def test_admin_listing_delete_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.admin_listing_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.admin_listing_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.admin_listing_delete)
#         self.assertEqual(response.status_code, 302)
#
#     def test_admin_listing_update_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.admin_listing_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_listing_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_listing_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_admin_listing_update_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.admin_listing_update)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.admin_listing_update)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.admin_listing_update)
#         self.assertEqual(response.status_code, 200)
#
#     def test_admin_listing_image_delete_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.admin_listing_image_delete)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_listing_image_delete)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_listing_image_delete)
#         self.assertEqual(response.status_code, 302)
#
#     def test_admin_listing_image_add_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.admin_listing_image_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_listing_image_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_listing_image_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_admin_listing_image_add_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.admin_listing_image_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.admin_listing_image_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.admin_listing_image_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_admin_listing_add_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.admin_listing_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_listing_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_listing_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_admin_listing_add_post(self):
#         # Testing Anonymous User
#         response = self.client.post(self.admin_listing_add)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.post(self.admin_listing_add)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.post(self.admin_listing_add)
#         self.assertEqual(response.status_code, 200)
#
#     def test_admin_listing_dashboard_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.admin_listing_dashboard)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_listing_dashboard)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_listing_dashboard)
#         self.assertEqual(response.status_code, 200)
#
#     def test_admin_listing_list_get(self):
#         # Testing Anonymous User
#         response = self.client.get(self.admin_listing_list)
#         self.assertEqual(response.status_code, 302)
#
#         # Testing Authenticated User
#         self.client.login(email="test@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_listing_list)
#         self.assertEqual(response.status_code, 403)
#
#         # Testing Authenticated  Staff
#         self.client.login(email="admin@gmail.com", password="Test@321")
#         response = self.client.get(self.admin_listing_list)
#         self.assertEqual(response.status_code, 200)
#
