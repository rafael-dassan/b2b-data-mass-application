import sys
from json import loads

# Custom
from helper import *

# Validate if account exists in Middleware
def check_account_exists_middleware(abi_id, zone, environment):
    
    # Define headers
    headers = get_header_request(zone, 'false', 'true')
    
    # Define URL Middleware
    url = get_middleware_base_url(zone, environment, "v5") + "/accounts/" + abi_id
    
    # Send request
    response = place_request("GET", url, "", headers)
    json_data = loads(response.text)
    if response.status_code == 200 and json_data != '':
        return 'success'
    elif response.status_code == 404:
        return 'false'
    else:
        return response.status_code

# Create account request on middleware
def create_account_request(url, headers, id_abi, name, zone, environment):
    
    # Create body
    request_body = get_middleware_payload_create_account(zone, id_abi, name, environment)

    # Execute request
    response = place_request("POST", url, request_body, headers)

    return response

# Help with how to use script
def show_how_to_use():
    print ('\n|===== Create account - Middleware =====\n')
    print ('| - Parameters:')
    print ('| #1 - ID AB-Inbev (Must contain 10 characters)')
    print ('| #2 - Account Name')
    print ('| #3 - Zone (DO, ZA, AR, CL)')
    print ('| #4 - Environment (QA, UAT)')
    print ('\n')
    print ('| Example: "$ python3.6 create_account.py 1234567890 Test ZA UAT"')
    print ('\n')

# Create account on middleware
def create_account(id_abi, name, zone, environment):

    # Validation of ID AB-Inbev
    if validateAccount(id_abi) == 'false':
        print('\n- [Error] Incorrect parameter "ID AB-Inbev" (Must contain 10 characters)')
        return 'false'
 
    # Define headers
    headers = get_header_request(zone, 'false', 'true')

    # Define URL Middleware
    url = get_middleware_base_url(zone, environment, "v5") + "/accounts"
    
    # Send request
    response = create_account_request(url, headers, id_abi, name, zone, environment)
    if response.status_code == 202:
        return 'success'
    else:
        return response.status_code
