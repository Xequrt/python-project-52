from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label

User = get_user_model()


class LabelTest(TestCase):
    fixtures = ['labels_list.json', 'users_list.json']

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.another_user = User.objects.get(username='Test')
        self.client.force_login(self.user)

    def test_create_label(self):
        response = self.client.post(reverse('label_create'),
            {
                'name': 'Новая метка',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Новая метка').exists())

    def test_update_label(self):
        label = Label.objects.get(pk=1)
        response = self.client.post(reverse('label_update',
                                            kwargs={'pk': label.pk}),
            {
                'name': 'new_test'
            }
        )
        updated_label = Label.objects.get(pk=1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_label.name, "new_test")

    def test_delete_label(self):
        label = Label.objects.get(pk=1)
        response = self.client.post(reverse('label_delete',
                                            kwargs={'pk': label.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=1).exists())

    def test_delete_label_another_author(self):
        self.client.force_login(self.another_user)
        label = Label.objects.get(pk=1)
        response = self.client.post(reverse('label_delete',
                                            kwargs={'pk': label.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(label.name, self.another_user)
        self.assertTrue(Label.objects.filter(name='Фича').exists())
