from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from profiles.views import signout_user


class SignoutUserViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.signout_url = reverse('signout')
        self.signin_url = reverse('signin')

    def test_authenticated_user_signout(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        self.client.login(username='testuser', password='testpassword')

        session = self.client.session

        session['user_id'] = user.id
        session.save()

        request = self.factory.get(self.signout_url)
        request.user = user
        request.session = session

        response = signout_user(request)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(response.url, self.signin_url)
