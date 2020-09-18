# Standard library imports
import json
import os

# Local application imports
from common import get_header_request, get_microservice_base_url, update_value_to_json, create_list, \
    convert_json_to_string, place_request
from classes.text import text


# Include credit for account on microservice
def add_credit_to_account_microservice(abi_id, zone, environment, credit, balance):
    # Get headers
    request_headers = get_header_request(zone, 'false', 'true', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/account-relay/credits'

    # Default value for credit available
    if credit == '':
        credit = '5000'

    # Default value for credit balance
    if balance == '':
        balance = '15000'

    credit = int(credit)
    balance = int(balance)

    # Create dictionary with credit values
    dict_values = {
        'accountId': abi_id,
        'available': credit,
        'balance': balance,
        'total': credit + balance
    }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_credit_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Update the credit values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Account Relay Service] Failure to add credit to account. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'
