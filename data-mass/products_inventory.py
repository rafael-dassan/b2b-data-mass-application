import sys
from json import dumps
import time
from datetime import date, datetime, timedelta
import calendar
from products import *



# Show all available SKUs of the account in the screen
def display_available_products_account(account_id, zone, environment, delivery_center_id):
    
    # Retrieve all SKUs for the specified Account and DeliveryCenter IDs
    product_offers = request_get_offers_microservice(account_id, zone, environment, delivery_center_id)

    print(text.default_text_color + "\n[Products Inventory] Checking enabled products available in the account " + account_id + ". It may take a while...")

    enabled_skus = list()
    aux_index = 0

    while aux_index < len(product_offers):
        # Check if the SKU is enabled on Items MS
        recommended_sku = check_item_enabled(product_offers[aux_index], zone, environment)
        while recommended_sku == False:
            aux_index = aux_index + 1
            recommended_sku = check_item_enabled(product_offers[aux_index], zone, environment)
            
        enabled_skus.append(recommended_sku)
        aux_index = aux_index + 1

    # Check if the account has at least one SKU added to it
    if len(enabled_skus) > 0:

        quantity_product_offers = len(enabled_skus)

        # Store and display all the SKUs on the screen
        sku = []
        aux_index = 0
        while aux_index < quantity_product_offers:
            sku.append(enabled_skus[aux_index])
            aux_index = aux_index + 1

        aux_index = 0
        while aux_index < quantity_product_offers:
            print(text.default_text_color + "\n SKU: " + text.White + enabled_skus[aux_index])
            aux_index = aux_index + 1

        sku_id = input(text.default_text_color + "\n Type here the SKU from the list above you want to add quantity: ")
        
        while validate_sku(sku_id, enabled_skus) != "true":
            print(text.Red + "\n[Products Inventory] Invalid SKU. Please check the list above and try again.")
            sku_id = input(text.default_text_color + "\n Type here the SKU from the list above you want to add quantity: ")
        
        sku_quantity = input(text.default_text_color + "\n Type here the quantity you want to add to it: ")

        while sku_quantity.isdigit() == False:
            print(text.Red + "\n[Products Inventory] Invalid option")
            sku_quantity = input(text.default_text_color + "\n Type here the quantity you want to add to it: ")

        update_sku = update_sku_inventory_microservice(account_id, zone, environment, delivery_center_id, sku_id, sku_quantity)

        if update_sku == "true":
            return("true")
        else:
            return("false")
    else:
        return("error_len")

# Update SKU inventory
def update_sku_inventory_microservice(account_id, zone, environment, delivery_center_id, sku_id, sku_quantity):
    
    # Define headers
    request_headers = get_header_request(zone, "false", "false", "true")

    # Define url request
    request_url = get_microservice_base_url(environment) + "/inventory-relay/add"

    dict_values = {
        "fulfillmentCenterId": delivery_center_id,
        "inventory": [
            {
                "sku": sku_id,
                "quantity": int(sku_quantity)
            }
        ]
    }

    # Create body
    request_body = convert_json_to_string(dict_values)

    # Send request
    response = place_request("PUT", request_url, request_body, request_headers)
    
    if (response.status_code == 202) or (response.status_code == 202):
        return "true"
    else:
        return "false"

# Update SKU inventory
def validate_sku(sku_id, enabled_skus):
        aux_index = 0
        while aux_index < len(enabled_skus):
            if enabled_skus[aux_index] == sku_id:
                return "true"
            aux_index = aux_index + 1