from django.test import TestCase

from schema_viewer.schema import get_schema


class SchemaTest(TestCase):
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
        schema = get_schema()
        self.assertTrue({t['name'] for t in schema['resources']} == tables)
