import cherrypy
from cherrypy.test import helper
from doctorapp.api import ApiV1
import json


SECRET_VALUE = "hello!"


def _fake_datasource():
    """
    Returns the mock secret value used for testing
    """
    return SECRET_VALUE


# See http://docs.cherrypy.org/en/latest/advanced.html#testing-your-application
class TestApp(helper.CPWebCase):
    @staticmethod
    def setup_server():
        cherrypy.tree.mount(ApiV1())
        cherrypy.engine.subscribe("get:secret", _fake_datasource)

    @staticmethod
    def teardown_server():
        cherrypy.engine.unsubscribe("get:secret", _fake_datasource)

    def test_health(self):
        """
        Test the health endpoint
        """
        self.getPage("/health")
        # OK response code
        self.assertStatus('200 OK')

        # json content type
        self.assertHeader('Content-Type', 'application/json')

        # json is correctly parsed (as both UTF8 then json)
        body = json.loads(self.body.decode("UTF-8"))

        # json has the 3 expected keys
        expected_keys = {'status', 'project', 'container'}
        assert set(body.keys()) == expected_keys

        # the keys should contain values
        for key in expected_keys:
            assert body[key]

        # the app should be "healthy"
        assert body['status'] == "healthy"

    def test_secret(self):
        """
        Test the secret endpoint.
        """
        self.getPage("/secret")
        # OK response code
        self.assertStatus('200 OK')

        # json content type
        self.assertHeader('Content-Type', 'application/json')

        # json is correctly parsed (as both UTF8 then json)
        body = json.loads(self.body.decode("UTF-8"))
        print(body)

        # json has the 3 expected keys
        expected_keys = {'secret_code'}
        assert set(body.keys()) == expected_keys

        # the secret should match
        assert body['secret_code'] == SECRET_VALUE

