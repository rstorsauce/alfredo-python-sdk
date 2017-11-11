import sys
from unittest.case import TestCase

from alfredo.cli import CLI
from tests import use_mock_http, mock_http

import ruamel.yaml as yaml

from alfredo import cli

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class CLIRuntimeError(RuntimeError):
    def __init__(self, exit_code, stdout, stderr):
        super(CLIRuntimeError, self).__init__(exit_code)
        self._exit_code = exit_code
        self._stdout = stdout
        self._stderr = stderr

    def __str__(self):
        return "%d\n%s\n%s" % (self._exit_code, self._stdout, self._stderr)


class AlfredoCLITest(TestCase):

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
        print(args)
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
            raise CLIRuntimeError(exit_code, stdout, stderr)

        return yaml.safe_load(stdout)

    @use_mock_http
    def test_cli_can_navigate_through_the_endpoints(self):
        mock_http()

        user = self.sh("ruote", "users", "me")
        self.assertEqual(user['first_name'], 'Bob')

        user = self.sh("ruote", "users", "me", "-X", "-i", repr({"first_name": "Alice"}))
        self.assertEqual(user['first_name'], 'Alice')

        user = self.sh("ruote", "users", "me", "-U", "-i", repr({"first_name": "Charles"}))
        self.assertEqual(user['first_name'], 'Charles')

        app = self.sh("ruote", "apps", "-C", "-i", repr({"name": "Octave"}))
        self.assertEqual(app['name'], 'Octave')

        apps = self.sh("ruote", "apps")
        self.assertEqual(apps, [{'id': 1, 'name': 'Octave'}])

        app = self.sh("ruote", "apps", "id:1")
        self.assertEqual(app, {'name': 'Octave'})

        app_deleted = self.sh("ruote", "apps", "id:1", "-D")
        self.assertEqual(app_deleted, {})

        files = self.sh("ruote", "files")
        self.assertEqual(files, [])

    @use_mock_http
    def test_cli_can_get_output_attrs(self):
        mock_http()

        apps = self.sh("ruote", "apps", "-o", "id,name")
        self.assertEqual(apps, [{'id': 1, 'name': 'Octave'}])

        apps = self.sh("ruote", "apps", "-o", "id")
        self.assertEqual(apps, [1])

    @use_mock_http
    def test_cli_can_get_different_content_types(self):
        mock_http()

        stdout = self.sh("ruote", "jobs", "id:1", "stdout")
        self.assertEqual(stdout, "hello")

    def t(self, *args, **kwargs):
        pass

    @use_mock_http
    def test_cli_can_manage_different_errors(self):
        mock_http()

        with self.assertRaisesRegexp(CLIRuntimeError, str(CLI.COMMAND_LINE_ERROR)):
            self.sh("ruote", "jobs", "-C", "-i")

        with self.assertRaisesRegexp(CLIRuntimeError, str(CLI.INPUT_ERROR)):
            self.sh("ruote", "jobs", "-C", "-i", "string")

        with self.assertRaisesRegexp(CLIRuntimeError, str(CLI.INPUT_ERROR)):
            self.sh("ruote", "jobs", "-C", "-i", "3")

        with self.assertRaisesRegexp(CLIRuntimeError, str(CLI.INPUT_ERROR)):
            self.sh("ruote", "jobs", "-C", "-i", "{3:a,")

        with self.assertRaisesRegexp(CLIRuntimeError, str(CLI.HTTP_UPSTREAM_SERVER_ERROR)):
            self.sh("ruote", "jobs")

        with self.assertRaisesRegexp(CLIRuntimeError, str(CLI.HTTP_UPSTREAM_CLIENT_ERROR)):
            self.sh("ruote", "users")

        with self.assertRaisesRegexp(CLIRuntimeError, str(CLI.CONNECTION_ERROR)):
            self.sh("ruote", "users", "id:1")
