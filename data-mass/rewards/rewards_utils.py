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
from common import get_header_request, get_microservice_base_url, place_request, update_value_to_json, \
    convert_json_to_string, create_list
from products import request_get_products_microservice
from classes.text import text


def generate_id():
    # Generates an sequential number based on Epoch time using seconds and the first two chars milliseconds
    # time() return an Epoch time with milliseconds separeted with a dot (.)

    parsed_time = str(time()).replace('.', '')
    epoch_id = parsed_time[:11]

    return epoch_id


# Retrieve Digital Trade combos (DT Combos) for the specified zone
def get_dt_combos_from_zone(zone, environment, page_size=9999):
    
    header_request = get_header_request(zone, 'true', 'false', 'false', 'false')
    
    # Define url request
    request_url = get_microservice_base_url(environment) + '/combos/?types=DT&includeDeleted=false&includeDisabled=false&page=0&pageSize=' + str(page_size)
    
    # Send request
    response = place_request('GET', request_url, '', header_request)

    if response.status_code == 200:
        return response
    elif response.status_code == 404:
        print(text.Red + '\n- [Combo Service] There is no combo type digital trade registered. \n- Response Status: "{}". \n- Response message "{}".'
                .format(str(response.status_code), response.text))
    else:
        print(text.Red + '\n- [Combo Service] Failure to retrieve combo type digital trade. \n- Response Status: "{}". \n- Response message "{}".'
                .format(str(response.status_code), response.text))
    
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
            'description': dt_combos_to_associate[i]['id'],
            'startDate': dt_combos_to_associate[i]['startDate'],
            'endDate': dt_combos_to_associate[i]['endDate'],
            'updatedAt': dt_combos_to_associate[i]['updatedAt'],
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
        print(text.Green + '\n- [Combo Relay Service] Total of "{}" combos associated successfully to account "{}".'
            .format(str(len(dt_combos_to_associate)), account_id))
    else:
        print(text.Red + '\n- [Combo Relay Service] Failure when associating combos to the account. \n- Response Status: "{}". \n- Response message: "{}"'
            .format(str(response.status_code), response.text))

    return response


# Generates the SKUs for the rules for Rewards program
def create_product_list_from_zone(zone, environment):
    response_products = request_get_products_microservice(zone, environment)

    sku_rules = list()

    if response_products != 'false':
        for i in range(len(response_products)):
            sku_rules.append(response_products[i]['sku'])

    return sku_rules


def get_id_rewards(abi_id, header_request, environment):
    request_url = get_microservice_base_url(environment,'true') + '/rewards-service/rewards/' + abi_id
    response = place_request('GET', request_url, '', header_request)
    if response.status_code == 200:
        return loads(response.text).get("programId")
    else:
        return 'false ' + str(response.status_code)


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


# Generates the Combos for Rewards program
def generate_combos_information(zone_dt_combos):
    zone_dt_combos = zone_dt_combos['combos']
    combos_list = list()

    for i in range(len(zone_dt_combos)):
        points = i + 1

        dic_combos  = {
            'comboId' : zone_dt_combos[i]['id'],
            'points' : points * 250
        }

        combos_list.append(dic_combos)

    return combos_list


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