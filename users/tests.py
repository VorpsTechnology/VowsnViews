# from django.test import TestCase, SimpleTestCase, Client, RequestFactory
# from django.urls import reverse, resolve
# from django.contrib.auth.models import AnonymousUser
#
# from users.models import User, Address, Task, Budget, GuestList
# from . import views
#
#
# class TestViews(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(
#             user_full_name='test',
#             email='pytest_tests@gmail.com',
#             password='Test@321',
#             phone_number=1230237891,
#             is_active=True
#         )
#         self.user2 = User.objects.create_user(
#             user_full_name='test2',
#             email='pytest_tests2@gmail.com',
#             password='Test@321',
#             phone_number=1230237891,
#             is_active=True
#         )
#
#         self.address = Address.objects.create(
#             street_address='test',
#             pin_code=425001,
#             city='Jalgaon',
#             state='Maharashtra',
#         )
#
#         self.address2 = Address.objects.create(
#             street_address='test2',
#             pin_code=422001,
#             city='Jalgaon2',
#             state='Maharashtra2',
#         )
#
#         self.user.address.add(self.address)
#         self.user.save()
#
#         self.user2.address.add(self.address2)
#         self.user2.save()
#
#         self.update_url = reverse('users-update', kwargs={'pk': self.user.id})
#
#         self.address_list_url = reverse('users-address-list')
#         self.address_add_url = reverse('users-address-add')
#         self.address_update_url = reverse('users-address-update', kwargs={'pk': self.user.address.all().first().id})
#         self.address_delete_url = reverse('users-address-delete', kwargs={'pk': self.user.address.all().first().id})
#
#         self.user_update_url = reverse('users-update', kwargs={'pk': self.user.id})
#
#     def test_user_address_list_get(self):
#         request = self.factory.get(self.address_list_url)
#
#         request.user = AnonymousUser()
#         response = views.AddressListView.as_view()(request)
#         self.assertEqual(response.status_code, 302)
#
#         request.user = self.user
#         response = views.AddressListView.as_view()(request)
#         self.assertEqual(response.status_code, 200)
#
#     def test_user_address_list_get_query(self):
#         request = self.factory.get(self.address_list_url)
#         request.user = self.user
#         view = views.AddressListView()
#         view.setup(request)
#
#         queryset = Address.objects.filter(user=request.user)
#         context = view.get_queryset()
#         self.assertEqual(queryset.first().street_address, context.first().street_address)
#
#     def test_user_address_add(self):
#         request = self.factory.get(self.address_add_url)
#         request.user = AnonymousUser()
#         response = views.AddressAddView.as_view()(request)
#         self.assertEqual(response.status_code, 302)
#
#         request.user = self.user
#
#         response = views.AddressAddView.as_view()(request)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(request.user.address.all().first(), self.address)
#
#     def test_user_address_update(self):
#         # Non login user can do nothing
#         request = self.factory.get(self.address_update_url)
#         request.user = AnonymousUser()
#         response = views.AddressUpdateView.as_view()(request)
#         self.assertEqual(response.status_code, 302)
#
#         # login user can update
#         self.client.login(email="pytest_tests@gmail.com", password="Test@321")
#         data = {
#             'street_address': 'tesst',
#             'pin_code': 425001,
#             'city': 'Jalgaonn',
#             'state': 'Maharashtra',
#             'default': False
#         }
#         res = self.client.post(self.address_update_url, data)
#         address = self.user.address.all().first()
#         self.assertEqual(res.status_code, 302)
#         self.assertEqual(address.street_address, 'tesst')
#         self.assertEqual(address.city, 'Jalgaonn')
#
#         # Not updating if data is invalid
#         self.client.login(email="pytest_tests@gmail.com", password="Test@321")
#         data = {
#             'street_address': 'test',
#             'pin_code': 'asdf',
#             'city': 'Jalgann',
#             'state': 'Maharashtra',
#             'default': False
#         }
#         res = self.client.post(self.address_update_url, data)
#         address = self.user.address.all().first()
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(address.street_address, 'tesst')
#         self.assertEqual(address.city, 'Jalgaonn')
#
#     def test_user_address_update_other_user(self):
#         self.client.login(email="pytest_tests2@gmail.com", password="Test@321")
#         res = self.client.post(self.address_update_url)
#         self.assertEqual(res.status_code, 403)
#
#     def test_user_address_delete(self):
#         response = self.client.post(self.address_delete_url)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/user/login/?next=/user/address/delete/3/')
#
#         self.client.login(email="pytest_tests@gmail.com", password="Test@321")
#         self.assertEqual(self.user.address.count(), 1)
#
#         res = self.client.post(self.address_delete_url)
#
#         self.assertEqual(res.status_code, 302)
#         self.assertEqual(self.user.address.count(), 0)
#
#         res = self.client.post(self.address_delete_url)
#         self.assertEqual(res.status_code, 404)
#
#     def test_user_address_delete_other_user(self):
#         self.client.login(email="pytest_tests2@gmail.com", password="Test@321")
#         self.assertEqual(self.user.address.count(), 1)
#         self.assertEqual(self.user2.address.count(), 1)
#
#         res = self.client.post(self.address_delete_url)
#         self.assertEqual(res.status_code, 403)
#         self.assertEqual(self.user.address.count(), 1)
#         self.assertEqual(self.user2.address.count(), 1)
#
#         res = self.client.post(self.address_delete_url)
#         self.assertEqual(res.status_code, 403)
#
#     def test_user_update(self):
#         # Non login user can do nothing
#         request = self.factory.get(self.user_update_url)
#         request.user = AnonymousUser()
#         response = views.UserUpdateView.as_view()(request)
#         self.assertEqual(response.status_code, 302)
#
#         # user = User.objects.create_user(
#         #     user_full_name='test',
#         #     email='pytest_tests3@gmail.com',
#         #     password='Test@321',
#         #     phone_number=1230237891,
#         #     is_active=True
#         # )
#
#         # login user can update
#         # self.client.login(email="pytest_tests3@gmail.com", password="Test@321")
#         # data = {
#         #     'user_full_name': 'tesst',
#         #     'email': 'pytest_tests2@gmail.com',
#         #     'phone_number': 1230237891,
#         #     'partner_full_name': 'testt',
#         #     'wedding_venue': 'Jalgaon',
#         #     'wedding_date': 2020-12-18,
#         #     'user_bride_groom': 'Groom',
#         #     'partner_bride_groom': 'Bride',
#         #     'user_profile_pic': 'http://127.0.0.1:8000/media/default.jpg',
#         #     'partner_profile_pic': 'http://127.0.0.1:8000/media/default.jpg',
#         # }
#         #
#         # res = self.client.put(reverse('users-update', kwargs={'pk': user.id}), data)
#         # print(res, 'response')
#         # # self.assertEqual(res.status_code, 302)
#         # user.refresh_from_db()
#         # user = User.objects.get(email='pytest_tests@gmail.com')
#         # self.assertEqual(user.user_full_name, 'tesst')
#         # self.assertEqual(user.phone_number, 1234567891)
#
#         # Not updating if data is invalid
#         self.client.login(email="pytest_tests@gmail.com", password="Test@321")
#         data = {
#             'user_full_name': 'tessst',
#             'email': 'pytest_tests2@gmail.com',
#             'phone_number': 1230333237891
#         }
#         res = self.client.post(self.user_update_url, data)
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(self.user.user_full_name, 'test')
#         self.assertEqual(self.user.phone_number, 1230237891)
#
#     def test_user_update_user(self):
#         self.client.login(email="pytest_tests2@gmail.com", password="Test@321")
#         res = self.client.post(self.user_update_url)
#         self.assertEqual(res.status_code, 403)
#
#
# class TestCoupleDashboardViews(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#
#         self.user = User.objects.create_user(
#             user_full_name='test',
#             email='pytest_tests@gmail.com',
#             password='Test@321',
#             phone_number=1230237891,
#             is_active=True
#         )
#         self.user2 = User.objects.create_user(
#             user_full_name='test2',
#             email='pytest_tests2@gmail.com',
#             password='Test@321',
#             phone_number=1230237891,
#             is_active=True
#         )
#
#         self.checklist_obj = Task.objects.create(
#             name='test checklist',
#             category='test',
#             user=self.user,
#         )
#
#         self.checklist2 = Task.objects.create(
#             name='test2 checklist',
#             category='test2',
#             user=self.user2,
#         )
#
#         self.checklist = reverse('users-checklist')
#         self.delete_checklist = reverse('users-checklist-delete', kwargs={'pk': 1})
#
#     def test_user_task_list_get(self):
#         response = self.client.get(self.checklist)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url,  '/user/login/?next=' + self.checklist)
#
#         self.client.login(email="pytest_tests@gmail.com", password="Test@321")
#         response = self.client.get(self.checklist)
#         self.assertEqual(response.status_code, 200)
#
#     def test_user_task_post(self):
#         # Anonymous User
#         response = self.client.post(self.checklist)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/user/login/?next=' + self.checklist)
#
#         # User's Trying to create task
#         self.client.login(email="pytest_tests@gmail.com", password="Test@321")
#         self.assertEqual(Task.objects.filter(user=self.user).count(), 1)
#
#         response = self.client.post(self.checklist, {
#             'name': 'test checklist_2',
#             'category': 'teest',
#             'user': self.user
#         })
#
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(Task.objects.filter(user=self.user).count(), 2)
#         self.assertEqual(Task.objects.filter(user=self.user).last().name, 'test checklist_2')
#
#     def test_user_delete_other_user(self):
#         # User's Trying to delete task of other user
#         self.client.login(email="pytest_tests2@gmail.com", password="Test@321")
#
#         self.assertEqual(Task.objects.filter(user=self.user).count(), 1)
#         self.assertEqual(Task.objects.filter(user=self.user2).count(), 1)
#
#         res = self.client.post(reverse('users-checklist-delete',
#                                        kwargs={'pk': Task.objects.filter(user=self.user).first().id}))
#         self.assertEqual(res.status_code, 302)
#         self.assertEqual(Task.objects.filter(user=self.user).count(), 1)
#         self.assertEqual(Task.objects.filter(user=self.user2).count(), 1)
#
#         res = self.client.post(reverse('users-checklist-delete',
#                                        kwargs={'pk': Task.objects.filter(user=self.user).first().id}))
#         self.assertEqual(res.status_code, 302)
#
#     def test_user_task_delete(self):
#         # Anonymous User
#         response = self.client.post(self.delete_checklist)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/user/login/?next=' + self.delete_checklist)
#
#         # User's Trying to delete task
#         self.client.login(email="pytest_tests@gmail.com", password="Test@321")
#         self.assertEqual(Task.objects.filter(user=self.user).count(), 1)
#         self.assertEqual(Task.objects.count(), 2)
#
#         check_list_delete_id = Task.objects.filter(user=self.user).first().id
#         res = self.client.post(reverse('users-checklist-delete', kwargs={'pk': check_list_delete_id}))
#
#         self.assertEqual(res.status_code, 302)
#         self.assertEqual(Task.objects.count(), 1)
#         self.assertEqual(Task.objects.filter(user=self.user).count(), 0)
#
#
# class TestCoupleDashboardGuestViews(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#
#         self.user = User.objects.create_user(
#             user_full_name='test',
#             email='pytest_tests@gmail.com',
#             password='Test@321',
#             phone_number=1230237891,
#             is_active=True
#         )
#         self.user2 = User.objects.create_user(
#             user_full_name='test2',
#             email='pytest_tests2@gmail.com',
#             password='Test@321',
#             phone_number=1230237891,
#             is_active=True
#         )
#
#         self.checklist_obj = Budget.objects.create(
#             name='test checklist',
#             amount=200,
#             user=self.user,
#         )
#
#         self.checklist2 = Budget.objects.create(
#             name='test2 checklist',
#             amount=500,
#             user=self.user2,
#         )
#
#         self.checklist = reverse('users-budget-list')
#         self.delete_checklist = reverse('users-budget-delete', kwargs={'pk': 1})
#
#     def test_user_task_list_get(self):
#         response = self.client.get(self.checklist)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url,  '/user/login/?next=' + self.checklist)
#
#         self.client.login(email="pytest_tests@gmail.com", password="Test@321")
#         response = self.client.get(self.checklist)
#         self.assertEqual(response.status_code, 200)
#
#     def test_user_task_post(self):
#         # Anonymous User
#         response = self.client.post(self.checklist)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/user/login/?next=' + self.checklist)
#
#         # User's Trying to create task
#         self.client.login(email="pytest_tests@gmail.com", password="Test@321")
#         self.assertEqual(Budget.objects.filter(user=self.user).count(), 1)
#
#         response = self.client.post(self.checklist, {
#             'name': 'test checklist_2',
#             'amount': 400,
#             'user': self.user
#         })
#
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(Budget.objects.filter(user=self.user).count(), 2)
#         self.assertEqual(Budget.objects.filter(user=self.user).last().name, 'test checklist_2')
#
#     def test_user_delete_other_user(self):
#         # User's Trying to delete task of other user
#         self.client.login(email="pytest_tests2@gmail.com", password="Test@321")
#
#         self.assertEqual(Budget.objects.filter(user=self.user).count(), 1)
#         self.assertEqual(Budget.objects.filter(user=self.user2).count(), 1)
#
#         res = self.client.post(reverse('users-budget-delete', kwargs={'pk': 1}))
#         self.assertEqual(res.status_code, 302)
#         self.assertEqual(Budget.objects.filter(user=self.user).count(), 1)
#         self.assertEqual(Budget.objects.filter(user=self.user2).count(), 1)
#
#         res = self.client.post(self.delete_checklist)
#         self.assertEqual(res.status_code, 302)
#
#     def test_user_task_delete(self):
#         # Anonymous User
#         response = self.client.post(self.delete_checklist)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/user/login/?next=' + self.delete_checklist)
#
#         # User's Trying to delete task
#         self.client.login(email="pytest_tests@gmail.com", password="Test@321")
#         self.assertEqual(Budget.objects.filter(user=self.user).count(), 1)
#         self.assertEqual(Budget.objects.count(), 2)
#
#         check_list_delete_id = Budget.objects.filter(user=self.user).first().id
#         res = self.client.post(reverse('users-budget-delete', kwargs={'pk': check_list_delete_id}))
#
#         self.assertEqual(res.status_code, 302)
#         self.assertEqual(Budget.objects.count(), 1)
#         self.assertEqual(Budget.objects.filter(user=self.user).count(), 0)
#
#
#
#
