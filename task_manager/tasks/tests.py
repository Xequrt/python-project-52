from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.tasks.models import Task

User = get_user_model()

class TaskTest(TestCase):
    fixtures = ['statuses_list.json', 'users_list.json', 'tasks_list.json']


    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.another_user = User.objects.get(username='Test')
        self.client.force_login(self.user)


    def test_create_task(self):
        response = self.client.post(reverse('tasks_create'),
            {
                'name': 'test_task',
                'status': 2
            }
        )

        created_task = Task.objects.get(name='test_task')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(created_task.name, 'test_task')

    def test_update_task(self):
        task = Task.objects.get(name='#3')
        response = self.client.post(reverse('tasks_update',
                                            kwargs={'pk': task.pk}),
            {
                'name': '#3 test',
                'status': 2
            }
        )
        updated_task = Task.objects.get(name='#3 test')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_task.name, '#3 test')

    def test_delete_task_another_author(self):
        self.client.force_login(self.another_user)
        task = Task.objects.get(name='#3')
        response = self.client.post(reverse('tasks_delete',
                                            kwargs={'pk': task.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(task.author, self.another_user)
        self.assertTrue(Task.objects.filter(name='#3').exists())

    def test_delete_task(self):
        task = Task.objects.get(name='#3')
        response = self.client.post(reverse('tasks_delete',
                                            kwargs={'pk': task.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name='#3').exists())