# Standard library imports
import json
from json import loads
import os
from time import time
from random import randint
from uuid import uuid1

# Third party imports
from tabulate import tabulate

# Local application imports
from .common import update_value_to_json, create_list, convert_json_to_string, get_microservice_base_url, \
    place_request, get_header_request, set_to_dictionary
from .classes.text import text


def create_all_recommendations(zone, environment, account_id, products):
    # Get responses
    quick_order_response = request_quick_order(zone, environment, account_id, products)
    sell_up_response = request_sell_up(zone, environment, account_id, products)
    forgotten_items_response = request_forgotten_items(zone, environment, account_id, products)

    if quick_order_response == 'success' and sell_up_response == 'success' and forgotten_items_response == 'success':
        return 'success'
    else:
        return 'false'


# Define JSON to submit QUICK ORDER recommendation type
def create_quick_order_payload(account_id, zone, product_list):
    countries_es = ['AR', 'CO', 'DO', 'EC', 'MX', 'PA', 'PE', 'PY']

    if zone in countries_es:
        language = 'es'
        text = 'Pedido Fácil'
        text_description = 'Productos que ordenaste anteriormente <link>Añadir todo al camión</link>'
    elif zone == 'BR':
        language = 'pt'
        text = 'Pedido Facil'
        text_description = 'Produtos comprados anteriormente <link>Adicionar todos itens ao carrinho</link>'
    else:
        language = 'en'
        text = 'Quick Order'
        text_description = 'Products ordered before <link>Add all items to cart</link>'

    items = list()
    index = 0
    while index < len(product_list):
        items_values = {
            "sku": product_list[index],
            "quantity": randint(1, 10),
            "score": index + 1,
            "type": "clustering",
            "discount": 0
        }
        items.append(items_values)
        index = index + 1

    dict_values = {
        'recommendationId': 'DM-{0}-{1}'.format(zone, str(randint(1, 100000))),
        'useCase': 'QUICK_ORDER',
        'useCaseId': account_id,
        'descriptions[0].language': language,
        'descriptions[0].text': text,
        'descriptions[0].description': text_description,
        'combos': None
    }
    set_to_dictionary(dict_values, 'items', items)

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_beer_recommender_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    return request_body


# Define JSON to submit FORGOTTEN ITEMS recommendation type
def create_forgotten_items_payload(account_id, zone, product_list):
    countries_es = ['AR', 'CO', 'DO', 'EC', 'MX', 'PA', 'PE', 'PY']

    if zone in countries_es:
        language = 'es'
        text = 'Productos Populares para Negocios como el tuyo'
        text_description = ''
    elif zone == 'BR':
        language = 'pt'
        text = 'Produtos Populares para Negocios como o seu'
        text_description = ''
    else:
        language = 'en'
        text = 'Popular Products for Businesses like yours'
        text_description = ''

    items = list()
    index = 0
    while index < len(product_list):
        items_values = {
            "sku": product_list[index],
            "quantity": randint(1, 10),
            "score":  index + 1,
            "type": "clustering",
            "discount": 0
        }
        items.append(items_values)
        index = index + 1

    dict_values = {
        'recommendationId': 'DM-{0}-{1}'.format(zone, str(randint(1, 100000))),
        'useCase': 'FORGOTTEN_ITEMS',
        'useCaseId': account_id,
        'descriptions[0].language': language,
        'descriptions[0].text': text,
        'descriptions[0].description': text_description,
        'combos': None
    }
    set_to_dictionary(dict_values, 'items', items)

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_beer_recommender_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    return request_body


# Define JSON to submit UP SELL recommendation type
def create_upsell_payload(account_id, zone, product_list):
    countries_es = ['AR', 'CO', 'DO', 'EC', 'MX', 'PA', 'PE', 'PY']

    if zone in countries_es:
        language = 'es'
        text = 'Productos Populares para Negocios como el tuyo'
        text_description = 'Los Productos mas Vendidos en tu Zona'
    elif zone == 'BR':
        language = 'pt'
        text = 'Produtos Populares para Negocios como o seu'
        text_description = 'Os Produtos mais Vendidos em tua região'
    else:
        language = 'en'
        text = 'Popular Products for Businesses like yours'
        text_description = 'The Best Selling Products in your zone'

    items = list()
    index = 0
    while index < len(product_list):
        items_values = {
            "sku": product_list[index],
            "quantity": randint(1, 10),
            "score": index + 1,
            "type": "clustering",
            "discount": 0
        }
        items.append(items_values)
        index = index + 1

    dict_values = {
        'recommendationId': 'DM-{0}-{1}'.format(zone, str(randint(1, 100000))),
        'descriptions[0].language': language,
        'descriptions[0].text': text,
        'descriptions[0].description': text_description,
        'useCaseId': account_id
    }
    set_to_dictionary(dict_values, 'items', items)
    
    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_beer_recommender_sell_up_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    return request_body


