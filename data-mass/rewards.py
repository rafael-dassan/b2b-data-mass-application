# Standard library imports
import json
from json import loads
import os
from random import randint
from datetime import timedelta, datetime

# Third party imports
from tabulate import tabulate

# Local application imports
from common import get_header_request, get_microservice_base_url, update_value_to_json, convert_json_to_string, \
    place_request, create_list
from validations import is_number
from products import request_get_offers_microservice, request_get_products_by_account_microservice, \
    request_get_products_microservice, get_sku_name
from account import check_account_exists_microservice
from classes.text import text


# Create Rewards Program
def create_new_program(zone, environment):

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Verify if the zone already have a reward program created
    program_found = locate_program_for_zone(zone, environment, request_headers)

    if program_found != 'false':
        print(text.Yellow + '\n- [Rewards] This zone already have a reward program created - ID: ' + program_found)
        return 'error_found'

    balance = input(text.Yellow + '\nDo you want to create the program with initial balance (20.000)? y/N: ')
    balance = balance.upper()

    if balance == 'Y':
        initial_balance = 20000
    else:
        initial_balance = 0

    # Generates the new Program ID
    reward_id = 'DM-REWARDS-' + str(randint(100,900))

    # Define url request
    request_url = get_microservice_base_url(environment) + '/rewards-service/programs/' + reward_id

    deals = request_get_dt_combos(environment, request_headers)
    if deals == 'false':
        return 'false'

    # Verify if the zone has combos available
    if len(deals) > 0:

        sku_rules = generate_skus_for_rules(zone, environment)

        # Verify if the zone has at least 20 SKUs available
        if len(sku_rules) >= 20:

            print(text.default_text_color + '\nCreating new Rewards program in ' + zone + ' - ' + environment + '. Please wait...')
            
            sku_rules_premium = list()
            sku_rules_core = list()
            i = 0

            while i <= 9:
                # Getting 10 SKUs for premium rule
                sku_rules_premium.append(sku_rules[i])

                # Getting 10 SKUs for core rule
                sku_rules_core.append(sku_rules[i+10])
                i += 1

            # Getting all the basic information for the Program to be created
            generated_combos = generate_combos_information(deals)
            categories = generate_categories_information(zone)
            terms = generate_terms_information(zone)

            # Create file path
            path = os.path.abspath(os.path.dirname(__file__))
            file_path = os.path.join(path, 'data/create_rewards_program_payload.json')

            # Load JSON file
            with open(file_path) as file:
                json_data = json.load(file)

            dict_values  = {
                'name' : reward_id,
                'rules[0].moneySpentSkuRule.skus' : sku_rules_premium,
                'rules[1].moneySpentSkuRule.skus' : sku_rules_core,
                'combos' : generated_combos,
                'initialBalance' : initial_balance,
                'categories[0].categoryId' : categories[0],
                'categories[0].categoryIdWeb' : categories[1],
                'categories[0].description' : categories[2],
                'categories[0].buttonLabel' : categories[3],
                'categories[0].image' : categories[4],
                'categories[0].title' : 'Premium',
                'categories[0].subtitle' : categories[2],
                'categories[0].headerImage' : "https://cdn-b2b-abi.global.ssl.fastly.net/sit/images/br/redesign/premium/img-premium-chopp-brahma-logo@2x.png",
                'categories[0].brands' : [{
                    "brandId": "123",
                    "title": "premium brand",
                    "image": "https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/premium/img_puntos_20.png"
                }],
                'categories[1].categoryId' : categories[5],
                'categories[1].categoryIdWeb' : categories[6],
                'categories[1].description' : categories[7],
                'categories[1].buttonLabel' : categories[8],
                'categories[1].image' : categories[9],
                'categories[1].title' : 'Core',
                'categories[1].subtitle' : categories[7],
                'categories[1].headerImage' : "https://cdn-b2b-abi.global.ssl.fastly.net/sit/images/br/redesign/core/img-core-brahmachopp-logo@2x.png",
                'categories[1].brands' : [{
                    "brandId": "321",
                    "title": "core brand",
                    "image": "https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png"
                }],
                'termsAndConditions[0].documentURL' : terms[0],
                'termsAndConditions[0].changeLog' : terms[1]
            }

            for key in dict_values.keys():
                json_object = update_value_to_json(json_data, key, dict_values[key])

            #Create body
            request_body = convert_json_to_string(json_object)

            # Send request
            response = place_request('PUT', request_url, request_body, request_headers)

            if response.status_code == 200:
                return reward_id
            else:
                print(text.Red + '\n- [Rewards Service] Failure when creating a new program. Response Status: '
                                + str(response.status_code) + '. Response message ' + response.text)
                return 'false'
        else:
            return 'error_len_sku'
    else:
        return 'error_len_combo'


