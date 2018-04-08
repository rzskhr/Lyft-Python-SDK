# Lyft-Python-SDK

Welcome to Lyft-Python-SDK. This SDK enables Python developers to programmatically interact with Lyft's rider and driver network using Lyft API.

## RIDE REQUEST API

### Availability - Ride Types
A GET to the /ridetypes endpoint returns the ride types available at the specified location, indicated by latitude and longitude. If no ride types are available at the specified location, the response will be an error.

Usage:
```python
from lyft.availability import Availability
availability_obj = Availability(<TOKEN_TYPE>, <ACCESS_TOKEN>)

response = availability_obj.get_ride_types(37.7763, -122.3918)
```

Response Object:
```python
{
  'ride_types': [
    {
      'display_name': 'Lyft Line',
      'pricing_details': {
        'base_charge': 200,
        'cost_minimum': 475,
        'cost_per_minute': 22,
        'cost_per_mile': 121,
        'currency': 'USD',
        'trust_and_service': 200,
        'cancel_penalty_amount': 500
      },
      'image_url': 'https://cdn.lyft.com/assets/car_standard.png',
      'seats': 2,
      'ride_type': 'lyft_line'
    },
    {
      'display_name': 'Lyft',
      'pricing_details': {
        'base_charge': 200,
        'cost_minimum': 500,
        'cost_per_minute': 22,
        'cost_per_mile': 121,
        'currency': 'USD',
        'trust_and_service': 200,
        'cancel_penalty_amount': 500
      },
      'image_url': 'https://cdn.lyft.com/assets/car_standard.png',
      'seats': 4,
      'ride_type': 'lyft'
    },
    ...
    ...
    ...
  ]
}
```

Usage - With Ride type:
```python
from lyft.availability import Availability
availability_obj = Availability(<TOKEN_TYPE>, <ACCESS_TOKEN>)

response = availability_obj.get_ride_types(37.7763, -122.3918, 'lyft_line')
```

Response Object:
```python
{
  'ride_types': [
    {
      'display_name': 'Lyft Line',
      'pricing_details': {
        'base_charge': 200,
        'cost_minimum': 475,
        'cost_per_minute': 22,
        'cost_per_mile': 121,
        'currency': 'USD',
        'trust_and_service': 200,
        'cancel_penalty_amount': 500
      },
      'image_url': 'https://cdn.lyft.com/assets/car_standard.png',
      'seats': 2,
      'ride_type': 'lyft_line'
    }
  ]
}
```
