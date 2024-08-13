import requests

base_url = "http://gangadhar-web.prod-we.com"

def fetch_json_data(url, params):
    url = f"{url}?{params}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def fetch_preprocessed_itinerary(vehicleId, fromTime, toTime):
    return fetch_json_data(f"{base_url}/itinerary/preprocessed-itineraries", f"vehicleId={vehicleId}&fromTime={fromTime}&toTime={toTime}")

def fetch_postprocessed_itinerary(vehicleId, fromTime, toTime):
    return fetch_json_data(f"{base_url}/itinerary", f"vehicleId={vehicleId}&fromTime={fromTime}&toTime={toTime}")

def fetch_raw_data(vehicleId, fromTime, toTime):
    return fetch_json_data(f"{base_url}/fuel/time-series", f"vId={vehicleId}&fromTime={fromTime}&toTime={toTime}")

def fetch_gps_data(vehicleId, fromTime, toTime):
    params = f"vehicleIds={vehicleId}&fromTime={fromTime}&toTime={toTime}&sortOrder=desc"
    url = f"http://shaktiman-web.prod-we.com/gps/vehicles?{params}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