def update_dt_combos_rewards(zone, environment, abi_id):
    header_request = get_header_request(zone, 'true', 'false', 'false', 'false')
    program_id = get_id_rewards(abi_id, header_request, environment)

    if program_id.split(" ")[0] == 'false':
        return 'no_program'
    else:
        request_url = get_microservice_base_url(environment) + '/combos/?accountID=' + abi_id + '&types=DT&includeDeleted=false&includeDisabled=false'
        response = place_request('GET', request_url, '', header_request)
        if response.status_code != 200:
            return response.status_code
        else:
            combos_info = loads(response.text)
            combos_info_list = list()
            for i in combos_info['combos']:
                combos_info_list.append(i.get('id'))

            request_url = get_microservice_base_url(environment) + '/rewards-service/programs/' + str(program_id)
            response = place_request('GET', request_url, '', header_request)
            if response.status_code != 200:
                return response.status_code
            else:
                program_info = loads(response.text)
                program_combo_list = list()
                for i in program_info['combos']:
                    program_combo_list.append(i.get('comboId'))

                missing_combo = list(set(combos_info_list) - set(program_combo_list))

                if bool(missing_combo):
                    for j in range(len(missing_combo)):
                        dic_combos = {
                            'comboId': missing_combo[j],
                            'points': 500,
                            'redeemLimit': 5
                        }
                        program_info['combos'].append(dic_combos)

                    response = place_request('PUT', request_url, json.dumps(program_info), header_request)
                    if response.status_code != 200:
                        return response.status_code
                    else:
                        dict_values_account = {
                            'accounts': create_list(abi_id)
                        }
                        for i in combos_info['combos']:
                            for j in range(len(missing_combo)):
                                if i['id'] == missing_combo[j]:
                                    dict_missing_combo = {
                                        'id': i['id'],
                                        'externalId': i['id'],
                                        'title': i['title'],
                                        'description': i['id'],
                                        'startDate': i['startDate'],
                                        'endDate': i['endDate'],
                                        'updatedAt': i['updatedAt'],
                                        'type': 'DT',
                                        'image': 'https://test-conv-micerveceria.abi-sandbox.net/media/catalog/product/c/o/combo-icon_11.png',
                                        'freeGoods': i['freeGoods'],
                                        'limit': i['limit'],
                                        'originalPrice': 0,
                                        'price': 0,
                                        'score': 0,
                                    }
                                    dict_values_account.setdefault('combos', []).append(dict_missing_combo)

                        header_request = get_header_request(zone, 'false', 'false', 'true', 'false')

                        # Define url request to post the association
                        request_url = get_microservice_base_url(environment) + '/combo-relay/accounts'

                        # Send request to associate the combos to account
                        response = place_request('POST', request_url, json.dumps(dict_values_account), header_request)
                        return response.status_code
                else:
                    return 'none'


# Enroll POC to a zone's reward program
def enroll_poc_to_program(account_id, zone, environment):

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

    # Check if the zone already have a reward program created
    program_found = locate_program_for_zone(zone, environment, request_headers)

    if program_found != 'false':

        account_data = check_account_exists_microservice(account_id, zone, environment)

        seg_account = account_data[0]['segment']
        subseg_account = account_data[0]['subSegment']
        potent_account = account_data[0]['potential']

        if seg_account != 'DM-SEG' or subseg_account != 'DM-SUBSEG' or potent_account != 'DM-POTENT':
            turn_eligible = input(text.Yellow + '\nThis account is not eligible to a Reward program. Do you want to make it eligible now? y/N: ')
            turn_eligible = turn_eligible.upper()

            if turn_eligible == 'Y':
                account_eligible = make_account_eligible(account_id, zone, environment, request_headers)

                if account_eligible == 'true':
                    print(text.Green + '\n- [Rewards] The account is now eligible. Back to menu option "Enroll POC" to resume the enrollment process')
                    return 'true'
                else:
                    return 'false'
        else:
            # Define url request
            request_url = get_microservice_base_url(environment) + '/loyalty-business-service/rewards'

            dict_values  = {
                'accountId' : account_id
            }

            #Create body
            request_body = convert_json_to_string(dict_values)

            # Send request
            response = place_request('POST', request_url, request_body, request_headers)
            
            if response.status_code == 406 or response.status_code == 409 or response.status_code == 201:
                return response.status_code
            else:
                print(text.Red + '\n- [Rewards Service] Failure when enrolling an account to program. Response Status: '
                                + str(response.status_code) + '. Response message ' + response.text)
                return 'false'
    else:
        return 'pgm_not_found'


