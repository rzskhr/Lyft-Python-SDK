import json
import requests

from lyft.util.url_util import RIDE


class Rides:

    def __init__(self, token_type, access_token):
        """Class for various related operations

        :param token_type: Token type
        :param access_token:
        """
        self.token_type     = token_type
        self.__access_token = access_token

    def create_ride_request(self, ride_type, src_lat, src_lng, dest_lat, dest_lng, src_address=None, dest_address=None):
        """Creates a ride and returns a ride_response object.
        https://developer.lyft.com/reference#ride-request

        :param ride_type: Specify a ride type such as Lyft line, lyft etc
        :param src_lat: Source latitude of the location in float
        :param src_lng: Source longitude of the location in float
        :param dest_lat: Destination latitude of the location in float
        :param dest_lng: Destination longitude of the location in float
        :param src_address: Source address in string
        :param dest_address: Destination address in string

        :return: Ride response JSON object
        """
        src_lng     = float(src_lng),
        src_lat     = float(src_lat)
        dest_lng    = float(dest_lng)
        dest_lat    = float(dest_lat)

        headers = {"Authorization": "{} {}".format(self.token_type,
                                                   self.__access_token),
                   "content-type": "application/json"}

        if src_address is not None:
            data = {"ride_type"  : ride_type,
                    "origin"     : {
                        "lat"    : src_lat,
                        "lng"    : src_lng,
                        "address": src_address
                    },
                    "destination": {
                        "lat"    : dest_lat,
                        "lng"    : dest_lng
                    }}

        elif dest_address is not None:
            data = {"ride_type"  : ride_type,
                    "origin"     : {
                        "lat"    : src_lat,
                        "lng"    : src_lng
                    },
                    "destination": {
                        "lat"    : dest_lat,
                        "lng"    : dest_lng,
                        "address": dest_address
                    }}

        else:
            data = {"ride_type" : ride_type,
                    "origin"    : {
                        "lat"   : src_lat,
                        "lng"   : src_lng
                    },
                    "destination": {
                        "lat"   : dest_lat,
                        "lng"   : dest_lng
                    }}

        ride_request_response = requests.post(RIDE,
                                              headers=headers,
                                              data=data)

        if ride_request_response.status_code == 201:
            return ride_request_response.json()

        else:
            raise Exception(ride_request_response.json())

    def get_ride_details(self, ride_id):
        """Get details of the ride given the ride_id such as pending, picked-up, dropped, cancelled, etc
        https://developer.lyft.com/reference#ride-request-details

        :param ride_id: Ride ID retrieved from ride creation
        :return: Ride details JSON object
        """
        headers = {"Authorization": "{} {}".format(self.token_type,
                                                   self.__access_token),
                   "content-type" : "application/json"}

        ride_request_response = requests.post("{}/{}".format(RIDE, ride_id),
                                              headers=headers)

        if ride_request_response.status_code == 200:
            return ride_request_response.json()

        else:
            raise Exception(ride_request_response.json())

    def update_destination(self, ride_id, lat, lng, address=None):
        """Update the destination of the specified ride. Note that the ride state must still be active (not droppedOff
        or canceled), and that destinations on Lyft Line rides cannot be changed.
        https://developer.lyft.com/reference#ride-request-destination

        :param address: Address of the destination
        :param ride_id: Id of ride
        :param lat: Latitude of the destination
        :param lng: Longitude of the destination
        :return: Message object
        """
        lat = float(lat)
        lng = float(lng)

        headers = {"Authorization": "{} {}".format(self.token_type,
                                                   self.__access_token),
                   "content-type" : "application/json"}

        data = {"lat" : lat,
                "lng" : lng}

        update_destination_response = requests.put("{}/{}/destination".format(RIDE,
                                                                              ride_id),
                                                   headers=headers,
                                                   data=data)

        if update_destination_response.status_code == 200:
            return json.dumps({"message": "Success"})

        else:
            raise Exception(update_destination_response.json())

