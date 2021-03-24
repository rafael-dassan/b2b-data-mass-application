# Standard library imports
import json
from json import loads
import os
from random import randint

# Third party imports
from tabulate import tabulate

# Local application imports
from ..common import get_header_request, get_microservice_base_url, convert_json_to_string, place_request, print_input_number
from ..products import request_get_offers_microservice, get_sku_name
from ..classes.text import text
from ..rewards.rewards_programs import get_all_programs, get_specific_program, get_DM_rewards_program_for_zone
from ..rewards.rewards_utils import print_input_decision, make_account_eligible, get_dt_combos_from_zone, \
    post_combo_relay_account, print_input_combo_qty

APP_B2B = 'b2b'
APP_ADMIN = 'membership'

# Enroll POC to a zone's reward program
def enroll_poc_to_program(account_id, zone, environment, account_info):

    enroll_response = put_rewards(account_id, zone, environment)

    if enroll_response.status_code == 406:

        response_all_programs = get_all_programs(zone, environment, set(["DEFAULT"]))
        if response_all_programs is None:
            return None
    
        # Verify if the zone already have a reward program created
        DM_program = get_DM_rewards_program_for_zone(loads(response_all_programs.text))

        if DM_program is not None:

            # Getting account information to check eligibility for DM Rewards program
            seg_account = account_info[0]['segment']
            subseg_account = account_info[0]['subSegment']
            potential_account = account_info[0]['potential']

            if seg_account != 'DM-SEG' or subseg_account != 'DM-SUBSEG' or potential_account != 'DM-POTENT':
                turn_eligible = print_input_decision('Do you want to make the account eligible now')

                if turn_eligible == 'Y':
                    is_account_eligible = make_account_eligible(account_info, zone, environment)

                    if is_account_eligible:
                        print(text.Green + '\n- [Rewards] The account "{}" is now eligible. Back to menu option "Enroll POC" to resume the enrollment process'
                                .format(account_id))
    
    return enroll_response
           

# Disenroll a POC from the rewards program
def disenroll_poc_from_program(account_id, zone, environment):

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id, APP_ADMIN + '-' + zone.lower())

    # Define url request
    request_url = get_microservice_base_url(environment, 'false') + '/rewards-service/rewards/' + account_id

    response = place_request('DELETE', request_url, '', request_headers)

    if response.status_code == 204:
        print(text.Green + '\n- [Rewards] The account "{}" was successfully disenrolled from the Rewards program.'.format(account_id))

    elif response.status_code == 404:
        print(text.Red + '\n- [Rewards] The account "{}" is not enrolled to a Rewards program.'.format(account_id))

    else:
        print(text.Red + '\n- [Rewards] Failure when disenrolling the account "{}" from rewards program.  \n- Response Status: "{}". \n- Response message "{}".'
                .format(account_id, str(response.status_code), response.text))

    return response    


# Add Redeem products to account
def associate_dt_combos_to_poc(account_id, zone, environment):

    # Get the reward information for the account
    reward_response = get_rewards(account_id, zone, environment)
    
    if reward_response is None: return None 

    json_reward_response = loads(reward_response.text)

    program_id = json_reward_response['programId']

    print(text.Yellow + '\n- [Rewards] The account "{}" is enrolled to the rewards program "{}".'
            .format(account_id, program_id))
    
    # Get the account's rewards program information
    response_program = get_specific_program(program_id, zone, environment, set(["COMBOS"]))

    if response_program is None:
        print(text.Red + '- Please use the menu option "Unenroll a POC from a program" to disenroll this account and the option "Enroll POC to a program" to enroll this account to an existing rewards program.')
        return None
            
    # Getting the DT combos configured in the rewards program
    json_program_combos = loads(response_program.text)
    program_dt_combos = json_program_combos['combos']

    if len(program_dt_combos) == 0:
        print(text.Red + '\n- [Rewards] There are no combos configured for rewards program "{}".'.format(program_id))
        return None

    # Get all the DT combos of the specified zone
    response_combos_from_zone = get_dt_combos_from_zone(zone, environment)

    if response_combos_from_zone is None: return None

    # Get all the combos that exists on the specified zone
    json_combos_from_zone = loads(response_combos_from_zone.text)
    zone_dt_combos = json_combos_from_zone['combos']

    # Get a SKU to be used on FreeGood's list below
    response_product_offers = request_get_offers_microservice(account_id, zone, environment)
    
    if response_product_offers == 'not_found':
        print(text.Red + '\n- [Catalog Service] There are no products associated with the account "{}"'.format(account_id))
        return None
    elif response_product_offers == 'false': return None

    # Define the list of FreeGoods for the main payload 
    index_offers = randint(0, (len(response_product_offers) - 1))
    sku = response_product_offers[index_offers]['sku']
    
    dt_combos_to_associate = match_dt_combos_to_associate(program_dt_combos, zone_dt_combos)
    if len(dt_combos_to_associate) == 0:
        return None

    associate_matched_combos = print_input_decision('Do you want to associate the matched DT combos to the POC')
    
    if associate_matched_combos == 'Y':
        dt_combos_qty = print_input_combo_qty('Number of DT combos to associate', len(dt_combos_to_associate))
        dt_combos_to_associate = dt_combos_to_associate[0:dt_combos_qty]

        print(text.Yellow + '\n- Associating matched DT combos, please wait...')
        
        return post_combo_relay_account(zone, environment, account_id, dt_combos_to_associate, sku)

    else:
        return None


