import json
import logging
import os
from datetime import datetime, timedelta
from json import loads
from typing import Any, Optional

import pkg_resources
from tabulate import tabulate

from data_mass.classes.text import text
# Local application imports
from data_mass.common import (
    convert_json_to_string,
    find_values,
    generate_erp_token,
    get_header_request,
    get_microservice_base_url,
    place_request,
    set_to_dictionary,
    update_value_to_json,
    validate_user_entry_date,
    validate_yes_no_change_date
)
from data_mass.config import get_settings
from data_mass.orders.service import get_changed_order_payload


def request_order_creation(
        account_id: str,
        delivery_center_id: str,
        zone: str,
        environment: str,
        allow_order_cancel: str,
        order_items: list,
        order_status: str,
        delivery_date: str,
        items: list = None,
        has_empties: bool = False) -> Optional[Any]:
    """
    Create an order through the Order Service.

    Parameters
    ----------
    account_id : str
        POC unique identifier.
    delivery_center_id : str
        POC's delivery center.
    zone : str
        One of AR, BR, CO, DO, MX, ZA, ES and US.
    environment : str
        One of DEV, SIT and UAT.
    allow_order_cancel : str
        One of `Y` or `N`.
    order_items : list
        List of SKUs
    order_status : str
        PLACED, CANCELLED, etc.
    delivery_date : str
        The delivery date.

    Returns
    -------
    Optional[Any]
        A deserialized s \
        (a str, bytes or bytearray instance containing a JSON document)\
        to a Python object.
    """
    # Define headers
    request_headers = get_header_request(
        zone,
        True,
        False,
        False,
        False,
        account_id
    )

    # Define url request
    if zone == "US":
        endpoint = "order-service/v2/"
        is_v1 = False
        settings = get_settings()

        request_body = json.dumps({
            "accountId": account_id,
            "channel": "B2B_WEB",
            "deliveryCenterId": delivery_center_id,
            "delivery":{
              "date": delivery_date  
            },
            "itemsQuantity": len(order_items.get("items")),
            "placementDate": datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '+00:00',
            "status": order_status,
            "items": items,
            "empties": {
                "hasEmpties": has_empties
            },
            "subtotal": order_items.get("subTotal"),
            "total": order_items.get("total"),
            "vendor": {
                "accountId": account_id,
                "id": settings.vendor_id
            },
            "paymentMethod": "CASH"
        })
    else:
        endpoint = "order-service"
        is_v1 = True

        # Get body
        request_body = create_order_payload(
            account_id=account_id,
            delivery_center_id=delivery_center_id,
            allow_order_cancel=allow_order_cancel,
            order_items=order_items,
            order_status=order_status,
            delivery_date=delivery_date,
            is_v2=False
        )

    base_url = get_microservice_base_url(environment, is_v1)
    request_url = f"{base_url}/{endpoint}"

    # Send request
    response = place_request("POST", request_url, request_body, request_headers)
    json_data = loads(response.text)

    if response.status_code in [200, 202] and json_data:
        return json_data

    print(
        f"{text.Red}\n"
        "[Order Service] Failure to create an order.\n"
        f"Response Status: {response.status_code}.\n"
        f"Response message {response.text}"
    )

    return None


def create_order_payload(
        account_id: str,
        delivery_center_id: str, 
        allow_order_cancel: str, 
        order_items: list, 
        order_status: str,
        delivery_date: str,
        is_v2: Optional[bool] = False) -> str:
    """
    Create payload for order creation.

    Parameters
    ----------
    account_id : str
    delivery_center_id : str
    allow_order_cancel : str
    order_items : list
    order_status : str
    delivery_date : str
    zone : Optional[bool], optional
        By default `False`.

    Returns
    -------
    str
        The payload as string.
    """
    # Sets the format of the placement date of the order (current date and time)
    placement_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '+00:00'

    # Sets the format of the cancellable date of the order (current date and time more ten days)
    cancellable_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%dT%H:%M:%S') + '+00:00'

    line_items = order_items.get('lineItems')
    items = []

    for product in line_items:
        items.append({
            "price": product.get("price"),
            "unitPrice": product.get("unitPrice"),
            "unitPriceInclTax": product.get("unitPriceInclTax"),
            "quantity": product.get("quantity"),
            "discountAmount": product.get("discountAmount"),
            "deposit": product.get("deposit"),
            "subtotal": product.get("subtotal"),
            "taxAmount": product.get("taxAmount"),
            "total": product.get("total"),
            "totalExclDeposit": product.get("totalExclDeposit"),
            "sku": product.get("sku"),
            "hasInventory": product.get("hasInventory"),
            "freeGood": product.get("freeGood"),
            "originalPrice": product.get("originalPrice"),
        })

    dict_values = {
        'accountId': account_id,
        'delivery': {
            'date': delivery_date
        },
        'deposit': order_items.get('deposit'),
        'discount': order_items.get('discountAmount'),
        'interestAmount': order_items.get('interestAmount'),
        'itemsQuantity': len(order_items.get('lineItems')),
        'total': order_items.get('total'),
        'subtotal': order_items.get('subtotal'),
        'tax': order_items.get('taxAmount'),
        'placementDate': placement_date,
        'status': order_status,
        'items': items
    }

    if is_v2:
        payload_path = "data/create_order_payload_v2.json"
        dict_values.update({
            "deliveryCenterId": delivery_center_id,
            "vendor": {
                "accountId": account_id,
                "id": "9d72627a-02ea-4754-986b-0b29d741f5f0"
            }
        })
    else:
        payload_path = "data/create_order_payload.json"
        dict_values.update({
            "deliveryCenter": delivery_center_id,
        })

    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        payload_path
    )
    json_data: dict = json.loads(content.decode("utf-8"))

    if order_status == 'PLACED':
        if allow_order_cancel == 'Y':
            dict_values.update({"cancellableUntil": cancellable_date})

    elif order_status == 'CANCELLED':
        dict_values.update({
            "cancellationReason": "Order cancelled for testing purposes"
        })

    json_data.update(dict_values)

    return convert_json_to_string(json_data)


def request_changed_order_creation(zone, environment, order_data):
    """
    Change/Update order information through the Order Relay Service
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        order_data: order information

    Returns `success` or error message in case of failure
    """
    # Define headers
    request_headers = get_header_request(zone, False, False, True, False)

    # Define url request
    request_url = get_microservice_base_url(environment) + '/order-relay/'

    # Get body
    request_body = get_changed_order_payload(order_data)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)
    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Order Relay Service] Failure to change an order. Response Status: {response_status}. '
                         'Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return False
