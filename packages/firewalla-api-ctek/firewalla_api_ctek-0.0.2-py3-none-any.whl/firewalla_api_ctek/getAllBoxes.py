import requests

def get_all_boxes(api_baseurl, api_token):
    headers = { "Authorization": f"Token {api_token}" }
    try:
        response = requests.get(f"{api_baseurl}/v2/boxes", headers=headers)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching boxes: {e}")
        return None, f"Error fetching boxes: {e}"





