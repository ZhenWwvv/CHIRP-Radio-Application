import time
import json

from mock import patch
from tornado import gen
from tornado.websocket import websocket_connect
from tornado.testing import AsyncHTTPTestCase, gen_test
from chirp.common.printing import cprint

from . import app


class TestPages(AsyncHTTPTestCase):
    def get_app(self):
        return app.get_app()

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        body = response.body.decode('utf-8')

        # Check that title is there.
        self.assertIn('<h1>CHIRP Command Center</h1>', body)

        # Check that links are present.
        self.assertRegexpMatches(
            body,
            r'<a href="/new-artists/" class="[^"]+">See new artists</a>')

    def test_new_artists_page(self):
        response = self.fetch('/new-artists/')
        self.assertEqual(response.code, 200)
        body = response.body.decode('utf-8')

        self.assertIn('See new artists</h1>', body)
        self.assertIn(
            'This command will show you what artists are (supposedly) not yet in the database.',
            body)


class TestCommands(AsyncHTTPTestCase):
    @patch.object(app, 'COMMAND_PAGES')
    def get_app(self, command_pages):
        # Fake command function that runs for 0.5 seconds.
        def new_artists():
            time.sleep(0.25)
            yield
            time.sleep(0.25)
            yield
            cprint('123 new artists found')

        command_pages.__iter__.return_value = [
            ('new-artists', new_artists),
        ]
        self.current_app = app.get_app()
        return self.current_app

    @gen_test
    def test_start_command(self):
        # Connect to websocket.
        url = 'ws://localhost:%s/new-artists/messages/' % self.get_http_port()
        conn = yield websocket_connect(url)

        # Check that command is not running.
        self.assertIsNone(self.current_app.current_task)

        # Start the command.
        response = yield self.http_client.fetch(self.get_url('/new-artists/start/'))
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'ok')

        # Check that command is still running.
        self.assertIsNotNone(self.current_app.current_task)

        # Check the messages from the command.
        msg = yield conn.read_message()
        obj = json.loads(msg)
        self.assertEqual(obj['value'], '123 new artists found')

        msg = yield conn.read_message()
        obj = json.loads(msg)
        self.assertEqual(obj, {'type': 'finish'})

        # Check that command has stopped.
        yield gen.sleep(0.5)
        self.assertIsNone(self.current_app.current_task)

    @gen_test
    def test_stop_command(self):
        # Connect to websocket.
        url = 'ws://localhost:%s/new-artists/messages/' % self.get_http_port()
        conn = yield websocket_connect(url)

        # Check that command is not running.
        self.assertIsNone(self.current_app.current_task)

        # Start the command.
        yield self.http_client.fetch(self.get_url('/new-artists/start/'))

        # Check that command was started.
        self.assertIsNotNone(self.current_app.current_task)

        # Stop the command.
        response = yield self.http_client.fetch(self.get_url('/new-artists/stop/'))
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'ok')

        # Check the message from the command.
        msg = yield conn.read_message()
        obj = json.loads(msg)
        self.assertEqual(obj, {'type': 'stop'})

        # Check that command has stopped.
        self.assertIsNone(self.current_app.current_task)


class TestErrorInCommand(AsyncHTTPTestCase):
    @patch.object(app, 'COMMAND_PAGES')
    def get_app(self, command_pages):
        # Fake command function that raises an exception.
        def new_artists():
            yield
            raise Exception('Something crazy happened!')
            yield

        command_pages.__iter__.return_value = [
            ('new-artists', new_artists),
        ]
        self.current_app = app.get_app()
        return self.current_app

    @gen_test
    def test_error_in_command(self):
        # Connect to websocket.
        url = 'ws://localhost:%s/new-artists/messages/' % self.get_http_port()
        conn = yield websocket_connect(url)

        # Start the command.
        self.http_client.fetch(self.get_url('/new-artists/start/'))

        # Check the message from the command.
        msg = yield conn.read_message()
        obj = json.loads(msg)
        self.assertEqual(obj['value'], 'Something crazy happened!')
        self.assertEqual(obj['type'], 'failure')
        self.assertIn('Traceback (most recent call last)', obj['stacktrace'])

        # Check that command has stopped.
        self.assertIsNone(self.current_app.current_task)
