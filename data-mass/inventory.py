from json import loads
from tabulate import tabulate
from products import request_get_account_product_assortment, check_item_enabled, get_sku_name
from classes.text import text
from common import get_header_request, get_microservice_base_url, convert_json_to_string, place_request, \
    check_sku_by_account


# Show all available SKUs of the account in the screen
def display_available_products_account(account_id, zone, environment, delivery_center_id):
    # Retrieve all SKUs for the specified Account and DeliveryCenter IDs
    product_offers = request_get_account_product_assortment(account_id, zone, environment, delivery_center_id)

    print(text.default_text_color + '\n[Inventory] Checking enabled products available in the account ' + account_id +
          '. It may take a while...')

    enabled_skus = list()
    aux_index = 0

    while aux_index < len(product_offers):
        # Check if the SKU is enabled on Items MS
        sku_enable = check_item_enabled(product_offers[aux_index], zone, environment, True)

        while not sku_enable:
            if aux_index <= (len(product_offers) - 1):
                aux_index = aux_index + 1
                sku_enable = check_item_enabled(product_offers[aux_index], zone, environment, True)

        enabled_skus.append(sku_enable)
        aux_index = aux_index + 1

    if len(enabled_skus) > 0:
        quantity_enabled_skus = len(enabled_skus)

        # Store the name of all enabled SKUs
        sku_description = list()
        aux_index = 0

        while aux_index < quantity_enabled_skus:
            sku_description.append(get_sku_name(zone, environment, enabled_skus[aux_index]))
            aux_index = aux_index + 1

    # Check if the account has at least one SKU enabled on it
    if len(enabled_skus) > 0:

        stock_option = input(text.Yellow + '\nDo you want to choose which product will have the stock updated? '
                                           '\nIf you don\'t, stock will be added to all products linked to your '
                                           'account (1. Yes / 2. No): ')

        while stock_option != '1' and stock_option != '2':
            print(text.Red + '\n- Invalid option')
            stock_option = input(text.Yellow + '\nDo you want to choose which product will have the stock updated? '
                                               '\nIf don\'t, stock will be added to all products linked to your account'
                                               ' (1. Yes / 2. No): ')

        if stock_option == '2':
            update_sku = update_sku_inventory_microservice(zone, environment, delivery_center_id,
                                                           enabled_skus)
        else:
            # Show all the enabled SKUs and its respective names on the screen
            aux_index = 0

            while aux_index < quantity_enabled_skus:
                print(text.default_text_color + '\n SKU: ' + text.Blue + enabled_skus[aux_index] + '  ||  ' +
                      sku_description[aux_index].upper())
                aux_index = aux_index + 1

            sku_id = input(text.default_text_color + '\n Type here the SKU from the list above you want to add '
                                                     'inventory: ')

            while validate_sku(sku_id.strip(), enabled_skus) != 'true':
                print(text.Red + '\n- Invalid SKU. Please check the list above and try again.')
                sku_id = input(text.default_text_color + '\n Type here the SKU from the list above you want to add '
                                                         'inventory: ')

            sku_quantity = input(text.default_text_color + '\n Type here the quantity you want to add to it: ')

            while not sku_quantity.isdigit():
                print(text.Red + '\n- Invalid option.')
                sku_quantity = input(text.default_text_color + '\n Type here the quantity you want to add to it: ')

            update_sku = update_sku_inventory_microservice(zone, environment, delivery_center_id,
                                                           enabled_skus, sku_id, sku_quantity)

        if update_sku == 'true':
            return 'true'
        else:
            return 'false'
    else:
        return 'error_len'


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
        return 'false'


# Validate SKU inventory
def validate_sku(sku_id, enabled_skus):
    aux_index = 0

    while aux_index < len(enabled_skus):
        if enabled_skus[aux_index] == sku_id:
            return 'true'
        aux_index = aux_index + 1


def display_inventory_by_account(zone, environment, abi_id, delivery_window_id):

    if zone == 'ZA':
        sku_inventory = check_sku_by_account(zone, environment, abi_id)
        if sku_inventory != 'false':
            sku_list = list()

            for i in range(len(sku_inventory)):
                sku_list.append(sku_inventory[i]['sku'])

            dict_values = {
                'fulfillmentCenterId': delivery_window_id,
                'skus': sku_list
            }
            request_body = convert_json_to_string(dict_values)
            response = inventory_sku(dict_values, environment, zone, request_body)

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
    else:
        product_offers = request_get_account_product_assortment(abi_id, zone, environment, delivery_window_id)

        dict_values = {
            'fulfillmentCenterId': delivery_window_id,
            'skus': product_offers
        }
        request_body = convert_json_to_string(dict_values)
        response = inventory_sku(dict_values, environment, zone, request_body)

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


def inventory_sku(dict_values, environment, zone, request_body):
    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false')
    # Define url request
    request_url = get_microservice_base_url(environment) + '/inventory/'
    response = place_request('POST', request_url, request_body, request_headers)
    return response






