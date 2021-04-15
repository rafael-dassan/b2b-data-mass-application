import json
from random import randint
from requests import Response
from typing import Union

from tabulate import tabulate

# Local application imports
from data_mass.common import get_header_request, \
    get_microservice_base_url, convert_json_to_string, \
    place_request, print_input_number
from data_mass.product.products import request_get_offers_microservice, \
    get_sku_name
from data_mass.classes.text import text
from data_mass.rewards.programs import (
    get_all_programs,
    get_specific_program,
    get_DM_rewards_program_for_zone
)
from data_mass.rewards.utils import (
    print_input_decision,
    make_account_eligible,
    get_dt_combos_from_zone,
    post_combo_relay_account,
    print_input_combo_qty,
)

APP_B2B = 'b2b'
APP_ADMIN = 'membership'


def enroll_poc_to_program(
        account_id: str,
        zone: str,
        environment: str,
        account_info: str) -> Union[None, Response]:
    """
    Enroll POC to a zone's reward program.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str
    account_info : str

    Returns
    -------
    None or Response
        None when there's no program in the selected zone, \
        else, the http response.
    """
    enroll_response = put_rewards(
        account_id=account_id,
        zone=zone,
        environment=environment
    )

    if enroll_response.status_code == 406:
        response_all_programs = get_all_programs(
            zone=zone,
            environment=environment,
            projections=set(["DEFAULT"])
        )

        if response_all_programs is None:
            return None

        # Verify if the zone already have a reward program created
        zone_programs_list = json.loads(response_all_programs.text)
        dm_program = get_DM_rewards_program_for_zone(zone_programs_list)

        if dm_program is not None:
            # Getting account information to check
            # eligibility for DM Rewards program
            seg_account = account_info[0]['segment']
            subseg_account = account_info[0]['subSegment']
            potential_account = account_info[0]['potential']

            if (seg_account != 'DM-SEG' or
                    subseg_account != 'DM-SUBSEG' or
                    potential_account != 'DM-POTENT'):
                turn_eligible = print_input_decision(
                    'Do you want to make the account eligible now? '
                )

                if turn_eligible == 'Y':
                    is_account_eligible = make_account_eligible(
                        account_info=account_info,
                        zone=zone,
                        environment=environment
                    )

                    if is_account_eligible:
                        print((
                            f'{text.Green}\n'
                            f'- [Rewards] The account "{account_id}" '
                            'is now eligible. '
                            'Back to menu option "Enroll POC" '
                            'to resume the enrollment process'
                        ))

    return enroll_response


def disenroll_poc_from_program(
        account_id: str,
        zone: str,
        environment: str) -> Response:
    """
    Disenroll a POC from the rewards program.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str

    Returns
    -------
    Response
        The http response.
    """
    jwt_app_claim = f"{APP_ADMIN}-{zone.lower()}"
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        account_id=account_id,
        jwt_app_claim=jwt_app_claim
    )

    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/rewards-service/rewards/{account_id}"

    response = place_request(
        request_method="DELETE",
        request_url=request_url,
        request_body='',
        request_headers=request_headers
    )

    if response.status_code == 204:
        print((
            f'{text.Green}\n'
            f'- [Rewards] The account "{account_id}" was successfully '
            'disenrolled from the Rewards program.'
        ))

    elif response.status_code == 404:
        print((
            f'{text.Red}\n'
            f'- [Rewards] The account "{account_id}" is not '
            'enrolled to a Rewards program.'
        ))

    else:
        print((
            f'{text.Red}\n'
            '- [Rewards] Failure when disenrolling the account '
            f'"{account_id}" from rewards program.\n'
            f'- Response Status: "{response.status_code}".\n'
            f'- Response message "{response.text}".'
        ))

    return response


