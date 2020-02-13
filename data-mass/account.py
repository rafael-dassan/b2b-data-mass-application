import sys
from json import loads

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
def create_account_request(url, headers, abi_id, name, zone, environment):
    # Create body
    request_body = get_middleware_payload_create_account(zone, abi_id, name, environment)

    # Send request
    response = place_request("POST", url, request_body, headers)

    return response

# Helper - how to use script
def show_how_to_use():
    print ("\n|===== Create account - Middleware =====\n")
    print ("| - Parameters:")
    print ("| #1 - ID AB-Inbev (Must contain 10 characters)")
    print ("| #2 - Account Name")
    print ("| #3 - Zone (ZA, AR, CL)")
    print ("| #4 - Environment (QA, UAT)")
    print ("\n")
    print ("| Example: '$ python3.6 create_account.py 1234567890 Test ZA UAT'")
    print ("\n")

# Create account on Middleware
def create_account(abi_id, name, zone, environment):
    # Define headers
    headers = get_header_request(zone, "false", "true", "false", "false")

    # Define Middleware URL 
    url = get_middleware_base_url(zone, environment, "v5") + "/accounts"
    
    # Send request
    response = create_account_request(url, headers, abi_id, name, zone, environment)

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

def create_account_ms(accountId, name, zone, environment):
    # Validation of Account ID for BR
    if (validateAccount(accountId) == "false") and (zone == "BR" or zone == "DO"):
        print(text.Yellow + "\n- Account ID should not be empty or it must contain at least 10 characters")
        finishApplication()

    # Get header request
    request_headers = get_header_request(zone, "false", "true", "false", "false")

    # Get base URL
    request_url = get_microservice_base_url(environment) + "/account-relay"    
    
    # Get body request
    request_body = get_microservice_payload_create_account(zone, accountId, name, environment)

    # Place request
    response = place_request("POST", request_url, request_body, request_headers)

    if response.status_code == 202:
        return "success"
    else:
        return response.status_code