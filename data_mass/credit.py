# Standard library imports
import json
import os

import pkg_resources

from data_mass.classes.text import text
# Local application imports
from data_mass.common import (
    convert_json_to_string,
    create_list,
    get_header_request,
    get_microservice_base_url,
    place_request,
    update_value_to_json
    )


# Include credit for account in microservice
def add_credit_to_account_microservice(account_id, zone, environment, credit, balance):
    # Get headers
    request_headers = get_header_request(zone, False, True, False, False)

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
        'accountId': account_id,
        'available': credit,
        'balance': balance,
        'total': credit + balance
    }
    
    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/create_credit_payload.json"
    )
    json_data = json.loads(content.decode("utf-8"))

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
        print(text.Red + '\n- [Account Relay Service] Failure to add credit to the account {account_id}. '
                         'Response Status: {response_status}. Response message: {response_message}'
              .format(account_id=account_id, response_status=str(response.status_code), response_message=response.text))
        return False