def associate_dt_combos_to_poc(
        account_id: str,
        zone: str,
        environment: str) -> Union[None, Response]:
    """
    Add Redeem products to account.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str

    Returns
    -------
    None or Response

    """
    reward_response = get_rewards(account_id, zone, environment)

    if reward_response is None:
        return None

    json_reward_response = json.loads(reward_response.text)
    program_id = json_reward_response['programId']

    print((
        f'{text.Yellow}\n'
        f'- [Rewards] The account "{account_id}" '
        f'is enrolled to the rewards program "{program_id}".'
    ))

    response_program = get_specific_program(
        program_id=program_id,
        zone=zone,
        environment=environment,
        projections=set(["COMBOS"])
    )

    if response_program is None:
        print((
            f'{text.Red}'
            '- Please use the menu option "Unenroll a POC from a program" '
            'to disenroll this account and the option '
            '"Enroll POC to a program" to enroll this '
            'account to an existing rewards program.'
        ))

        return None

    # Getting the DT combos configured in the rewards program
    json_program_combos = json.loads(response_program.text)
    program_dt_combos = json_program_combos['combos']

    if not program_dt_combos:
        print((
            f'{text.Red}\n'
            '- [Rewards] There are no combos configured '
            f'for rewards program "{program_id}".'
        ))

        return None

    response_combos_from_zone = get_dt_combos_from_zone(
        zone=zone,
        environment=environment
    )

    if response_combos_from_zone is None:
        return None

    json_combos_from_zone = json.loads(response_combos_from_zone.text)
    zone_dt_combos = json_combos_from_zone['combos']

    response_product_offers = request_get_offers_microservice(
        account_id=account_id,
        zone=zone,
        environment=environment
    )

    if response_product_offers == 'not_found':
        print((
            f'{text.Red}\n'
            '- [Catalog Service] There are no products '
            f'associated with the account "{account_id}"'
        ))
        return None
    elif not response_product_offers:
        return None

    # Define the list of FreeGoods for the main payload
    index_offers = randint(0, (len(response_product_offers) - 1))
    sku = response_product_offers[index_offers]['sku']

    dt_combos_to_associate = match_dt_combos_to_associate(
        program_dt_combos,
        zone_dt_combos
    )

    if not dt_combos_to_associate:
        return None

    associate_matched_combos = print_input_decision(
        "Do you want to associate the matched DT combos to the POC"
    )

    if associate_matched_combos == 'Y':
        dt_combos_qty = print_input_combo_qty(
            "Number of DT combos to associate",
            len(dt_combos_to_associate)
        )

        dt_combos_to_associate = dt_combos_to_associate[0:dt_combos_qty]

        print((
            f'{text.Yellow}\n'
            '- Associating matched DT combos, please wait...'
        ))

        return post_combo_relay_account(
            zone=zone,
            environment=environment,
            account_id=account_id,
            dt_combos_to_associate=dt_combos_to_associate,
            sku=sku
        )

    return None


def match_dt_combos_to_associate(
        program_dt_combos: list,
        zone_dt_combos: list) -> list:
    """
    Verify which combos of the zone matchs with \
    the ones added to the rewards program.

    Parameters
    ----------
    program_dt_combos : list
    zone_dt_combos : list

    Returns
    -------
    list
        Macthed combos list.
    """
    print((
        f"{text.Yellow}\n"
        f'- Found "{len(program_dt_combos)}" '
        'DT combos configured for the program.'
    ))
    print((
        f"{text.Yellow}\n"
        f'- Found "{len(zone_dt_combos)}" DT combos configured for the zone.'
    ))

    dt_combos_matched = []
    for program_dt_combo in program_dt_combos:
        for zone_dt_combo in zone_dt_combos:
            if zone_dt_combo['id'] == program_dt_combo['comboId']:
                dt_combos_matched.append(zone_dt_combo)
                break

    print((
        f'{text.Yellow}\n'
        f'- Found "{len(dt_combos_matched)}" '
        'DT combos matching the program and the zone configuration.'
    ))

    return dt_combos_matched


