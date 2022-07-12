from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import json
import requests


def get_photo(city, state):
    # Create a dictionary for the headers to use in the request
    # Create the URL for the request with the city and state
    # Make the request
    # Parse the JSON response
    # Return a dictionary that contains a `picture_url` key and
    #   one of the URLs for one of the pictures in the response
    place = {
        'query': f"{city}, {state}",
        'per_page': 1
        }
    response = requests.get(
        url="https://api.pexels.com/v1/search",
        headers={'Authorization': PEXELS_API_KEY},
        params=place
        )
    content = json.loads(response.content)
    try:
        return {'picture_url': content['photos'][0]['src']['original']}
    except (KeyError, IndexError):
        return {'picture_url': None}


def get_weather_data(city, state):
    params = {
        'q': f'{city}, {state}, US',
        'limit': 1,
        'appid': OPEN_WEATHER_API_KEY
    }
    # Create the URL for the geocoding API with the city and state
    url = 'http://api.openweathermap.org/geo/1.0/direct'
    # Make the request
    response = requests.get(
        url,
        params=params,
    )
    # Parse the JSON response
    content = json.loads(response.content)
    # Get the latitude and longitude from the response
    try:
        latitude = content[0]['lat']
        longitude = content[0]['lon']
    except(KeyError, IndexError):
        return None

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial"
    }

    # Create the URL for the current weather API with the latitude
    #   and longitude
    url = "http://api.openweathermap.org/data/2.5/weather"
    # Make the request
    response = requests.get(url=url, params=params)
    # Parse the JSON response
    content = json.loads(response.content)
    # Get the main temperature and the weather's description and put
    #   them in a dictionary
    # Return the dictionary
    try:
        return {
            "description": content["weather"][0]["description"],
            "temp": content["main"]["temp"],
        }
    except (KeyError, IndexError):
        return None
