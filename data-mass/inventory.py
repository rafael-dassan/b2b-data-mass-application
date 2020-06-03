import sys
from json import dumps
import time
from datetime import date, datetime, timedelta
import calendar
from products import *

# Show all available SKUs of the account in the screen
def display_available_products_account(account_id, zone, environment, delivery_center_id):
    
    # Retrieve all SKUs for the specified Account and DeliveryCenter IDs
    product_offers = request_get_account_product_assortment(account_id, zone, environment, delivery_center_id)

    print(text.default_text_color + '\n[Inventory] Checking enabled products available in the account ' + account_id + '. It may take a while...')

    enabled_skus = list()
    aux_index = 0

    while aux_index < len(product_offers):
        # Check if the SKU is enabled on Items MS
        sku_enable = check_item_enabled(product_offers[aux_index], zone, environment, True)
        
        while sku_enable == False:
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
            sku_description.append(get_sku_name(account_id, zone, environment, enabled_skus[aux_index]))
            aux_index = aux_index + 1


    # Check if the account has at least one SKU enabled on it
    if len(enabled_skus) > 0:

        stock_option = input(text.default_text_color + '\nDo you want to choose which product will be updated the stock? (1 - Yes, 2 - No) \nIf you do not wish to choose, stock will be added to all products linked to your account ')
        
        while stock_option != '1' and stock_option != '2':
            print(text.Red + '\n[Inventory] Invalid option.')
            stock_option = input(text.default_text_color + '\nDo you want to choose which product will be updated the stock? (1 - Yes, 2 - No) \nIf you do not wish to choose, stock will be added to all products linked to your account ')

        if stock_option == '2':
            update_sku = update_sku_inventory_microservice(account_id, zone, environment, delivery_center_id, enabled_skus)
        else:
            # Show all the enabled SKUs and its respective names on the screen
            aux_index = 0

            while aux_index < quantity_enabled_skus:
                print(text.default_text_color + '\n SKU: ' + text.Blue + enabled_skus[aux_index] + '  ||  ' + sku_description[aux_index].upper())
                aux_index = aux_index + 1

            sku_id = input(text.default_text_color + '\n Type here the SKU from the list above you want to add inventory: ')
            
            while validate_sku(sku_id.strip(), enabled_skus) != 'true':
                print(text.Red + '\n[Inventory] Invalid SKU. Please check the list above and try again.')
                sku_id = input(text.default_text_color + '\n Type here the SKU from the list above you want to add inventory: ')
            
            sku_quantity = input(text.default_text_color + '\n Type here the quantity you want to add to it: ')

            while sku_quantity.isdigit() == False:
                print(text.Red + '\n[Inventory] Invalid option.')
                sku_quantity = input(text.default_text_color + '\n Type here the quantity you want to add to it: ')

            update_sku = update_sku_inventory_microservice(account_id, zone, environment, delivery_center_id, [sku_id], sku_quantity)
        
        if update_sku == 'true':
            return('true')
        else:
            return('false')
    else:
        return('error_len')

# Update SKU inventory
def update_sku_inventory_microservice(account_id, zone, environment, delivery_center_id, list_skus, sku_quantity = 0):
    # Define headers
    request_headers = get_header_request(zone, 'false', 'false', 'true')

    # Define url request
    request_url = get_microservice_base_url(environment) + '/inventory-relay/add'
    
    quantity = 999999
    if int(sku_quantity) > 0:
        quantity = int(sku_quantity)

    inventory_list = []
    index = 0
    while index < len(list_skus):
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
    
    if (response.status_code == 202):
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

# Get SKU name
def get_sku_name(account_id, zone, environment, sku_id):
    # Get header request
    headers = get_header_request(zone, 'true')

    # Get url base
    request_url = get_microservice_base_url(environment, 'false') + '/items/' + sku_id + '?includeDisabled=false'

    # Place request
    response = place_request('GET', request_url, '', headers)

    json_data = loads(response.text)
    sku_name = json_data['itemName']

    return sku_name