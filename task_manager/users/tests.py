from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreationTest(TestCase):
    fixtures = ['users_list.json']

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.client.force_login(self.user)
        User.objects.create(username='user1')
        User.objects.create(username='user2')
        User.objects.create(username='user3')

    def test_load_users(self):
        users = User.objects.all()
        print(users)
        self.assertEqual(len(users), 6)

    def test_user_admin(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(self.user.username, 'admin')
        self.assertTrue(self.user.is_superuser)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = self.client.post(reverse('user_create'),
            {
                'username': 'test',
                'password1': 'TestUserPassword',
                'password2': 'TestUserPassword',
                'first_name': 'test',
                'last_name': 'test',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='test').exists())

    def test_update_user(self):
        user = User.objects.get(pk=6)
        response = self.client.post(reverse('user_update',
                                            kwargs={'pk': user.pk}),
            {
                'username': 'new_username'
            }
        )
        updated_user = User.objects.get(pk=6)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_user.username, 'new_username')

    def test_delete_user(self):
        user = User.objects.get(pk=6)
        response = self.client.post(reverse('user_delete',
                                            kwargs={'pk': user.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=6).exists())