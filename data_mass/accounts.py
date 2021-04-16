import json
import os

from tabulate import tabulate

from data_mass.common import get_header_request, \
    get_microservice_base_url, place_request, \
    update_value_to_json, create_list, \
    convert_json_to_string, set_to_dictionary
from data_mass.classes.text import text
from data_mass.menus.account_menu import print_minimum_order_type_menu, \
    print_minimum_order_value_menu


def check_account_exists_microservice(
        account_id: int,
        zone: str,
        environment: str):
    """
    Check if a given `accout_id` exists in the microservice.

    Parameters
    ----------
    account_id : int
    zone : str
    environment : str

    Returns
    -------
    bool or json
        `False` if not exists, else the account data.
    """
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        use_root_auth=False,
        use_inclusion_auth=False,
        sku_product=False,
        account_id=account_id
    )

    base_url = get_microservice_base_url(environment=environment)
    request_url = f"{base_url}/accounts?accountId={account_id}"
    response = place_request(
        request_method='GET',
        request_url=request_url,
        request_body='',
        request_headers=request_headers
    )

    json_data = json.loads(response.text)

    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        print((
            f"{text.Red}\n- "
            f"[Account Service] "
            f"The account {account_id} does not exist"
        ))

        return False
    else:
        print((
            f"{text.Red}\n-"
            f" [Account Service]"
            f" Failure to retrieve the account {account_id}."
            f" Response Status: {str(response.status_code)}."
            f" Response message: {response.text}"
        ))

        return False


