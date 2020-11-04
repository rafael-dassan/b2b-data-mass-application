# Standard library imports
import json
import os

# Third party imports
from tabulate import tabulate

# Local application imports
from common import get_header_request, update_value_to_json, convert_json_to_string, \
    place_request, get_microservice_base_url
from classes.text import text


# Order simulation by Microservice
def process_simulation_microservice(zone, environment, abi_id, account, order_items, order_combos, empties_skus,
                                    payment_method, payment_term):
    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Define URL Microservice
    request_url = get_microservice_base_url(environment, 'false') + '/cart-service/v2'

    # Inputs for default payload simulation
    dict_values = {
        'accountId': abi_id,
        'deliveryCenterId': account[0]['deliveryCenterId'],
        'paymentMethod': payment_method,
        'paymentTerm': int(payment_term),
        'lineItems': order_items,
        'combos': order_combos,
        'deliveryDate': None,
        'empties': empties_skus
    }

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/order_simulation_microservice_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Send request
    response = place_request("POST", request_url, request_body, request_headers)
    if response.status_code == 200:
        order_simulation = json.loads(response.text)
        summary_order_values = [{
            "Subtotal": order_simulation["subtotal"],
            "TaxAmount": order_simulation["taxAmount"],
            "DepositAmount": order_simulation["deposit"],
            "DiscountAmount": order_simulation["discountAmount"],
            "Total": order_simulation["total"],
        }]

        summary_items_values = []
        for item in order_simulation["lineItems"]:
            item_values = {
                "Sku": item["sku"],
                "Quantity": item["quantity"],
                "OriginalPrice": item["originalPrice"],
                "Subtotal": item["subtotal"],
                "TaxAmount": item["taxAmount"],
                "DepositAmount": item["deposit"],
                "DiscountAmount": item["discountAmount"],
                "HasInventory": item["hasInventory"],
                "Total": item["total"],
            }

            summary_items_values.append(item_values)
        
        summary_combo_values = []
        for item in order_simulation["combos"]:
            item_values = {
                "Sku": item["comboId"],
                "Quantity": item["quantity"],
                "OriginalPrice": item["originalPrice"],
                "Subtotal": item["subtotal"],
                "TaxAmount": item["taxAmount"],
                "DepositAmount": item["deposit"],
                "DiscountAmount": item["discountAmount"],
                "Total": item["total"],
            }

            summary_combo_values.append(item_values)

        print_summary_order_simulation(summary_order_values, summary_items_values, summary_combo_values)
    
    else:
        print(text.Red + '\n- [Cart Service] Failure to simulate the order. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)


# Print Summary order simulation
def print_summary_order_simulation(summary_order_values, summary_items_values, summary_combo_values):
    print(text.White + "Order Summary ")
    print(tabulate(summary_order_values, headers='keys', tablefmt="grid"))
    
    if len(summary_items_values) >= 1:
        print("\n")
        print(text.White + "Order Items Summary ")
        print(tabulate(summary_items_values, headers='keys', tablefmt="grid"))

    if len(summary_combo_values) >= 1:
        print("\n")
        print(text.White + "Order Combo Summary ")
        print(tabulate(summary_combo_values, headers='keys', tablefmt="grid"))
