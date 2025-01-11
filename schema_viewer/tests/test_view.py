import json

from django.test import TestCase


class ViewTest(TestCase):
    def test_view(self):
        response = self.client.get('/schema-viewer/')
        self.assertContains(response, 'django-schema-viewer')

    def test_schema(self):
        tables = {
            'auth_permission',
            'django_admin_log',
            'auth_group',
            'auth_group_permissions',
            'auth_user',
            'auth_user_user_permissions',
            'auth_user_groups',
            'django_content_type',
            'django_session',
        }

        response = self.client.get('/schema-viewer/schema/')
        schema = json.loads(response.content)
        self.assertTrue({t['name'] for t in schema['resources']}, tables)
