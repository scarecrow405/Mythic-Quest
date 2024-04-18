from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User

from characters.models import Character
from items.models import Item
from items.views import PotionShopView


class PotionShopViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.character = Character.objects.create(user=self.user, gold=1000)
        self.item = Item.objects.create(name='Test Potion', effect='EXP Boost', price=100)

    def test_view_loads_successfully(self):
        url = reverse('items_potions')
        request = self.factory.get(url)
        request.user = self.user
        response = PotionShopView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_purchase_item(self):
        url = reverse('items_potions')
        request = self.factory.post(url, {'buy_item': '', 'item_id': self.item.pk})
        request.user = self.user
        response = PotionShopView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.character.refresh_from_db()
        self.assertEqual(self.character.gold, 900)


class PotionShopIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.character = Character.objects.create(user=self.user, gold=1000)
        self.item = Item.objects.create(name='Test Potion', effect='EXP Boost', price=100)

    def test_purchase_item(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('items_potions'), {'buy_item': '', 'item_id': self.item.pk})
        self.assertEqual(response.status_code, 302)
        self.character.refresh_from_db()
        self.assertEqual(self.character.gold, 900)
