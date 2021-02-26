# Standard library imports
from json import loads
from multiprocessing import Pool
from itertools import repeat


# Third party imports
from tabulate import tabulate

# Local application imports
from common import convert_json_to_string, get_header_request, get_microservice_base_url, place_request, return_first_and_last_date_year_payload, update_value_to_json
from products import request_get_account_product_assortment, check_item_enabled, get_sku_name, \
    request_get_products_microservice
from classes.text import text
import os
import json


# Show all available SKUs of the account in the screen
def display_available_products(account_id, zone, environment, delivery_center_id):
    # Retrieve all SKUs for the specified Account and DeliveryCenter IDs
    product_offers = request_get_account_product_assortment(account_id, zone, environment, delivery_center_id)
    # Retrieve all SKUs for the specified Zone
    products = request_get_products_microservice(zone, environment)
    if products != 'false':
        products_list = list()
        for sku in products:
            products_list.append(sku['sku'])

        valid_products = list(set(product_offers).intersection(products_list))

        if isinstance(product_offers, list):
            # Check if the SKU is enabled
            enabled_skus = list()
            if len(product_offers):
                with Pool(20) as pool:
                    enabled_skus = pool.starmap(check_item_enabled,
                                                zip(valid_products, repeat(zone), repeat(environment)))

            # Get SKU name
            if len(enabled_skus) > 0:
                print(text.default_text_color + '\n Wait. We are bringing the available products: ')
                quantity_enabled_skus = len(enabled_skus)
                with Pool(20) as pool:
                    sku_name = pool.starmap(get_sku_name, zip(repeat(zone), repeat(environment), enabled_skus))

                    aux_index = 0

                    while aux_index < quantity_enabled_skus:
                        if enabled_skus[aux_index] == 'false':
                            aux_index = aux_index + 1
                        else:
                            print(
                                text.default_text_color + '\n SKU: ' + text.Blue + enabled_skus[aux_index] + '  ||  ' +
                                sku_name[aux_index].upper())
                            aux_index = aux_index + 1

                    sku_id = input(text.default_text_color + '\n Type here the SKU from the list above you want to add '
                                                             'SKU Limit: ')

                    while validate_sku(sku_id.strip(), enabled_skus) != 'true':
                        print(text.Red + '\n- Invalid SKU. Please check the list above and try again.')
                        sku_id = input(
                            text.default_text_color + '\n Type here the SKU from the list above you want to add '
                                                      'SKU Limit: ')

                    sku_quantity = input(text.default_text_color + '\n Type here the quantity you want to add to it: ')

                    while not sku_quantity.isdigit():
                        print(text.Red + '\n- Invalid option.')
                        sku_quantity = input(
                            text.default_text_color + '\n Type here the quantity you want to add to it: ')

                    update_sku_limit = update_sku_limit_enforcement_microservice(zone, environment, account_id,
                                                                                sku_id, sku_quantity)

                if update_sku_limit == 'true':
                    return 'true'
                else:
                    return 'false'
            else:
                return 'error_len'
        else:
            return product_offers
    else:
        return 'false'


# Update SKU Limit
def update_sku_limit_enforcement_microservice(zone, environment, account_id, sku_id=None, sku_quantity=0):

    # Define url request
    request_url = get_microservice_base_url(environment) + '/enforcement-relay-service/'

    # Get start and end dates
    dates_payload = return_first_and_last_date_year_payload()

    # Create dictionary with sku limits values
    dict_values = {
        'accounts': [account_id],
        'enforcements[0].entityId': sku_id,
        'enforcements[0].startDate': dates_payload['startDate'] + 'T00:00:00.000Z',
        'enforcements[0].endDate': dates_payload['endDate'] + 'T00:00:00.000Z',
        'enforcements[0].limits[0].value': int(sku_quantity)
    }

    # Define headers
    request_headers = get_header_request(zone, 'false', 'false', 'false', 'false')

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/update_sku_limit_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'true'
    else:
        print(text.Red + '\n- [Enforcement Relay Service] Failure to add SKU Limit. Response Status: '
                         '{response_status}. Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return 'false'


# Validate SKU
def validate_sku(sku_id, enabled_skus):
    aux_index = 0

    while aux_index < len(enabled_skus):
        if enabled_skus[aux_index] == sku_id:
            return 'true'
        aux_index = aux_index + 1