def create_account_ms(
        account_id: str,
        name: str,
        payment_method: list,
        minimum_order: list,
        zone: str,
        environment: str,
        delivery_address: dict,
        account_status: str = 'ACTIVE',
        enable_empties_loan: bool = False):
    """
    Create account on the microservice.

    Parameters
    ---------
    account_id : str
    name : str
    payment_method : list
    minimum_order : list
    zone : str
    environment : str
    delivery_address : dict
    account_status : str
    enable_empties_loan : bool

    Returns
    -------
    bool
        Whenever an account is successfully created.
    """
    payment_term = None
    if zone == 'BR' and 'BANK_SLIP' in payment_method:
        payment_term = return_payment_term_bank_slip()

    dict_values = {
        'accountId': account_id,
        'challengeIds': [account_id],
        'deliveryCenterId': account_id,
        'deliveryScheduleId': account_id,
        'liquorLicense[0].number': account_id,
        'priceListId': account_id,
        'taxId': account_id,
        'name': name,
        'paymentMethods': payment_method,
        'deliveryAddress.address': delivery_address.get('address'),
        'deliveryAddress.city': delivery_address.get('city'),
        'deliveryAddress.state': delivery_address.get('state'),
        'deliveryAddress.zipcode': delivery_address.get('zipcode'),
        'paymentTerms': payment_term,
        'status': account_status,
        'hasEmptiesLoan': enable_empties_loan
    }

    if minimum_order is not None:
        set_to_dictionary(
            dict_values,
            'minimumOrder.type',
            minimum_order[0]
        )
        set_to_dictionary(
            dict_values,
            'minimumOrder.value',
            int(minimum_order[1])
        )
    else:
        set_to_dictionary(dict_values, 'minimumOrder', minimum_order)

    request_headers = get_header_request(zone, False, True, False, False)

    request_url = get_microservice_base_url(environment) + '/account-relay/'

    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_account_payload.json')

    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    response = place_request(
        request_method='POST',
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 202:
        return True
    else:
        print((
            f"\n- [Account Relay Service]"
            f" Failure to create the account {account_id}."
            f" Response status {str(response.status_code)}."
            f" Response message: {response.text}"
        ))

        return False


def display_account_information(account: str):
    """
    Display account information.

    Parameters
    ---------
    account: str
        All account data
    """
    account_data = account[0]

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

    liquor_license = account_data['liquorLicense']
    if len(liquor_license) == 0:
        liquor_license = 'None'
    else:
        liquor_license = liquor_license[0]['number']

    challenge_ids = account_data['challengeIds']
    if challenge_ids is None:
        challenge_ids = 'None'
    else:
        challenge_ids = str(challenge_ids)\
            .replace('[', '')\
            .replace(']', '')\
            .replace('\'', '')

    payment_methods = account_data['paymentMethods']
    if len(payment_methods) == 0:
        payment_methods = 'None'
    else:
        payment_methods = str(payment_methods)\
            .replace('[', '')\
            .replace(']', '')\
            .replace('\'', '')

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
        'Challenge IDs': challenge_ids,
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

    print(f"{text.default_text_color}\nAccount - Basic Information")
    print(tabulate(
        tabular_data=basic_information,
        headers='keys',
        tablefmt='grid'
    ))

    print(f"{text.default_text_color}\nAccount - Credit Information")
    print(tabulate(
        tabular_data=credit_information,
        headers='keys',
        tablefmt='grid'
    ))

    print(f"{text.default_text_color}\nAccount - Delivery Window Information")
    print(tabulate(
        tabular_data=delivery_window_information,
        headers='keys',
        tablefmt='grid'
    ))

    print(f"{text.default_text_color}\nAccount - Minimum Order Information")
    print(tabulate(
        tabular_data=minimum_order_information,
        headers='keys',
        tablefmt='grid'
    ))

    print(f"{text.default_text_color}\nAccount - Maximum Order Information")
    print(tabulate(
        tabular_data=maximum_order_information,
        headers='keys',
        tablefmt='grid'
    ))


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
        min_value = input((
            f"{text.default_text_color} "
            f"Define the minimum order value to not pay any delivery fee: "
        ))

        tax_value = input((
            f"{text.default_text_color} "
            f"Define the delivery fee value: "
        ))

    delivery_cost_values = {
        'min_order_value': min_value,
        'fee_value': tax_value
    }

    return delivery_cost_values


def get_credit_info():
    """
    Prompts to the user for credit information.

    Returns
    ------
    dict
        The credit info.
    """
    credit = input((
        f"{text.default_text_color} "
        "Desired credit available (Default 5000): "
    ))
    balance = input((
        f"{text.default_text_color} "
        "Desired credit balance (Default 15000): "
    ))

    credit_info = {
        'credit': credit,
        'balance': balance
    }

    return credit_info


def get_minimum_order_list(minimum_order_values: dict):
    """
    Convert minimum order to list.

    Parameters
    ----------
    minimum_order_values : dict

    Returns
    -------
    list
    """
    minimum_order = None

    if minimum_order_values is not None:
        minimum_order = [
            minimum_order_values.get('type'),
            minimum_order_values.get('value')
        ]

    return minimum_order


def return_payment_term_bank_slip(days: int = 5):
    """
    Return payment term value for `BANK_SLIP` payment method.

    Parameters
    ----------
    days : int

    Returns
    -------
    list
    """
    term_periods = []

    for day in range(1, days + 1):
        list_term_periods = {
            'days': day
        }

        term_periods.append(list_term_periods)

    list_payment_term = {
        'type': 'BANK_SLIP',
        'termPeriods': term_periods
    }

    return [list_payment_term]


def get_account_delivery_address(zone):
    params = {
        'AR': {
            'address': 'Guaiviravi 1486',
            'city': 'Isidro Casanova',
            'state': 'Buenos Aires',
            'zipcode': 'N/A'
        },
        'BR': {
            'address': 'Rua Carlos Maul 315',
            'city': 'Duque de Caxias',
            'state': 'Rio de Janeiro',
            'zipcode': '25261-270'
        },
        'CA': {
            'address': '1305  Heatherleigh',
            'city': 'Cooksville',
            'state': 'Ontario',
            'zipcode': 'L5A 1V9'
        },
        'CO': {
            'address': 'Cr 72 No. 74B-39, C.P 11001',
            'city': 'Bogota',
            'state': 'Bogota',
            'zipcode': 'N/A'
        },
        'DO': {
            'address': '14 D Junio, No 150',
            'city': 'Santo Domingo',
            'state': 'Santo Domingo',
            'zipcode': 'N/A'
        },
        'EC': {
            'address': 'Rocafuerte 742',
            'city': 'Guayas',
            'state': 'Guayaquil',
            'zipcode': 'N/A'
        },
        'MX': {
            'address': 'Aguacate No. 19 El Rosario',
            'city': 'Actopan',
            'state': 'Hidalgo',
            'zipcode': 'N/A'
        },
        'PA': {
            'address': 'Via Rdo J Alfaro',
            'city': 'Panama',
            'state': 'Panama',
            'zipcode': 'N/A'
        },
        'PE': {
            'address': 'Avenida Salaverry, 674',
            'city': 'Jesus Maria',
            'state': 'Lima',
            'zipcode': 'N/A'
        },
        'PY': {
            'address': 'De las Llanas 3.796',
            'city': 'N/A',
            'state': 'Asuncion',
            'zipcode': 'N/A'
        },
        'ZA': {
            'address': '726  Thomas St',
            'city': 'Blood River',
            'state': 'KwaZulu-Natal',
            'zipcode': '3024'
        }
    }

    return params[zone]