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
from common import get_header_request, get_microservice_base_url, update_value_to_json, convert_json_to_string, \
    place_request, create_list
from products import request_get_offers_microservice, get_sku_name
from classes.text import text
from rewards.rewards_programs import get_DM_program_for_zone, get_sku_rewards
from rewards.rewards_utils import get_id_rewards, make_account_eligible


# Enroll POC to a zone's reward program
def enroll_poc_to_program(account_id, zone, environment, account_info):

    enroll_response = put_rewards(account_id, zone, environment)

    json_data = loads(enroll_response.text)

    if enroll_response.status_code == 406:

        # Check if the zone has a DM reward program created
        DM_program = get_DM_program_for_zone(zone, environment)

        if DM_program != None:

            # Getting account information to check eligibility for DM Rewards program
            seg_account = account_info[0]['segment']
            subseg_account = account_info[0]['subSegment']
            potential_account = account_info[0]['potential']

            if seg_account != 'DM-SEG' or subseg_account != 'DM-SUBSEG' or potential_account != 'DM-POTENT':
                turn_eligible = input(text.Yellow + '\n- Do you want to make it eligible now? y/N: ')

                while turn_eligible.upper() != 'Y' and turn_eligible.upper() != 'N':
                    print(text.Red + '\n- Invalid option\n')
                    turn_eligible = input(text.Yellow + '\n- Do you want to make it eligible now? y/N: ')

                if turn_eligible.upper() == 'Y':
                    is_account_eligible = make_account_eligible(account_info, zone, environment)

                    if is_account_eligible:
                        print(text.Green + '\n- [Rewards] The account "{accountId}" is now eligible. Back to menu option "Enroll POC" to resume the enrollment process'
                                .format(accountId=account_id))
           

# Disenroll a POC from the rewards program
def delete_enroll_poc_to_program(account_id, zone, environment):

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

    # Define url request
    request_url = get_microservice_base_url(environment, 'false') + '/rewards-service/rewards/' + account_id

    response = place_request('DELETE', request_url, '', request_headers)

    if response.status_code == 204:
        print(text.Green + '\n- [Rewards] The account "{accountId}" was successfully disenrolled from the Rewards program.'.format(accountId=account_id))

    elif response.status_code == 404:
        print(text.Red + '\n- [Rewards] The account "{accountId}" is not enrolled to a Rewards program.'.format(accountId=account_id))

    else:
        print(text.Red + '\n- [Rewards] Failure when disenrolling the account "{accountId}" from rewards program.  \n- Response Status: "{statusCode}". \n- Response message "{message}".'
                .format(accountId=account_id, statusCode=str(response.status_code), message=response.text))

    return response    
    

# Input transactions to a account
def input_transactions_to_account(account_id, zone, environment):

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

    # Check if the zone already have a reward program created
    program_found = get_DM_program_for_zone(zone, environment)

    if program_found == 'false':
        return 'pgm_not_found'
    else:
         # Define url request
        request_url_offer = get_microservice_base_url(environment) + '/rewards-service/rewards/' + account_id + '/transaction/rewards-offer'
        request_url_redemption = get_microservice_base_url(environment) + '/rewards-service/rewards/' + account_id + '/transaction/redemption'

        body_offer = {
            "points": 1500,
            "campaignId": "BRZ8635",
            "description": "Bonus for customers signing up to Rewards Program from 5/1 to 31/1; Braze campaign ID BRZ8635"          
        }

        body_redemption = {
            "combos": [
                        {
                            "comboId": "DT_01",
                            "quantity": 5
                        }
                    ],
            "orderId": "546A456"
        }

        #Create bodys
        request_body_offer = convert_json_to_string(body_offer)
        request_body_redemption = convert_json_to_string(body_redemption)

        response_offer = place_request('POST', request_url_offer, request_body_offer, request_headers)
        response_redemption = place_request('POST', request_url_redemption, request_body_redemption, request_headers)

        if response_offer.status_code != 201:
             print(text.Red + '\n- [Rewards Service] Failure when input a offer transaction to account. Response Status: '
                            + str(response_offer.status_code) + '. Response message ' + response_offer.text)

        if response_redemption.status_code != 200:
             print(text.Red + '\n- [Rewards Service] Failure when input a redemption transaction to account. Response Status: '
                            + str(response_redemption.status_code) + '. Response message ' + response_redemption.text)   
        
        return 201 if response_offer.status_code == 201 and response_redemption.status_code == 200 else 'post_error'


