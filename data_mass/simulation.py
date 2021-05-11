# Standard library imports
import json
import os
from datetime import datetime, timedelta
from json import loads

from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.common import (
    convert_json_to_string,
    get_header_request,
    get_microservice_base_url,
    place_request,
    update_value_to_json,
    validate_user_entry_date,
    validate_yes_no_change_date
    )


def request_order_simulation(
    zone: str,
    environment: str,
    account_id: int,
    delivery_center_id: int,
    items: list,
    combos: list,
    empties: list,
    payment_method: str,
    payment_term: bool,
):
    """
    Request order simulation through Cart Service

    Parameters
    ----------
    zone : str
        e.g., AR, BR, DO, etc
    environment : str
        e.g., DEV, SIT, UAT
    account_id : int
        POC unique identifier
    delivery_center_id : int
        POC's delivery center
    items : list
        list of items
    combos : list
        list of combos
    empties : list
        list of empties
    payment_method : str
        desired payment method (default is CASH)
    payment_term : bool
        payment terms according to the payment method

    Returns
    -------
    str or Bool
        response payload in case of success or `false` in case of failure
    """
    if empties is None:
        empties = []
    if combos is None:
        combos = []

    # Define headers
    request_headers = get_header_request(
        zone, True, False, False, False, account_id
    )

    # Define URL Microservice
    request_url = (
        get_microservice_base_url(environment, False) + "/cart-service/v2"
    )

    option_change_date = validate_yes_no_change_date()
    if option_change_date.upper() == "Y": 
        date_entry = validate_user_entry_date(
            'Enter Date for Delivery-Date (YYYY-mm-dd)'
        )
    else:
        tomorrow = datetime.today() + timedelta(1)
        date_entry = str(datetime.date(tomorrow))

    # Inputs for default payload simulation
    dict_values = {
        "accountId": account_id,
        "deliveryCenterId": delivery_center_id,
        "paymentMethod": payment_method,
        "paymentTerm": int(payment_term),
        "lineItems": items,
        "combos": combos,
        "deliveryDate": date_entry,
        "empties": empties,
    }

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(
        abs_path, "data/order_simulation_microservice_payload.json"
    )

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Send request
    response = place_request(
        "POST", request_url, request_body, request_headers
    )
    if response.status_code == 200:
        return loads(response.text)
    else:
        print(
            text.Red
            + "\n- [Cart Service] Failure to simulate the order."
            f"Response Status: {response.status_code}. "
            f"Response message: {response.text}"
        )
        return False


# Order simulation by Microservice
def process_simulation_microservice(order_simulation):
    summary_order_values = [
        {
            "Subtotal": order_simulation["subtotal"],
            "TaxAmount": order_simulation["taxAmount"],
            "DepositAmount": order_simulation["deposit"],
            "DiscountAmount": order_simulation["discountAmount"],
            "Total": order_simulation["total"],
        }
    ]

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

    print_summary_order_simulation(
        summary_order_values, summary_items_values, summary_combo_values
    )


# Print Summary order simulation
def print_summary_order_simulation(
    summary_order_values, summary_items_values, summary_combo_values
):
    print(text.White + "Order Summary ")
    print(tabulate(summary_order_values, headers="keys", tablefmt="grid"))

    if len(summary_items_values) >= 1:
        print("\n")
        print(text.White + "Order Items Summary ")
        print(tabulate(summary_items_values, headers="keys", tablefmt="grid"))

    if len(summary_combo_values) >= 1:
        print("\n")
        print(text.White + "Order Combo Summary ")
        print(tabulate(summary_combo_values, headers="keys", tablefmt="grid"))
