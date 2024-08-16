import requests

def get_all_devices(api_baseurl, api_token, box_id):
    headers = { "Authorization": f"Token {api_token}" }
    try:
        response = requests.get(f"{api_baseurl}/v2/devices?box={box_id}", headers=headers)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching devices: {e}")
        return None, f"Error fetching devices: {e}"