# Disenroll a POC from the rewards program
def delete_enroll_poc_to_program(account_id, zone, environment):

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

    # Check if the zone already have a reward program created
    program_found = locate_program_for_zone(zone, environment, request_headers)

    if program_found != 'false':
        # Define url request
        request_url = get_microservice_base_url(environment) + '/rewards-service/rewards/' + account_id

        response = place_request('DELETE', request_url, '', request_headers)

        if response.status_code != 204:
             print(text.Red + '\n- [Rewards Service] Failure when disenroll an account to program. Response Status: '
                            + str(response.status_code) + '. Response message ' + response.text)
           
        return response.status_code
    else:
        return 'pgm_not_found'


# Input transactions to a account
def input_transactions_to_account(account_id, zone, environment):

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

    # Check if the zone already have a reward program created
    program_found = locate_program_for_zone(zone, environment, request_headers)

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

    # Check if the zone already have a reward program created
    program_found = locate_program_for_zone(zone, environment, request_headers)

    if program_found != 'false':

        print(text.default_text_color + '\nAdding redeem products, please wait...')

        # Define url request to read the Rewards program of the zone
        request_url = get_microservice_base_url(environment) + '/rewards-service/programs/' + program_found

        # Send request
        response = place_request('GET', request_url, '', request_headers)
        json_program = loads(response.text)

        combos_dt_program = json_program['combos']
        len_combos_program = len(combos_dt_program)
        if len_combos_program > 50:
            len_combos_program = 50

        # Get all the combo IDs that are added to the reward program
        i = 0
        combos_id_program = list()
        while i < len_combos_program:
            combos_id_program.append(combos_dt_program[i]['comboId'])
            i += 1

        # Define url request to get all the combos of the specified zone
        request_url = get_microservice_base_url(environment) + '/combos/?types=DT&comboIds=&includeDeleted=false&includeDisabled=false'

        # Send request
        response = place_request('GET', request_url, '', request_headers)
        json_combos = loads(response.text)
        
        combos_dt_zone = json_combos['combos']
        len_combos_zone = len(combos_dt_zone)

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

        # Get a SKU to be used on FreeGood's list below
        product_offers = request_get_offers_microservice(account_id, zone, environment)
        
        if product_offers == 'false':
            return 'false'
        elif product_offers == 'not_found':
            print(text.Red + '\n- [Catalog Service] There is no product associated with the account ' + account_id)
            return 'false'

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

        #Create body to associate the combos to account
        request_body = convert_json_to_string(dict_values_account)
 
        # Send request to associate the combos to account
        response = place_request('POST', request_url, request_body, request_headers)

        if response.status_code == 201:
            print(text.Green + '\n- [Rewards] Total of ' + str(i) + ' combos added successfully')
        else:
            print(text.Red + '\n- [Combo Relay Service] Failure when associating combos to the account. Response Status: '
                                    + str(response.status_code) + '. Response message: ' + response.text)

    else:
        print(text.Red + '\n- [Rewards] This zone does not have a program created. Please use the menu option "Create new program" to create it')

    return


