import json
from json import loads
import os
from tabulate import tabulate
from data_mass.common import get_header_request, get_microservice_base_url, \
    convert_json_to_string, place_request, update_value_to_json, finish_application
from data_mass.classes.text import text


def request_inventory_creation(zone, environment, account_id, delivery_center_id, products, sku_id=None, sku_quantity=0):
    # Get headers
    request_headers = get_header_request(zone, False, False, True)

    # Get URL
    request_url = '{0}/inventory-relay/add'.format(get_microservice_base_url(environment))

    # Get request body
    request_body = get_inventory_payload(zone, environment, account_id, products, delivery_center_id, sku_id, sku_quantity)

    # Send request
    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
        return True
    else:
        print('\n{0}- [Inventory Relay Service] Failure to add stock for products. Response Status: {1}. Response message: {2}'
              .format(text.Red, response.status_code, response.text))
        return False


def get_inventory_payload(zone, environment, account_id, products, delivery_center_id, sku_id, sku_quantity):
    get_inventory_response = get_delivery_center_inventory(environment, zone, account_id, delivery_center_id, products)
    if get_inventory_response != 'not_found':
        inv = get_inventory_response['inventory']

    quantity = 999999
    if int(sku_quantity) >= 0:
        specific_quantity = int(sku_quantity)

    inventory_list = list()
    for product in products:
        if sku_id is not None:
            if sku_id == product:
                specific_inventory = {
                    'sku': sku_id,
                    'quantity': specific_quantity
                }
                inventory_list.append(specific_inventory)
            else:
                current_inventory = {
                    'sku': inv[products.index(product)]['sku'],
                    'quantity': inv[products.index(product)]['quantity']
                }
                inventory_list.append(current_inventory)
        else:
            default_inventory = {
                'sku': product,
                'quantity': quantity
            }
            inventory_list.append(default_inventory)

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/create_inventory_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'fulfillmentCenterId': delivery_center_id,
        'inventory': inventory_list
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    return request_body


def display_inventory_by_account(inventory):
    inventory_info = list()
    if len(inventory) == 0:
        inventory_values = {
            'Inventory': 'None'
        }
        inventory_info.append(inventory_values)
    else:
        for i in range(len(inventory['inventory'])):
            inventory_values = {
                'sku': inventory['inventory'][i]['sku'],
                'quantity': inventory['inventory'][i]['quantity']
            }
            inventory_info.append(inventory_values)

    print(text.default_text_color + '\nInventory/stock information ')
    print(tabulate(inventory_info, headers='keys', tablefmt='grid'))


def get_delivery_center_inventory(environment, zone, account_id, delivery_center_id, products):
    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/get_inventory_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for i in range(len(products)):
        dict_values = {
            'fulfillmentCenterId': delivery_center_id,
            'skus': products
        }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Define headers
    request_headers = get_header_request(zone, True, False, False, False, account_id)

    # Define url request
    request_url = '{0}/inventory/'.format(get_microservice_base_url(environment))

    response = place_request('POST', request_url, request_body, request_headers)
    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 404:
        return 'not_found'
    else:
        print('\n{0}- [Inventory Service] Failure to retrieve inventory information. Response Status: {1}. Response message: {2}'
              .format(text.Red, response.status_code, response.text))
        return False
