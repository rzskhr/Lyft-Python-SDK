## Installation
This project only supports python 3 or greater and can be installed using the following command:

    pip3 install lyft-python

## Authentication
Lyft API follows O-Auth for authentication and it uses two types of authentication 2 legged and 3 legged.
2-legged authentication will let you use the services that have non user context such as ETA, cost, ride types, whereas the 3-legged flow will is used to request access to a Lyft user's account in order to make requests on their behalf. More information can be found [here](https://developer.lyft.com/docs/authentication#section-access-tokens)

**Note**: use **sandbox_mode=True** if you want to try in dev environment

**2 legged auth**
The following code stub will give you a dictionary containing the access token to do the 2 legged API calls.

    from lyft.authentication import LyftPublicAuth
    auth = LyftPublicAuth({"client_id": "<client_id>", "client_secret": "<client_secret>"}, sandbox_mode=True/False})
    auth.access_token()
	
**response**

    {"x-ratelimit-limit" :"",  
     "x-ratelimit-remaining" : "",  
     "expires_in" : "",  
     "access_token" : "",  
     "token_type" : ""}
  
  **3 legged auth**
Before doing 3 legged auth you need to get the permission from the user, So when you are creating a developer account in Lyft provide a redirect URL which will redirect the customer to this URL to give permission. More information can be found [here](https://developer.lyft.com/docs/authentication#section-3-legged-flow-for-accessing-user-specific-endpoints)

    from lyft.authentication import LyftUserAuth
    user_auth = LyftUserAuth({"client_id": "<client_id>", "client_secret": "<client_secret>"}, [<list of scopes>], state, sandbox_mode=True/False})
    user_auth.get_authorization_uri()  #This URL is used to redirect the user
    user_auth.get_access_token("authorization_code")  # You will get authorization code once the user accepts

**response**

     {"x-ratelimit-limit" :"",  
      "x-ratelimit-remaining" : "",  
      "expires_in" : "",  
      "access_token" : "",  
      "token_type" : "",
      "refresh_token": ""}


## Refreshing Tokens
The tokens given by lyft have a specific expiry time, you need to refresh token after the expiry. The SDK provides support to refresh your tokens.

    from lyft.session import Session
    session_obj = Session({"client_id": "<client_id>", "client_secret": "<client_secret>"}, refresh_token, sandbox_mode=True/False}
    session_obj.refresh_access_token()
	# to revoke token
	session_obj.revoke_token()


**response**

    {"x-ratelimit-limit" :"",  
      "x-ratelimit-remaining" : "",  
      "expires_in" : "",  
      "access_token" : "",  
      "token_type" : ""}

## Activities using the 3-legged flow
The response references to the below methods is available [here](https://developer.lyft.com/v1/reference)

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

