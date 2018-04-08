import unittest
import json

from lyft.session.session import Session


class SessionTest(unittest.TestCase):
    with open('config.json', 'r') as config:
        config_file = json.loads(config.read())

    def test_refresh_token_empty_config(self):
        config = {"client_id": "", "client_secret": ""}
        refresh_token = ""
        session = Session(config, refresh_token)
        self.assertGreater(len(session.refresh_access_token().get("error")), 1)

    def test_refresh_token_none_config(self):
        config = {"client_id": None, "client_secret": None}
        refresh_token = None
        session = Session(config, refresh_token)
        self.assertGreater(len(session.refresh_access_token().get("error")), 1)

    def test_refresh_token(self):
        refresh_token = self.config_file.get("refresh_token")
        session = Session(self.config_file, refresh_token)
        self.assertGreater(len(session.refresh_access_token().get("access_token")), 1)

    def test_reovke_token_empty_config(self):
        config = {"client_id": "", "client_secret": ""}
        refresh_token = ""
        session = Session(config, refresh_token)
        self.assertGreater(len(session.revoke_token()), 1)

    def test_revoke_token(self):
        refresh_token = self.config_file.get("refresh_token")
        session = Session(self.config_file, refresh_token)
        self.assertEqual(session.revoke_token().get("status"), True)
