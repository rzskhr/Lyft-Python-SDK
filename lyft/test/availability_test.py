import configparser
import json
import unittest

from lyft.authentication.auth import LyftPublicAuth
from lyft.availability import Availability
from lyft.test import availability_res

# path to secret access config file
ACCESS_TOKEN_PATH = "/Users/Raj/Root/Code/_PRIVATE_KEYS/lyft/test_app.cfg"
# file format/ content, save as .cfg
"""
[lyft]
client_id: YOUR CLIENT ID
client_secret: YOUR CLIENT SECRET
"""

config = configparser.ConfigParser()
config.read(ACCESS_TOKEN_PATH)
client_id = config.get('lyft', 'client_id')
client_secret = config.get('lyft', 'client_secret')

# get access token and token type
LyftPublicAuth_obj = LyftPublicAuth({'client_id': client_id, 'client_secret': client_secret})
res = json.loads(LyftPublicAuth_obj.get_access_token())
access_token = res['access_token']
token_type = res['token_type']


class TestAvailability(unittest.TestCase):
    def test_get_ride_types(self):
        ride_types = Availability(token_type, access_token).get_ride_types(37.7763, -122.3918)
        self.assertEqual(ride_types, availability_res.ride_types_res)

    def test_get_ride_types_lyft_line(self):
        ride_types = Availability(token_type, access_token).get_ride_types(37.7763, -122.3918, 'lyft_line')
        self.assertEqual(ride_types, availability_res.ride_types_lyft_line_res)

    def test_get_ride_types_lyft(self):
        ride_types = Availability(token_type, access_token).get_ride_types(37.7763, -122.3918, 'lyft')
        self.assertEqual(ride_types, availability_res.ride_types_lyft_res)

    def test_get_ride_types_lyft_plus(self):
        ride_types = Availability(token_type, access_token).get_ride_types(37.7763, -122.3918, 'lyft_plus')
        self.assertEqual(ride_types, availability_res.ride_types_lyft_plus_res)

    def test_get_ride_types_lyft_premier(self):
        ride_types = Availability(token_type, access_token).get_ride_types(37.7763, -122.3918, 'lyft_premier')
        self.assertEqual(ride_types, availability_res.ride_types_lyft_premier_res)

    def test_get_ride_types_lyft_lux(self):
        ride_types = Availability(token_type, access_token).get_ride_types(37.7763, -122.3918, 'lyft_lux')
        self.assertEqual(ride_types, availability_res.ride_types_lyft_lux_res)

    def test_get_ride_types_lyft_luxsuv(self):
        ride_types = Availability(token_type, access_token).get_ride_types(37.7763, -122.3918, 'lyft_luxsuv')
        self.assertEqual(ride_types, availability_res.ride_types_lyft_luxsuv_res)


if __name__ == '__main__':
    unittest.main()
