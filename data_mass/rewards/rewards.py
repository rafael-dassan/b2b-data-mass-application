from json import loads
from multiprocessing import Pool, cpu_count
from random import choice, randint

from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.common import (
    convert_json_to_string,
    get_header_request,
    get_microservice_base_url,
    place_request
    )
from data_mass.menus.order_menu import print_allow_cancellable_order_menu
from data_mass.product.products import (
    get_sku_name,
    request_get_offers_microservice
    )
from data_mass.rewards.rewards_programs import (
    get_all_programs,
    get_DM_rewards_program_for_zone,
    get_specific_program
    )
from data_mass.rewards.rewards_utils import (
    get_dt_combos_from_zone,
    get_rewards_combos_by_account,
    make_account_eligible,
    post_combo_relay_account,
    post_orders_rewards,
    print_input_combo_qty,
    print_input_decision
    )

APP_B2B = "b2b"
APP_ADMIN = "membership"
CPU_COUNT = cpu_count() // 2


# Enroll POC to a zone's reward program
def enroll_poc_to_program(account_id, zone, environment, account_info):

    enroll_response = put_rewards(account_id, zone, environment)

    if enroll_response.status_code == 406:

        response_all_programs = get_all_programs(
            zone, environment, {"DEFAULT"}
        )
        if response_all_programs is None:
            return None

        # Verify if the zone already have a reward program created
        DM_program = get_DM_rewards_program_for_zone(
            loads(response_all_programs.text)
        )

        if DM_program is not None:

            # Getting account information to check eligibility
            # for DM Rewards program
            seg_account = account_info[0]["segment"]
            subseg_account = account_info[0]["subSegment"]
            potential_account = account_info[0]["potential"]

            if (
                seg_account != "DM-SEG"
                or subseg_account != "DM-SUBSEG"
                or potential_account != "DM-POTENT"
            ):
                turn_eligible = print_input_decision(
                    "Do you want to make the account eligible now"
                )

                if turn_eligible == "Y":
                    is_account_eligible = make_account_eligible(
                        account_info, zone, environment
                    )

                    if is_account_eligible:
                        print(
                            text.Green
                            + f'\n- [Rewards] The account "{account_id}" '
                            'is now eligible. Back to menu option '
                            '"Enroll POC" to resume the enrollment process'
                        )

    return enroll_response


# Disenroll a POC from the rewards program
def disenroll_poc_from_program(account_id, zone, environment):

    # Define headers
    request_headers = get_header_request(
        zone,
        True,
        False,
        False,
        False,
        account_id,
        APP_ADMIN + "-" + zone.lower(),
    )

    # Define url request
    request_url = (
        get_microservice_base_url(environment, False)
        + "/rewards-service/rewards/"
        + account_id
    )

    response = place_request("DELETE", request_url, "", request_headers)

    if response.status_code == 204:
        print(
            text.Green
            + f'\n- [Rewards] The account "{account_id}" was successfully '
            'disenrolled from the Rewards program.'
        )

    elif response.status_code == 404:
        print(
            text.Red
            + f'\n- [Rewards] The account "{account_id}" is not enrolled to '
            'a Rewards program.'
        )

    else:
        print(
            text.Red
            + '\n- [Rewards] Failure when disenrolling the account '
            f'"{account_id}" from rewards program.'
            f'\n- Response Status: "{str(response.status_code)}". '
            f'\n- Response message "{response.text}".'
        )

    return response


