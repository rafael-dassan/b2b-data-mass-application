import json
import os
from time import time

from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.common import (
    convert_json_to_string,
    create_list,
    get_header_request,
    get_microservice_base_url,
    place_request,
    print_input_number,
    update_value_to_json
    )
from data_mass.orders import request_order_creation
from data_mass.product.products import request_get_products_microservice
from data_mass.simulation import request_order_simulation
from data_mass.validations import validate_yes_no_option

APP_B2B = "b2b"


def generate_id():
    # Generates an sequential number based on Epoch time using seconds and
    # the first two chars milliseconds
    # time() return an Epoch time with milliseconds separeted with a dot (.)

    parsed_time = str(time()).replace(".", "")
    epoch_id = parsed_time[:11]

    return epoch_id


def get_payload(file_path):
    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, file_path)

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    return json_data


def format_datetime_to_str(date):
    return date.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


# Get the DT Combos for the specified zone from Combos MS
def get_dt_combos_from_zone(zone, environment, page_size=9999):

    header_request = get_header_request(zone, True, False, False, False)

    # Define url request
    query_params = (
        "?types=DT&includeDeleted=false&includeDisabled=false&page=0&pageSize="
        + str(page_size)
    )
    request_url = (
        get_microservice_base_url(environment) + "/combos/" + query_params
    )

    # Send request
    response = place_request("GET", request_url, "", header_request)

    if response.status_code == 200:
        return response
    elif response.status_code == 404:
        print(
            text.Red
            + f"\n- [Combo Service] There are no DT combos registered."
            f'\n- Response Status: "{str(response.status_code)}".'
            f'\n- Response message "{response.text}".'
        )
    else:
        print(
            text.Red + "\n- [Combo Service] Failure to retrieve DT combos."
            f'\n- Response Status: "{str(response.status_code)}".'
            f'\n- Response message "{response.text}".'
        )

    return None


def get_rewards_combos_by_account(account_id, zone, environment):
    header_request = get_header_request(
        zone, True, False, False, False, account_id, APP_B2B
    )

    request_url = (
        get_microservice_base_url(environment, False)
        + "/loyalty-business-service/programs/accounts/"
        + account_id
        + "/combos"
    )

    response = place_request("GET", request_url, "", header_request)

    if response.status_code == 200:
        json_data = json.loads(response.text)
        if len(json_data["combos"]) > 0:
            return response
        else:
            print(
                text.Red
                + "\n- [Rewards] There are no DT combos available for "
                f'the account "{account_id}".'
                '\n- Please use the menu option "" to associate DT combos '
                "to this account."
            )
    elif response.status_code == 404:
        print(
            text.Red
            + '\n- [Rewards] The account "{account_id}" is not enrolled to any'
            " rewards program."
            '\n- Please use the menu option "Enroll POC to a program" to '
            "enroll this account to a rewards program."
        )
    else:
        print(
            text.Red
            + "\n- [Rewards] Failure when getting DT combos for account"
            f'"{account_id}".'
            f'\n- Response Status: "{str(response.status_code)}".'
            f'\n- Response message "{response.text}".'
        )

    return None


def post_combo_relay_account(
    zone, environment, account_id, dt_combos_to_associate, sku
):
    # Define headers to post the association
    request_headers = get_header_request(zone, False, False, True, False)

    # Define url request to post the association
    request_url = (
        get_microservice_base_url(environment) + "/combo-relay/accounts"
    )

    # Define the list of Limits for the main payload
    dict_values_limit = {
        "daily": 200,
        "monthly": 200,
    }

    # Define the list of ConsumedLimits for the main payload
    dict_values_consumed_limit = {"daily": 0, "monthly": 0}

    dict_values_freegoods = {
        "quantity": 5,
        "skus": create_list(sku),
    }

    # Define the entire list of Combos for the main payload
    dt_combos_list = list()
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
                "https://test-conv-micerveceria.abi-sandbox.net/media/"
                "catalog/product/c/o/combo-icon_11.png"
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

    # Creates the main payload based on the lists created above
    dict_values_account_combos = {
        "accounts": create_list(account_id),
        "combos": dt_combos_list,
    }

    # Create body to associate the combos to account
    request_body = convert_json_to_string(dict_values_account_combos)

    # Send request to associate the combos to account
    response = place_request(
        "POST", request_url, request_body, request_headers
    )

    if response.status_code == 201:
        print(
            text.Green + "\n- [Combo Relay Service] Total of "
            f'"{str(len(dt_combos_to_associate))}" DT combos associated '
            f'successfully to account "{account_id}".'
        )
    else:
        print(
            text.Red
            + "\n- [Combo Relay Service] Failure when associating DT combos "
            "to the account."
            f'\n- Response Status: "{str(response.status_code)}".'
            f'\n- Response message: "{response.text}"'
        )

    return response


# Generates the SKU list available for a zone
def create_product_list_from_zone(zone, environment):
    response_products = request_get_products_microservice(zone, environment)

    if not response_products:
        return None
    else:
        sku_list = list()
        for product in response_products:
            sku_list.append(product["sku"])

        return sku_list


