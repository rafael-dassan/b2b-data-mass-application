import json
import logging
from json import loads
from random import randint
from time import time
from typing import Dict, List, Union
from urllib.parse import urlencode
from uuid import uuid1

import pkg_resources
from tabulate import tabulate

from data_mass.account.accounts import check_account_exists_microservice
from data_mass.classes.text import text
from data_mass.common import (
    convert_json_to_string,
    create_list,
    get_header_request,
    get_microservice_base_url,
    place_request,
    resources_warning,
    set_to_dictionary,
    update_value_to_json
)
from data_mass.config import get_settings

logger = logging.getLogger(__name__)

COUNTRIES_ES = ["AR", "CO", "DO", "EC", "MX", "PA", "PE", "PY", "SV", "UY"]


def create_all_recommendations(zone, environment, account_id, products):
    # Get responses
    quick_order_response = request_quick_order(
        zone=zone,
        environment=environment,
        account_id=account_id,
        products=products
    )
    sell_up_response = request_sell_up(
        zone=zone,
        environment=environment,
        account_id=account_id,
        products=products
    )
    forgotten_items_response = request_forgotten_items(
        zone=zone,
        environment=environment,
        account_id=account_id,
        products=products
    )
    

    if quick_order_response and sell_up_response and forgotten_items_response:
        return True

    return False


def create_list_product_items(
        product_list: List) -> List[Dict[str, Union[int, str]]]:
    """
    Create a list of dicts using the list of skus.

    Parameters
    ----------
    product_list : list
        a list of skus.

    Returns
    -------
    list
        A list of dicts.
    """
    items_list = []
    for product in product_list:
        items_values = {
            "sku": product,
            "quantity": randint(1, 10),
            "score":  product_list.index(product) + 1,
            "type": "clustering",
            "discount": 0
        }
        items_list.append(items_values)
    return items_list


def create_quick_order_payload(
        account_id: str,
        zone: str,
        environment: str,
        product_list: list) -> dict:
    """
    Define JSON to submit QUICK ORDER recommendation type

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str
    product_list : list

    Returns
    -------
    dict
        A `payload` for quick order creation.
    """
    if zone in COUNTRIES_ES:
        language = 'es'
        text = 'Pedido Fácil'
        text_description = 'Productos que ordenaste anteriormente <link>Añadir todo al camión</link>'
    elif zone == 'BR':
        language = 'pt'
        text = 'Pedido Facil'
        text_description = 'Produtos comprados anteriormente <link>Adicionar todos itens ao carrinho</link>'
    else:
        language = "en"
        text = "Quick Order"
        text_description = "Products ordered before <link>Add all items to cart</link>"

    items = create_list_product_items(product_list)

    dict_values = {
        'recommendationId': f'DM-{zone}-{str(randint(1, 100000))}',
        'useCase': 'QUICK_ORDER',
        'useCaseId': account_id,
        'items': items,
        'descriptions': [{
            'language': language,
            'text': text,
            'description': text_description
        }],
        'combos': None
    }

    if zone == "US":
        resources_warning()
        settings = get_settings()
        dict_values.update({"vendorId": settings.vendor_id})
    else:
        account, = check_account_exists_microservice(account_id, zone, environment)
        dict_values.update({"vendorId": account.get("vendorId")})

    # Create file path
    content = pkg_resources.resource_string(
        "data_mass",
        "data/create_beer_recommender_payload.json"
    )

    json_data = json.loads(content.decode("utf-8"))

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    return request_body


