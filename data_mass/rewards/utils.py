"""Reward utils file."""
import json
import os

from datetime import datetime
from json import loads
from time import time
from typing import Any, Optional, Union
from requests import Response

from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request,
    update_value_to_json,
    convert_json_to_string,
    create_list,
    print_input_number,
)
from data_mass.product.products import (
    request_get_products_microservice
)
from data_mass.validations import validate_yes_no_option

APP_B2B = "b2b"


def generate_id() -> str:
    """
    Generates an sequential number based on Epoch time \
        using seconds and the first two chars milliseconds.

    Returns
    -------
    str
        The epoch id.
    """
    parsed_time = str(time()).replace('.', '')
    epoch_id = parsed_time[:11]

    return epoch_id


def get_payload(file_path: str) -> Any:
    """
    Extract data from payload.

    Parameters
    ----------
    file_path : str

    Returns
    -------
    Any
        The json data.
    """
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, file_path)

    with open(file_path) as file:
        json_data = json.load(file)

    return json_data


def format_datetime_to_str(date: datetime) -> str:
    """
    Convert datetime to string.

    Returns
    -------
    str
        The formatted string.
    """
    return f"{date.strftime('%Y-%m-%dT%H:%M:%S.%f')}Z"


def get_dt_combos_from_zone(
        zone: str,
        environment: str,
        page_size: Optional[int] = 9999) -> Union[None, Response]:
    """
    Get the DT Combos for the specified zone from Combos MS.

    Parameters
    ----------
    zone : str
    environment : str
    page_size : int
        Default to 9999.

    Returns
    -------
    None or Response
        None when fail to retrive DT combos, else, the http response.
    """
    header_request = get_header_request(
        zone=zone,
        use_jwt_auth=True,
    )

    base_url = get_microservice_base_url(environment)
    query_params = (
        "?types=DT&includeDeleted=false&"
        "includeDisabled=false&page=0&pageSize="
    )
    request_url = f"{base_url}/combos/{query_params}{page_size}"

    response = place_request(
        request_method="GET",
        request_url=request_url,
        request_body="",
        request_headers=header_request,
    )

    if response.status_code == 200:
        return response

    if response.status_code == 404:
        print((
            f'{text.Red}\n'
            '- [Combo Service] There are no DT combos registered.\n'
            f'- Response Status: "{response.status_code}".\n'
            f'- Response message "{response.text}".'
        ))
    else:
        print((
            f'{text.Red}n'
            '- [Combo Service] Failure to retrieve DT combos.\n'
            f'- Response Status: "{response.status_code}".\n'
            f'- Response message "{response.text}".'
        ))

    return None


def get_rewards_combos_by_account(
        account_id: str,
        zone: str,
        environment: str) -> Union[None, Response]:
    """

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str

    Returns
    -------
    None or Response
        None when fail to retrive DT combos, else, the http response.
    """
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        account_id=account_id,
        jwt_app_claim=APP_B2B
    )

    base_url = get_microservice_base_url(environment, False)
    request_url = (
        f"{base_url}"
        "/loyalty-business-service"
        "/programs/accounts"
        f"/{account_id}/combos"
    )

    response = place_request(
        request_method="GET",
        request_url=request_url,
        request_body="",
        request_headers=request_headers
    )

    if response.status_code == 200:
        json_data = loads(response.text)

        if json_data['combos']:
            return response

        print((
            f'{text.Red}\n'
            '- [Rewards] There are no DT combos available '
            f'for the account "{account_id}".\n'
            '- Please use the menu option to associate '
            'DT combos to this account.'
        ))
    elif response.status_code == 404:
        print((
            f"{text.Red}\n"
            f'- [Rewards] The account "{account_id}" '
            'is not enrolled to any rewards program.\n'
            '- Please use the menu option "Enroll POC to a program" '
            'to enroll this account to a rewards program.'
        ))
    else:
        print((
            f'{text.Red}\n'
            '- [Rewards] Failure when getting DT combos'
            f' for account "{account_id}".\n'
            f'- Response Status: "{response.status_code}".\n'
            f'- Response message "{response.text}".'
        ))

    return None


