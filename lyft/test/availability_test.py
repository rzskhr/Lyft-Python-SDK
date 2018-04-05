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
        """
        This test case tests the get_ride_types(self, lat, lng, ride_type=None) method
        in lyft.availability.Availability module
        """
        self.assertEqual(Availability(token_type, access_token).get_ride_types(37.7763, -122.3918),
                         availability_res.ride_types_res)
        self.assertEqual(Availability(token_type, access_token).get_ride_types(37.7763, -122.3918, 'lyft_line'),
                         availability_res.ride_types_lyft_line_res)
        self.assertEqual(Availability(token_type, access_token).get_ride_types(37.7763, -122.3918, 'lyft'),
                         availability_res.ride_types_lyft_res)
        self.assertEqual(Availability(token_type, access_token).get_ride_types(37.7763, -122.3918, 'lyft_plus'),
                         availability_res.ride_types_lyft_plus_res)
        self.assertEqual(Availability(token_type, access_token).get_ride_types(37.7763, -122.3918, 'lyft_premier'),
                         availability_res.ride_types_lyft_premier_res)
        self.assertEqual(Availability(token_type, access_token).get_ride_types(37.7763, -122.3918, 'lyft_lux'),
                         availability_res.ride_types_lyft_lux_res)
        self.assertEqual(Availability(token_type, access_token).get_ride_types(37.7763, -122.3918, 'lyft_luxsuv'),
                         availability_res.ride_types_lyft_luxsuv_res)


if __name__ == '__main__':
    unittest.main()
