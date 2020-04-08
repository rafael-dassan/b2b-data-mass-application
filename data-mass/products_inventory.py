import sys
from json import dumps
import time
from datetime import date, datetime, timedelta
import calendar
from products import *



# Display on the screen all available SKUs of the account
def display_available_products_account(account_id, zone, environment, delivery_center_id):

    print(text.Green + "\n- [Products Inventory] Searching all the SKUs available in the account...")
    
    # Retrieve all SKUs of the specified Account and DeliveryCenter IDs
    product_offers = request_get_offers_microservice(account_id, zone, environment, delivery_center_id)

    # Check if the account has at least one SKU added to it
    if len(product_offers) > 0:

        quantity_product_offers = len(product_offers)

        # Store and display all the SKUs on the screen
        sku = []
        aux_index = 0
        while aux_index < quantity_product_offers:
            sku.append(product_offers[aux_index])
            aux_index = aux_index + 1

        aux_index = 0
        while aux_index < quantity_product_offers:
            print(text.Yellow + "\n SKU: " + text.White + product_offers[aux_index])
            aux_index = aux_index + 1

        sku_id = input(text.Green + "\n Type here the SKU from the list above you want to add quantity: ")
        sku_quantity = input(text.Green + "\n Type here the quantity you want to add to it: ")

        update_sku = update_sku_inventory_microservice(account_id, zone, environment, delivery_center_id, sku_id, sku_quantity)

        return("true")
    else:
        return("false")

# Update SKU inventory
def update_sku_inventory_microservice(account_id, zone, environment, delivery_center_id, sku_id, sku_quantity):
    print(sku_id)
    
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
    print(request_url)
    print(request_body)
    print(request_headers)
    
    response = place_request("PUT", request_url, request_body, request_headers)

    print(response.status_code)
    print(response.text)
    
    if response.status_code == 202:
        return 'success'
    else:
        return response.status_code