def post_combo_relay_account(
        zone: str,
        environment: str,
        account_id: str,
        dt_combos_to_associate: list,
        sku: list) -> Response:
    """
    Create new Combo Relay Account on the microservice.

    Parameters
    ----------
    zone : str
    environment : str
    account_id : str
    dt_combos_to_associate : list
    sku : list

    Returns
    -------
    Response
        The http response.
    """
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=False,
        use_root_auth=False,
        use_inclusion_auth=True,
        sku_product=False
    )

    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/combo-relay/accounts"

    # Define the list of Limits for the main payload
    dict_values_limit = {
        "daily": 200,
        "monthly": 200,
    }

    # Define the list of ConsumedLimits for the main payload
    dict_values_consumed_limit = {
        "daily": 0,
        "monthly": 0
    }

    dict_values_freegoods = {
        "quantity": 5,
        "skus": create_list(sku),
    }

    # Define the entire list of Combos for the main payload
    dt_combos_list = []
    for dt_combo in dt_combos_to_associate:
        dict_values_dt_combo = {
            "id": dt_combo["id"],
            "externalId": dt_combo["id"],
            "title": dt_combo["title"],
            "description": dt_combo["description"],
            "startDate": dt_combo["startDate"],
            "endDate": dt_combo["endDate"],
            "type": "DT",
            "image": (
                "https://test-conv-micerveceria.abi-sandbox.net/"
                "media/catalog/product/c/o/combo-icon_11.png"
            ),
            "items": None,
            "freeGoods": dict_values_freegoods,
            "limit": dict_values_limit,
            "consumedLimit": dict_values_consumed_limit,
            "originalPrice": 0,
            "price": 0,
            "discountPercentOff": 0,
            "score": 0,
        }
        dt_combos_list.append(dict_values_dt_combo)

    dict_values_account_combos = {
        "accounts": create_list(account_id),
        "combos": dt_combos_list
    }

    request_body = convert_json_to_string(dict_values_account_combos)
    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 201:
        print((
            f"{text.Green}\n"
            f'- [Combo Relay Service] Total of "{len(dt_combos_to_associate)}"'
            f' DT combos associated successfully to account "{account_id}".'
        ))
    else:
        print((
            f"{text.Red}\n"
            "- [Combo Relay Service] Failure when associating DT "
            "combos to the account.\n"
            f'- Response Status: "{str(response.status_code)}".\n'
            f'- Response message: "{response.text}"'
        ))

    return response


def create_product_list_from_zone(
        zone: str,
        environment: str) -> Union[None, list]:
    """
    Generates the SKU list available for a zone.

    Parameters
    ----------
    zone : str
    environment : str

    Returns
    -------
    None or list
        None if there's no products in the microservice, \
        else, a list with sku's.
    """
    response_products = request_get_products_microservice(zone, environment)
    sku_list = []

    if not response_products:
        return None

    for product in response_products:
        sku_list.append(product['sku'])

    return sku_list


def display_all_programs_info(
        list_all_programs: list,
        show_initial_balance: bool = False,
        show_redeem_limit: bool = False) -> None:
    """
    Displays all programs information.

    Parameters
    ----------
    list_all_programs : list
    show_initial_balance : bool
        Default to False.
    show_redeem_limit : bool
        Default to False.
    """
    all_programs_dictionary = {}
    print(f"{text.Yellow}\nExisting Reward programs: ")

    for program in list_all_programs:
        all_programs_dictionary.setdefault(
            "Program ID",
            []
        ).append(program["id"])

        all_programs_dictionary.setdefault(
            "Program Name",
            []
        ).append(program["name"])

        if show_initial_balance:
            all_programs_dictionary.setdefault(
                "Current initial balance",
                []
            ).append(program["initialBalance"])

        if show_redeem_limit:
            all_programs_dictionary.setdefault(
                "Current redeem limit",
                []
            ).append(program["redeemLimit"])

    tabulate_data = tabulate(
        all_programs_dictionary,
        headers="keys",
        tablefmt="grid"
    )
    print(f"{text.default_text_color}{tabulate_data}")


