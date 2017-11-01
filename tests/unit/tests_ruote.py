import os
import tempfile
import uuid
from os.path import basename
from unittest.case import TestCase

import alfredo


class AlfredoSDKTest(TestCase):
    def setUp(self):
        self.email = os.environ['TEST_USER']
        self.password = os.environ['TEST_PASSWORD']

    def test_can_do_a_complete_flow(self):
        token = alfredo.ruote().sso.token_by_email.create(email=self.email, password=self.password).token
        self.assertEqual(len(token), 40)

        ruote = alfredo.ruote(token)
        self.assertGreaterEqual(set(dict(ruote).keys()), {'files', 'jobs', 'users', 'queues', 'apps', 'clusters'})
        self.assertIsNotNone(ruote.jobs.create.__call__)

        me = ruote.users.me
        self.assertTrue(bool(me))
        self.assertTrue(me.ok)
        self.assertEqual(me.email, self.email)

        with self.assertRaises(AttributeError):
            print(me.missing_attribute)

        changed_name = me.update(first_name='Bob')
        self.assertEqual(changed_name.first_name, "Bob")

        tried_change_name = me.replace(first_name='Bob')
        self.assertFalse(tried_change_name.ok, tried_change_name)
        self.assertEqual(tried_change_name.status, 405)

        user = ruote.users.id(me.id)
        self.assertEqual(user.email, self.email)

        cluster_created = ruote.clusters.create(name=uuid.uuid4())
        self.assertIn(cluster_created.id, (cluster.id for cluster in ruote.clusters))

        queue_q = ruote.queues.create(cluster=cluster_created.id, name='q')
        self.assertEqual(queue_q.cluster, cluster_created.id)

        queue_p = ruote.queues.create(cluster=cluster_created, name='p')
        self.assertEqual(queue_p.cluster, cluster_created.id)

        uploaded_file = tempfile.NamedTemporaryFile()

        file_created = ruote.files.create(name=uuid.uuid4(), file=uploaded_file.name)
        self.assertTrue(file_created.ok, file_created)
        self.assertEqual(file_created.name, uploaded_file.name.split('/')[-1])

        file_deleted = ruote.files.id(file_created.id).delete()
        self.assertTrue(file_deleted.ok, file_deleted)

        app_created = ruote.apps.create(name='app', container_checksum='000', container_url='http://example.com/app')
        self.assertTrue(app_created.ok, app_created)
