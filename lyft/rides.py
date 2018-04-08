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
                                              data=json.dumps(data))

        ride_request_response_json = ride_request_response.json()
        ride_request_response_json["status_code"] = ride_request_response.status_code
        return ride_request_response_json

    def get_ride_details(self, ride_id):
        """Get details of the ride given the ride_id such as pending, picked-up, dropped, cancelled, etc
        https://developer.lyft.com/reference#ride-request-details

        :param ride_id: Ride ID retrieved from ride creation
        :return: Ride details JSON object
        """
        headers = {"Authorization": "{} {}".format(self.token_type,
                                                   self.__access_token),
                   "content-type" : "application/json"}

        ride_details_response = requests.post("{}/{}".format(RIDE, ride_id),
                                              headers=headers)

        ride_details_response_json = ride_details_response.json()
        ride_details_response_json["status_code"] = ride_details_response.status_code
        return ride_details_response_json

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

        if address is None:
            data = {"lat" : lat,
                    "lng" : lng}
        else:
            data = {"lat"    : lat,
                    "lng"    : lng,
                    "address": address}

        update_destination_response = requests.put("{}/{}/destination".format(RIDE,
                                                                              ride_id),
                                                   headers=headers,
                                                   data=json.dumps(data))

        if update_destination_response.status_code == 200:
            response = {"status_code": update_destination_response.status_code, "message": "Success"}
            return response

        else:
            return update_destination_response.json()

    def set_rating_and_tip(self, ride_id, rating, tip_amount=None, currency="USD"):
        """Allows to tip the user and set rating for him, Rating is mandatory and accepts values from 1 to 5, while
        tip is optional
        https://developer.lyft.com/reference#ride-request-rating-and-tipping

        :param ride_id: Id of the ride that you want to give rating and tip to
        :param tip_amount: Amount to tip in float
        :param rating: Rating from range 1 to 5
        :param currency: Currency format, by default currency is USD
        :return: Message object
        """
        headers = {"Authorization": "{} {}".format(self.token_type,
                                                   self.__access_token),
                   "content-type" : "application/json"}

        if int(rating) > 5:
            return {"error": "Please enter rating less than 5"}

        if tip_amount is None:
            data = {"rating": rating}

        else:
            data = {"rating": rating,
                    "tip"   : {
                        "amount": tip_amount,
                        "currency": currency
                    }}

        rating_tip_response = requests.put("{}/{}/rating".format(RIDE, ride_id),
                                           headers=headers,
                                           data=json.dumps(data))

        if rating_tip_response.status_code == 204:
            response = {}
            response["status_code"] = rating_tip_response.status_code
            response["message"] = "Success"
            return response

        else:
            return rating_tip_response.json()

    def get_receipt(self, ride_id):
        """Get a receipt for the ride. Receipts are only available after the passenger has rated the ride and the
        payment processing has been completed

        :param ride_id: Id of ride you want to retrieve the receipt
        :return: Receipt JSON object
        """
        headers = {"Authorization": "{} {}".format(self.token_type,
                                                   self.__access_token),
                   "content-type": "application/json"}

        receipt_response = requests.get("{}/{}/receipt".format(RIDE, ride_id),
                                        headers=headers)

        if receipt_response.status_code == 200:
            receipt_response_json = receipt_response.json()
            receipt_response_json["status_code"] = receipt_response.status_code
            return receipt_response_json
        else:
            return receipt_response.json()

    def cancel_ride(self, ride_id):
        """Cancel ride

        :param ride_id: Id of ride you want to retrieve the receipt
        :return: Message object
        """
        headers = {"Authorization": "{} {}".format(self.token_type,
                                                   self.__access_token),
                   "content-type": "application/json"}
        receipt_response = requests.get("{}/{}/cancel".format(RIDE, ride_id),
                                        headers=headers)

        if receipt_response.status_code == 204:
            return json.dumps({"message": "Success"})

        else:
            raise Exception(receipt_response.json())
