import json
from typing import Dict

import click
import pkg_resources
from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request,
    set_to_dictionary,
)
from data_mass.config import get_settings
from data_mass.menus.account_menu import (
    print_minimum_order_type_menu,
    print_minimum_order_value_menu
)


def check_account_exists_microservice(
        account_id: str,
        zone: str,
        environment: str) -> bool:
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

    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/accounts?accountId={account_id}"

    if zone == "US":
        settings = get_settings()

        request_url = (
            f"{base_url}"
            "/accounts"
            f"?vendorAccountId={account_id}"
            f"&vendorId={settings.vendor_id}"
        )

    response = place_request(
        request_method='GET',
        request_url=request_url,
        request_body='',
        request_headers=request_headers
    )

    json_data = json.loads(response.text)

    if response.status_code == 200 and len(json_data) != 0:
        verification_list = [
            'DM-SUBSEG',
            'DM-SEG',
            'DM-SUBSEG_NO_REWARDS',
            'DM-SEG_NO_REWARDS'
        ]
        if (
            zone == "PY"
            and json_data[0]['segment'] not in verification_list
            and json_data[0]['subSegment'] not in verification_list
          ):

            print(
                f"{text.Red}\n-"
                f" [Account Service]"
                f" The account {account_id} was not created by Data Mass."
                f" Response message: "
                "https://ab-inbev.atlassian.net/secure/RapidBoard.jspa?r\
                    apidView=1565&modal=detail&selectedIssue=BEESDM-81"
            )

            return False
        return json_data

    elif response.status_code == 200 and not json_data:
        print(
            f"{text.Red}\n- "
            f"[Account Service] "
            f"The account {account_id} does not exist"
        )

        return False

    print(
        f"{text.Red}\n-"
        f" [Account Service]"
        f" Failure to retrieve the account {account_id}."
        f" Response Status: {str(response.status_code)}."
        f" Response message: {response.text}"
    )

    return False


def get_multivendor_account_id(
        vendor_account_id: str,
        zone: str,
        environment: str) -> str:
    """
    Get accountId of the vendorAccountId

    Parameters
    ----------
    vendor_account_id : str
    zone : str
    environment : str

    Returns
    -------
    str
        The accountId.
    """
    request_headers = get_header_request(zone=zone)
    settings = get_settings()

    base_url = get_microservice_base_url(environment)
    request_url = (
        f"{base_url}"
        "/accounts/"
        f"?vendorAccountId={vendor_account_id}"
        f"&vendorId={settings.vendor_id}"
    )

    response = place_request(
        request_method='GET',
        request_url=request_url,
        request_body='',
        request_headers=request_headers
    )

    json_data: dict = json.loads(response.text)

    if response.status_code == 200 and json_data:
        account, = json_data
        account_id = account.get("accountId", None)

        return account_id

    if response.status_code == 200 and not json_data:
        print(
            f"{text.Red}\n- "
            f"[Account Service] "
            f"The account {vendor_account_id} does not exist"
        )

        return None

    print(
        f"{text.Red}\n-"
        f" [Account Service] "
        f"Failure to retrieve the account {vendor_account_id}.\n"
        f"Response Status: {response.status_code}.\n"
        f"Response message: {response.text}.\n"
    )

    return None