def match_dt_combos_to_associate(program_dt_combos, zone_dt_combos):

    print(text.Yellow + '\n- Found "{}" DT combos configured for the program.'.format(str(len(program_dt_combos))))

    print(text.Yellow + '\n- Found "{}" DT combos configured for the zone.'.format(str(len(zone_dt_combos))))

    # Verify which combos of the zone matchs with the ones added to the rewards program
    dt_combos_matched = list()
    for program_dt_combo in program_dt_combos:
        for zone_dt_combo in zone_dt_combos:
            if zone_dt_combo['id'] == program_dt_combo['comboId']:
                dt_combos_matched.append(zone_dt_combo)
                break

    print(text.Yellow + '\n- Found "{}" DT combos matching the program and the zone configuration.'.format(str(len(dt_combos_matched))))

    return dt_combos_matched


# Displays the SKU's for rewards shopping
def display_program_rules_skus(zone, environment, abi_id):

    reward_response = get_rewards(abi_id, zone, environment)

    if reward_response is not None:
        json_reward_response = loads(reward_response.text)

        program_id = json_reward_response['programId']
        program_response = get_specific_program(program_id, zone, environment, set(["RULES"]))

        if program_response is not None:
            json_program_response = loads(program_response.text)

            print(text.Yellow + '\nProgram ID: "{}" | Program Name: "{}"'
                    .format(json_program_response['id'], json_program_response['name']))

            program_rules_skus = dict()

            for rule in json_program_response['rules']:
                print(text.Yellow + "\nRule name: ", rule['moneySpentSkuRule']['name'])
                print(text.Yellow + "Earn {} points per {} spent"
                    .format(str(rule['moneySpentSkuRule']['points']), str(rule['moneySpentSkuRule']['amountSpent'])))
                
                for sku in rule['moneySpentSkuRule']['skus']:
                    sku_name = get_sku_name(zone, environment, sku)
                    program_rules_skus.setdefault('SKU ID', []).append(sku)
                    program_rules_skus.setdefault('SKU name', []).append(sku_name)

                print(text.default_text_color + tabulate(program_rules_skus, headers='keys', tablefmt='grid'))


def get_rewards(account_id, zone, environment):
    header_request = get_header_request(zone, 'true', 'false', 'false', 'false', account_id, APP_B2B)

    request_url = get_microservice_base_url(environment, 'false') + '/loyalty-business-service/rewards/' + account_id

    response = place_request('GET', request_url, '', header_request)

    if response.status_code == 200:
        return response
    elif response.status_code == 404 or response.status_code == 406:
        print(text.Red + '\n- [Rewards] The account "{}" is not enrolled to any rewards program. \n- Please use the menu option "Enroll POC to a program" to enroll this account to a rewards program.'
            .format(account_id))
    else:
        print(text.Red + '\n- [Rewards] Failure when getting enrollment information for account "{}". \n- Response Status: "{}". \n- Response message "{}".'
                .format(account_id, str(response.status_code), response.text))
    
    return None


def put_rewards(account_id, zone, environment):
    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id, APP_B2B)

    # Define url request
    request_url = get_microservice_base_url(environment, 'false') + '/loyalty-business-service/rewards'

    # Create request body
    dict_values  = {
        'accountId' : account_id
    }

    request_body = convert_json_to_string(dict_values)

    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 201:
        json_data = loads(response.text)
        program_id = json_data['programId']
        
        print(text.Green + '\n- [Rewards] The account "{}" has been successfully enrolled to the Rewards program "{}".'
                .format(account_id, program_id))

    elif response.status_code == 409:
        print(text.Red + '\n- [Rewards] The account "{}" is already enrolled to a Rewards program.'.format(account_id))

    elif response.status_code == 406:
        print(text.Red + '\n- [Rewards] The account "{}" is not eligible to a Rewards program.'.format(account_id))

    else:
        print(text.Red + '\n- [Rewards] Failure when enrolling the account "{}" to a rewards program.  \n- Response Status: "{}". \n- Response message "{}".'
                .format(account_id, str(response.status_code), response.text))

    return response