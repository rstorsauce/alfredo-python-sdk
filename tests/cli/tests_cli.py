import sys
import uuid
from os.path import basename
from unittest.case import TestCase

import ruamel.yaml as yaml

from alfredo import cli

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class AlfredoCLITest(TestCase):
    def setUp(self):
        self.email = "%s@example.com" % (uuid.uuid4().hex,)
        self.password = 'password'

    @classmethod
    def fake_exit(cls, exit_code):
        cls.exit_code = exit_code

    def mock_std_streams(self):
        self.sys_stdout_backup = sys.stdout
        self.sys_stderr_backup = sys.stderr

        sys.stdout = StringIO()
        sys.stderr = StringIO()

    def restore_std_streams(self):
        sys.stdout.close()
        sys.stderr.close()

        sys.stdout = self.sys_stdout_backup
        sys.stderr = self.sys_stderr_backup

    def sh(self, *args):
        self.mock_std_streams()

        try:
            sys.argv = ['alfredo-test'] + [str(arg) for arg in args]
            cli.main()
            exit_code = 0
        except SystemExit as e:
            exit_code = int(e.code)

        stdout = sys.stdout.getvalue()
        stderr = sys.stderr.getvalue()

        self.restore_std_streams()

        if exit_code != 0:
            raise RuntimeError("%d\n%s\n%s" % (exit_code, stdout, stderr))

        return yaml.safe_load(stdout)

    def test_can_do_a_complete_flow(self):
        try:
            self.sh("logout")
        except RuntimeError:
            pass

        user_created = self.sh("ruote", "users", "-C", "-i", repr({"email": self.email, "password": self.password}))
        self.assertIsInstance(user_created['id'], int)

        token = self.sh("ruote", "sso", "token_by_email", "-C", "-i", repr({"email": self.email, "password": self.password}))["token"]
        self.assertEqual(len(token), 40)

        self.sh("login", "-i", repr({"email": self.email, "password": self.password}))

        me = self.sh("ruote", "users", "me")
        self.assertEqual(me['email'], self.email)
        self.assertEqual(me['id'], user_created['id'])
        self.assertNotIn('missing_attribute', me)

        first_name = 'Bob'
        payload = yaml.safe_dump({"first_name": first_name})
        changed_name = self.sh("ruote", "users", "me", "-U", "-i", payload)
        self.assertEqual(changed_name['first_name'], first_name)

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

        app_created = self.sh("ruote", "apps", "-C", "-i",
                              repr({"name": 'app', "container_checksum": '000', "container_url": 'http://app/'}))
        self.assertIsInstance(app_created['id'], int)
