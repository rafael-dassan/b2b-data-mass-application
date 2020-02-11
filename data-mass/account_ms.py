import sys
import json

# Custom
from helper import *

def create_account_ms(accountId, name, zone, environment):
    
    # Validation of ID AB-Inbev
    if validateAccount(accountId) == 'false':
        print('\n- [Error] Incorrect parameter "ID AB-Inbev" (Must contain 10 characters)')
        sys.exit();

    # Get header request
    request_headers = get_header_request(zone, 'false', 'true')

    # Get url base
    request_url = get_microservice_base_url(environment) + "/account-relay"    
    
    # Get body request
    request_body = get_microservice_payload_create_account(zone, accountId, name, environment)

    # Place request
    response = place_request("POST", request_url, request_body, request_headers)
    if response.status_code == 202:
        return 'success'
    else:
        return response.status_cod


def check_account_exists_microservice(accountId, zone, environment):
    
    # Validation of ID AB-Inbev
    if validateAccount(accountId) == 'false':
        print('\n- [Error] Incorrect parameter "ID AB-Inbev" (Must contain 10 characters)')
        sys.exit()

    # Get header request
    request_headers = get_header_request(zone, 'true')

    # Get url base
    request_url = get_microservice_base_url(environment) + "/accounts?accountId=" + accountId + '&country=' + zone

    # Place request
    response = place_request("GET", request_url, "", request_headers)
    if response.status_code == 200 and response.text != '':
        return json.loads(response.text)
    else:
        return 'false'
