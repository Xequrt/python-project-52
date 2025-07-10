from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status

User = get_user_model()

class StatusTest(TestCase):
    fixtures = ['statuses_list.json']

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.client.force_login(self.user)

    def test_create_status(self):
        response = self.client.post(reverse('statuses_create'),
            {
                'name': 'test',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='test').exists())

    def test_update_status(self):
        status = Status.objects.get(pk=3)
        response = self.client.post(reverse('statuses_update',
                                            kwargs={'pk': status.pk}),
            {
                'name': 'new_test'
            }
        )
        updated_status = Status.objects.get(pk=3)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_status.name, "new_test")

    def test_delete_status(self):
        status = Status.objects.get(pk=3)
        response = self.client.post(reverse('statuses_delete',
                                            kwargs={'pk': status.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=3).exists())