def request_quick_order(zone, environment, account_id, products):
    # Define headers
    request_headers = get_header_request_recommender(zone, environment)

    # Define url request 
    request_url = get_microservice_base_url(environment) + '/global-recommendation-relay'

    # Get body
    request_body = create_quick_order_payload(account_id, zone, products)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)
    
    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Recommendation Relay Service] Failure to add recommendation. Response Status: {0}. '
                         'Response message: {1}'.format(response.status_code, response.text))
        return 'false'


def request_forgotten_items(zone, environment, account_id, products):
    # Define headers
    request_headers = get_header_request_recommender(zone, environment)

    # Define url request
    request_url = get_microservice_base_url(environment) + '/global-recommendation-relay'

    # Get body
    request_body = create_forgotten_items_payload(account_id, zone, products)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Recommendation Relay Service] Failure to add recommendation. Response Status: {0}. '
                         'Response message: {1}'.format(response.status_code, response.text))
        return 'false'


def request_sell_up(zone, environment, account_id, products):
    # Define headers
    request_headers = get_header_request_recommender(zone, environment)

    # Define url request
    request_url = get_microservice_base_url(environment) + '/global-recommendation-relay'

    # Get body
    request_body = create_upsell_payload(account_id, zone, products)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Recommendation Relay Service] Failure to add recommendation. Response Status: {0}. '
                         'Response message: {1}'.format(response.status_code, response.text))
        return 'false'


# Define an exclusive header for Recommended Products
def get_header_request_recommender(zone, environment):
    # Define headers
    if environment == 'SIT' or environment == 'DEV':
        request_headers = get_header_request(zone, 'false', 'true')
    elif environment == 'UAT':
        switcher = {
            'AR': 'America/Buenos_Aires',
            'BR': 'America/Sao_Paulo',
            'CA': 'America/Toronto',
            'CO': 'America/Bogota',
            'DO': 'America/Santo_Domingo',
            'EC': 'America/Guayaquil',
            'MX': 'America/Mexico_City',
            'PA': 'America/Panama',
            'PE': 'America/Lima',
            'PY': 'America/Asuncion',
            'ZA': 'Africa/Johannesburg'
        }
        timezone = switcher.get(zone, 'false')

        request_headers = {
            'Content-Type': 'application/json',
            'country': zone,
            'requestTraceId': str(uuid1()),
            'x-timestamp': str(int(round(time() * 1000))),
            'cache-control': 'no-cache',
            'timezone': timezone,
            'Authorization': 'Basic ZGV4dGVyOktZTVU5MndHUjNZaENlRHI='
        }
        
    return request_headers


def get_recommendation_by_account(account_id, zone, environment, use_case):
    headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

    request_url = get_microservice_base_url(environment, 'true') + '/global-recommendation/?useCase={0}&useCaseId=' \
                                                                   '{1}&useCaseType=ACCOUNT'.format(use_case, account_id)

    response = place_request('GET', request_url, '', headers)

    recommendation_data = loads(response.text)

    if response.status_code == 200:
        content = recommendation_data['content']
        if len(content) != 0:
            return recommendation_data
        elif len(content) == 0:
            print(text.Yellow + '\n- [Global Recommendation Service] The account {0} does not have recommendation type'
                                ' {1}'.format(account_id, use_case))
            return 'not_found'
    else:
        print(text.Red + '\n- [Global Recommendation Service] Failure to retrieve recommendation. Response Status: {0}.'
                         ' Response message: {1}'.format(response.status_code, response.text))
        return 'false'


