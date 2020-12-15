# Standard library imports
import json
from json import loads
import os

# Third party imports
from tabulate import tabulate

# Local application imports
from common import get_header_request, update_value_to_json, convert_json_to_string, \
    place_request, get_microservice_base_url, set_to_dictionary
from classes.text import text


def request_order_simulation(zone, environment, account_id, delivery_center_id, items, combos, empties, payment_method,
                             payment_term):
    """
    Request order simulation through Cart Service
    Args:
        zone: e.g., AR, BR, DO, etc
        environment: e.g., DEV, SIT, UAT
        account_id: POC unique identifier
        delivery_center_id: POC's delivery center
        items: array of items
        combos: array of combos
        empties: array of empties
        payment_method: desired payment method (default is CASH)
        payment_term: payment terms according to the payment method

    Returns: response payload in case of success or `false` in case of failure
    """
    if empties is None:
        empties = []
    if combos is None:
        combos = []

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Define URL Microservice
    request_url = get_microservice_base_url(environment, 'false') + '/cart-service/v2'

    # Inputs for default payload simulation
    dict_values = {
        'accountId': account_id,
        'deliveryCenterId': delivery_center_id,
        'paymentMethod': payment_method,
        'paymentTerm': int(payment_term),
        'lineItems': items,
        'combos': combos,
        'deliveryDate': None,
        'empties': empties
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
    response = place_request('POST', request_url, request_body, request_headers)
    if response.status_code == 200:
        return loads(response.text)
    else:
        print(text.Red + '\n- [Cart Service] Failure to simulate the order. Response Status: {response_status}. '
                         'Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return 'false'


# Order simulation by Microservice
def process_simulation_microservice(order_simulation):
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
