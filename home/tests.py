# from django.test import TestCase, SimpleTestCase, Client, RequestFactory
# from django.urls import reverse, resolve
#
# from home.views import Home, NewsLetterCreateView, ContactView, SearchView, DestinationWeddingView, PlanningDecorView
# from home.models import NewsLetter, Contact, DestinationWedding
#
# from users.models import User
#
#
# # Url testing
# class TestUrls(SimpleTestCase):
#
#     def test_home_url_resolves(self):
#         url = reverse('home')
#         self.assertEqual(resolve(url).func.view_class, Home)
#
#     def test_news_letter_url_resolves(self):
#         url = reverse('news-letter')
#         self.assertEqual(resolve(url).func.view_class, NewsLetterCreateView)
#
#     def test_contact_url_resolves(self):
#         url = reverse('contact')
#         self.assertEqual(resolve(url).func.view_class, ContactView)
#
#     def test_search_url_resolves(self):
#         url = reverse('search')
#         self.assertEqual(resolve(url).func.view_class, SearchView)
#
#     def test_destination_wedding_url_resolves(self):
#         url = reverse('destination-wedding')
#         self.assertEqual(resolve(url).func.view_class, DestinationWeddingView)
#
#     def test_planning_decor_url_resolves(self):
#         url = reverse('planning-decor')
#         self.assertEqual(resolve(url).func.view_class, PlanningDecorView)
#
#
# class TestViews(TestCase):
#
#     def setUp(self):
#         # request = self.factory.post(reverse('home')
#         # self.factory = RequestFactory()
#         self.client = Client()
#         self.user = User.objects.create(
#             user_full_name='pytest_tests',
#             email='pytest_tests@gmail.com',
#             password='Test@321',
#             phone_number=1230237891,
#             is_active=True
#         )
#
#     def test_home_get(self):
#         response = self.client.get(reverse('home'))
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'home/home.html')
#
#     def test_home_post(self):
#         currency = 'INR'
#         self.user.currency = currency
#         session = self.client.session
#
#         response = self.client.post(reverse('home'), {
#             'currency': currency
#         })
#
#         session.update({
#             "currency": currency,
#         })
#         session.save()
#
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(session['currency'], currency)
#         self.assertEqual(self.user.currency, currency)
#
#     def test_home_post_no_data(self):
#         session = self.client.session
#
#         response = self.client.post(reverse('home'))
#
#         session.update({})
#         session.save()
#
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(self.user.currency, 'INR')
#
#     def test_new_letter_get(self):
#         response = self.client.get(reverse('news-letter'))
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'home/home.html')
#
#     def test_new_letter_post(self):
#         email = 'pytest_tests@gamil.com'
#         response = self.client.post(reverse('news-letter'), {
#             'email': email
#         })
#         news_letter = NewsLetter.objects.all().first()
#
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(news_letter.email, email)
#
#     # def test_new_letter_post_no_data(self):
#     #     response = self.client.post(reverse('news-letter'))
#     #     # news_letter = NewsLetter.objects.all().count()
#     #
#     #     self.assertEqual(response.status_code, 302)
#     #     self.assertEqual(0, 0)
#
#     def test_contact_get(self):
#         response = self.client.get(reverse('contact'))
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'home/contact.html')
#
#     def test_contact_create_POST(self):
#         url = reverse('contact')
#         response = self.client.post(url, {
#             'name': 'test1',
#             'email': 'pytest_tests@gmail.com',
#             'mobile': 1230237891,
#             'description': 'Test@321'
#         })
#
#         contact = Contact.objects.all().first()
#
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(contact.name, 'test1')
#
#     def test_contact_create_POST_no_data(self):
#         url = reverse('contact')
#         response = self.client.post(url)
#         contact = Contact.objects.all().count()
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(contact, 0)
#         self.assertTemplateUsed(response, 'home/contact.html')
#
#     def test_search_get(self):
#         response = self.client.get(reverse('search'))
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'home/search.html')
#
#     def test_destination_wedding_get(self):
#         response = self.client.get(reverse('destination-wedding'))
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'home/destination_wedding.html')
#
#     def test_planning_decor_get(self):
#         response = self.client.get(reverse('planning-decor'))
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'home/planning_decor.html')
#
#
#