def delete_recommendation_by_id(environment, recommendation_data):
    recommendation_id = recommendation_data['content'][0]['id']

    headers = {
        'requestTraceId': str(uuid1()),
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3Nlc'
                         'nZpY2VzIiwiZXhwIjoxNjE2MjM5MDIyLCJpYXQiOjE1MTYyMzkwMjIsInVwZGF0ZWRfYXQiOjExMTExMTEsIm5hbWUiOi'
                         'J1c2VyQGFiLWluYmV2LmNvbSIsImFjY291bnRJRCI6IiIsInVzZXJJRCI6IjIxMTgiLCJyb2xlcyI6WyJST0xFX0FETUl'
                         'OIl19.Hpthi-Joez6m2lNiOpC6y1hfPOT5nvMtYdNnp5NqVTM'
    }

    request_url = get_microservice_base_url(environment, 'true') + '/global-recommendation/{0}'.format(recommendation_id)

    response = place_request('DELETE', request_url, '', headers)

    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Global Recommendation Service] Failure to delete recommendation. Response Status: {0}.'
                         ' Response message: {1}'.format(response.status_code, response.text))
        return 'false'


def display_recommendations_by_account(data):
    recommendations = data['content']
    recommender_list = list()
    items_list = list()
    combo_list = list()

    for i in range(len(recommendations)):
        dict_value = {
            'ID': recommendations[i]['recommendationId'],
            'Use Case': recommendations[i]['useCase'],
            'Created Date': recommendations[i]['createdDate'],
            'Update Date': recommendations[i]['updatedDate']
        }
        recommender_list.append(dict_value)

        items = recommendations[i]['items']
        combos = recommendations[i]['combos']
        if len(items) != 0:
            for x in range(len(items)):
                items_value = {
                    'Recommendation': recommendations[i]['useCase'],
                    'SKU': items[x]['sku'],
                    'Quantity': items[x]['quantity'],
                    'Score': items[x]['score']
                }
                items_list.append(items_value)
        else:
            items_value = {
                'Recommendation': recommendations[i]['useCase'],
                'Items': 'None'
            }
            items_list.append(items_value)

        if len(combos) != 0:
            for z in range(len(combos)):
                combos_value = {
                    'Recommendation': recommendations[i]['useCase'],
                    'ID Combo': combos[z]['id'],
                    'Quantity': combos[z]['quantity'],
                    'Score': combos[z]['score'],
                    'Type': combos[z]['type']
                }
                combo_list.append(combos_value)
        else:
            combos_value = {
                'Recommendation': recommendations[i]['useCase'],
                'Combos': 'None'
            }
            combo_list.append(combos_value)

    print(text.default_text_color + '\nRecommendations Information By Account')
    print(tabulate(recommender_list, headers='keys', tablefmt='grid'))

    print(text.default_text_color + '\nItems Recommendations Information By Account')
    print(tabulate(items_list, headers='keys', tablefmt='grid'))

    print(text.default_text_color + '\nCombos Recommendations Information By Account')
    print(tabulate(combo_list, headers='keys', tablefmt='grid'))


def input_combos_quick_order(zone, environment, account_id):
    # Retrieve quick order recommendation of the account
    account_recommendation = get_recommendation_by_account(account_id, zone, environment, 'QUICK_ORDER')
    
    if account_recommendation == 'not_found' or account_recommendation == 'false':
        return 'false'
    else: 
        # Retrieve combos type discount of the account
        request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

        request_url = get_microservice_base_url(environment, 'true') + '/combos/?accountID={0}&types=D&includeDeleted' \
                                                                       '=false&includeDisabled=false'.format(account_id)

        response = place_request('GET', request_url, '', request_headers)

        if response.status_code == 200:
            combos_data = loads(response.text)
            combos_discount = combos_data['combos']
            combos_id = list()

            for i in range(len(combos_discount)):
                dict_combos = {
                    'id': combos_discount[i]['id'],
                    'quantity': 1,
                    'score': 100,
                    'type': 'HISTORICAL'
                }
                combos_id.append(dict_combos)
        else:
            print(text.Red + '\n- [Combos Service] Failure to retrieve combos. Response Status: {0}. Response message:'
                             ' {1}'.format(response.status_code, response.text))
            return 'false'

        updated_recommendation = update_value_to_json(account_recommendation, 'content[0].combos', combos_id)
        updated_recommendation = convert_json_to_string(updated_recommendation['content'])

        # Define headers
        request_headers = get_header_request_recommender(zone, environment)

        # Define url request 
        request_url = get_microservice_base_url(environment) + '/global-recommendation-relay'

        # Send request
        response = place_request('POST', request_url, updated_recommendation, request_headers)

        if response.status_code == 202:
            return 'success'
        else:
            print(text.Red + '\n- [Recommendation Relay Service] Failure to retrieve combos. Response Status: {0}. '
                             'Response message: {1}'.format(response.status_code, response.text))
            return 'false'
