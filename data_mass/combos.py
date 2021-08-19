import json
from json import loads
from random import randint

import pkg_resources

from data_mass.classes.text import text
# Local application imports
from data_mass.common import (
    convert_json_to_string,
    create_list,
    get_header_request,
    get_microservice_base_url,
    place_request,
    update_value_to_json
)
from data_mass.product.service import get_sku_price

CREATE_COMBO_PAYLOAD = "data/create_combo_payload.json"


def input_combo_type_discount(
        account_id,
        zone,
        environment,
        sku,
        discount_value,
        combo_id=None):

    if combo_id is None:
        combo_id = 'DM-' + str(randint(1, 100000))

    original_price = get_sku_price(account_id, sku, zone, environment)
    price = round(original_price - original_price * (discount_value/100), 2)
    score = randint(1, 100)
    combo_info = get_combo_information(zone, combo_id, 'DISCOUNT')
    title = combo_info['title']
    description = combo_info['description']

    # get data from Data Mass files
    content = pkg_resources.resource_string(
        "data_mass",
        CREATE_COMBO_PAYLOAD
    )
    json_data = json.loads(content.decode("utf-8"))

    dict_values = {
        'accounts': [account_id],
        'combos': [{
            'description': description,
            'startDate': '2020-01-01T00:00:00Z',
            'endDate': '2045-02-28T00:00:00Z',
            'id': combo_id,
            'items[0].sku': sku,
            'originalPrice': original_price,
            'price': price,
            'score': score,
            'title': title,
            "limit": {
                "daily": 200,
                "monthly": 200,
            },
            'type': 'D',
            'externalId': combo_id,
            'discountPercentOff': discount_value,
            'freeGoods': None
        }]
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Get base URL
    base_url = get_microservice_base_url(environment)
    request_url = f'{base_url}/combo-relay/accounts'

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get header request
    request_headers = get_header_request(
        zone,
        False,
        False,
        True,
        False,
        account_id)

    # Send requests
    create_combo_response = place_request(
        'POST',
        request_url,
        request_body,
        request_headers)

    update_consumption_response = update_combo_consumption(
        account_id,
        zone,
        environment,
        combo_id)

    if create_combo_response.status_code == 201:
        if update_consumption_response == 'success':
            return combo_id

        return False

    print(
        f'{text.Red}\n- [Combo Relay Service] Failure '
        'when creating a new combo. \n'
        f'Response status: {create_combo_response.status_code}. \n'
        f'Response message: {create_combo_response.text}'
    )
    return False


def input_combo_type_digital_trade(abi_id, zone, environment):

    # Get header request
    request_headers = get_header_request(zone, False, False, True, False)

    # Get base URL
    base_url = get_microservice_base_url(environment)
    request_url = base_url + '/combo-relay/accounts'

    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        CREATE_COMBO_PAYLOAD
    )
    json_data = json.loads(content.decode("utf-8"))

    combo_id = 'DM-DT-' + str(randint(1, 100000))

    dict_values = {
        'accounts': [abi_id],
        'combos': [{
            'id': combo_id,
            'externalId': combo_id,
            'title': combo_id + ' type digital trade',
            'description': combo_id + ' type digital trade',
            'startDate': '2020-01-01T00:00:00Z',
            'endDate': '2045-02-28T00:00:00Z',         
            'originalPrice': 0,
            'price': 0,
            'type': 'DT',
        }]
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Send request
    create_combo_response = place_request(
        'POST',
        request_url,
        request_body,
        request_headers
        )
    update_consumption_response = update_combo_consumption(
        abi_id,
        zone,
        environment,
        combo_id)

    if create_combo_response.status_code == 201:
        if update_consumption_response == 'success':
            return combo_id
        return False
    print(
        f'{text.Red}\n'
        '[Combo Relay Service] Failure when creating a new combo.\n'
        + f'Response Status: {create_combo_response.status_code}\n'
        + f'Response message: {create_combo_response.text}'
        )
    return False


def input_combo_type_free_good(
        account_id,
        zone,
        environment,
        sku,
        combo_id=None):
    if combo_id is None:
        combo_id = 'DM-' + str(randint(1, 100000))

    price = get_sku_price(account_id, sku, zone, environment)
    score = randint(1, 100)
    combo_info = get_combo_information(zone, combo_id, 'FREE_GOOD')
    title = combo_info['title']
    description = combo_info['description']

    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        CREATE_COMBO_PAYLOAD
    )
    json_data = json.loads(content.decode("utf-8"))

    dict_values = {
        'accounts': [account_id],
        'combos[0].description': description,
        'combos[0].id': combo_id,
        'combos[0].items[0].sku': sku,
        'combos[0].originalPrice': price,
        'combos[0].price': price,
        'combos[0].score': score,
        'combos[0].title': title,
        'combos[0].type': 'FG',
        'combos[0].externalId': combo_id,
        'combos[0].freeGoods.quantity': 1,
        'combos[0].freeGoods.skus': [sku]
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Get base URL
    base_url = get_microservice_base_url(environment)
    request_url = f'{base_url}/combo-relay/accounts'

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get header request
    request_headers = get_header_request(
        zone,
        False,
        False,
        True,
        False,
        account_id
    )

    # Send request
    create_combo_response = place_request(
        'POST',
        request_url,
        request_body,
        request_headers
    )

    update_consumption_response = update_combo_consumption(
        account_id,
        zone,
        environment,
        combo_id
    )

    if create_combo_response.status_code == 201:
        if update_consumption_response == 'success':
            return combo_id
        return False
    print(
        f'\n{text.Red}'
        '[Combo Relay Service] Failure when creating a new combo.\n'
        f'Response status: {create_combo_response.status_code}.\n'
        f'Response message: {create_combo_response.text}'
    )
    return False


def input_combo_only_free_good(
        account_id,
        zone,
        environment,
        sku,
        combo_id=None):

    if combo_id is None:
        combo_id = 'DM-' + str(randint(1, 100000))

    score = randint(1, 100)
    combo_info = get_combo_information(zone, combo_id, 'FREE_GOOD')
    title = combo_info['title']
    description = combo_info['description']

    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        CREATE_COMBO_PAYLOAD
    )
    json_data = json.loads(content.decode("utf-8"))

    dict_values = {
        'accounts': [account_id],
        'combos[0].description': description,
        'combos[0].id': combo_id,
        'combos[0].items': None,
        'combos[0].score': score,
        'combos[0].title': title,
        'combos[0].type': 'FG',
        'combos[0].externalId': combo_id,
        'combos[0].freeGoods.quantity': 1,
        'combos[0].freeGoods.skus': [sku]
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(
            json_data,
            key,
            dict_values[key]
        )

    # Get base URL
    base_url = get_microservice_base_url(environment)
    request_url = f'{base_url}/combo-relay/accounts'

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get header request
    request_headers = get_header_request(zone, False, False, True, False)

    # Send request
    create_combo_response = place_request(
        'POST',
        request_url,
        request_body,
        request_headers
    )
    update_consumption_response = update_combo_consumption(
        account_id,
        zone,
        environment,
        combo_id
    )

    if create_combo_response.status_code == 201:
        if update_consumption_response == 'success':
            return combo_id
        return False
    print(
        f'\n{text.Red}- \n'
        '[Combo Relay Service] Failure when creating a new combo. '
        f'Response status: {create_combo_response.status_code}. '
        f'Response message: {create_combo_response.text}'
    )
    return False


# Turn combo quantity available
def update_combo_consumption(abi_id, zone, environment, combo_id):
    # Get base URL
    base_url = get_microservice_base_url(environment)
    request_url = base_url + '/combo-relay/consumption'

    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/update_combo_consumption_payload.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    dict_values = {
        'accountId': abi_id,
        'combos[0].comboId': combo_id
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    request_headers = get_header_request(zone, False, False, True, False)

    response = place_request(
        'POST',
        request_url,
        request_body,
        request_headers
    )

    if response.status_code == 201:
        return 'success'
    print(
        f'{text.Red} \n'
        '[Combo Relay Service] Failure to update combo consumption.'
        f'Response Status: {response.status_code}'
        f'Response message: {response.text}'
    )
    return False


def check_combo_exists_microservice(account_id, zone, environment, combo_id):
    # Get header request
    request_headers = get_header_request(
        zone,
        True,
        False,
        False,
        False,
        account_id
    )

    # Get base URL
    request_url = get_microservice_base_url(environment) \
        + '/combos/?accountID=' + account_id \
        + '&comboIds=' + combo_id \
        + '&includeDeleted=false&includeDisabled=false'

    # Place request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        print(
            f'{text.Red} \n'
            f'[Combo Service] The combo {combo_id} does not exist'
        )
        return False
    print(
        f'{text.Red} + \n'
        '[Combo Service] Failure to retrieve the combo.'
        f'Response Status: {response.status_code}'
        f'Response message {response.text}'
    )
    return False


def get_combo_information(zone, combo_id, combo_type):
    zones_es = ['AR', 'CO', 'DO', 'EC', 'MX', 'PE']
    zones_en = ['ZA']

    if zone in zones_es:
        combo_info = {
            'DISCOUNT': {
                'title': combo_id,
                'description': 'Obtienes descuentos en\
                la compra de este combo'
            },
            'FREE_GOOD': {
                'title': combo_id,
                'description': 'Obtienes un producto gratis\
                 con la compra de este combo'
            }
        }
    elif zone in zones_en:
        combo_info = {
            'DISCOUNT': {
                'title': combo_id,
                'description': 'You get discounts \
                 on the purchase of this combo'
            },
            'FREE_GOOD': {
                'title': combo_id,
                'description': 'You get one product for \
                free on the purchase of this combo'
            }
        }
    else:
        combo_info = {
            'DISCOUNT': {
                'title': combo_id,
                'description': 'Voce ganha descontos na compra deste combo'
            },
            'FREE_GOOD': {
                'title': combo_id,
                'description': 'Na compra de um produto \
                 voce ganha outro neste combo'
            }
        }
    return combo_info[combo_type]
