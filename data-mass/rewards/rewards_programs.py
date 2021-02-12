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
    place_request, create_list, print_input_number, print_input_text, set_to_dictionary
from validations import is_number
from products import request_get_products_microservice
from classes.text import text
from rewards.rewards_utils import display_programs_info, get_dt_combos_from_zone, get_id_rewards


# Create Rewards Program
def create_new_program(zone, environment):

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Verify if the zone already have a reward program created
    DM_program = get_DM_program_for_zone(zone, environment)

    if DM_program != None:
        program_id = DM_program['id']
        print(text.Yellow + '\n- [Rewards] This zone already have a reward program created - ID: "{programId}"'.format(programId=program_id))
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

    zone_dt_combos = get_dt_combos_from_zone(zone, environment)
    if zone_dt_combos == 'false':
        return 'false'

    # Verify if the zone has combos available
    if len(zone_dt_combos) > 0:

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
            generated_combos = generate_combos_information(zone_dt_combos)
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


# Patches the selected program root field
def patch_program_root_field(zone, environment, field):

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    all_programs = get_all_programs(zone, environment)

    if all_programs != None:

        initial_balance = True if field == 'initial_balance' else False
        redeem_limit = True if field == 'redeem_limit' else False

        json_all_programs = loads(all_programs.text)
        display_programs_info(json_all_programs, initial_balance, redeem_limit)

        program_id = print_input_text('\nPlease inform the Program ID')

        dict_values_patch_program = dict()

        if initial_balance:
            new_balance = print_input_number('\nPlease inform the new balance amount (greater or equal zero)')
            while int(new_balance) < 0:
                print(text.Red + '\nInvalid value!! Must be greater or equal zero!!')
                new_balance = print_input_number('\nPlease inform the new balance amount (greater or equal zero)')
            
            set_to_dictionary(dict_values_patch_program, 'initialBalance', int(new_balance))
        
        elif redeem_limit:
            new_redeem_limit = print_input_number('\nPlease inform the new redeem limit value (greater than zero)')
            while int(new_redeem_limit) <= 0:
                print(text.Red + '\nInvalid value!! Must be greater than zero!!')
                new_redeem_limit = print_input_number('\nPlease inform the new redeem limit value (greater than zero)')
            
            set_to_dictionary(dict_values_patch_program, 'redeemLimit', int(new_redeem_limit))
       
        request_body = convert_json_to_string(dict_values_patch_program)

        return patch_program(program_id, zone, environment, request_body)


# Generates the Combos for Rewards program
def generate_combos_information(deals_list):
    combos = deals_list['combos']
    combos_id = list()

    for i in range(len(combos)):
        points = i + 1

        dic_combos  = {
            'comboId' : combos[i]['id'],
            'points' : points * 250
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


# Check if DM Rewards program exists for the zone
def get_DM_program_for_zone(zone, environment):

    DM_program = None

    # Send request
    response = get_all_programs(zone, environment)
    
    if response != None:

        program_list = loads(response.text)
        for i in range(len(program_list)):
            program_id = program_list[i]['id']
            preffix_program_id = program_id[0:9]

            if preffix_program_id == 'DM-REWARD':
                DM_program = program_list[i]
                break
    
    return DM_program


def get_sku_rewards(program_id, header_request, environment):
    request_url = get_microservice_base_url(environment,'true') + '/rewards-service/programs/' + program_id
    response = place_request('GET', request_url, '', header_request)
    if response.status_code == 200:
        return loads(response.text)
    else:
        return 'false ' + str(response.status_code)

# Get all reward program for the zone
def get_all_programs(zone, environment):

    header_request = get_header_request(zone, 'true', 'false', 'false', 'false')
    
    # Define url request
    request_url = get_microservice_base_url(environment, 'false') + '/rewards-service/programs'
    
    # Send request
    response = place_request('GET', request_url, '', header_request)
    json_data = loads(response.text)

    if response.status_code == 200 and len(json_data) > 0:
        return response
    elif response.status_code == 200 and len(json_data) == 0:
        print(text.Red + '\n- [Rewards] There are no Reward programs available in "{zone}" zone.'.format(zone=zone))
    else:
        print(text.Red + '\n- [Rewards] Failure when getting all programs in "{zone}" zone. \n- Response Status: "{statusCode}". \n- Response message "{message}".'
                .format(zone=zone, statusCode=str(response.status_code), message=response.text))
    
    return None

# Get an specific reward program for the zone
def get_specific_program(program_id, zone, environment):

    header_request = get_header_request(zone, 'true', 'false', 'false', 'false')
    
    # Define url request
    request_url = get_microservice_base_url(environment, 'false') + '/rewards-service/programs/' + program_id
    
    # Send request
    response = place_request('GET', request_url, '', header_request)

    if response.status_code == 200:
        return response
    else:
        return None

def patch_program(program_id, zone, environment, request_body):

    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Define url request to patch the Rewards program selected
    request_url = get_microservice_base_url(environment, 'false') + '/rewards-service/programs/' + program_id

    # Send request
    response = place_request('PATCH', request_url, request_body, request_headers)

    if response.status_code == 200:
        print(text.Green + '\n- [Rewards] The Rewards program "{programId}" has been successfully updated.'.format(programId=program_id))

    elif response.status_code == 404:
        print(text.Red + '\n- [Rewards] The Rewards program "{programId}" does not exist.'.format(programId=program_id))

    else:
        print(text.Red + '\n- [Rewards] Failure when updating the program "{programId}" configuration. \n- Response Status: "{statusCode}". \n- Response message "{message}".'
                .format(programId=program_id, statusCode=str(response.status_code), message=response.text))

    return response