def create_forgotten_items_payload(
        account_id: str,
        zone: str,
        environment: str,
        product_list: list) -> dict:
    """
    Define JSON to submit FORGOTTEN ITEMS recommendation type

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str
    product_list : list

    Returns
    -------
    dict
        A `payload` for forgotten items creation.
    """
    if zone in COUNTRIES_ES:
        language = 'es'
        text = '¡Socio! Complete tu order'
        text_description = 'Clientes como tu tambíen compraron'
    elif zone == 'BR':
        language = 'pt'
        text = 'Produtos Populares para Negocios como o seu'
        text_description = ''
    else:
        language = 'en'
        text = 'Popular Products for Businesses like yours'
        text_description = ''

    items = create_list_product_items(product_list)

    dict_values = {
        'recommendationId': f'DM-{zone}-{str(randint(1, 100000))}',
        'useCase': 'FORGOTTEN_ITEMS',
        'useCaseId': account_id,
        'descriptions': [{
            'language': language,
            'text': text,
            'description': text_description,
        }],
        'combos': None
    }

    if zone == "US":
        resources_warning()
        settings = get_settings()
        dict_values.update({"vendorId": settings.vendor_id})
    else:
        account, = check_account_exists_microservice(account_id, zone, environment)
        dict_values.update({"vendorId": account.get("vendorId")})

    set_to_dictionary(dict_values, 'items', items)

    content = pkg_resources.resource_string(
        "data_mass",
        "data/create_beer_recommender_payload.json"
    )

    json_data = json.loads(content.decode("utf-8"))

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    return request_body


# Define JSON to submit UP SELL recommendation type
def create_upsell_payload(account_id, zone, environment, product_list):

    if zone in COUNTRIES_ES:
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

    items = create_list_product_items(product_list)

    dict_values = {
        'recommendationId': f'DM-{zone}-{str(randint(1, 100000))}',
        'descriptions': [{
            'language': language,
            'text': text,
            'description': text_description
        }],
        'useCaseId': account_id
    }

    if zone == "US":
        resources_warning()
        settings = get_settings()
        dict_values.update({"vendorId": settings.vendor_id})
    else:
        account, = check_account_exists_microservice(account_id, zone, environment)
        dict_values.update({"vendorId": account.get("vendorId")})

    set_to_dictionary(dict_values, 'items', items)

    # get data from Data Mass files
    content = pkg_resources.resource_string(
        "data_mass",
        "data/create_beer_recommender_sell_up_payload.json"
    )
    json_data = json.loads(content.decode("utf-8"))

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
    request_body = create_quick_order_payload(
        account_id=account_id,
        zone=zone,
        environment=environment,
        product_list=products
    )

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return True
    else:
        print(text.Red + '\n- [Recommendation Relay Service] Failure to add recommendation. Response Status: {}. '
                         'Response message: {}'.format(response.status_code, response.text))
        return False


def request_forgotten_items(zone, environment, account_id, products):
    # Define headers
    request_headers = get_header_request_recommender(zone, environment)

    # Define url request
    base_url = get_microservice_base_url(environment)
    request_url =  f"{base_url}/global-recommendation-relay"

    # Get body
    request_body = create_forgotten_items_payload(account_id, zone, environment, products)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return True
    else:
        print(text.Red + '\n- [Recommendation Relay Service] Failure to add recommendation. Response Status: {}. '
                         'Response message: {}'.format(response.status_code, response.text))
        return False


def request_sell_up(zone, environment, account_id, products):
    # Define headers
    request_headers = get_header_request_recommender(zone, environment)

    # Define url request
    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/global-recommendation-relay"

    # Get body
    request_body = create_upsell_payload(account_id, zone, environment, products)

    # Send request
    response = place_request(
        'POST', request_url, request_body, request_headers
    )

    if response.status_code == 202:
        return True

    print(
        f"{text.Red}- [Recommendation Relay Service] Failure to add "
        f"recommendation.\n Response Status: {response.status_code}.\n"
        f"Response message: {response.text}."
    )
    return False


# Define an exclusive header for Recommended Products
def get_header_request_recommender(zone, environment):
    # Define headers
    if environment == 'SIT' or environment == 'DEV':
        request_headers = get_header_request(zone, False, True)
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
            'SV': 'America/San_Salvador',
            'US': 'America/New_York',
            'ZA': 'Africa/Johannesburg',
            'UY': 'America/Montevideo',
            'TZ': 'Africa/Dar_es_Salaam'
        }
        timezone = switcher.get(zone, False)

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


