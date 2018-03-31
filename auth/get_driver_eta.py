import requests
from lyft.generate_token import generate_token
from lyft.get_my_location import get_coordinates

AUTH_URL      = "https://api.lyft.com/v1/eta?"


def get_driver_eta():
    """Get the drivers ETA object

    :return: {
                "eta_estimates": [{"display_name": "Lyft Line", "ride_type": "lyft_line", "eta_seconds": 180,
                                    "is_valid_estimate": true},{},..]
                "timezone"     : "America/Los_Angeles"
            }
    """
    auth_token_json = generate_token()

    headers = {"content-type"   : "application/json",
               "Authorization"  : "{} {}".format(auth_token_json["token_type"],
                                                 auth_token_json["access_token"])}

    lat, lng = get_coordinates()

    driver_eta_response = requests.get("{}lat={}&lng={}".format(AUTH_URL,
                                                                lat,
                                                                lng),
                                       headers=headers)
    if driver_eta_response.status_code == 200:
        return driver_eta_response.json(), True

    else:
        return driver_eta_response.json(), False
