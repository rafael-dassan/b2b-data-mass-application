from json import dumps
from random import randint
from common import *
from classes.text import text


def input_combo_type_discount(abi_id, zone, environment, sku, discount_value):
    combo_id = 'DM-' + str(randint(1, 100000))
    
    # Get base URL
    request_url = get_microservice_base_url(environment) + '/combo-relay/accounts'
    
    original_price = get_sku_price(abi_id, sku, zone, environment)
    price = round(original_price - original_price * (discount_value/100), 2)
    score = randint(1, 100)

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_combo_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'accounts': [abi_id],
        'combos[0].description': combo_id + ' type discount',
        'combos[0].id': combo_id,
        'combos[0].items[0].sku': sku,
        'combos[0].originalPrice': original_price,
        'combos[0].price': price,
        'combos[0].score': score,
        'combos[0].title': combo_id + ' type discount',
        'combos[0].type': 'D',
        'combos[0].externalId': combo_id,
        'combos[0].discountPercentOff': discount_value,
        'combos[0].freeGoods': None
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get header request
    request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

    # Send requests
    create_combo_response = place_request('POST', request_url, request_body, request_headers)
    update_consumption_response = update_combo_consumption(abi_id, zone, environment, combo_id)

    if create_combo_response.status_code == 201:
        if update_consumption_response == 'success':
            return combo_id
        else:
            return 'false'
    else:
        print(text.Red + '\n- [Combo Relay Service] Failure when creating a new combo. Response Status: '
                    + str(create_combo_response.status_code) + '. Response message ' + create_combo_response.text) 
        return 'false'


def input_combo_type_digital_trade(abi_id, zone, environment):
    
    # Get header request
    request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/combo-relay/accounts'

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_combo_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    combo_id = 'DM-DT-' + str(randint(1, 100000))

    dict_values = {
        'accounts[0]': abi_id,
        'combos[0].id': combo_id,
        'combos[0].externalId': combo_id,
        'combos[0].title': combo_id + ' type digital trade',
        'combos[0].description': combo_id + ' type digital trade',
        'combos[0].originalPrice': 0,
        'combos[0].price': 0,
        'combos[0].type': 'DT',
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Send request
    create_combo_response = place_request('POST', request_url, request_body, request_headers)
    update_consumption_response = update_combo_consumption(abi_id, zone, environment, combo_id)

    if create_combo_response.status_code == 201:
        if update_consumption_response == 'success':
            return combo_id
        else:
            return 'false'
    else:
        print(text.Red + '\n- [Combo Relay Service] Failure when creating a new combo. Response Status: '
                        + str(create_combo_response.status_code) + '. Response message ' + create_combo_response.text)
        return 'false'


def input_combo_type_free_good(abi_id, zone, environment, sku):
    combo_id = 'DM-' + str(randint(1, 100000))

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/combo-relay/accounts'

    price = get_sku_price(abi_id, sku, zone, environment)
    score = randint(1, 100)

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_combo_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'accounts': [abi_id],
        'combos[0].description': combo_id + ' type free good',
        'combos[0].id': combo_id,
        'combos[0].items[0].sku': sku,
        'combos[0].originalPrice': price,
        'combos[0].price': price,
        'combos[0].score': score,
        'combos[0].title': combo_id + ' type free good',
        'combos[0].type': 'FG',
        'combos[0].externalId': combo_id,
        'combos[0].freeGoods.quantity': 1,
        'combos[0].freeGoods.skus': [sku]
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get header request
    request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

    # Send request
    create_combo_response = place_request('POST', request_url, request_body, request_headers)
    update_consumption_response = update_combo_consumption(abi_id, zone, environment, combo_id)

    if create_combo_response.status_code == 201:
        if update_consumption_response == 'success':
            return combo_id
        else:
            return 'false'
    else:
        print(text.Red + '\n- [Combo Relay Service] Failure when creating a new combo. Response Status: '
                    + str(create_combo_response.status_code) + '. Response message ' + create_combo_response.text) 


def input_combo_free_good_only(abi_id, zone, environment, sku):
    combo_id = 'DM-' + str(randint(1, 100000))
    score = randint(1, 100)

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/combo-relay/accounts'

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_combo_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'accounts': [abi_id],
        'combos[0].description': combo_id + ' with free good only',
        'combos[0].id': combo_id,
        'combos[0].items': None,
        'combos[0].score': score,
        'combos[0].title': combo_id + ' with free good only',
        'combos[0].type': 'FG',
        'combos[0].externalId': combo_id,
        'combos[0].freeGoods.quantity': 1,
        'combos[0].freeGoods.skus': [sku]
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get header request
    request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

    # Send request
    create_combo_response = place_request('POST', request_url, request_body, request_headers)
    update_consumption_response = update_combo_consumption(abi_id, zone, environment, combo_id)

    if create_combo_response.status_code == 201:
        if update_consumption_response == 'success':        
            return combo_id
        else:
            return 'false'
    else:
        print(text.Red + '\n- [Combo Relay Service] Failure when creating a new combo. Response Status: '
                    + str(create_combo_response.status_code) + '. Response message ' + create_combo_response.text) 


# Turn combo quantity available
def update_combo_consumption(abi_id, zone, environment, combo_id):
    # Get base URL
    request_url = get_microservice_base_url(environment) + '/combo-relay/consumption'

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/update_combo_consumption_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'accountId': abi_id,
        'combos[0].comboId': combo_id
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 201:
        return 'success'
    else:
        print(text.Red + '\n- [Combo Relay Service] Failure to update combo consumption. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def check_combo_exists_microservice(abi_id, zone, environment, combo_id):
    # Get header request
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/combos/?accountID=' + abi_id + '&comboIds=' + combo_id \
                  + '&includeDeleted=false&includeDisabled=false'

    # Place request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        print(text.Red + '\n- [Combo Service] The combo ' + combo_id + ' does not exist')
        return 'false'
    else:
        print(text.Red + '\n- [Combo Service] Failure to retrieve the combo. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'
