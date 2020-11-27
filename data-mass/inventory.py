# Standard library imports
from json import loads
from multiprocessing import Pool
from itertools import repeat

# Third party imports
from tabulate import tabulate

# Local application imports
from common import get_header_request, get_microservice_base_url, convert_json_to_string, place_request
from products import request_get_account_product_assortment, check_item_enabled, get_sku_name, request_get_products_microservice
from classes.text import text


# Show all available SKUs of the account in the screen
def display_available_products_account(account_id, zone, environment, delivery_center_id):
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
                quantity_enabled_skus = len(enabled_skus)
                with Pool(20) as pool:
                    sku_name = pool.starmap(get_sku_name, zip(repeat(zone), repeat(environment), enabled_skus))

                stock_option = input(text.Yellow + '\nDo you want to choose which product will have the stock updated? '
                                                   '\nIf you don\'t, stock will be added to all products linked to your '
                                                   'account (1. Yes / 2. No): ')

                while stock_option != '1' and stock_option != '2':
                    print(text.Red + '\n- Invalid option')
                    stock_option = input(
                        text.Yellow + '\nDo you want to choose which product will have the stock updated? '
                                      '\nIf don\'t, stock will be added to all products linked to your account'
                                      ' (1. Yes / 2. No): ')

                if stock_option == '2':
                    update_sku = update_sku_inventory_microservice(zone, environment, delivery_center_id,
                                                                   enabled_skus)
                else:
                    # Show all the enabled SKUs and its respective names on the screen
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
                                                             'inventory: ')

                    while validate_sku(sku_id.strip(), enabled_skus) != 'true':
                        print(text.Red + '\n- Invalid SKU. Please check the list above and try again.')
                        sku_id = input(
                            text.default_text_color + '\n Type here the SKU from the list above you want to add '
                                                      'inventory: ')

                    sku_quantity = input(text.default_text_color + '\n Type here the quantity you want to add to it: ')

                    while not sku_quantity.isdigit():
                        print(text.Red + '\n- Invalid option.')
                        sku_quantity = input(
                            text.default_text_color + '\n Type here the quantity you want to add to it: ')

                    update_sku = update_sku_inventory_microservice(zone, environment, delivery_center_id,
                                                                   enabled_skus, sku_id, sku_quantity)

                if update_sku == 'true':
                    return 'true'
                else:
                    return 'false'
            else:
                return 'error_len'
        else:
            return product_offers
    else:
        return 'false'




# Update SKU inventory
def update_sku_inventory_microservice(zone, environment, delivery_center_id, list_skus, sku_id=None, sku_quantity=0):
    # Define headers
    request_headers = get_header_request(zone, 'false', 'false', 'true')

    # Define url request
    request_url = get_microservice_base_url(environment) + '/inventory-relay/add'

    quantity = 999999
    if int(sku_quantity) >= 0:
        specific_quantity = int(sku_quantity)

    inventory_list = []
    index = 0
    while index < len(list_skus):
        if sku_id is not None:
            if sku_id == list_skus[index]:
                specific_inventory = {
                    'sku': sku_id,
                    'quantity': specific_quantity
                }
                inventory_list.append(specific_inventory)
            else:
                inventory_data = {
                    'sku': list_skus[index],
                    'quantity': quantity
                }
                inventory_list.append(inventory_data)
        else:
            inventory_data = {
                'sku': list_skus[index],
                'quantity': quantity
            }
            inventory_list.append(inventory_data)

        index = index + 1

    dict_values = {
        'fulfillmentCenterId': delivery_center_id,
        'inventory': inventory_list
    }

    # Create body
    request_body = convert_json_to_string(dict_values)

    # Send request
    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'true'
    else:
        print(text.Red + '\n- [Inventory Relay Service] Failure to add stock for products. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


# Validate SKU inventory
def validate_sku(sku_id, enabled_skus):
    aux_index = 0

    while aux_index < len(enabled_skus):
        if enabled_skus[aux_index] == sku_id:
            return 'true'
        aux_index = aux_index + 1


def display_inventory_by_account(zone, environment, abi_id, delivery_center_id):
    product_offers = request_get_account_product_assortment(abi_id, zone, environment, delivery_center_id)
    if len(product_offers) != 0:
        dict_values = {
            'fulfillmentCenterId': delivery_center_id,
            'skus': product_offers
        }
        request_body = convert_json_to_string(dict_values)
        response = get_delivery_center_inventory(environment, zone, request_body)

        json_data = loads(response.text)
        inventory_info = list()

        if len(json_data) == 0:
            inventory_values = {
                'Inventory': 'None'
            }
            inventory_info.append(inventory_values)
        else:
            for i in range(len(json_data['inventory'])):
                inventory_values = {
                    'sku': json_data['inventory'][i]['sku'],
                    'quantity': json_data['inventory'][i]['quantity']
                }
                inventory_info.append(inventory_values)

            print(text.default_text_color + '\nInventory - Sku and Inventory from one account ')
            print(tabulate(inventory_info, headers='keys', tablefmt='grid'))


def get_delivery_center_inventory(environment, zone, request_body):
    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false')

    # Define url request
    request_url = get_microservice_base_url(environment) + '/inventory/'

    response = place_request('POST', request_url, request_body, request_headers)

    return response
