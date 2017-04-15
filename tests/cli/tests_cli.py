import subprocess
import uuid
from os.path import basename
from unittest.case import TestCase

import ruamel.yaml as yaml


class AlfredoCLITest(TestCase):
    def setUp(self):
        self.email = "%s@example.com" % (uuid.uuid4().hex,)
        self.password = 'password'

    @staticmethod
    def sh(*args):
        full_command = ["python", "./cli.py"] + [str(arg) for arg in args]
        process = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = process.communicate()
        exit_code = process.poll()
        if exit_code != 0:
            raise RuntimeError("%dxx - %s" % (exit_code, stdout,))
        return yaml.safe_load(stdout)

    def test_can_do_a_complete_flow(self):
        try:
            self.sh("logout")
        except RuntimeError:
            pass

        user_created = self.sh("ruote", "users", "-C", "-i", repr({"email": self.email, "password": self.password}))
        self.assertIsInstance(user_created['id'], int)

        token = self.sh("ruote", "sso", "token_by_email", "-C", "-i",
                        repr({"email": self.email, "password": self.password}))["token"]
        self.assertEqual(len(token), 40)

        self.sh("login", "-i", repr({"email": self.email, "password": self.password}))

        me = self.sh("ruote", "users", "me")
        self.assertEqual(me['email'], self.email)
        self.assertEqual(me['id'], user_created['id'])
        self.assertNotIn('missing_attribute', me)

        changed_name = self.sh("ruote", "users", "me", "-U", "-i", repr({"first_name": 'Bob'}))
        self.assertEqual(changed_name['first_name'], "Bob")

        user = self.sh("ruote", "users", "id:{}".format(me['id']))
        self.assertEqual(user['email'], self.email)

        cluster_created = self.sh("ruote", "clusters", "-C", "-i", repr({"name": uuid.uuid4().hex}))
        self.assertIn(cluster_created["id"], (cluster['id'] for cluster in self.sh("ruote", "clusters")))

        queue_q = self.sh("ruote", "queues", "-C", "-i", repr({"name": "q", "cluster": cluster_created['id']}))
        self.assertEqual(queue_q['cluster'], cluster_created['id'])

        for f in self.sh("ruote", "files"):
            self.sh("ruote", "files", "id:{}".format(f['id']), "-D")

        files = self.sh("ruote", "files")
        self.assertEqual(len(files), 0)

        file_created = self.sh("ruote", "files", "-C", "-i", repr({'name': uuid.uuid4().hex, "file": __file__}))
        self.assertIsInstance(file_created['id'], int)
        self.assertEqual(file_created['name'], basename(__file__))

        with self.assertRaisesRegexp(RuntimeError, 'already.*uploaded'):
            self.sh("ruote", "files", "-C", "-i", repr({'name': uuid.uuid4().hex, "file": __file__}))

        files = self.sh("ruote", "files")
        self.assertEqual(len(files), 1)

        for f in self.sh("ruote", "files"):
            self.sh("ruote", "files", "id:{}".format(f['id']), "-D")

        app_created = self.sh("ruote", "apps", "-C", "-i", repr({"name": 'app', "container_checksum": '000', "container_url": 'http://app/'}))
        self.assertIsInstance(app_created['id'], int)
