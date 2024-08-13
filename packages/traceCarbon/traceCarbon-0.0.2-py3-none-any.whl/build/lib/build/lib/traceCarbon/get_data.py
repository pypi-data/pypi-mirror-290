"""
Fetch carbon emissions data from Electricity Maps API
"""
import json
from datetime import datetime, timedelta
import requests
from requests.exceptions import HTTPError
import geocoder

def get_location():
    """Use geocoder to get longitude and latitude from ip"""
    g = geocoder.ip('me')
    return g.x, g.y

def fetch(url):
    """Fetch data from URL"""
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
    return data

def load(filename):
    """Load JSON from file"""
    with open(filename, 'r', encoding = "utf-8") as file:
        data = json.load(file)
    return data

def save(data, filename):
    """Save JSON to file"""
    with open(filename, 'w', encoding = "utf-8") as file:
        json.dump(data, file)

def load_intensity_data(region='none'):
    """Loads carbon intensity data from Electricity Maps API"""
    url_stem = 'https://api.electricitymap.org/v3/carbon-intensity/latest'
    if region == 'none':      
        #Get longitude and latitude coordinates
        lat, lon = get_location()
        #Load relevant carbon intensity from the API corresponding to coords
        url = url_stem + f'?lat={lat}&lon={lon}'
    else:
        url = url_stem + f'?zone={region}'
    try:
        data = fetch(url)
        carbon_intensity = data['carbonIntensity']
    except HTTPError as e:
        print(f"An error occured when trying to load data from {url}")
        print(e.response.text)
        raise 

    return carbon_intensity

def process_historical_data(data):
    """Dealing with the data returned from querying the carbon intensity history from Electricity Maps API"""
    #history is a list containing dictionaries
    history = data['history']
    history_dict = {}
    for dictionary in history:
        history_dict[dictionary['datetime']] = dictionary['carbonIntensity']
    return history_dict


def load_historical_intensity_data(region='none'):
    """Loads historical carbon intensity data from Electricity Maps API"""
    url_stem = 'http://api.electricitymap.org/v3/carbon-intensity/history'
    if region == 'none':      
        #Get longitude and latitude coordinates
        lat, lon = get_location()
        #Load relevant carbon intensity from the API corresponding to coords
        url = url_stem + f'?lat={lat}&lon={lon}'
    else:
        url = url_stem + f'?zone={region}'

    try:
        data = fetch(url)
        return process_historical_data(data)
    except HTTPError as e:
        print(f"An error occured when trying to load data from {url}")
        print(e.response.text)
        raise

