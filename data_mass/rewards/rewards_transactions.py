# Standard library imports
import json
from json import loads
import os
from random import randint

# Local application imports
from data_mass.tools.prompt import print_input_number
from data_mass.tools.requests import (
    get_header_request,
    get_microservice_base_url,
    place_request
)
from data_mass.tools.utils import convert_json_to_string
from data_mass.classes.text import text
from data_mass.rewards.rewards_utils import get_rewards_combos_by_account

APP_ADMIN = 'membership'

# Create REDEMPTION transaction for an account
def create_redemption(account_id, zone, environment):

    rewards_combos_response = get_rewards_combos_by_account(account_id, zone, environment)

    if rewards_combos_response is None: return None

    json_rewards_combos = loads(rewards_combos_response.text)
    
    comboId = json_rewards_combos['combos'][0]['id']
    order_id = 'DM-' + account_id + str(randint(100,900))

    dict_redemption = {
        "combos": [
            {
                "comboId": comboId,
                "quantity": 1
            }
        ],
        "orderId": order_id
    }

    request_body_redemption = convert_json_to_string(dict_redemption)

    return post_redemption(account_id, zone, environment, request_body_redemption)


# Create REWARDS_OFFER transaction for an account
def create_rewards_offer(account_id, zone, environment):

    points_amount = print_input_number('\nPlease inform the points amount (greater than zero)')

    while int(points_amount) <= 0:
        print(text.Red + '\nInvalid value!! Must be greater than zero!!')
        points_amount = print_input_number('\nPlease inform the new balance amount (greater than zero)')
    
    dict_rewards_offer = {
        'points': int(points_amount),
        'campaignId': 'DM-' + str(randint(100,900)),
        'description': 'DM-Bonus for customers signing up to Rewards Program'
    }

    request_body_rewards_offer = convert_json_to_string(dict_rewards_offer)

    return post_rewards_offer(account_id, zone, environment, request_body_rewards_offer)


# Create POINTS_REMOVAL transaction for an account
def create_points_removal(account_id, zone, environment):

    points_amount = print_input_number('\nPlease inform the points amount (greater than zero)')

    while int(points_amount) <= 0:
        print(text.Red + '\nInvalid value!! Must be greater than zero!!')
        new_balance = print_input_number('\nPlease inform the new balance amount (greater than zero)')
    
    dict_points_removal = {
        'points': int(points_amount),
        'description': 'DM Transaction to remove the balance from a POC.'
    }

    request_body_points_removal = convert_json_to_string(dict_points_removal)

    return post_points_removal(account_id, zone, environment, request_body_points_removal)


def post_rewards_offer(account_id, zone, environment, request_body):
    # Define headers
    request_headers = get_header_request(zone, True, False, False, False, account_id, APP_ADMIN + '-' + zone.lower())

    # Define url request
    request_url = get_microservice_base_url(environment, False) + '/rewards-service/rewards/' + account_id + '/transaction/rewards-offer'

    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 201:
        print(text.Green + '\n- [Rewards] The REWARDS_OFFER transaction was successfully created for the account "{}".'
                .format(account_id))
    elif response.status_code == 404:
        print(text.Red + '\n- [Rewards] The account "{}" is not enrolled to any rewards program. \n- Please use the menu option "Enroll POC to a program" to enroll this account to a rewards program.'
            .format(account_id))
    else:
        print(text.Red + '\n- [Rewards] Failure when creating a REWARDS_OFFER transaction for account "{}". \n- Response Status: "{}". \n- Response message "{}".'
                .format(account_id, str(response.status_code), response.text))
    
    return response


def post_redemption(account_id, zone, environment, request_body):
    # Define headers
    request_headers = get_header_request(zone, True, False, False, False, account_id, APP_ADMIN + '-' + zone.lower())

    # Define url request
    request_url = get_microservice_base_url(environment, False) + '/rewards-service/rewards/' + account_id + '/transaction/redemption'

    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 201:
        print(text.Green + '\n- [Rewards] The REDEMPTION transaction was successfully created for the account "{}".'
                .format(account_id))
    elif response.status_code == 404:
        print(text.Red + '\n- [Rewards] The account "{}" is not enrolled to any rewards program. \n- Please use the menu option "Enroll POC to a program" to enroll this account to a rewards program.'
            .format(account_id))
    else:
        print(text.Red + '\n- [Rewards] Failure when creating a REDEMPTION transaction for account "{}". \n- Response Status: "{}". \n- Response message "{}".'
                .format(account_id, str(response.status_code), response.text))
    
    return response


def post_points_removal(account_id, zone, environment, request_body):
    # Define headers
    request_headers = get_header_request(zone, True, False, False, False, account_id, APP_ADMIN + '-' + zone.lower())

    # Define url request
    request_url = get_microservice_base_url(environment, False) + '/rewards-service/rewards/' + account_id + '/transaction/points-removal'

    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 201:
        print(text.Green + '\n- [Rewards] The POINTS_REMOVAL transaction was successfully created for the account "{}".'
                .format(account_id))
    elif response.status_code == 404:
        print(text.Red + '\n- [Rewards] The account "{}" is not enrolled to any rewards program. \n- Please use the menu option "Enroll POC to a program" to enroll this account to a rewards program.'
            .format(account_id))
    else:
        print(text.Red + '\n- [Rewards] Failure when creating a POINTS_REMOVAL transaction for account "{}". \n- Response Status: "{}". \n- Response message "{}".'
                .format(account_id, str(response.status_code), response.text))
    
    return response