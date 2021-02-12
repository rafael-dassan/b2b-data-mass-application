# Standard library imports
import json
from json import loads
import os
from random import randint
from datetime import timedelta, datetime
from time import time

# Third party imports
from tabulate import tabulate

# Local application imports
from common import get_header_request, get_microservice_base_url, place_request, update_value_to_json, convert_json_to_string
from classes.text import text


def generate_id():
    # Generates an sequential number based on Epoch time using seconds and the first two chars milliseconds
    # time() return an Epoch time with milliseconds separeted with a dot (.)

    parsed_time = str(time()).replace('.', '')
    epoch_id = parsed_time[:11]

    return epoch_id


# Retrieve Digital Trade combos (DT Combos) for the specified zone
def get_dt_combos_from_zone(zone, environment):
    
    header_request = get_header_request(zone, 'true', 'false', 'false', 'false')
    
    # Define url request
    request_url = get_microservice_base_url(environment) + '/combos/?types=DT&includeDeleted=false&includeDisabled=false'
    
    # Send request
    response = place_request('GET', request_url, '', header_request)
    if response.status_code == 200:
        return loads(response.text)
    elif response.status_code == 404:
        print(text.Red + '\n- [Combo Service] There is no combo type digital trade registered. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'
    else:
        print(text.Red + '\n- [Combo Service] Failure to retrieve combo type digital trade. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def get_id_rewards(abi_id, header_request, environment):
    request_url = get_microservice_base_url(environment,'true') + '/rewards-service/rewards/' + abi_id
    response = place_request('GET', request_url, '', header_request)
    if response.status_code == 200:
        return loads(response.text).get("programId")
    else:
        return 'false ' + str(response.status_code)


# Displays all programs information
def display_programs_info(list_all_programs, show_initial_balance=False, show_redeem_limit=False):
    all_programs_dictionary = dict()
    
    print(text.Yellow + '\nExisting Reward programs:')
    for program in list_all_programs:
        all_programs_dictionary.setdefault('Program ID', []).append(program['id'])
        all_programs_dictionary.setdefault('Program Name', []).append(program['name'])
        if show_initial_balance:
            all_programs_dictionary.setdefault('Current initial balance', []).append(program['initialBalance'])
        if show_redeem_limit:
            all_programs_dictionary.setdefault('Current redeem limit', []).append(program['redeemLimit'])

    print(text.default_text_color + tabulate(all_programs_dictionary, headers='keys', tablefmt='grid'))


# Make an account eligible to DM Rewards program
def make_account_eligible(account_info, zone, environment):

    # Get header request
    request_headers = get_header_request(zone, 'false', 'true', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/account-relay/'

    # Update the account's information with the right values to associate to a Reward program
    json_object = update_value_to_json(account_info, '[0][potential]', 'DM-POTENT')
    json_object = update_value_to_json(account_info, '[0][segment]', 'DM-SEG')
    json_object = update_value_to_json(account_info, '[0][subSegment]', 'DM-SUBSEG')

    # Create body
    request_body = convert_json_to_string(json_object)

    # Place request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return True
    else:
        return False