import tempfile
import uuid
from unittest.case import TestCase

import alfredo
from tests import use_mock_http, mock_http


class HttpTest(TestCase):
    def setUp(self):
        self.ruote = alfredo.ruote()

    @use_mock_http
    def test_sdk_can_navigate_through_the_endpoints(self):
        mock_http()

        user = self.ruote.users.me
        self.assertTrue(user.ok)
        self.assertEqual(user.first_name, 'Bob')

        user = self.ruote.users.me.replace(first_name='Alice')
        self.assertTrue(bool(user))
        self.assertTrue(user.ok)
        self.assertEqual(user.first_name, 'Alice')

        user = self.ruote.users.me.update(first_name='Charles')
        self.assertTrue(bool(user))
        self.assertTrue(user.ok)
        self.assertEqual(user.first_name, 'Charles')

        app = self.ruote.apps.create(name='Octave')
        self.assertTrue(bool(app))
        self.assertTrue(app.ok)
        self.assertEqual(app.name, 'Octave')

        apps = self.ruote.apps
        self.assertTrue(bool(apps))
        self.assertTrue(apps.ok)
        self.assertEqual(len(apps), 1)
        self.assertEqual(apps[0].id, 1)

        app = self.ruote.apps.id(1)
        self.assertTrue(bool(app))
        self.assertTrue(app.ok)
        self.assertEqual(app.name, 'Octave')
        self.assertEqual(app.native()['name'], 'Octave')

        app_deleted = self.ruote.apps.id(1).delete()
        self.assertTrue(bool(app_deleted))
        self.assertTrue(app_deleted.ok)
        self.assertEqual(app_deleted.status, 204)

        files = self.ruote.files
        self.assertEqual(len(files), 0)
        self.assertFalse(bool(files))
        self.assertTrue(files.ok)

        # uploaded_file = tempfile.NamedTemporaryFile()
        # file_created = self.ruote.files.create(name=uuid.uuid4(), file=uploaded_file.name)
        # self.assertTrue(bool(file_created))
        # self.assertTrue(file_created.ok)
        # self.assertEqual(file_created.name, uploaded_file.name.split('/')[-1])

        # file_error = self.ruote.files.create(name=uuid.uuid4(), file=uuid.uuid4())
        # self.assertTrue(bool(file_error))
        # self.assertFalse(file_error.ok)
        # self.assertEqual(file_created.name, uploaded_file.name.split('/')[-1])
