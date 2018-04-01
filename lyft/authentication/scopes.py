class Scopes:
    """You'll need to include a list of requested scopes during the OAuth flow. When using the 3-legged flow, users will
    be asked to grant permission to your application's requested scopes when they authenticate.

    Scope	                Access	                    Description
    public	                default	                    Grants access to the ride types, ETAs, and cost endpoints
    rides.read	            default	                    Grants access to the user's current and past ride information
    offline	                optional	                Required in order to get access to a refresh_token
    rides.request	        optional	                For requesting and managing a passenger's rides
    profile	                optional	                For requesting profile information about a user
    """

    PUBLIC          = "public"
    READ_RIDES      = "rides.read"
    OFFLINE         = "offline"
    RIDES_REQUEST   = "rides.request"
    PROFILE         = "profile"
