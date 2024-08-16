Scripts rely on .env file with the required variables defined


Available functions:

# Fetch the list of all firewalla boxes in MSP tenant
get_all_boxes(api_baseurl, api_token)

# Fetch the list of devices for a specific box (using GID)
get_all_devices(api_baseurl, api_token, box_id)