def display_all_challenges_info(list_all_challenges: list) -> None:
    """
    Displays all challenges information

    Parameters
    ----------
    list_all_challenges : list
    """
    all_challenges_dictionary = {}
    print(f"{text.Yellow}\nExisting challenges: ")

    for challenge in list_all_challenges:
        all_challenges_dictionary.setdefault(
            "Challenge ID",
            []
        ).append(challenge["id"])

        all_challenges_dictionary.setdefault(
            "Title",
            []
        ).append(challenge["title"])

        all_challenges_dictionary.setdefault(
            "Execution Method",
            []
        ).append(challenge["executionMethod"])

        all_challenges_dictionary.setdefault(
            "Points",
            []
        ).append(challenge["points"])

        all_challenges_dictionary.setdefault(
            "Start Date",
            []
        ).append(challenge["startDate"])

        all_challenges_dictionary.setdefault(
            "End Date",
            []
        ).append(challenge["endDate"])

    tabulate_data = tabulate(
        tabular_data=all_challenges_dictionary,
        headers='keys',
        tablefmt='grid'
    )

    print(f"{text.default_text_color}{tabulate_data}")


def make_account_eligible(
        account_info: str,
        zone: str,
        environment: str) -> bool:
    """
    Make an account eligible to DM Rewards program.

    Parameters
    ----------
    account_info : str
    zone : str
    environment : str

    Returns
    -------
    bool
        `True`, when no error accours, else, `False`.
    """
    request_headers = get_header_request(zone=zone, use_root_auth=True)
    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/account-relay/"

    # Update the account's information with the right
    # values to associate to a Reward program
    json_object = update_value_to_json(
        account_info,
        '[0][potential]',
        'DM-POTENT'
    )
    json_object = update_value_to_json(
        account_info,
        '[0][segment]',
        'DM-SEG'
    )
    json_object = update_value_to_json(
        account_info,
        '[0][subSegment]',
        'DM-SUBSEG'
    )

    request_body = convert_json_to_string(json_object)
    response = place_request(
        request_method='POST',
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers,
    )

    if response.status_code == 202:
        return True

    return False


def build_request_url_with_projection_query(
        request_url: str,
        projections: list) -> str:
    """
    Format request.

    Parameters
    ----------
    request_url : str
    projections : list

    Returns
    -------
    str
        The formated string.
    """
    if projections:
        i = 0
        for projection in projections:
            if i == 0:
                projection_query = f"?projection={str(projection).upper()}"
            else:
                projection_query += f"?projection={str(projection).upper()}"
            i += 1
        request_url += projection_query

    return request_url


def print_input_combo_qty(message: str, max_value: int) -> int:
    """
    Prompts input combo quantity.

    Parameters
    ----------
    message : str
    max_value : int

    Returns
    -------
    int
        The combo quantity.
    """
    combos_qty = print_input_number(
        f"\n- {message} (Maximum: {str(max_value)})"
    )

    while combos_qty <= 0 or combos_qty > max_value:
        print((
            f"{text.Red}\n"
            "Invalid value! Must be greater than zero, "
            f"up to {str(max_value)}!"
        ))

        combos_qty = print_input_number(
            f"\n- {message} (Maximum: {str(max_value)})"
        )

    return combos_qty


def print_input_decision(message: str) -> str:
    """
    Prompts user decision.

    Parameters
    ----------
    message : str

    Returns
    -------
    str
        The decision chosen by the user
    """
    decision = input((
        f"{text.Yellow}\n"
        f"{message}? y/N: "
    )).upper()

    while not validate_yes_no_option(decision):
        print(f"{text.Red}\n- Invalid option !!")
        decision = input((
            f"{text.Yellow}\n"
            f"{message}? y/N: "
        )).upper()

    return decision
