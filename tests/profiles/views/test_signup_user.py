from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.views import signup_user


class SignupUserViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.signup_url = reverse('signup')
        self.index_url = reverse('index')

    def test_signup_with_authenticated_user(self):
        request = self.factory.get(self.signup_url)
        request.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        response = signup_user(request)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(response.url, self.index_url)
