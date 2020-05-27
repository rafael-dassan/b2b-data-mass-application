from json import loads
from common import *
from tabulate import tabulate


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
        return json_data
    else:
        return 'false'


def create_account_ms(abi_id, name, payment_method, minimum_order, zone, environment, state):
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
        return response.status_code


def display_account_information(abi_id, zone, environment):
    """Display account information
    Arguments:
        - zone: (e.g, BR,ZA,DO)
        - environment: (e.g, UAT,SIT)
        - abi_id: account_id
    Return a table containing the available account information
    """
    account_response = check_account_exists_microservice(abi_id, zone, environment)

    if account_response == 'false':
        return 'error_ms'
    elif len(account_response) == 0:
        return 'not_found'
    else:
        account = account_response[0]

    # Validate delivery windows
    delivery_window = account['deliveryWindows']
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
    liquor_license = account['liquorLicense']
    if len(liquor_license) == 0:
        liquor_license = 'None'
    else:
        liquor_license = liquor_license[0]['number']

    # Validate payment methods
    payment_methods = account_response[0]['paymentMethods']
    if len(payment_methods) == 0:
        payment_methods = 'None'

    # Validate minimum order
    minimum_order_information = list()
    minimum_order = account['minimumOrder']
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
    maximum_order = account['maximumOrder']
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
        'Account ID': account['accountId'],
        'Name': account['name'],
        'Status': account['status'],
        'Tax ID': account['taxId'],
        'Liquor License Number': liquor_license,
        'Payment Methods': payment_methods
    }
    basic_information.append(account_values)

    credit_information = list()
    credit = account['credit']
    if credit is None:
        account_credit_values = {
            'Credit': 'None'
        }
    else:
        account_credit_values = {
            'Credit Balance': account['credit']['balance'],
            'Credit Overdue': account['credit']['overdue'],
            'Credit Available': account['credit']['available'],
            'Credit Total': account['credit']['total'],
            'Credit Consumption': account['credit']['consumption']
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
