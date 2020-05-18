import sys
from json import loads
import json
from common import *

# Validate if account exists on Middleware
def check_account_exists_middleware(abi_id, zone, environment, return_account_data = "false"):
    # Define headers
    headers = get_header_request(zone, "false", "true", "false", "false")
    
    # Define Middleware URL
    url = get_middleware_base_url(zone, environment, "v5") + "/accounts/" + abi_id
    
    # Send request
    response = place_request("GET", url, "", headers)
    json_data = loads(response.text)
    
    if response.status_code == 200 and json_data != "" and return_account_data == "true":
        return json_data
    elif response.status_code == 200 and json_data != "":
        return "success"
    elif response.status_code == 404:
        return "false"
    else:
        return response.status_code

# Create account request on Middleware
def create_account_request(url, headers, abi_id, name, payment_method, minimum_order, zone, environment, state):
    if minimum_order != None:
        dict_values = {
            'accountId': abi_id,
            'deliveryCenterId': abi_id,
            'deliveryScheduleId': abi_id,
            'liquorLicense[0].number': abi_id,
            'minimumOrder.type': minimum_order[0],
            'minimumOrder.value': int(minimum_order[1]),
            'priceListId': abi_id,
            'taxId': abi_id,
            'name': name,
            'paymentMethods': payment_method,
            'deliveryAddress.state': state
        }
    else:
        dict_values = {
            'accountId': abi_id,
            'deliveryCenterId': abi_id,
            'deliveryScheduleId': abi_id,
            'liquorLicense[0].number': abi_id,
            'minimumOrder': minimum_order,
            'priceListId': abi_id,
            'taxId': abi_id,
            'name': name,
            'paymentMethods': payment_method,
            'deliveryAddress.state': state
        }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "data/create_account_payload.json")

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Send request
    response = place_request("POST", url, request_body, headers)

    return response

# Create account on Middleware
def create_account(abi_id, name, zone, payment_method, environment, minimum_order, state):
    # Define headers
    headers = get_header_request(zone, "false", "true", "false", "false")

    # Define Middleware URL 
    url = get_middleware_base_url(zone, environment, "v5") + "/accounts"
    
    # Send request
    response = create_account_request(url, headers, abi_id, name, payment_method, minimum_order, zone, environment, state)

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

    if response.status_code == 200 and response.text != "[]":
        return loads(response.text)
    else:
        return "false"

def create_account_ms(abi_id, name, payment_method, minimum_order, zone, environment, state):
    # Validation of Account ID for BR
    if (validateAccount(abi_id) == "false") and (zone == "BR" or zone == "DO"):
        print(text.Yellow + "\n- Account ID should not be empty or it must contain at least 10 characters")
        finishApplication()
    
    payment_term = None
    if zone.upper() == "BR" and "BANK_SLIP" in payment_method:
        payment_term = return_payment_term_bank_slip()

    if minimum_order != None:
        dict_values = {
            'accountId': abi_id,
            'deliveryCenterId': abi_id,
            'deliveryScheduleId': abi_id,
            'liquorLicense[0].number': abi_id,
            'minimumOrder.type': minimum_order[0],
            'minimumOrder.value': int(minimum_order[1]),
            'priceListId': abi_id,
            'taxId': abi_id,
            'name': name,
            'paymentMethods': payment_method,
            'deliveryAddress.state': state,
            'paymentTerms': payment_term,
        }
    else:
        dict_values = {
            'accountId': abi_id,
            'deliveryCenterId': abi_id,
            'deliveryScheduleId': abi_id,
            'liquorLicense[0].number': abi_id,
            'minimumOrder': minimum_order,
            'priceListId': abi_id,
            'taxId': abi_id,
            'name': name,
            'paymentMethods': payment_method,
            'deliveryAddress.state': state,
            'paymentTerms': payment_term,
        }

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