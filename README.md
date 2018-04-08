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