def create_account_ms(
        account_id: str,
        name: str,
        payment_method: list,
        minimum_order: list,
        zone: str,
        environment: str,
        delivery_address: dict,
        owner: dict = None,
        account_status: str = 'ACTIVE',
        enable_empties_loan: bool = False,
        eligible_rewards: bool = True,
        **kwargs
) -> bool:
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
    owner: dict
    account_status : str
    enable_empties_loan : bool
    eligible_rewards : bool

    Returns
    -------
    bool
        Whenever an account is successfully created.
    """
    if not owner:
        owner = {}
    payment_term = None
    if zone == "BR" and "BANK_SLIP" in payment_method:
        payment_term = return_payment_term_bank_slip()

    dict_values = {
        "challengeIds": [account_id],
        "deliveryCenterId": account_id,
        "deliveryScheduleId": account_id,
        "liquorLicense": [{
            "number": account_id
        }],
        "priceListId": account_id,
        "taxId": account_id,
        "name": name,
        "paymentMethods": payment_method,
        "deliveryAddress": {
            "address": delivery_address.get("address"),
            "street": delivery_address.get('street'),
            "city": delivery_address.get("city"),
            "state": delivery_address.get("state"),
            "zipcode": delivery_address.get("zipcode")
        },
        "paymentTerms": payment_term,
        "status": account_status,
        "hasEmptiesLoan": enable_empties_loan,
        "owner": {
            "email": owner.get("email", "test@mailinator.com"),
            "firstName": owner.get("first_name", "TEST OWNER FIRST NAME"),
            "lastName": owner.get("last_name", "TEST OWNER LAST NAME"),
            "phone": 11999999999
        }
    }

    if zone == "US":
        schema = "data/create_account_us_payload.json"

        dict_values.update({
            "vendorAccountId": account_id,
            "hasPONumberRequirement": kwargs.get(
                "hasPONumberRequirement",
                False
            )
        })
    else:
        schema = "data/create_account_payload.json"
        dict_values.update({"accountId": account_id})

    content = pkg_resources.resource_string("data_mass", schema)

    if minimum_order is not None:
        dict_values.update({
            "minimumOrder": {
                "type": minimum_order[0],
                "value": int(minimum_order[1])
            }
        })
    else:
        dict_values.update({"minimumOrder": minimum_order})

    # If the user chooses to make an account eligible for rewards program,
    # we will include the necessary information to match
    # with a Data Mass available one
    # If not, we associate random information that will
    # not match with any available program
    if eligible_rewards:
        set_to_dictionary(dict_values, 'potential', 'DM-POTENT')
        set_to_dictionary(dict_values, 'segment', 'DM-SEG')
        set_to_dictionary(dict_values, 'subSegment', 'DM-SUBSEG')
    else:
        set_to_dictionary(dict_values, 'potential', 'DM-POTENT_NO_REWARDS')
        set_to_dictionary(dict_values, 'segment', 'DM-SEG_NO_REWARDS')
        set_to_dictionary(dict_values, 'subSegment', 'DM-SUBSEG_NO_REWARDS')

    request_headers = get_header_request(zone, False, True, False, False)
    request_url = f"{get_microservice_base_url(environment)}/account-relay/"

    body: dict = json.loads(content.decode("utf-8"))
    body.update(dict_values)

    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=json.dumps([body]),
        request_headers=request_headers
    )

    if response.status_code in [202, 200]:
        return True

    print(
        f"{text.Red}"
        f"\n- [Account Relay Service]"
        f" Failure to create the account {account_id}.\n"
        f" Response status {str(response.status_code)}.\n"
        f" Response message: {response.text}"
    )

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
    delivery_window_information = []
    if not delivery_window:
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
    if not payment_methods:
        payment_methods = 'None'
    else:
        payment_methods = str(payment_methods)\
            .replace('[', '')\
            .replace(']', '')\
            .replace('\'', '')

    minimum_order_information = []
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

    basic_information = []
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

    owner_info = []
    owner_info_values = {
        'Owner E-mail': account_data.get('owner').get("email", ""),
        'Owner Name': (
            f'{account_data.get("owner").get("firstName", "")} '
            f'{account_data.get("owner").get("lastName", "")}'
        ),
    }
    owner_info.append(owner_info_values)

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
        tablefmt='fancy_grid'
    ))

    print(f"{text.default_text_color}\nAccount - Owner Information")
    print(tabulate(
        tabular_data=owner_info,
        headers='keys',
        tablefmt='fancy_grid'
    ))

    print(f"{text.default_text_color}\nAccount - Credit Information")
    print(tabulate(
        tabular_data=credit_information,
        headers='keys',
        tablefmt='fancy_grid'
    ))

    print(f"{text.default_text_color}\nAccount - Delivery Window Information")
    print(tabulate(
        tabular_data=delivery_window_information,
        headers='keys',
        tablefmt='fancy_grid'
    ))

    print(f"{text.default_text_color}\nAccount - Minimum Order Information")
    print(tabulate(
        tabular_data=minimum_order_information,
        headers='keys',
        tablefmt='fancy_grid'
    ))

    print(f"{text.default_text_color}\nAccount - Maximum Order Information")
    print(tabulate(
        tabular_data=maximum_order_information,
        headers='keys',
        tablefmt='fancy_grid'
    ))


def get_minimum_order_info():
    minimum_order_type = print_minimum_order_type_menu()
    minimum_order_value = print_minimum_order_value_menu()

    minimum_order_values = []
    minimum_order_values.append(minimum_order_type)
    minimum_order_values.append(minimum_order_value)

    return minimum_order_values


def get_delivery_cost_values(option: str) -> Dict[str, str]:
    """
    Get delivery cost values.

    Parameters
    ----------
    option : str

    Returns
    -------
    dict
        A dict delivery object with `min_order_value`\
        and `fee_value` properties.
    """
    min_value = tax_value = "0"

    if option.upper() == "Y":
        min_value = input(
            f"{text.default_text_color}"
            f"Define the minimum order value to not pay any delivery fee: "
        )

        tax_value = input(
            f"{text.default_text_color}"
            f"Define the delivery fee value: "
        )

    delivery_cost_values = {
        "min_order_value": min_value,
        "fee_value": tax_value
    }

    return delivery_cost_values


def get_credit_info() -> Dict:
    """
    Prompts to the user for credit information,
    to create a dict with types of credit and the values.

    Returns
    ------
    dict
        The credit ammount for "available", "balance", "consumption" and \
        "overdue".
    """
    credit_types = {
        "available": 5000,
        "balance": 15000,
        "consumption": 5000,
        "overdue": 15000,
    }

    for key, value in credit_types.items():
        updated = get_user_prompt_credit_info(key, value)
        credit_types.update(updated)

    total = sum(credit_types.values())
    credit_types.update({"total": total})

    return credit_types


def get_user_prompt_credit_info(credit_type: str, value: int) -> Dict:
    """
    Ask user two questions, one y_n answer and another to input the desired
    value to credit type.

    Parameters
    ----------
    credit_type : str
        type of credit.
    value : int
        ammount of credit.

    Returns
    -------
    Dict
        key with defalt or the new value credit type.
    """
    user_choice = click.prompt(
        f"{text.LightYellow}"
        f"Would like to insert value for {credit_type}? (Default {value})",
        type=click.Choice(["y", "n"], case_sensitive=False),
    )
    if user_choice.upper() == "Y":
        value = click.prompt(
            f"{text.default_text_color}"
            f"Desired credit {credit_type}",
            type=int
        )
    return {credit_type: value}


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


def get_account_delivery_address(zone: str) -> dict:
    params = {
        'AR': {
            'address': 'Guaiviravi 1486',
            'street': 'Guaiviravi',
            'city': 'Isidro Casanova',
            'state': 'Buenos Aires',
            'zipcode': 'N/A'
        },
        'BR': {
            'address': 'Rua Carlos Maul 315',
            'street': 'Rua Carlos Maul',
            'city': 'Duque de Caxias',
            'state': 'Rio de Janeiro',
            'zipcode': '25261-270'
        },
        'CA': {
            'address': '1305  Heatherleigh',
            'strret': 'Heatherleigh',
            'city': 'Cooksville',
            'state': 'Ontario',
            'zipcode': 'L5A 1V9'
        },
        'CO': {
            'address': 'Cr 72 No. 74B-39, C.P 11001',
            'street': 'Bogota street',
            'city': 'Bogota',
            'state': 'Bogota',
            'zipcode': 'N/A'
        },
        'DO': {
            'address': '14 D Junio, No 150',
            'street': '14 D Junio',
            'city': 'Santo Domingo',
            'state': 'Santo Domingo',
            'zipcode': 'N/A'
        },
        'EC': {
            'address': 'Rocafuerte 742',
            'street': 'Rocafuerte',
            'city': 'Guayas',
            'state': 'Guayaquil',
            'zipcode': 'N/A'
        },
        'MX': {
            'address': 'Aguacate No. 19 El Rosario',
            'street': 'Aguacate',
            'city': 'Actopan',
            'state': 'Hidalgo',
            'zipcode': 'N/A'
        },
        'PA': {
            'address': 'Via Rdo J Alfaro, 155',
            'street': 'Via Rdo J Alfaro',
            'city': 'Panama',
            'state': 'Panama',
            'zipcode': 'N/A'
        },
        'PE': {
            'address': 'Avenida Salaverry, 674',
            'street': 'Avenida Salaverry',
            'city': 'Jesus Maria',
            'state': 'Lima',
            'zipcode': 'N/A'
        },
        'PY': {
            'address': 'De las Llanas 3.796',
            'street': 'De las Llanas',
            'city': 'N/A',
            'state': 'Asuncion',
            'zipcode': 'N/A'
        },
        'ZA': {
            'address': '726  Thomas St',
            'street': 'Thomas St',
            'city': 'Blood River',
            'state': 'KwaZulu-Natal',
            'zipcode': '3024'
        },
        'US': {
            'address': 'McDowell Street, 1639',
            'street': 'McDowell Street',
            'city': 'Nashville',
            'state': 'Tennessee',
            'zipcode': '87334'
        }
    }

    return params[zone]
