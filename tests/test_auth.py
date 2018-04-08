import unittest
import json

from lyft.authentication.auth import LyftPublicAuth, LyftUserAuth


class PublicAuthTest(unittest.TestCase):
    with open('config.json', 'r') as config:
        config_file = json.loads(config.read())

    def test_access_token_empty_config(self):
        config = {"client_id": "", "client_secret": ""}
        auth = LyftPublicAuth(config, sandbox_mode=True)
        self.assertGreater(len(auth.get_access_token().get("error")), 1)

    def test_access_token_None_config(self):
        config = {"client_id": None, "client_secret": None}
        auth = LyftPublicAuth(config, sandbox_mode=True)
        self.assertGreater(len(auth.get_access_token().get("error")), 1)

    def test_access_token_wrong(self):
        config = {"client_id": "3423423", "client_secret": None}
        auth = LyftPublicAuth(config, sandbox_mode=True)
        self.assertGreater(len(auth.get_access_token().get("error")), 1)

    def test_access_token_correct(self):
        auth = LyftPublicAuth(self.config_file, sandbox_mode=True)
        self.assertGreater(len(auth.get_access_token().get("access_token")), 1)


class UserAuthTest(unittest.TestCase):
    with open('config.json', 'r') as config:
        config_file = json.loads(config.read())

    def test_auth_uri_empty_config(self):
        config = {"client_id": "", "client_secret": ""}
        auth = LyftUserAuth(config, [], "", sandbox_mode=True)
        self.assertEqual(auth.get_authorization_uri(), None)

    def test_auth_uri_empty_scope(self):
        config = {"client_id": "ertyy", "client_secret": ""}
        auth = LyftUserAuth(config, [], "", sandbox_mode=True)
        self.assertEqual(auth.get_authorization_uri(), None)

    def test_auth_uri_correct_config(self):
        auth = LyftUserAuth(self.config_file, ["rides.read", "offline"], "hello")
        self.assertIsNotNone(auth.get_authorization_uri())

    def test_get_access_token_invalid_authorization_code(self):
        auth = LyftUserAuth(self.config_file, ["rides.read", "offline"], "hello")
        self.assertGreater(len(auth.get_access_token("3-Kad").get("error")), 1)
