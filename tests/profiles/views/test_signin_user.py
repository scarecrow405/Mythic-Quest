from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.views import signin_user


class SigninUserViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.signin_url = reverse('signin')
        self.index_url = reverse('index')

    def test_authenticated_user_redirect_to_index(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        request = self.factory.get(self.signin_url)
        request.user = user
        response = signin_user(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.index_url)
