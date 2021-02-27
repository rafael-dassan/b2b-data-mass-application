# Standard library imports
import json
from json import loads
import os
from datetime import timedelta, datetime
from time import time

# Third party imports
from tabulate import tabulate

# Local application imports
from common import get_header_request, get_microservice_base_url, place_request, update_value_to_json, \
    convert_json_to_string, create_list
from products import request_get_products_microservice
from classes.text import text
from validations import validate_yes_no_option


def generate_id():
    # Generates an sequential number based on Epoch time using seconds and the first two chars milliseconds
    # time() return an Epoch time with milliseconds separeted with a dot (.)

    parsed_time = str(time()).replace('.', '')
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


# Get the DT Combos for the specified zone from Combos MS
def get_dt_combos_from_zone(zone, environment, page_size=9999):
    
    header_request = get_header_request(zone, 'true', 'false', 'false', 'false')
    
    # Define url request
    request_url = get_microservice_base_url(environment) + '/combos/?types=DT&includeDeleted=false&includeDisabled=false&page=0&pageSize=' + str(page_size)
    
    # Send request
    response = place_request('GET', request_url, '', header_request)

    if response.status_code == 200:
        return response
    elif response.status_code == 404:
        print(text.Red + '\n- [Combo Service] There are no DT combos registered. \n- Response Status: "{}". \n- Response message "{}".'
                .format(str(response.status_code), response.text))
    else:
        print(text.Red + '\n- [Combo Service] Failure to retrieve DT combos. \n- Response Status: "{}". \n- Response message "{}".'
                .format(str(response.status_code), response.text))
    
    return None


def get_rewards_combos_by_account(account_id, zone, environment):
    header_request = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

    request_url = get_microservice_base_url(environment, 'false') + '/loyalty-business-service/programs/accounts/' + account_id + '/combos'

    response = place_request('GET', request_url, '', header_request)

    if response.status_code == 200:
        json_data = loads(response.text)
        if len(json_data['combos']) > 0:
            return response
        else:
            print(text.Red + '\n- [Rewards] There are no DT combos available for the account "{}". \n- Please use the menu option "" to associate DT combos to this account.'
                .format(account_id))    
    elif response.status_code == 404:
        print(text.Red + '\n- [Rewards] The account "{}" is not enrolled to any rewards program. \n- Please use the menu option "Enroll POC to a program" to enroll this account to a rewards program.'
            .format(account_id))
    else:
        print(text.Red + '\n- [Rewards] Failure when getting DT combos for account "{}". \n- Response Status: "{}". \n- Response message "{}".'
                .format(account_id, str(response.status_code), response.text))
    
    return None
    

def post_combo_relay_account(zone, environment, account_id, dt_combos_to_associate, sku):
    # Define headers to post the association
    request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

    # Define url request to post the association
    request_url = get_microservice_base_url(environment) + '/combo-relay/accounts'

    # Define the list of Limits for the main payload 
    dict_values_limit  = {
        'daily': 200,
        'monthly': 200,
    }

    # Define the list of ConsumedLimits for the main payload 
    dict_values_consumed_limit = {
        "daily": 0,
        "monthly": 0
    }

    dict_values_freegoods  = {
        'quantity': 5,
        'skus': create_list(sku),
    }

    # Define the entire list of Combos for the main payload
    i = 0
    combos_list = list()
    while i < len(dt_combos_to_associate):

        dict_values_combos  = {
            'id': dt_combos_to_associate[i]['id'],
            'externalId': dt_combos_to_associate[i]['id'],
            'title': dt_combos_to_associate[i]['title'],
            'description': dt_combos_to_associate[i]['description'],
            'startDate': dt_combos_to_associate[i]['startDate'],
            'endDate': dt_combos_to_associate[i]['endDate'],
            'type': 'DT',
            'image': 'https://test-conv-micerveceria.abi-sandbox.net/media/catalog/product/c/o/combo-icon_11.png',
            'items': None,
            'freeGoods': dict_values_freegoods,
            'limit': dict_values_limit,
            'consumedLimit': dict_values_consumed_limit,
            'originalPrice': 0,
            'price': 0,
            'discountPercentOff': 0,
            'score': 0,
        }

        combos_list.append(dict_values_combos)
        i += 1

    # Creates the main payload based on the lists created above
    dict_values_account = {
        'accounts': create_list(account_id),
        'combos': combos_list
    }

    #Create body to associate the combos to account
    request_body = convert_json_to_string(dict_values_account)

    # Send request to associate the combos to account
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 201:
        print(text.Green + '\n- [Combo Relay Service] Total of "{}" DT combos associated successfully to account "{}".'
            .format(str(len(dt_combos_to_associate)), account_id))
    else:
        print(text.Red + '\n- [Combo Relay Service] Failure when associating DT combos to the account. \n- Response Status: "{}". \n- Response message: "{}"'
            .format(str(response.status_code), response.text))

    return response


# Generates the SKU list available for a zone
def create_product_list_from_zone(zone, environment):
    response_products = request_get_products_microservice(zone, environment)

    sku_list = list()

    if response_products != 'false':
        for product in response_products:
            sku_list.append(product['sku'])

    return sku_list


# Displays all programs information
def display_all_programs_info(list_all_programs, show_initial_balance=False, show_redeem_limit=False):
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


# Displays all challenges information
def display_all_challenges_info(list_all_challenges):
    all_challenges_dictionary = dict()
    
    print(text.Yellow + '\nExisting challenges:')
    for challenge in list_all_challenges:
        all_challenges_dictionary.setdefault('Challenge ID', []).append(challenge['id'])
        all_challenges_dictionary.setdefault('Title', []).append(challenge['title'])
        all_challenges_dictionary.setdefault('Execution Method', []).append(challenge['executionMethod'])
        all_challenges_dictionary.setdefault('Points', []).append(challenge['points'])
        all_challenges_dictionary.setdefault('Start Date', []).append(challenge['startDate'])
        all_challenges_dictionary.setdefault('End Date', []).append(challenge['endDate'])

    print(text.default_text_color + tabulate(all_challenges_dictionary, headers='keys', tablefmt='grid'))


def print_make_account_eligible():
    option = input(text.Yellow + '\n- Do you want to make the account eligible now? y/N: ')

    while validate_yes_no_option(option.upper()) is False:
        print(text.Red + '\n- Invalid option\n')
        option = input(text.Yellow + '\n- Do you want to make the account eligible now: ')
    
    return option.upper()


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


def build_request_url_with_projection_query(request_url, projections):
    if len(projections) > 0:
        i = 0
        for projection in projections:
            if i == 0:
                projection_query = '?projection=' + str(projection).upper()
            else:
                projection_query += '&projection=' + str(projection).upper()
            i += 1
        request_url += projection_query
    
    return request_url