def display_program_rules_skus(zone: str, environment: str, abi_id: str):
    """
    Displays the SKU's for rewards shopping.

    Parameters
    ----------
    zone : str
    environment : str
    abi_id : str
    """
    reward_response = get_rewards(abi_id, zone, environment)

    if reward_response is not None:
        json_reward_response = json.loads(reward_response.text)
        program_id = json_reward_response['programId']

        program_response = get_specific_program(
            program_id=program_id,
            zone=zone,
            environment=environment,
            projections=set(["RULES"])
        )

        if program_response is not None:
            json_program_response = json.loads(program_response.text)
            p_response_id = json_program_response['id']
            p_response_response = json_program_response['name']

            print((
                f'{text.Yellow}\n'
                f'Program ID: "{p_response_id}" | '
                f'Program Name: "{p_response_response}"'
            ))

            program_rules_skus = dict()

            for rule in json_program_response['rules']:
                money_spent_name = rule['moneySpentSkuRule']['name']
                money_spent_points = rule['moneySpentSkuRule']['points']
                money_spent_amount = rule['moneySpentSkuRule']['amountSpent']

                print((
                    f'{text.Yellow}\n'
                    f'Rule name: {money_spent_name}'
                ))

                print((
                    f'{text.Yellow}'
                    f'Earn {money_spent_points} points '
                    f'per {money_spent_amount} spent.'
                ))

                for sku in rule['moneySpentSkuRule']['skus']:
                    sku_name = get_sku_name(zone, environment, sku)
                    program_rules_skus.setdefault(
                        'SKU ID',
                        []
                    ).append(sku)

                    program_rules_skus.setdefault(
                        'SKU name',
                        []
                    ).append(sku_name)

                tabulate_data = tabulate(
                    tabular_data=program_rules_skus,
                    headers="keys",
                    tablefmt="grid"
                )

                print(f"{text.default_text_color}{tabulate_data}")


def get_rewards(
        account_id: str,
        zone: str,
        environment: str) -> Union[None, Response]:
    """
    Get rewards from the microservices.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str

    Returns
    -------
    None or Response
        None when any http error accours, else, the http response.
    """
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        account_id=account_id,
        jwt_app_claim=APP_B2B
    )

    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/loyalty-business-service/rewards/{account_id}"

    response = place_request(
        request_method="GET",
        request_url=request_url,
        request_body="",
        request_headers=request_headers
    )

    if response.status_code == 200:
        return response
    elif response.status_code in [404, 406]:
        print((
            f'{text.Red}\n'
            f'- [Rewards] The account "{account_id}" is not enrolled '
            'to any rewards program.\n'
            '- Please use the menu option "Enroll POC to a program" '
            'to enroll this account to a rewards program.'
        ))
    else:
        print((
            f'{text.Red}\n'
            '- [Rewards] Failure when getting enrollment '
            f'information for account "{account_id}".\n'
            f'- Response Status: "{response.status_code}".\n'
            f'- Response message "{response.text}".'
        ))

    return None


def put_rewards(
        account_id: str,
        zone: str,
        environment: str) -> Response:
    """
    Create new rewards on the microservice.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str

    Returns
    -------
    Response
        The http response.
    """
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        account_id=account_id,
        jwt_app_claim=APP_B2B,
    )

    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/loyalty-business-service/rewards"

    dict_values = {"accountId": account_id}
    request_body = convert_json_to_string(dict_values)

    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 201:
        json_data = json.loads(response.text)
        program_id = json_data['programId']

        print((
            f'{text.Green}\n'
            f'- [Rewards] The account "{account_id}" has been successfully '
            f'enrolled to the Rewards program "{program_id}".'
        ))

    elif response.status_code == 409:
        print((
            f'{text.Red}\n'
            f'- [Rewards] The account "{account_id}" '
            'is already enrolled to a Rewards program.'
        ))

    elif response.status_code == 406:
        print((
            f'{text.Red}\n'
            f'- [Rewards] The account "{account_id}" '
            'is not eligible to a Rewards program.'
        ))

    else:
        print(text.Red + '\n- [Rewards] Failure when enrolling the account "{}" to a rewards program.  \n- Response Status: "{}". \n- Response message "{}".'
                .format(account_id, str(response.status_code), response.text))

    return response