# Updates the program's initial balance
def update_program_balance(zone, environment):

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Check if the zone already have a reward program created
    program_found = locate_program_for_zone(zone, environment, request_headers)

    if program_found != 'false':

        confirm_program = input(text.Yellow + '\nDo you confirm update the balance for the program ' + program_found + '? y/N: ')
        confirm_program = confirm_program.upper()

        while confirm_program != 'Y' and confirm_program != 'N':
            print(text.Red + '\n- Invalid option\n')
            confirm_program = input(text.Yellow + '\nDo you confirm update the balance for the program ' + program_found + '? y/N: ')
            confirm_program = confirm_program.upper()

        if confirm_program == 'Y':
            new_balance = input(text.Yellow + '\nPlease inform the new balance ammount: ')

            while is_number(new_balance) == 'false':
                print(text.Red + '\n- Invalid option\n')
                new_balance = input(text.Yellow + '\nPlease inform the new balance ammount: ')

            while int(new_balance) < 0:
                print(text.Red + '\n- Invalid option. Only positive numbers are allowed\n')
                new_balance = input(text.Yellow + '\nPlease inform the new balance ammount: ')

            # Define url request to read the Rewards program selected
            request_url = get_microservice_base_url(environment) + '/rewards-service/programs/' + program_found

            # Send request
            response = place_request('GET', request_url, '', request_headers)

            json_rewards_old = loads(response.text)
            json_rewards_new = update_value_to_json(json_rewards_old, 'initialBalance', int(new_balance))

            # Define url request to update the Rewards program selected
            request_url = get_microservice_base_url(environment) + '/rewards-service/programs/' + program_found

            request_body = convert_json_to_string(json_rewards_new)

            # Send request
            response = place_request('PUT', request_url, request_body, request_headers)

            if response.status_code == 200:
                return program_found
            else:
                print(text.Red + '\n- [Rewards Service] Failure when enrolling an account to program. Response Status: '
                                + str(response.status_code) + '. Response message ' + response.text)
                return 'false'
        else:
            return 'no_confirm'
    else:
        return 'no_program'


# Add Reward challenges to a zone
def input_challenge_to_zone(abi_id, zone, environment):

    # Gets the account's SKUs to use only for challenge type = PURCHASE
    product_offers = request_get_products_by_account_microservice(abi_id, zone, environment)
    
    # Verify if the account has at least 10 SKUs inside for PURCHASE type
    if len(product_offers) > 10:
        offers_flag = 'true'
    else:
        offers_flag = 'false'  

    # Generates challenges - two of each type (take_photo, mark_complete, purchase and purchase_multiple)
    i = 1
    error_flag = 'false'
    while i <= 8:
        # Generates the new Program ID
        challenge_id = 'DM-CHALLENGE-100' + str(i)

        # Getting all the basic information to create the challenges
        if i == 1:
            generated_challenges = challenge_details(1)
        elif i == 3:
            generated_challenges = challenge_details(2)
        elif i == 5 and offers_flag == 'true':
            generated_challenges = challenge_details(3, product_offers)
        elif i == 7 and offers_flag == 'true':
            generated_challenges = challenge_details(4, product_offers)

        # Create file path
        path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(path, 'data/create_rewards_challenges_payload.json')

        # Load JSON file
        with open(file_path) as file:
            json_data = json.load(file)

        if i == 1 or i == 3:
            dict_values  = {
                'title' : challenge_id,
                'description' : generated_challenges[0],
                'detailedDescription' : generated_challenges[1],
                'startDate' : generated_challenges[2],
                'endDate' : generated_challenges[3],
                'image' : generated_challenges[4],
                'executionMethod' : generated_challenges[5],
                'goodPhotoSample' : generated_challenges[6],
                'badPhotoSample' : generated_challenges[7]
            }
        elif i == 2 or i == 4:
            dict_values  = {
                'title' : challenge_id,
                'description' : generated_challenges[8],
                'detailedDescription' : generated_challenges[9],
                'startDate' : generated_challenges[10],
                'endDate' : generated_challenges[11],
                'image' : generated_challenges[12],
                'executionMethod' : generated_challenges[13],
                'goodPhotoSample' : generated_challenges[14],
                'badPhotoSample' : generated_challenges[15]
            }
        elif i == 5 or i == 7 and offers_flag == 'true':
            dict_values  = {
                'title' : challenge_id,
                'description' : generated_challenges[0],
                'detailedDescription' : generated_challenges[1],
                'startDate' : generated_challenges[2],
                'endDate' : generated_challenges[3],
                'image' : generated_challenges[4],
                'executionMethod' : generated_challenges[5],
                'goodPhotoSample' : generated_challenges[6],
                'badPhotoSample' : generated_challenges[7],
                'skus' : generated_challenges[8]
            }
        elif i == 6 or i == 8 and offers_flag == 'true':
            dict_values  = {
                'title' : challenge_id,
                'description' : generated_challenges[9],
                'detailedDescription' : generated_challenges[10],
                'startDate' : generated_challenges[11],
                'endDate' : generated_challenges[12],
                'image' : generated_challenges[13],
                'executionMethod' : generated_challenges[14],
                'goodPhotoSample' : generated_challenges[15],
                'badPhotoSample' : generated_challenges[16],
                'skus' : generated_challenges[17]
            }

        for key in dict_values.keys():
            json_object = update_value_to_json(json_data, key, dict_values[key])

        #Create body
        request_body = convert_json_to_string(json_object)

        # Define headers
        request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

        # Define url request
        request_url = get_microservice_base_url(environment) + '/rewards-service/challenges/' + challenge_id

        # Verify if the challenge is PURCHASE and the account has at least 10 SKUs inside
        if i <= 6 or (i >= 7 and offers_flag == 'true'):
            # Send request
            response = place_request('PUT', request_url, request_body, request_headers)

            if response.status_code == 200:
                print(text.Green + '\n- [Rewards] The new challenge has been successfully created. ID: ' + challenge_id)
            else:
                error_flag = 'true'

        i += 1

    if offers_flag == 'false':
        print(text.Yellow + '\n- [Rewards] The PURCHASE challenges could not be created. The specified account needs at least 10 SKUs inside for that')

    # Verify if all challenges were created succesfully or if some failed
    if error_flag == 'true':
        return 'false'
    else:
        return 'true'


