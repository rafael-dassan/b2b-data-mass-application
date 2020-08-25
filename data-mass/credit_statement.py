from common import *
import json


def create_credit_statement(zone, abi_id, environment, month, year):
    """
     Create a credit_statement via the file-management-relay
     Args:
         abi_id: POC unique identifier
         zone: e.g., ZA
         environment: e.g., DEV, SIT, UAT
         month: month that I want to create the document
         year: year that I want to create the document
     Returns: new json_data if success or error message in case of failure
     """

    # Define headers
    request_headers = get_header_request(zone, 'false', 'false', 'false', 'false')

    # Define url request
    request_url = get_microservice_base_url(environment) + '/files-relay'

    # Get body
    request_body = create_credit_statement_payload(year, month, abi_id)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)
    if response.status_code == 202:
        print(text.Green + 'Credit Statement create for the account: ' + abi_id)
        return 'true'
    else:
        print(text.Red + '\n- [file-management Service] Failure to create an order. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def create_credit_statement_payload(year, month, abi_id):
    """
    Create payload for order creation
    Args:
         abi_id: POC unique identifier
         month: month that I want to create the document
         year: year that I want to create the document
    Returns: order payload
    """
    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/credit_statement_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'fileName': 'credit-statement-about-month-' + month + '-for-account-' + str(abi_id) + '.pdf',
        'metadata.accountId': str(abi_id),
        'metadata.date': str(month) + '/' + str(year),
        'title': 'Credit Statement for customer ' + str(abi_id) + ' from ' + str(month) + '/' + str(year)
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data[0], key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    return '[' + request_body + ']'
