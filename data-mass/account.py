import sys
from json import loads
import json

# Custom
from helper import *

# Validate if account exists on Middleware
def check_account_exists_middleware(abi_id, zone, environment):
    # Define headers
    headers = get_header_request(zone, "false", "true", "false", "false")
    
    # Define Middleware URL
    url = get_middleware_base_url(zone, environment, "v5") + "/accounts/" + abi_id
    
    # Send request
    response = place_request("GET", url, "", headers)
    json_data = loads(response.text)
    
    if response.status_code == 200 and json_data != "":
        return "success"
    elif response.status_code == 404:
        return "false"
    else:
        return response.status_code

# Create account request on Middleware
def create_account_request(url, headers, abi_id, name, payment_method, zone, environment):
    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "data/create_account_payload.json")

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'accountId': abi_id,
        'deliveryCenterId': abi_id,
        'deliveryScheduleId': abi_id,
        'liquorLicense[0].number': abi_id,
        'priceListId': abi_id,
        'taxId': abi_id,
        'name': name,
        'paymentMethods': payment_method
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Send request
    response = place_request("POST", url, request_body, headers)

    return response

# Create account on Middleware
def create_account(abi_id, name, zone, payment_method, environment):
    # Define headers
    headers = get_header_request(zone, "false", "true", "false", "false")

    # Define Middleware URL 
    url = get_middleware_base_url(zone, environment, "v5") + "/accounts"
    
    # Send request
    response = create_account_request(url, headers, abi_id, name, payment_method, zone, environment)

    if response.status_code == 202:
        return "success"
    else:
        return response.status_code

def check_account_exists_microservice(accountId, zone, environment):
    # Get header request
    request_headers = get_header_request(zone, "true", "false", "false", "false")

    # Get base URL
    request_url = get_microservice_base_url(environment) + "/accounts?accountId=" + accountId + "&country=" + zone

    # Place request
    response = place_request("GET", request_url, "", request_headers)

    if response.status_code == 200 and response.text != "":
        return loads(response.text)
    else:
        return "false"

def create_account_ms(accountId, name, payment_method, zone, environment):
    # Validation of Account ID for BR
    if (validateAccount(accountId) == "false") and (zone == "BR" or zone == "DO"):
        print(text.Yellow + "\n- Account ID should not be empty or it must contain at least 10 characters")
        finishApplication()

    # Get header request
    request_headers = get_header_request(zone, "false", "true", "false", "false")

    # Get base URL
    request_url = get_microservice_base_url(environment) + "/account-relay"

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "data/create_account_payload.json")

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'accountId': accountId,
        'deliveryCenterId': accountId,
        'deliveryScheduleId': accountId,
        'liquorLicense[0].number': accountId,
        'priceListId': accountId,
        'taxId': accountId,
        'name': name,
        'paymentMethods': payment_method
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Place request
    response = place_request("POST", request_url, request_body, request_headers)

    if response.status_code == 202:
        return "success"
    else:
        return response.status_code