# Add Redeem products to account
def associate_dt_combos_to_poc(account_id, zone, environment):

    # Get the reward information for the account
    reward_response = get_rewards(account_id, zone, environment)

    if reward_response is None:
        return None

    json_reward_response = loads(reward_response.text)

    program_id = json_reward_response["programId"]

    print(
        text.Yellow
        + f'\n- [Rewards] The account "{account_id}" is enrolled to '
        f'the rewards program "{program_id}".'
    )

    # Get the account's rewards program information
    response_program = get_specific_program(
        program_id, zone, environment, {"COMBOS"}
    )

    if response_program is None:
        print(
            text.Red
            + '- Please use the menu option "Unenroll a POC from a program" '
            'to disenroll this account and the option '
            '"Enroll POC to a program" to enroll this account to an '
            'existing rewards program.'
        )
        return None

    # Getting the DT combos configured in the rewards program
    json_program_combos = loads(response_program.text)
    program_dt_combos = json_program_combos["combos"]

    if len(program_dt_combos) == 0:
        print(
            text.Red
            + '\n- [Rewards] There are no combos configured '
            f'for rewards program "{program_id}".'
        )
        return None

    # Get all the DT combos of the specified zone
    response_combos_from_zone = get_dt_combos_from_zone(zone, environment)

    if response_combos_from_zone is None:
        return None

    # Get all the combos that exists on the specified zone
    json_combos_from_zone = loads(response_combos_from_zone.text)
    zone_dt_combos = json_combos_from_zone["combos"]

    # Get a SKU to be used on FreeGood's list below
    response_product_offers = request_get_offers_microservice(
        account_id, zone, environment
    )

    if response_product_offers == "not_found":
        print(
            text.Red
            + '\n- [Catalog Service] There are no products '
            f'associated with the account "{account_id}"'
        )
        return None
    elif not response_product_offers:
        return None

    # Define the list of FreeGoods for the main payload
    index_offers = randint(0, (len(response_product_offers) - 1))
    sku = response_product_offers[index_offers]["sku"]

    dt_combos_to_associate = match_dt_combos_to_associate(
        program_dt_combos, zone_dt_combos
    )
    if len(dt_combos_to_associate) == 0:
        return None

    associate_matched_combos = print_input_decision(
        "Do you want to associate the matched DT combos to the POC"
    )

    if associate_matched_combos == "Y":
        dt_combos_qty = print_input_combo_qty(
            "Number of DT combos to associate", len(dt_combos_to_associate)
        )
        dt_combos_to_associate = dt_combos_to_associate[0:dt_combos_qty]

        print(
            text.Yellow + "\n- Associating matched DT combos, please wait..."
        )

        return post_combo_relay_account(
            zone, environment, account_id, dt_combos_to_associate, sku
        )

    else:
        return None


def match_dt_combos_to_associate(program_dt_combos, zone_dt_combos):

    print(
        text.Yellow
        + f'\n- Found "{str(len(program_dt_combos))}" DT '
        'combos configured for the program.'
    )

    print(
        text.Yellow
        + f'\n- Found "{str(len(zone_dt_combos))}" DT combos '
        'configured for the zone.'
    )

    # Verify which combos of the zone matchs with the ones
    # added to the rewards program
    dt_combos_matched = list()
    for program_dt_combo in program_dt_combos:
        for zone_dt_combo in zone_dt_combos:
            if zone_dt_combo["id"] == program_dt_combo["comboId"]:
                dt_combos_matched.append(zone_dt_combo)
                break

    print(
        text.Yellow
        + f'\n- Found "{str(len(dt_combos_matched))}" DT combos matching '
        'the program and the zone configuration.'
    )

    return dt_combos_matched


# Displays the SKU's for rewards shopping
def display_program_rules_skus(zone, environment, abi_id):

    reward_response = get_rewards(abi_id, zone, environment)

    if reward_response is not None:
        json_reward_response = loads(reward_response.text)

        program_id = json_reward_response["programId"]
        program_response = get_specific_program(
            program_id, zone, environment, {"RULES"}
        )

        if program_response is not None:
            json_program_response = loads(program_response.text)

            print(
                text.Yellow
                + '\nProgram ID: "{}" | Program Name: "{}"'.format(
                    json_program_response["id"], json_program_response["name"]
                )
            )

            program_rules_skus = dict()

            for rule in json_program_response["rules"]:
                print(
                    text.Yellow + "\nRule name: ",
                    rule["moneySpentSkuRule"]["name"],
                )
                print(
                    text.Yellow
                    + "Earn {} points per {} spent".format(
                        str(rule["moneySpentSkuRule"]["points"]),
                        str(rule["moneySpentSkuRule"]["amountSpent"]),
                    )
                )

                for sku in rule["moneySpentSkuRule"]["skus"]:
                    sku_name = get_sku_name(zone, environment, sku)
                    program_rules_skus.setdefault("SKU ID", []).append(sku)
                    program_rules_skus.setdefault("SKU name", []).append(
                        sku_name
                    )

                print(
                    text.default_text_color
                    + tabulate(
                        program_rules_skus, headers="keys", tablefmt="grid"
                    )
                )


