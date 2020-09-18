# Standard library imports
import json
from json import loads
import os

# Third party imports
from tabulate import tabulate

# Local application imports
from common import get_header_request, get_microservice_base_url, place_request, return_payment_term_bank_slip, \
    update_value_to_json, create_list, convert_json_to_string, set_to_dictionary
from classes.text import text


def check_account_exists_microservice(abi_id, zone, environment):
    # Get header request
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/accounts?accountId=' + abi_id

    # Place request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        print(text.Red + '\n- [Account Service] The account ' + abi_id + ' does not exist')
        return 'false'
    else:
        print(text.Red + '\n- [Account Service] Failure to retrieve the account ' + abi_id + '. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def create_account_ms(abi_id, name, payment_method, minimum_order, zone, environment, state, account_status='ACTIVE', enable_empties_loan=False, has_overprice=False):
    payment_term = None
    if zone.upper() == 'BR' and 'BANK_SLIP' in payment_method:
        payment_term = return_payment_term_bank_slip()

    if minimum_order is not None:
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
            'status': account_status,
            'hasEmptiesLoan': enable_empties_loan,
            'hasOverprice': has_overprice,
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
            'status': account_status,
            'hasEmptiesLoan': enable_empties_loan,
            'hasOverprice': has_overprice,
        }

    # Get header request
    request_headers = get_header_request(zone, 'false', 'true', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/account-relay/'

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_account_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    # Place request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'success'
    else:
        print('\n- [Account Relay Service] Failure to create the account ' + abi_id + '. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def display_account_information(account):
    """Display account information
    Arguments:
        - account: all account data
    Print a table containing the available account information
    """
    account_data = account[0]

    # Validate delivery windows
    delivery_window = account_data['deliveryWindows']
    delivery_window_information = list()
    if len(delivery_window) == 0:
        account_delivery_window_values = {
            'Delivery Windows': 'None'
        }
        delivery_window_information.append(account_delivery_window_values)
    else:
        for i in range(len(delivery_window)):
            account_delivery_window_values = {
                'Start Date': delivery_window[i]['startDate'],
                'End Date': delivery_window[i]['endDate'],
                'Expiration Date': delivery_window[i]['expirationDate'],
                'Alternative Date': delivery_window[i]['alternative']
            }
            delivery_window_information.append(account_delivery_window_values)

    # Validate liquor license number
    liquor_license = account_data['liquorLicense']
    if len(liquor_license) == 0:
        liquor_license = 'None'
    else:
        liquor_license = liquor_license[0]['number']

    # Validate payment methods
    payment_methods = account_data['paymentMethods']
    if len(payment_methods) == 0:
        payment_methods = 'None'

    # Validate minimum order
    minimum_order_information = list()
    minimum_order = account_data['minimumOrder']
    if minimum_order is None:
        minimum_order_values = {
            'Minimum Order': 'None'
        }
    else:
        minimum_order_values = {
            'Type': minimum_order['type'],
            'Value': minimum_order['value']
        }
    minimum_order_information.append(minimum_order_values)

    # Validate maximum order
    maximum_order_information = list()
    maximum_order = account_data['maximumOrder']
    if maximum_order is None:
        maximum_order_values = {
            'Maximum Order': 'None'
        }
    else:
        maximum_order_values = {
            'Type': maximum_order['type'],
            'Value': maximum_order['value']
        }
    maximum_order_information.append(maximum_order_values)

    basic_information = list()
    account_values = {
        'Account ID': account_data['accountId'],
        'Name': account_data['name'],
        'Status': account_data['status'],
        'Tax ID': account_data['taxId'],
        'Liquor License Number': liquor_license,
        'Payment Methods': payment_methods
    }
    basic_information.append(account_values)

    credit_information = list()
    credit = account_data['credit']
    if credit is None:
        account_credit_values = {
            'Credit': 'None'
        }
    else:
        account_credit_values = {
            'Credit Balance': account_data['credit']['balance'],
            'Credit Overdue': account_data['credit']['overdue'],
            'Credit Available': account_data['credit']['available'],
            'Credit Total': account_data['credit']['total'],
            'Credit Consumption': account_data['credit']['consumption']
        }
    credit_information.append(account_credit_values)

    print(text.default_text_color + '\nAccount - Basic Information')
    print(tabulate(basic_information, headers='keys', tablefmt='grid'))

    print(text.default_text_color + '\nAccount - Credit Information')
    print(tabulate(credit_information, headers='keys', tablefmt='grid'))

    print(text.default_text_color + '\nAccount - Delivery Window Information')
    print(tabulate(delivery_window_information, headers='keys', tablefmt='grid'))

    print(text.default_text_color + '\nAccount - Minimum Order Information')
    print(tabulate(minimum_order_information, headers='keys', tablefmt='grid'))

    print(text.default_text_color + '\nAccount - Maximum Order Information')
    print(tabulate(maximum_order_information, headers='keys', tablefmt='grid'))


def display_all_account_info(account):
    """Display account information
    Arguments:
        - account: all account data
    Print a table containing information about which accounts it's active on the zone (accountID, taxId and LiquorLicense)
    """
    account_info = list()
    size_account = len(account)

    if len(account) == 0:
        account_values = {
            'Accounts': 'None'
        }
        account_info.append(account_values)
    else:
        for i in range(size_account):
            if account[i]['status'] == 'ACTIVE':
                account_values = {
                    'Account ID': account[i]['accountId'],
                    'Tax Id': account[i]['taxId'],
                    'Status': account[i]['status']
                }
                liquor_license = account[i]['liquorLicense']
                for y in range(len(liquor_license)):
                    set_to_dictionary(account_values, 'Liquor License', liquor_license[y]['number'])
                account_info.append(account_values)

    print(text.default_text_color + '\nAccount - Account ID, Tax ID and Liquor License information ')
    print(tabulate(account_info, headers='keys', tablefmt='grid'))


def display_account_with_products(account_info_list):
    print(text.default_text_color + '\nAccount - Account ID with products per zone')
    print(tabulate(account_info_list, headers='keys', tablefmt='grid'))