# Add Redeem products to account
def input_redeem_products(account_id, zone, environment):

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

    # Get the reward information for the account
    reward_found = get_rewards(account_id, zone, environment)
    
    if reward_found != None:

        program_id = reward_found['programId']

        print(text.default_text_color + '\n- [Rewards] The account "' + account_id + '" is enrolled to the rewards program "' + program_id + '".')
        
        # Define url request to read the Rewards program of the zone
        request_url = get_microservice_base_url(environment, 'false') + '/rewards-service/programs/' + program_id + '?projection=COMBOS'

        # Send request
        response = place_request('GET', request_url, '', request_headers)

        if response.status_code == 200:
            
            json_program_combos = loads(response.text)

            # Getting the DT combos configured in the rewards program
            combos_dt_program = json_program_combos['combos']
            len_combos_program = len(combos_dt_program)
            
            print(text.default_text_color + '\n- Found "' + str(len_combos_program) + '" redeem products for rewards program "' + program_id + '".')

            if len_combos_program > 50:
                len_combos_program = 50

            # Get all the combo IDs that are added to the reward program
            i = 0
            combos_id_program = list()
            while i < len_combos_program:
                combos_id_program.append(combos_dt_program[i]['comboId'])
                i += 1

            # Define url request to get all the DT combos of the specified zone
            request_url = get_microservice_base_url(environment) + '/combos/?types=DT&comboIds=&includeDeleted=false&includeDisabled=false&page=0&pageSize=9999'

            # Send request
            response = place_request('GET', request_url, '', request_headers)
            json_combos = loads(response.text)
            
            combos_dt_zone = json_combos['combos']
            len_combos_zone = len(combos_dt_zone)

            print(text.default_text_color + '\n- Found "' + str(len_combos_zone) + '" redeem products for the zone "' + zone + '".')

            # Get all the combos that exists on the specified zone
            i = 0
            combos_zone = list()
            while i < len_combos_zone:
                combos_zone.append(combos_dt_zone[i])
                i += 1

            # Verify which combos of the zone matchs with the ones added to the rewards program
            x = 0
            y = 0
            combos_match = list()
            while x < len(combos_id_program):
                y = 0
                while y < len(combos_zone):
                    if combos_zone[y]['id'] == combos_id_program[x]:
                        combos_match.append(combos_zone[y])
                        break
                    y += 1
                x += 1

            len_combos_match = len(combos_match)

            print(text.default_text_color + '\n- Found "' + str(len_combos_match) + '" redeem products matching the program and the zone configuration.')

            # Get a SKU to be used on FreeGood's list below
            product_offers = request_get_offers_microservice(account_id, zone, environment)
            
            if product_offers == 'not_found':
                print(text.Red + '\n- [Catalog Service] There is no product associated with the account ' + account_id)
                return

            index_offers = randint(0, (len(product_offers) - 1))
            sku = product_offers[index_offers]['sku']

            # Define headers to post the association
            request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

            # Define url request to post the association
            request_url = get_microservice_base_url(environment) + '/combo-relay/accounts'

            # Define the list of Limits for the main payload 
            dict_values_limit  = {
                'daily': 200,
                'monthly': 200,
            }

            # Define the list of FreeGoods for the main payload 
            dict_values_freegoods  = {
                'quantity': 5,
                'skus': create_list(sku),
            }

            # Define the entire list of Combos for the main payload
            i = 0
            combos_list = list()
            while i < len_combos_match:

                dict_values_combos  = {
                    'id': combos_match[i]['id'],
                    'externalId': combos_match[i]['id'],
                    'title': combos_match[i]['title'],
                    'description': combos_match[i]['id'],
                    'startDate': combos_match[i]['startDate'],
                    'endDate': combos_match[i]['endDate'],
                    'updatedAt': combos_match[i]['updatedAt'],
                    'type': 'DT',
                    'image': 'https://test-conv-micerveceria.abi-sandbox.net/media/catalog/product/c/o/combo-icon_11.png',
                    'freeGoods': dict_values_freegoods,
                    'limit': dict_values_limit,
                    'originalPrice': 0,
                    'price': 0,
                    'score': 0,
                }

                combos_list.append(dict_values_combos)
                i += 1

            # Creates the main payload based on the lists created above
            dict_values_account = {
                'accounts': create_list(account_id),
                'combos': combos_list
            }

            print(text.default_text_color + '\n- Associating matched redeem products, please wait...')

            #Create body to associate the combos to account
            request_body = convert_json_to_string(dict_values_account)
    
            # Send request to associate the combos to account
            response = place_request('POST', request_url, request_body, request_headers)

            if response.status_code == 201:
                print(text.Green + '\n- [Combo Relay Service] Total of ' + str(i) + ' combos associated successfully to account "' + account_id + '".')
            else:
                print(text.Red + '\n- [Combo Relay Service] Failure when associating combos to the account. Response Status: '
                                        + str(response.status_code) + '. Response message: ' + response.text)

        else:
            print(text.Red + '\n- [Rewards] The program "' + program_id + '" does not exist. \nPlease use the menu option "Unenroll a POC from a program" to disenroll this account and the option "Enroll POC to a program" to enroll this account to an existing rewards program.')

    else:
        print(text.Red + '\n- [Rewards] The account "' + account_id + '" is not enrolled to any rewards program. \nPlease use the menu option "Enroll POC to a program" to enroll this account to a rewards program.')

    return


