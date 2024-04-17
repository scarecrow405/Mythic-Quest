from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from games.models import Game
from characters.models import Character
from profiles.models import UserProfile


class EarnGoldByClickingGameViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.character = Character.objects.create(user=self.user)
        self.game = Game.objects.create(name="Gold Game", gold_to_gain=1000)

    def test_redirect_for_anonymous_user(self):
        response = self.client.get(reverse('earn_gold_by_clicking'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_view_rendering_for_logged_in_user(self):
        self.client.login(username='testuser', password='password')

        response = self.client.get(reverse('earn_gold_by_clicking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/earn_gold_by_clicking_game.html')

    def test_gold_earning(self):
        self.client.login(username='testuser', password='password')

        self.character.current_clicks = 0
        self.character.save()

        response = self.client.post(reverse('earn_gold_by_clicking'))

        self.character.refresh_from_db()
        self.assertEqual(self.character.current_clicks, 100)
        self.assertEqual(self.character.gold, 1000)

    def test_clicking_button(self):
        self.client.login(username='testuser', password='password')

        self.character.current_clicks = 0
        self.character.save()

        self.client.get(reverse('earn_gold_by_clicking'))

        for _ in range(5):
            response = self.client.post(reverse('earn_gold_by_clicking'))

        self.character.refresh_from_db()
        self.assertEqual(self.character.current_clicks, 500)

    def test_game_existence(self):
        self.assertTrue(Game.objects.filter(gold_to_gain=1000).exists())