def challenge_details(challenge_type, products = None):
    # Sets the format of the challenge's start date (current date and time)
    start_date = datetime.now()
    start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S')
    start_date = start_date + 'Z'

    # Sets the format of the challenge's end date with expiration within 30 days
    end_date_one = datetime.now() + timedelta(days=30)
    end_date_one = end_date_one.strftime('%Y-%m-%dT%H:%M:%S')
    end_date_one = end_date_one + 'Z'

    # Sets the format of the challenge's end date with expiration within 60 days
    end_date_two = datetime.now() + timedelta(days=60)
    end_date_two = end_date_two.strftime('%Y-%m-%dT%H:%M:%S')
    end_date_two = end_date_two + 'Z'

    # Sets the format of the challenge's past start date (for expired challenges)
    expired_start_date = datetime.now() - timedelta(days=60)
    expired_start_date = expired_start_date.strftime('%Y-%m-%dT%H:%M:%S')
    expired_start_date = expired_start_date + 'Z'

    # Sets the format of the challenge's end date already expired (for expired challenges)
    expired_end_date = datetime.now() - timedelta(days=1)
    expired_end_date = expired_end_date.strftime('%Y-%m-%dT%H:%M:%S')
    expired_end_date = expired_end_date + 'Z'

    challenge_details = list()

    if challenge_type == 1:
        # Details of the take photo #1 (expiration within 30 days)
        challenge_details.append('TAKE A PHOTO')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(start_date)
        challenge_details.append(end_date_one)
        challenge_details.append('https://b2bfilemgmtsagbtest.blob.core.windows.net/files-do/rewards-admin_challenge-image.png?sig=IzFb2Eo16gb61Y92j3qry%2BiC61kqijYPkAZxuqf4ESI%3D&se=3019-06-23T15%3A38%3A29Z&sv=2015-04-05&sp=r&sr=b')
        challenge_details.append('TAKE_PHOTO')
        challenge_details.append('https://b2bstaticwebsagbdev.blob.core.windows.net/digitaltrade/uat/images/br/challenges/1659/photo_of_cooler_ok.jpg')
        challenge_details.append('https://b2bstaticwebsagbdev.blob.core.windows.net/digitaltrade/uat/images/br/challenges/1659/photo_of_cooler_nok.jpg')

       # Details of the take photo #2 (already expired)
        challenge_details.append('TAKE A PHOTO')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(expired_start_date)
        challenge_details.append(expired_end_date)
        challenge_details.append('https://b2bfilemgmtsagbtest.blob.core.windows.net/files-do/rewards-admin_challenge-image.png?sig=IzFb2Eo16gb61Y92j3qry%2BiC61kqijYPkAZxuqf4ESI%3D&se=3019-06-23T15%3A38%3A29Z&sv=2015-04-05&sp=r&sr=b')
        challenge_details.append('TAKE_PHOTO')
        challenge_details.append('https://b2bstaticwebsagbdev.blob.core.windows.net/digitaltrade/uat/images/br/challenges/1659/photo_of_cooler_ok.jpg')
        challenge_details.append('https://b2bstaticwebsagbdev.blob.core.windows.net/digitaltrade/uat/images/br/challenges/1659/photo_of_cooler_nok.jpg')
    elif challenge_type == 2:
        # Details of the mark complete #1 (expiration within 30 days)
        challenge_details.append('MARK COMPLETE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(start_date)
        challenge_details.append(end_date_one)
        challenge_details.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/br/challenges/1661/execution_2nd_display.jpg')
        challenge_details.append('MARK_COMPLETE')
        challenge_details.append('')
        challenge_details.append('')

        # Details of the mark complete #2 (already expired)
        challenge_details.append('MARK COMPLETE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(expired_start_date)
        challenge_details.append(expired_end_date)
        challenge_details.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/br/challenges/1661/execution_2nd_display.jpg')
        challenge_details.append('MARK_COMPLETE')
        challenge_details.append('')
        challenge_details.append('')
    elif challenge_type == 3:
        if len(products) >= 10:
            dict_values_purchase = [
                {
                    'sku' : products[0]['sku'],
                    'quantity' : 2
                },
                {
                    'sku' : products[1]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[2]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[3]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[4]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[5]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[6]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[7]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[8]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[9]['sku'],
                    'quantity' : 2,
                }
            ]
        else:
            dict_values_purchase = None

        # Details of the purchase #1 (expiration within 30 days)
        challenge_details.append('PURCHASE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(start_date)
        challenge_details.append(end_date_one)
        challenge_details.append('https://b2bstaticwebsagbprod.blob.core.windows.net/challenge/DO/images/afiche_12oz_PTE.jpg')
        challenge_details.append('PURCHASE')
        challenge_details.append('')
        challenge_details.append('')
        challenge_details.append(dict_values_purchase)

        # Details of the purchase #2 (already expired)
        challenge_details.append('PURCHASE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(expired_start_date)
        challenge_details.append(expired_end_date)
        challenge_details.append('https://b2bstaticwebsagbprod.blob.core.windows.net/challenge/DO/images/afiche_12oz_PTE.jpg')
        challenge_details.append('PURCHASE')
        challenge_details.append('')
        challenge_details.append('')
        challenge_details.append(dict_values_purchase)

    elif challenge_type == 4:
        if len(products) >= 10:
            dict_values_purchase = [
                {
                    'sku' : products[0]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 0,
                    'itemImage': products[0]['itemImage'],
                    'itemName': products[0]['itemName'],
                    'price': products[0]['price'],
                    'container' : products[0]['container'],
                    'package': products[0]['package'],
                },
                {
                    'sku' : products[1]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 1,
                    'itemImage': products[1]['itemImage'],
                    'itemName': products[1]['itemName'],
                    'price': products[1]['price'],
                    'container' : products[1]['container'],
                    'package': products[1]['package'],
                },
                {
                    'sku' : products[2]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 2,
                    'itemImage': products[2]['itemImage'],
                    'itemName': products[2]['itemName'],
                    'price': products[2]['price'],
                    'container' : products[2]['container'],
                    'package': products[2]['package'],
                },
                {
                    'sku' : products[3]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 3,
                    'itemImage': products[3]['itemImage'],
                    'itemName': products[3]['itemName'],
                    'price': products[3]['price'],
                    'container' : products[3]['container'],
                    'package': products[3]['package'],
                },
                {
                    'sku' : products[4]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 4,
                    'itemImage': products[4]['itemImage'],
                    'itemName': products[4]['itemName'],
                    'price': products[4]['price'],
                    'container' : products[4]['container'],
                    'package': products[4]['package'],
                },
                {
                    'sku' : products[5]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 5,
                    'itemImage': products[5]['itemImage'],
                    'itemName': products[5]['itemName'],
                    'price': products[5]['price'],
                    'container' : products[5]['container'],
                    'package': products[5]['package'],
                },
                {
                    'sku' : products[6]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 6,
                    'itemImage': products[6]['itemImage'],
                    'itemName': products[6]['itemName'],
                    'price': products[6]['price'],
                    'container' : products[6]['container'],
                    'package': products[6]['package'],
                },
                {
                    'sku' : products[7]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 7,
                    'itemImage': products[7]['itemImage'],
                    'itemName': products[7]['itemName'],
                    'price': products[7]['price'],
                    'container' : products[7]['container'],
                    'package': products[7]['package'],
                },
                {
                    'sku' : products[8]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 8,
                    'itemImage': products[8]['itemImage'],
                    'itemName': products[8]['itemName'],
                    'price': products[8]['price'],
                    'container' : products[8]['container'],
                    'package': products[8]['package'],
                },
                {
                    'sku' : products[9]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 9,
                    'itemImage': products[9]['itemImage'],
                    'itemName': products[9]['itemName'],
                    'price': products[9]['price'],
                    'container' : products[9]['container'],
                    'package': products[9]['package'],
                }
            ]
        else:
            dict_values_purchase = None

        # Details of the multiple purchase #1 (expiration within 30 days)
        challenge_details.append('MULTIPLE PURCHASE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(start_date)
        challenge_details.append(end_date_one)
        challenge_details.append('https://b2bstaticwebsagbprod.blob.core.windows.net/challenge/DO/images/afiche_12oz_PTE.jpg')
        challenge_details.append('PURCHASE_MULTIPLE')
        challenge_details.append('')
        challenge_details.append('')
        challenge_details.append(dict_values_purchase)

        # Details of the multiple purchase #2 (already expired)
        challenge_details.append('MULTIPLE PURCHASE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(expired_start_date)
        challenge_details.append(expired_end_date)
        challenge_details.append('https://b2bstaticwebsagbprod.blob.core.windows.net/challenge/DO/images/afiche_12oz_PTE.jpg')
        challenge_details.append('PURCHASE_MULTIPLE')
        challenge_details.append('')
        challenge_details.append('')
        challenge_details.append(dict_values_purchase)

    return challenge_details

# Make an account eligible to a Reward program
def make_account_eligible(abi_id, zone, environment, header_request):

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account != 'false':

        # Update the account's information with the right values to associate to a Reward program
        json_object = update_value_to_json(account, '[0][potential]', 'DM-POTENT')
        json_object = update_value_to_json(account, '[0][segment]', 'DM-SEG')
        json_object = update_value_to_json(account, '[0][subSegment]', 'DM-SUBSEG')

        # Get header request
        request_headers = get_header_request(zone, 'false', 'true', 'false', 'false')

        # Get base URL
        request_url = get_microservice_base_url(environment) + '/account-relay/'

        # Create body
        request_body = convert_json_to_string(json_object)

        # Place request
        response = place_request('POST', request_url, request_body, request_headers)

        if response.status_code == 202:
            return 'true'
        else:
            return 'false'


# Retrieve Digital Trade combos (DT Combos) for the specified zone
def request_get_dt_combos(environment, header_request):
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


# Locate Rewards program previously created in the zone
def locate_program_for_zone(zone, environment, header_request):

    # Define url request
    request_url = get_microservice_base_url(environment) + '/rewards-service/programs/'
    
    # Send request
    response = place_request('GET', request_url, '', header_request)
    
    program_list = loads(response.text)

    program_found = 'false'

    for i in range(len(program_list)):
        program_id = program_list[i]['id']
        program_id = program_id[0:9]

        if program_id == 'DM-REWARD':
            program_found = program_list[i]['id']
            break
    
    return program_found


# Generates the Combos for Rewards program
def generate_combos_information(deals_list):
    combos = deals_list['combos']
    combos_id = list()

    for i in range(len(combos)):
        points = i + 1

        dic_combos  = {
            'comboId' : combos[i]['id'],
            'points' : points * 500,
            'redeemLimit' : 5
        }

        combos_id.append(dic_combos)

    return combos_id


# Generates the SKUs for the rules for Rewards program
def generate_skus_for_rules(zone, environment):
    products = request_get_products_microservice(zone, environment)
    sku_rules = list()
    for i in range(len(products)):
        sku_rules.append(products[i]['sku'])

    return sku_rules


# Generates the Categories for Rewards program
def generate_categories_information(zone):
    category_info = list()
    
    if zone == 'DO':
        # Premium category
        category_info.append('96')
        category_info.append('94')
        category_info.append('Gana 100 puntos por cada RD $1000 pesos de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png')
        
        # Core category
        category_info.append('95')
        category_info.append('93')
        category_info.append('Gana 50 puntos por cada RD $1000 pesos de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png')
    elif zone == 'CO':
        # Premium category
        category_info.append('124')
        category_info.append('304')
        category_info.append('Gana 100 puntos por cada RD $1000 pesos de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png')
    
        # Core category
        category_info.append('123')
        category_info.append('261')
        category_info.append('Gana 50 puntos por cada RD $1000 pesos de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png')
    elif zone == 'AR':
        # Premium category
        category_info.append('582')
        category_info.append('494')
        category_info.append('Gana 100 puntos por cada RD $1000 pesos de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png')

        # Core category
        category_info.append('581')
        category_info.append('493')
        category_info.append('Gana 50 puntos por cada RD $1000 pesos de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png')
    elif zone == 'BR':
        # Premium category
        category_info.append('262')
        category_info.append('226')
        category_info.append('Ganhe 100 pontos para cada R$1000,00 gastos em compras e troque por produtos gratis.')
        category_info.append('COMPRAR AGORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/br/premium/img-premium-br-rules-2.png')

        # Core category
        category_info.append('272')
        category_info.append('236')
        category_info.append('Ganhe 50 pontos para cada R$1000,00 gastos em compras e troque por produtos gratis.')
        category_info.append('COMPRAR AGORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/br/premium/img-premium-br-rules-2.png')
    elif zone == 'ZA':
        # Premium category
        category_info.append('217')
        category_info.append('214')
        category_info.append('Earn 1 point for each R100 spent on quarts products.')
        category_info.append('BUY NOW')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/za/quarts-brands.png')

        # Core category
        category_info.append('219')
        category_info.append('216')
        category_info.append('Earn 10 points for each R100 spent on bonus products.')
        category_info.append('BUY NOW')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/za/bonus-brands.png')
    elif zone == 'MX':
        # Premium category
        category_info.append('9')
        category_info.append('1')
        category_info.append('Gana 1 punto por cada $10 de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/mx/core-brands.png')

        # Core category
        category_info.append('12')
        category_info.append('2')
        category_info.append('Gana 3 puntos por cada $10 de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/mx/premium-brands.png')
    elif zone == 'EC':
        # Premium category
        category_info.append('129')
        category_info.append('115')
        category_info.append('Gana 4 puntos por cada $1 de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/sit/images/ec/premium-brands.png')

        # Core category
        category_info.append('127')
        category_info.append('113')
        category_info.append('Gana 1 punto por cada $1 de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/ec/core-brands.png')
    elif zone == 'PE':
        # Premium category
        category_info.append('premium')
        category_info.append('premium')
        category_info.append('Gana 2 puntos por cada S/ 1.00 de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/pe/premium-brands.png')

        # Core category
        category_info.append('core')
        category_info.append('core')
        category_info.append('Gana 1 punto por cada S/ 1.00 de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/pe/core-brands.png')


    return category_info


# Generates the Terms and Conditions for Rewards program
def generate_terms_information(zone):
    terms_info = list()
    
    if zone == 'DO' or zone == 'CO' or zone == 'AR' or zone == 'MX' or zone == 'EC' or zone == 'PE':
        terms_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/terms/terms-co.html')
        terms_info.append('Términos iniciales introducidos al programa')
    elif zone == 'BR':
        terms_info.append('https://b2bstaticwebsagbdev.blob.core.windows.net/digitaltrade/terms/terms-br.html')
        terms_info.append('Termos iniciais introduzidos ao programa')
    elif zone == 'ZA':
        terms_info.append('https://cdn-b2b-abi-prod.global.ssl.fastly.net/prod/terms/terms-za.html')
        terms_info.append('Initial terms added to the program')

    return terms_info


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



def get_id_rewards(abi_id, header_request, environment):
    request_url = get_microservice_base_url(environment,'true') + '/rewards-service/rewards/' + abi_id
    response = place_request('GET', request_url, '', header_request)
    if response.status_code == 200:
        return loads(response.text).get("programId")
    else:
        return 'false ' + str(response.status_code)


def get_rewards_status(account_id, country, environment):
    """
        Returns the enrollment status of an account_id..

        Parameters:
            account_id  (str): AccountId (POC number)
            country     (str): Country code
            environment (str): Environment code

        Returns:
            str: 200 enrolled, 404 unenrolled, 406 ineligible
    """

    header_request = get_header_request(country, 'true', 'false', 'false', 'false')
    request_url = get_microservice_base_url(environment,'true') + '/rewards-service/rewards/' + account_id
    response = place_request('GET', request_url, '', header_request)
    return response.status_code


def get_sku_rewards(program_id, header_request, environment):
    request_url = get_microservice_base_url(environment,'true') + '/rewards-service/programs/' + program_id
    response = place_request('GET', request_url, '', header_request)
    if response.status_code == 200:
        return loads(response.text)
    else:
        return 'false ' + str(response.status_code)
