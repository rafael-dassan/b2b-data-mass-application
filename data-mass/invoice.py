# Standard library imports
import json
from json import loads
import os
from random import randint

# Local application imports
from common import update_value_to_json, set_to_dictionary, get_microservice_base_url, get_header_request, \
    create_list, convert_json_to_string, place_request
from classes.text import text


def create_invoice_request(zone, environment, order_id, status, order_details, order_items):
    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_invoice_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    invoice_id = 'DM-' + str(randint(1, 100000))
    order_placement_date = order_details.get('placementDate')

    if zone == 'DO':
        placement_date = order_placement_date.split('T')[0] + 'T00:00:00Z'
    else:
        placement_date = order_placement_date.split('+')[0] + 'Z'

    dict_values = {
        'accountId': order_details.get('accountId'),
        'channel': order_details.get('channel'),
        'date': placement_date,
        'interestAmount': order_details.get('interestAmount'),
        'orderDate': placement_date,
        'orderId': order_id,
        'subtotal': order_details.get('subtotal'),
        'invoiceId': invoice_id,
        'status': status,
        'tax': order_details.get('tax'),
        'total': order_details.get('total'),
        'poNumber': order_id,
        'paymentType': order_details.get('paymentMethod'),
        'discount': abs(order_details.get('discount')),
        'itemsQuantity': order_details.get('itemsQuantity')
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    set_to_dictionary(json_object, 'items', order_items)

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/invoices-relay'

    # Get headers
    request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return invoice_id
    else:
        print(text.Red + '\n- [Invoice Relay Service] Failure to create an invoice. Response Status: '
                         '{response_status}. Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return 'false'


def update_invoice_request(zone, environment, invoice_id, payment_method, status):
    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/update_invoice_status.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'invoiceId': invoice_id,
        'paymentType': payment_method,
        'status': status
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/invoices-service'

    # Get headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Create body
    request_body = convert_json_to_string(json_object)

    # Send request
    response = place_request('PATCH', request_url, request_body, request_headers)

    if response.status_code == 202:
        return True
    else:
        print(text.Red + '\n- [Invoice Service] Failure to update an invoice. Response Status: {response_status}. '
                         'Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return 'false'


def check_if_invoice_exists(account_id, invoice_id, zone, environment):
    # Get header request
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(
        environment) + '/invoices-service/?accountId=' + account_id + '&invoiceId=' + invoice_id

    # Place request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data['data']) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data['data']) == 0:
        print(text.Red + '\n- [Invoice Service] The invoice {invoice_id} does not exist'.format(invoice_id=invoice_id))
        return 'false'
    else:
        print(text.Red + '\n- [Invoice Service] Failure to retrieve the invoice {invoice_id}. Response status: '
                         '{response_status}. Response message: {response_message}'
              .format(invoice_id=invoice_id, response_status=response.status_code, response_message=response.text))
        return 'false'


def get_invoices(zone, abi_id, environment):
    header_request = get_header_request(zone, 'true', 'false', 'false', 'false')
    # Get url base
    request_url = get_microservice_base_url(environment, 'false') + '/invoices-service/?accountId=' + abi_id

    # Place request
    response = place_request('GET', request_url, '', header_request)
    invoice_info = loads(response.text)
    if response.status_code == 200:
        return invoice_info
    else:
        return 'false'
