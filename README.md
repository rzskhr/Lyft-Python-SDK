# Lyft-Python-SDK

Welcome to Lyft-Python-SDK. This SDK enables Python developers to programmatically interact with Lyft's rider and driver network using Lyft API.

## Installation
This project only supports python 3 or greater and can be installed using the following command:

```
   >>> $ pip3 install lyft-python
```

## Authentication
Lyft API follows O-Auth for authentication and it uses two types of authentication 2 legged and 3 legged.
2-legged authentication will let you use the services that have non user context such as ETA, cost, ride types, whereas the 3-legged flow will is used to request access to a Lyft user's account in order to make requests on their behalf. More information can be found [here](https://developer.lyft.com/docs/authentication#section-access-tokens)

**Note**: use **sandbox_mode=True** if you want to try in dev environment

**2 legged auth**
The following code stub will give you a dictionary containing the access token to do the 2 legged API calls.
```python
    from lyft.authentication import LyftPublicAuth
    auth = LyftPublicAuth({"client_id": "<client_id>", "client_secret": "<client_secret>"}, sandbox_mode=True/False})
    auth.access_token()
```
**response**
```python
    {"x-ratelimit-limit" :"",
     "x-ratelimit-remaining" : "",
     "expires_in" : "",
     "access_token" : "",
     "token_type" : ""}
```
  **3 legged auth**
Before doing 3 legged auth you need to get the permission from the user, So when you are creating a developer account in Lyft provide a redirect URL which will redirect the customer to this URL to give permission. More information can be found [here](https://developer.lyft.com/docs/authentication#section-3-legged-flow-for-accessing-user-specific-endpoints)
```python
    from lyft.authentication import LyftUserAuth
    user_auth = LyftUserAuth({"client_id": "<client_id>", "client_secret": "<client_secret>"}, [<list of scopes>], state, sandbox_mode=True/False})
    user_auth.get_authorization_uri()  #This URL is used to redirect the user
    user_auth.get_access_token("authorization_code")  # You will get authorization code once the user accepts
```
**response**
```python
     {"x-ratelimit-limit" :"",
      "x-ratelimit-remaining" : "",
      "expires_in" : "",
      "access_token" : "",
      "token_type" : "",
      "refresh_token": ""}
```

## Refreshing Tokens
The tokens given by lyft have a specific expiry time, you need to refresh token after the expiry. The SDK provides support to refresh your tokens.
```python
    from lyft.session import Session
    session_obj = Session({"client_id": "<client_id>", "client_secret": "<client_secret>"}, refresh_token, sandbox_mode=True/False}
    session_obj.refresh_access_token()
	# to revoke token
	session_obj.revoke_token()
```

**response**
```python
    {"x-ratelimit-limit" :"",
      "x-ratelimit-remaining" : "",
      "expires_in" : "",
      "access_token" : "",
      "token_type" : ""}
```

## Activities using the 3-legged flow
The response references to the below methods is available [here](https://developer.lyft.com/v1/reference)
```python
    from lyft.rides import Rides
    ride_obj = Rides(token_type="Bearer", access_token="Token retrived after user approves")

    # To request ride
    ride_obj.create_ride_request(ride_type, src_lat, src_lng, dest_lat, dest_lng, src_address=None, dest_address=None)

	# To get ride details
	ride_obj.get_ride_details(ride_id)

	# To update destination
	ride_obj.update_destination(ride_id, lat, lng, address=None)

	# To give rating to driver
	ride_obj.set_rating_and_tip(ride_id, rating, tip_amount=None, currency="USD")

	# To get receipt
	ride_obj.get_receipt(ride_id)

	# To cancel ride
	ride_obj.cancel_ride(ride_id)
```

## RIDE REQUEST API
Here are few examples of how to use the Ride Request API and how to use this SDK to make requests to Lyft's API.
#### Availability - Ride Types
A GET to the /ridetypes endpoint returns the ride types available at the specified location, indicated by latitude and longitude. If no ride types are available at the specified location, the response will be an error.

Usage:
```python
from lyft.availability import Availability
availability_obj = Availability(<TOKEN_TYPE>, <ACCESS_TOKEN>)

response = availability_obj.get_ride_types(37.7763, -122.3918)
```

Usage - With Ride type:
```python
from lyft.availability import Availability
availability_obj = Availability(<TOKEN_TYPE>, <ACCESS_TOKEN>)

response = availability_obj.get_ride_types(37.7763, -122.3918, 'lyft_line')
```

#### Availability - Driver ETA
A GET to the /eta endpoint returns the estimated time in sseconds it will take for the nearest driver to reach the specified location. A success response will be broken down by ridetypes available at the specified location. An optional ride_type parameter can be specified to only return the ETA for that ridetype. Valid inputs for the ride_type parameter can be found by querying the /v1/ridetypes endpoint.

An empty response indicates that the specified ride_type isn't available at the specified location. You can try requesting again without the ride_type parameter.

Usage:
```python
from lyft.availability import Availability
availability_obj = Availability(<TOKEN_TYPE>, <ACCESS_TOKEN>)

response = availability_obj.get_driver_eta(37.7763, -122.3918)
```

Usage - With Ride Type:
```python
from lyft.availability import Availability
availability_obj = Availability(<TOKEN_TYPE>, <ACCESS_TOKEN>)

response = availability_obj.get_driver_eta(37.7763, -122.3918, 'lyft_line')
```

Usage - With Destination:
```python
from lyft.availability import Availability
availability_obj = Availability(<TOKEN_TYPE>, <ACCESS_TOKEN>)

response = availability_obj.get_driver_eta(37.7763, -122.3918, 36.3452, -121.3435)
```

Usage - With Destination and Ride Type:
```python
from lyft.availability import Availability
availability_obj = Availability(<TOKEN_TYPE>, <ACCESS_TOKEN>)

response = availability_obj.get_driver_eta(37.7763, -122.3918, 36.3452, -121.3435, 'lyft_line')
```


## Prerequisites and Dependencies
- Python 3.X
- [requests](http://docs.python-requests.org/en/latest/)

## Getting help
Lyft developer community is very active on StackOverflow, keep an eye on the [Lyft Tag](https://stackoverflow.com/questions/tagged/lyft-api) and post your questions if you need any help in using the library. Don’t forget to tag your question with lyft-api and python!
For full documentation about Lyft API, visit Lyft’s [Developer Docs](https://developer.lyft.com/docs).

## Contribution
If you've found a bug in the Python SDK, or would like new features added you are welcome, go ahead and open an issue or create a pull request against this repository. But before that, please search for similar issues. It's possible somebody has encountered this issue already. Also write a test to show your bug was fixed or the feature works as expected.

GitHub's Documentation:
- [General GitHub Documentation](https://help.github.com/)
- [Collaborating with issues and pull requests](https://help.github.com/categories/collaborating-with-issues-and-pull-requests/)

## Terms of Use
Your use of this SDK is subject to, and by using or downloading the Lyft-Python-SDK files you agree to comply with, the Lyft API’s [Terms of Use](https://developer.lyft.com/docs/lyft-developer-platform-terms-of-use).

[Brand Guidelines for Lyft Developers](https://developer.lyft.com/docs/brand-guidelines)
<br/>
This is not an official Lyft product.

## License
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