# Displays all programs information
def display_all_programs_info(
    list_all_programs, show_initial_balance=False, show_redeem_limit=False
):
    all_programs_dictionary = dict()

    print(text.Yellow + "\nExisting Reward programs:")
    for program in list_all_programs:
        all_programs_dictionary.setdefault("Program ID", []).append(
            program["id"]
        )
        all_programs_dictionary.setdefault("Program Name", []).append(
            program["name"]
        )
        if show_initial_balance:
            all_programs_dictionary.setdefault(
                "Current initial balance", []
            ).append(program["initialBalance"])
        if show_redeem_limit:
            all_programs_dictionary.setdefault(
                "Current redeem limit", []
            ).append(program["redeemLimit"])

    print(
        text.default_text_color
        + tabulate(all_programs_dictionary, headers="keys", tablefmt="grid")
    )


# Displays all challenges information
def display_all_challenges_info(list_all_challenges):
    all_challenges_dictionary = dict()

    print(text.Yellow + "\nExisting challenges:")
    for challenge in list_all_challenges:
        all_challenges_dictionary.setdefault("Challenge ID", []).append(
            challenge["id"]
        )
        all_challenges_dictionary.setdefault("Title", []).append(
            challenge["title"]
        )
        all_challenges_dictionary.setdefault("Execution Method", []).append(
            challenge["executionMethod"]
        )
        all_challenges_dictionary.setdefault("Points", []).append(
            challenge["points"]
        )
        all_challenges_dictionary.setdefault("Start Date", []).append(
            challenge["startDate"]
        )
        all_challenges_dictionary.setdefault("End Date", []).append(
            challenge["endDate"]
        )

    print(
        text.default_text_color
        + tabulate(all_challenges_dictionary, headers="keys", tablefmt="grid")
    )


# Make an account eligible to DM Rewards program
def make_account_eligible(account_info, zone, environment):

    # Get header request
    request_headers = get_header_request(zone, False, True, False, False)

    # Get base URL
    request_url = get_microservice_base_url(environment) + "/account-relay/"

    # Update the account's information with the right values
    # to associate to a Reward program
    json_object = update_value_to_json(
        account_info, "[0][potential]", "DM-POTENT"
    )
    json_object = update_value_to_json(account_info, "[0][segment]", "DM-SEG")
    json_object = update_value_to_json(
        account_info, "[0][subSegment]", "DM-SUBSEG"
    )

    # Create body
    request_body = convert_json_to_string(json_object)

    # Place request
    response = place_request(
        "POST", request_url, request_body, request_headers
    )

    if response.status_code == 202:
        return True
    else:
        return False


def build_request_url_with_projection_query(request_url, projections):
    if len(projections) > 0:
        i = 0
        for projection in projections:
            if i == 0:
                projection_query = "?projection=" + str(projection).upper()
            else:
                projection_query += "&projection=" + str(projection).upper()
            i += 1
        request_url += projection_query

    return request_url


def print_input_combo_qty(message, max_value):
    combos_qty = print_input_number(
        f"\n- {message} (Maximum: {str(max_value)})"
    )
    while combos_qty <= 0 or combos_qty > max_value:
        print(
            text.Red + "\nInvalid value!! "
            f"Must be greater than zero, up to {str(max_value)} !!"
        )
        combos_qty = print_input_number(
            f"\n- {message} (Maximum: {str(max_value)})"
        )

    return combos_qty


def print_input_decision(message):
    decision = input(text.Yellow + f"\n- {message}? y/N: ")
    while validate_yes_no_option(decision.upper()) is False:
        print(text.Red + "\n- Invalid option !!")
        decision = input(text.Yellow + f"\n- {message}? y/N: ")

    return decision.upper()


def post_orders_rewards(
    zone: str,
    environment: str,
    account: list,
    item_list: list,
    dt_combos: list,
    pay_method: str,
    order_status: str,
    allow_order_cancel: str,
    delivery_date: str,
    empties: list = [],
    payment_term: bool = 0
) -> list:
    """
    Post methods for orders rewards.

    Parameters
    ----------
    zone : str
        e.g., AR, BR, DO, etc
    environment : str
        e.g., DEV, SIT, UAT
    account : list
        list with account infos.
    item_list : list
        list o skus to be used in creation.
    dt_combos : list
        list of digital trade combos to be used.
    pay_method : str
        desired payment method.
    order_status : str
        how order should be entered eg. Placed, Pending, Confirmed, etc.
    allow_order_cancel : str
        order could be cancellable ?
    delivery_date : str
        date of order to be delivered.
    empties : list, optional
        list of empties, by default []
    payment_term : bool, optional
        payment terms according to the payment method, by default 0

    Returns
    -------
    list
        response from http method or None.
    """

    order_items = request_order_simulation(
        zone=zone,
        environment=environment,
        account_id=account[0]['accountId'],
        delivery_center_id=account[0]['deliveryCenterId'],
        items=item_list,
        combos=dt_combos if dt_combos else [],
        empties=empties,
        payment_method=pay_method,
        payment_term=payment_term,
        delivery_date=delivery_date
    )
    if not order_items:
        return None

    response = request_order_creation(
        account_id=account[0]['accountId'],
        delivery_center_id=account[0]['deliveryCenterId'],
        zone=zone,
        environment=environment,
        allow_order_cancel=allow_order_cancel,
        order_items=order_items,
        order_status=order_status,
        delivery_date=delivery_date
    )
    if not response:
        return None

    return response