def get_rewards(account_id, zone, environment):
    header_request = get_header_request(
        zone, True, False, False, False, account_id, APP_B2B
    )

    request_url = (
        get_microservice_base_url(environment, False)
        + "/loyalty-business-service/rewards/"
        + account_id
    )

    response = place_request("GET", request_url, "", header_request)

    if response.status_code == 200:
        return response
    elif response.status_code == 404 or response.status_code == 406:
        print(
            text.Red
            + f'\n- [Rewards] The account "{account_id}" is not enrolled '
            'to any rewards program. \n- Please use the menu option '
            '"Enroll POC to a program" to enroll this account '
            'to a rewards program.'
        )
    else:
        print(
            text.Red
            + '\n- [Rewards] Failure when getting enrollment information '
            f'for account "{account_id}". '
            f'\n- Response Status: "{str(response.status_code)}". '
            f'\n- Response message "{response.text}".'
        )

    return None


def put_rewards(account_id, zone, environment):
    # Define headers
    request_headers = get_header_request(
        zone, True, False, False, False, account_id, APP_B2B
    )

    # Define url request
    request_url = (
        get_microservice_base_url(environment, False)
        + "/loyalty-business-service/rewards"
    )

    # Create request body
    dict_values = {"accountId": account_id}

    request_body = convert_json_to_string(dict_values)

    response = place_request(
        "POST", request_url, request_body, request_headers
    )

    if response.status_code == 201:
        json_data = loads(response.text)
        program_id = json_data["programId"]

        print(
            text.Green
            + f'\n- [Rewards] The account "{account_id}" has been '
            f'successfully enrolled to the Rewards program "{program_id}".'
        )

    elif response.status_code == 409:
        print(
            text.Red
            + f'\n- [Rewards] The account "{account_id}" '
            'is already enrolled to a Rewards program.'
        )

    elif response.status_code == 406:
        print(
            text.Red
            + f'\n- [Rewards] The account "{account_id}" is not '
            'eligible to a Rewards program.'
        )

    else:
        print(
            text.Red
            + '\n- [Rewards] Failure when enrolling the account '
            f'"{account_id}" to a rewards program.'
            f'\n- Response Status: "{str(response.status_code)}".'
            f'\n- Response message "{response.text}".'
        )

    return response


def flow_create_order_rewards(
    zone: str,
    environment: str,
    account: list,
    item_list: list,
    order_status: str,
    delivery_date: str,
    quantity_orders: int = 1,
):
    if order_status == "PLACED":
        allow_order_cancel = print_allow_cancellable_order_menu()
    else:
        allow_order_cancel = "N"

    # get payment method as the account permits
    pay_method = choice(account[0]["paymentMethods"])

    # TODO: DTcombos associated to the poc
    get_combos = get_rewards_combos_by_account(
        account_id=account[0]['accountId'],
        zone=zone,
        environment=environment
    )
    if not get_combos:
        return []

    dt_combos = loads(get_combos.text).get('combos', [])
    combos = [
        {
            "comboId": dt_combo["id"],
            "quantity": dt_combo["redeemLimit"]
         }
        for dt_combo in dt_combos
    ]

    # TODO: multiprocess verificar
    pool_orders = Pool(CPU_COUNT)
    orders = pool_orders.apply_async(
        post_orders_rewards(
            zone=zone,
            environment=environment,
            account=account,
            item_list=item_list,
            dt_combos=combos if combos else [],
            pay_method=pay_method,
            order_status=order_status,
            allow_order_cancel=allow_order_cancel,
            delivery_date=delivery_date
        ),
        range(quantity_orders),
    )
    if orders:
        return orders.get()
    return []
