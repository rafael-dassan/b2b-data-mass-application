# Standard library imports
import json
from json import loads
import os

# Third party imports
from tabulate import tabulate

# Local application imports
from common import get_header_request, get_microservice_base_url, place_request, update_value_to_json, create_list, \
    convert_json_to_string, set_to_dictionary
from classes.text import text
from menus.account_menu import print_minimum_order_type_menu, print_minimum_order_value_menu


def check_account_exists_microservice(account_id, zone, environment):
    # Get header request
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/accounts?accountId=' + account_id

    # Place request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        print(text.Red + '\n- [Account Service] The account {account_id} does not exist'.format(account_id=account_id))
        return 'false'
    else:
        print(text.Red + '\n- [Account Service] Failure to retrieve the account {account_id}. Response Status: '
                         '{response_status}. Response message: {response_message}'
              .format(account_id=account_id, response_status=str(response.status_code), response_message=response.text))
        return 'false'


def create_account_ms(account_id, name, payment_method, minimum_order, zone, environment, state,
                      account_status='ACTIVE', enable_empties_loan=False):
    payment_term = None
    if zone == 'BR' and 'BANK_SLIP' in payment_method:
        payment_term = return_payment_term_bank_slip()

    if minimum_order is not None:
        dict_values = {
            'accountId': account_id,
            'deliveryCenterId': account_id,
            'deliveryScheduleId': account_id,
            'liquorLicense[0].number': account_id,
            'minimumOrder.type': minimum_order[0],
            'minimumOrder.value': int(minimum_order[1]),
            'priceListId': account_id,
            'taxId': account_id,
            'name': name,
            'paymentMethods': payment_method,
            'deliveryAddress.state': state,
            'paymentTerms': payment_term,
            'status': account_status,
            'hasEmptiesLoan': enable_empties_loan
        }
    else:
        dict_values = {
            'accountId': account_id,
            'deliveryCenterId': account_id,
            'deliveryScheduleId': account_id,
            'liquorLicense[0].number': account_id,
            'minimumOrder': minimum_order,
            'priceListId': account_id,
            'taxId': account_id,
            'name': name,
            'paymentMethods': payment_method,
            'deliveryAddress.state': state,
            'paymentTerms': payment_term,
            'status': account_status,
            'hasEmptiesLoan': enable_empties_loan
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
        print('\n- [Account Relay Service] Failure to create the account {account_id}. Response status '
              '{response_status}. Response message: {response_message}'
              .format(account_id=account_id, response_status=str(response.status_code), response_message=response.text))
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
    Print a table containing information about which accounts it's active on the zone (accountID, taxId and
    LiquorLicense)
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


def get_minimum_order_info():
    minimum_order_type = print_minimum_order_type_menu()
    minimum_order_value = print_minimum_order_value_menu()

    minimum_order_values = list()
    minimum_order_values.append(minimum_order_type)
    minimum_order_values.append(minimum_order_value)

    return minimum_order_values


def get_delivery_cost_values(option):
    min_value = 0
    tax_value = 0

    if option.upper() == 'Y':
        min_value = input(text.default_text_color + 'Define the minimum order value to not pay any delivery fee: ')
        tax_value = input(text.default_text_color + 'Define the delivery fee value: ')

    delivery_cost_values = {
        'min_order_value': min_value,
        'fee_value': tax_value
    }

    return delivery_cost_values


def get_credit_info():
    credit = input(text.default_text_color + 'Desired credit available (Default 5000): ')
    balance = input(text.default_text_color + 'Desired credit balance (Default 15000): ')

    credit_info = {
        'credit': credit,
        'balance': balance
    }

    return credit_info


def get_minimum_order_list(minimum_order_values):
    if minimum_order_values is not None:
        minimum_order = [minimum_order_values.get('type'), minimum_order_values.get('value')]
    else:
        minimum_order = None

    return minimum_order


# Return payment term value for BANK_SLIP payment method
def return_payment_term_bank_slip():
    payment_term = []
    term_periods = []

    temp_index = 0
    while temp_index < 5:
        temp_index = temp_index + 1
        list_term_periods = {
            'days': temp_index
        }

        term_periods.append(list_term_periods)

    list_payment_term = {
        'type': 'BANK_SLIP',
        'termPeriods': term_periods
    }

    payment_term.append(list_payment_term)
    return payment_term
