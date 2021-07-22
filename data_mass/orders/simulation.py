import json
from json import loads
from typing import List, Union
from uuid import uuid1

import pkg_resources
from tabulate import tabulate

from data_mass.account.accounts import get_multivendor_account_id
from data_mass.classes.text import text
from data_mass.common import (
    convert_json_to_string,
    get_header_request,
    get_microservice_base_url,
    place_request,
    update_value_to_json
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
        delivery_date: str) -> Union[dict, bool]:
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
    Union[dict, bool]
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

    # Inputs for default payload simulation
    dict_values = {
        "accountId": account_id,
        "deliveryCenterId": delivery_center_id,
        "paymentMethod": payment_method,
        "paymentTerm": int(payment_term),
        "lineItems": items,
        "combos": combos,
        "deliveryDate": delivery_date,
        "empties": empties,
    }

    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass", "data/order_simulation_microservice_payload.json"
    )
    json_data = json.loads(content.decode("utf-8"))

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

    print(
        text.Red + "\n- [Cart Service] Failure to simulate the order."
        f"Response Status: {response.status_code}. "
        f"Response message: {response.text}"
    )
    return False


def request_order_simulation_v3(
    account_id: int,
    zone: str,
    environment: str,
    items: List[dict],
    delivery_date: str,
):
    """
    Request order simulation v3.

    Parameters
    ----------
    zone : str
    environment : str
    account_id : int
    items : list
    has_empties : str
        By default `None`.

    Returns
    -------
    str or Bool
        response payload in case of success or `false` in case of failure.
    """
    request_headers = get_header_request("US")
    base_url = get_microservice_base_url(environment, True)
    request_url = f"{base_url}/cart-service/v3"

    dict_values = {
        "accountId": get_multivendor_account_id(account_id, zone, environment),
        "userId": str(uuid1()),
        "deliveryDate": delivery_date,
        "items": [],
    }

    for item in items:
        schema = {"id": item.get("id"), "quantity": item.get("quantity")}
        dict_values["items"].append(schema)

    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=json.dumps(dict_values),
        request_headers=request_headers,
    )
    if response.status_code == 200:
        return loads(response.text)

    print(
        text.Red + "\n- [Cart Service] Failure to simulate the order."
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
    print(
        tabulate(summary_order_values, headers="keys", tablefmt="fancy_grid")
    )

    if len(summary_items_values) >= 1:
        print(f"\n{text.White}Order Items Summary ")
        print(
            tabulate(
                summary_items_values, headers="keys", tablefmt="fancy_grid"
            )
        )

    if len(summary_combo_values) >= 1:
        print("\n")
        print(text.White + "Order Combo Summary ")
        print(
            tabulate(
                summary_combo_values, headers="keys", tablefmt="fancy_grid"
            )
        )
