from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User

from monsters.models import Monster
from monsters.views import DungeonView


class DungeonViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.dungeon_url = reverse('dungeon')

    def test_render_dungeon_page_for_authenticated_user(self):
        user = User.objects.create_user(username='test_user', email='test@example.com',
                                        password='testpassword')

        request = self.factory.get(self.dungeon_url)
        request.user = user

        response = DungeonView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_get_context_data(self):
        user = User.objects.create_user(username='test_user', email='test@example.com',
                                        password='testpassword')
        # Create sample monsters with specific attributes
        monster1 = Monster.objects.create(
            name='Monster 1',
            description='Description for Monster 1',
            level=10,
            health=100,
            strength=50,
            agility=30,
            damage=40,
            armor=20,
            base_gold_gained=200,
            base_exp_gained=100,
            image_path='path/to/image1.jpg',
            rating=4
        )
        monster2 = Monster.objects.create(
            name='Monster 2',
            description='Description for Monster 2',
            level=5,
            health=44,
            strength=50,
            agility=30,
            damage=40,
            armor=20,
            base_gold_gained=200,
            base_exp_gained=100,
            image_path='path/to/image1.jpg',
            rating=3
        )

        request = self.factory.get(self.dungeon_url)
        request.user = user
        response = DungeonView.as_view()(request)

        # Check if the view returns a successful response
        self.assertEqual(response.status_code, 200)

        # Check if the context contains the expected monsters
        context = response.context_data
        self.assertIn('monsters', context)
        monsters = context['monsters']
        self.assertEqual(monsters.count(), 2)

        # Check if monsters are ordered by rating
        self.assertEqual(monsters[0].name, 'Monster 2')
        self.assertEqual(monsters[1].name, 'Monster 1')

        self.assertEqual(monsters[0].level, 5)
        self.assertEqual(monsters[0].health, 44)
        self.assertEqual(monsters[0].strength, 50)
        self.assertEqual(monsters[0].agility, 30)

        self.assertEqual(monsters[1].level, 10)
        self.assertEqual(monsters[1].health, 100)
        self.assertEqual(monsters[1].strength, 50)
        self.assertEqual(monsters[1].agility, 30)