def get_rewards_status(account_id, zone, environment):
    """
        Returns the enrollment status of an account_id..

        Parameters:
            account_id  (str): AccountId (POC number)
            country     (str): Country code
            environment (str): Environment code

        Returns:
            str: 200 enrolled, 404 unenrolled, 406 ineligible
    """

    header_request = get_header_request(zone, 'true', 'false', 'false', 'false')
    request_url = get_microservice_base_url(environment,'true') + '/rewards-service/rewards/' + account_id
    response = place_request('GET', request_url, '', header_request)

    return response.status_code


# Displays the SKU's for rewards shopping
def display_sku_rewards(zone, environment, abi_id):
    rewards_dictionary = dict()
    header_request = get_header_request(zone, 'true', 'false', 'false', 'false')
    program_id = get_id_rewards(abi_id, header_request, environment)
    if program_id.split(" ")[0] != 'false':
        print("\nProgram ID: ", program_id)
        program_data = get_sku_rewards(program_id, header_request, environment)
        if isinstance(program_data, dict):
            for i in program_data['rules']:
                print(text.Yellow + "\nProgram name: ", i['moneySpentSkuRule']['name'])
                print("Gain " + str(i['moneySpentSkuRule']['points']) + " points per " + str(i['moneySpentSkuRule']['amountSpent']) + " spent")
                for skus in i['moneySpentSkuRule']['skus']:
                    sku_name = get_sku_name(zone, environment, skus)
                    rewards_dictionary.setdefault('SKU name', []).append(sku_name)
                    rewards_dictionary.setdefault('SKU ID', []).append(skus)
                print(text.default_text_color + tabulate(rewards_dictionary, headers='keys', tablefmt='grid'))
            return '200'
        else:
            return program_data
    else:
        return program_id


def get_rewards(account_id, zone, environment):
    header_request = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

    request_url = get_microservice_base_url(environment, 'false') + '/rewards-service/rewards/' + account_id + '?projection=DEFAULT'

    response = place_request('GET', request_url, '', header_request)

    if response.status_code == 200:
        return response
    elif response.status_code == 404:
        print(text.Red + '\n- [Rewards] The account "{accountId}" is not enrolled to any rewards program. \nPlease use the menu option "Enroll POC to a program" to enroll this account to a rewards program.'
            .format(accountId=account_id))
    else:
        print(text.Red + '\n- [Rewards] Failure when getting enrollment information for account "{accountId}". \n- Response Status: "{statusCode}". \n- Response message "{message}".'
                .format(accountId=account_id, statusCode=str(response.status_code), message=response.text))
    
    return None


def put_rewards(account_id, zone, environment):
    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

    # Define url request
    request_url = get_microservice_base_url(environment, 'false') + '/loyalty-business-service/rewards'

    # Create request body
    dict_values  = {
        'accountId' : account_id
    }

    request_body = convert_json_to_string(dict_values)

    response = place_request('POST', request_url, request_body, request_headers)

    json_data = loads(response.text)

    if response.status_code == 201:
        program_id = json_data['programId']
        
        print(text.Green + '\n- [Rewards] The account "{accountId}" has been successfully enrolled to the Rewards program "{program_id}".'
                .format(accountId=account_id,program_id=program_id))

    elif response.status_code == 409:
        print(text.Red + '\n- [Rewards] The account "{accountId}" is already enrolled to a Rewards program.'.format(accountId=account_id))

    elif response.status_code == 406:
        print(text.Red + '\n- [Rewards] The account "{accountId}" is not eligible to a Rewards program.'.format(accountId=account_id))

    else:
        print(text.Red + '\n- [Rewards] Failure when enrolling the account "{accountId}" to a rewards program.  \n- Response Status: "{statusCode}". \n- Response message "{message}".'
                .format(accountId=account_id, statusCode=str(response.status_code), message=response.text))

    return response