def get_recommendation_by_account(
        account_id: str,
        zone: str,
        environment: str,
        use_case: list):
    headers = get_header_request(zone, True, False, False, False, account_id)

    base_url = get_microservice_base_url(environment, True)
    query: dict = {"useCaseId": account_id}
    case_query: list = []

    for case in use_case:
        case_query.append(("useCase", case))

    if zone == "US":
        resources_warning()
        settings = get_settings()
        query.update({"vendorId": settings.vendor_id})

    request_url = f"{base_url}/global-recommendation/?{urlencode(query)}&{urlencode(case_query)}&useCaseType=ACCOUNT"
    response = place_request('GET', request_url, '', headers)
    recommendation_data = loads(response.text)

    if response.status_code == 200:
        content = recommendation_data['content']

        if content:
            return recommendation_data

        print(
            f"{text.Yellow}- [Global Recommendation Service] "
            f"The account {account_id} does not contains any "
            f"recommendation type: {use_case}."
        )

        return 'not_found'

    print(
        f"{text.Red}- [Global Recommendation Service] "
        "Failure to retrieve recommendation.\n"
        f"Response Status: {response.status_code}.\n"
        f"Response message: {response.text}."
    )
    return False


def delete_recommendation_by_id(environment, recommendation_data, zone, account_id):
    recommendation_id = recommendation_data['content'][0]['id']

    headers = get_header_request(zone, True, False, False, False, account_id)

    # headers = {
    #     'requestTraceId': str(uuid1()),
    #     'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3Nlc'
    #                      'nZpY2VzIiwiZXhwIjoxNjE2MjM5MDIyLCJpYXQiOjE1MTYyMzkwMjIsInVwZGF0ZWRfYXQiOjExMTExMTEsIm5hbWUiOi'
    #                      'J1c2VyQGFiLWluYmV2LmNvbSIsImFjY291bnRJRCI6IiIsInVzZXJJRCI6IjIxMTgiLCJyb2xlcyI6WyJST0xFX0FETUl'
    #                      'OIl19.Hpthi-Joez6m2lNiOpC6y1hfPOT5nvMtYdNnp5NqVTM'
    # }

    base_url = get_microservice_base_url(environment, True)
    request_url = f"{base_url}/global-recommendation/{recommendation_id}"
    response = place_request('DELETE', request_url, '', headers)

    if response.status_code == 202:
        return True

    print(
        f"{text.Red}\n"
        "- [Global Recommendation Service] Failure to delete recommendation.\n"
        f"Response Status: {response.status_code}.\n"
        f"Response message: {response.text}\n"
    )

    return False


def display_recommendations_by_account(data):
    recommendations = data['content']
    recommender_list = []
    items_list = []
    combo_list = []

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
    print(tabulate(recommender_list, headers='keys', tablefmt='fancy_grid'))

    print(text.default_text_color + '\nItems Recommendations Information By Account')
    print(tabulate(items_list, headers='keys', tablefmt='fancy_grid'))

    print(text.default_text_color + '\nCombos Recommendations Information By Account')
    print(tabulate(combo_list, headers='keys', tablefmt='fancy_grid'))


def input_combos_quick_order(zone, environment, account_id):
    # Retrieve quick order recommendation of the account
    account_recommendation = get_recommendation_by_account(account_id, zone, environment, ['QUICK_ORDER'])

    if account_recommendation == 'not_found' or not account_recommendation:
        return False
    else:
        # Retrieve combos type discount of the account
        request_headers = get_header_request(zone, True, False, False, False, account_id)
        base_url = get_microservice_base_url(environment, True)

        request_url = (
            f'{base_url}'
            f'/combos/?accountID={account_id}'
            '&types=D&includeDeleted'
            '=false&includeDisabled=false'
        )

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
            print(text.Red + '\n- [Combos Service] Failure to retrieve combos. Response Status: {}. Response message:'
                             ' {}'.format(response.status_code, response.text))
            return False

        updated_recommendation = update_value_to_json(account_recommendation, 'content[0].combos', combos_id)
        updated_recommendation = convert_json_to_string(updated_recommendation['content'])

        # Define headers
        request_headers = get_header_request_recommender(zone, environment)

        # Define url request
        request_url = get_microservice_base_url(environment) + '/global-recommendation-relay'

        # Send request
        response = place_request('POST', request_url, updated_recommendation, request_headers)

        if response.status_code == 202:
            return True
        else:
            print(text.Red + '\n- [Recommendation Relay Service] Failure to retrieve combos. Response Status: {}. '
                             'Response message: {}'.format(response.status_code, response.text))
            return False
