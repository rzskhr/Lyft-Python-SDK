import requests

from lyft.util.url_util import AVAILABILITY


class Availability(object):
    def __init__(self, token_type, access_token):
        """
        Constructor fot the class Availability.
        Use for storing various related operations

        :param token_type: Token type. eg: "Bearer"
        :param access_token: access token
        """
        self.token_type = token_type
        self.__access_token = access_token

    def get_ride_types(self, lat, lng, ride_type=None):
        """
        A GET to the /ridetypes endpoint returns the ride types available at the specified location,
        indicated by latitude and longitude. If no ride types are available at the specified location,
        the response will be an error.

        :param lat: float, REQUIRED, Latitude of a location
        :param lng: float, REQUIRED, Longitude of a location
        :param ride_type: string, ID of a ride type. Returned by this endpoint
        :return: ride types available in JSON format
        """
        lat = float(lat)
        lng = float(lng)

        if ride_type is None:
            ride_types_url = "{}ridetypes?lat={}&lng={}".format(AVAILABILITY, lat, lng)
        else:
            ride_types_url = "{}ridetypes?lat={}&lng={}&ride_type={}".format(AVAILABILITY, lat, lng, ride_type)

        headers = {"Authorization": "{} {}".format(self.token_type,
                                                   self.__access_token)}

        ride_types_available_response = requests.get(ride_types_url, headers=headers)

        if ride_types_available_response.status_code == 200:
            return ride_types_available_response.json()

        else:
            raise Exception(ride_types_available_response.json())

    def get_driver_eta(self, lat, lng, end_lat=None, end_lng=None, ride_type=None):
        """
        A GET to the /eta endpoint returns the estimated time in seconds it will take for the nearest driver to
        reach the specified location. A success response will be broken down by ridetypes available at the
        specified location. An optional ride_type parameter can be specified to only return the ETA for that ridetype.
        Valid inputs for the ride_type parameter can be found by querying the /v1/ridetypes endpoint.

        An empty response indicates that the specified ride_type isn't available at the specified location.
        You can try requesting again without the ride_type parameter.

        :param lat: float, REQUIRED, Latitude of a location
        :param lng: float, REQUIRED, Longitude of a location
        :param end_lat: float, Latitude of a location
        :param end_lng: float, Longitude of a location
        :param ride_type: string, ID of a ride type. Returned by this endpoint
        :return: driver eta available in JSON format
        """
        lat = float(lat)
        lng = float(lng)
        # check if destination is given
        if all([end_lat, end_lng]) is True:
            end_lat = float(end_lat)
            end_lng = float(end_lng)

        # construct the request URL
        if ride_type is None and (end_lat is None or end_lng is None):
            driver_eta_url = "{}eta?lat={}&lng={}".format(AVAILABILITY, lat, lng)

        elif ride_type is not None and (end_lat is None or end_lng is None):
            driver_eta_url = "{}eta?lat={}&lng={}&ride_type={}".format(AVAILABILITY, lat, lng, ride_type)

        elif ride_type is not None and (end_lat is not None or end_lng is not None):
            driver_eta_url = "{}eta?lat={}&lng={}&end_lat={}&destination_lng={}&ride_type={}".format(
                AVAILABILITY, lat, lng, end_lat, end_lng, ride_type)

        elif ride_type is None and (end_lat is not None or end_lng is not None):
            driver_eta_url = "{}eta?lat={}&lng={}&end_lat={}&destination_lng={}".format(
                AVAILABILITY, lat, lng, end_lat, end_lng)

        headers = {"Authorization": "{} {}".format(self.token_type,
                                                   self.__access_token)}

        driver_eta_response = requests.get(driver_eta_url, headers=headers)

        if driver_eta_response.status_code == 200:
            return driver_eta_response.json()

        else:
            raise Exception(driver_eta_response.json())

    def get_ride_estimates(self, start_lat, start_lng, end_lat=None, end_lng=None, ride_type=None):
        """
        A GET to the /cost endpoint returns the estimated cost, distance, and duration of a ride between
        a start location and end location. A success response will be broken down by ride types available
        at the specified location. An optional ride_type parameter can be specified to only return the
        cost_estimate for that ride_type. Valid inputs for the ride_type parameter can be found by querying
        the /v1/ridetypes endpoint.

        If the destination parameters are not supplied, the cost endpoint will simply return the Prime Time
        pricing at the specified location.

        :param start_lat: float, REQUIRED, Latitude of a location
        :param start_lng: float, REQUIRED, Longitude of a location
        :param end_lat: float, Latitude of a location
        :param end_lng: float, Longitude of a location
        :param ride_type: string, ID of a ride type. Returned by this endpoint
        :return: ride estimates in JSON format
        """
        start_lat = float(start_lat)
        start_lng = float(start_lng)
        # check if destination is given
        if all([end_lat, end_lng]) is True:
            end_lat = float(end_lat)
            end_lng = float(end_lng)

        # construct the request URL
        if ride_type is None and (end_lat is None or end_lng is None):
            ride_estimates_url = "{}cost?start_lat={}&start_lng={}".format(AVAILABILITY,start_lat, start_lng)

        elif ride_type is not None and (end_lat is None or end_lng is None):
            ride_estimates_url = "{}cost?start_lat={}&start_lng={}&ride_type={}".format(AVAILABILITY,start_lat, start_lng, ride_type)

        elif ride_type is not None and (end_lat is not None or end_lng is not None):
            ride_estimates_url = "{}cost?start_lat={}&start_lng={}&end_lat={}&end_lng={}&ride_type={}".format(
                AVAILABILITY, start_lat, start_lng, end_lat, end_lng, ride_type)

        elif ride_type is None and (end_lat is not None or end_lng is not None):
            ride_estimates_url = "{}cost?start_lat={}&start_lng={}&end_lat={}&end_lng={}".format(
                AVAILABILITY, start_lat, start_lng, end_lat, end_lng)

        headers = {"Authorization": "{} {}".format(self.token_type,
                                                   self.__access_token)}

        ride_estimates_response = requests.get(ride_estimates_url, headers=headers)

        if ride_estimates_response.status_code == 200:
            return ride_estimates_response.json()

        else:
            raise Exception(ride_estimates_response.json())

    def get_nearby_drivers(self, lat, lng):
        """
        A GET to the /drivers endpoint returns the location of drivers near a location.
        The result will contain a list of 5 locations for a sample of drivers for each ride type available
        at the specified latitude and longitude.

        :param lat: float, REQUIRED, Latitude of a location
        :param lng: float, REQUIRED, Longitude of a location
        :return: nearby drivers in JSON format
        """
        lat = float(lat)
        lng = float(lng)

        nearby_drivers_url = "{}drivers?lat={}&lng={}".format(AVAILABILITY, lat, lng)

        headers = {"Authorization": "{} {}".format(self.token_type,
                                                   self.__access_token)}

        nearby_drivers_response = requests.get(nearby_drivers_url, headers=headers)

        if nearby_drivers_response.status_code == 200:
            return nearby_drivers_response.json()

        else:
            raise Exception(nearby_drivers_response.json())

    def get_eta_and_nearby_drivers(self, lat, lng, end_lat=None, end_lng=None, ride_type=None):
        """
        A GET to the /nearby-drivers-pickup-etas endpoint returns the estimated time for nearby
        drivers to reach the specified location, and their most recent locations.

        A success response will be broken down by ridetypes available at the specified location.
        An optional ride_type parameter can be specified to only return the ETA for that ridetype.
        Valid inputs for the ride_type parameter can be found by querying the /v1/ridetypes endpoint.

        An empty response indicates that the specified ride_type isn't available at the specified location.
        You can try requesting again without the ride_type parameter.

        :param lat: float, REQUIRED, Latitude of a location
        :param lng: float, REQUIRED, Longitude of a location
        :param end_lat: float, Latitude of a location
        :param end_lng: float, Longitude of a location
        :param ride_type: string, ID of a ride type. Returned by this endpoint
        :return: nearby drivers and eta in JSON format
        """
        lat = float(lat)
        lng = float(lng)
        # check if destination is given
        if all([end_lat, end_lng]) is True:
            end_lat = float(end_lat)
            end_lng = float(end_lng)

        # construct the request URL
        if ride_type is None and (end_lat is None or end_lng is None):
            eta_and_nearby_drivers_url = "{}nearby-drivers-pickup-etas?lat={}&lng={}".format(AVAILABILITY, lat, lng)

        elif ride_type is not None and (end_lat is None or end_lng is None):
            eta_and_nearby_drivers_url = "{}nearby-drivers-pickup-etas?lat={}&lng={}&ride_type={}".format(
                AVAILABILITY, lat, lng, ride_type)

        elif ride_type is not None and (end_lat is not None or end_lng is not None):
            eta_and_nearby_drivers_url = "{}nearby-drivers-pickup-etas?lat={}&lng={}&destination_lat={}&destination_lng={}&ride_type={}".format(
                AVAILABILITY, lat, lng, end_lat, end_lng, ride_type)

        elif ride_type is None and (end_lat is not None or end_lng is not None):
            eta_and_nearby_drivers_url = "{}nearby-drivers-pickup-etas?lat={}&lng={}&destination_lat={}&destination_lng={}".format(
                AVAILABILITY, lat, lng, end_lat, end_lng)

        headers = {"Authorization": "{} {}".format(self.token_type,
                                                   self.__access_token)}

        eta_and_nearby_drivers_response = requests.get(eta_and_nearby_drivers_url, headers=headers)

        if eta_and_nearby_drivers_response.status_code == 200:
            return eta_and_nearby_drivers_response.json()

        else:
            raise Exception(eta_and_nearby_drivers_response.json())
