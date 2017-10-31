import uuid
from os.path import basename
from unittest.case import TestCase

import alfredo


class AlfredoSDKTest(TestCase):
    def setUp(self):
        self.email = "%s@example.com" % (uuid.uuid4().hex,)
        self.password = 'pass!@#$%964'

    def test_can_do_a_complete_flow(self):
        user_created = alfredo.ruote().users.create(email=self.email, password=self.password)
        self.assertIsInstance(user_created.id, int)

        token = alfredo.ruote().sso.token_by_email.create(email=self.email, password=self.password).token
        self.assertEqual(len(token), 40)

        ruote = alfredo.ruote(token)
        self.assertGreaterEqual(set(dict(ruote).keys()), {'files', 'jobs', 'users', 'queues', 'apps', 'clusters'})
        self.assertIsNotNone(ruote.jobs.create.__call__)

        me = ruote.users.me
        self.assertTrue(bool(me))
        self.assertTrue(me.ok)
        self.assertEqual(me.email, self.email)
        self.assertEqual(me.id, user_created.id)

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

        for f in ruote.files:
            f.delete()

        files = ruote.files
        self.assertFalse(bool(files))
        self.assertEqual(len(files), 0)

        file_created = ruote.files.create(name=uuid.uuid4(), file=open(__file__, 'rb'))
        self.assertTrue(file_created.ok, file_created)
        self.assertEqual(file_created.name, basename(__file__))

        file_tried = ruote.files.create(name=uuid.uuid4(), file=open(__file__, 'rb'))
        self.assertFalse(file_tried.ok, file_tried)
        self.assertRegexpMatches(file_tried.detail, 'already.*uploaded')

        files = ruote.files
        self.assertTrue(bool(files))
        self.assertEqual(len(files), 1)

        for f in ruote.files:
            file_deleted = f.delete()
            self.assertTrue(file_deleted.ok, file_deleted)

        app_created = ruote.apps.create(name='app', container_checksum='000', container_url='http://example.com/app')
        self.assertTrue(app_created.ok, app_created)
