import json
from datetime import datetime, timedelta
from json import loads
from typing import Any, Optional

import pkg_resources

from data_mass.account.accounts import check_account_exists_microservice
from data_mass.classes.text import text
from data_mass.common import (
    convert_json_to_string,
    get_header_request,
    get_microservice_base_url,
    place_request
)
from data_mass.config import get_settings
from data_mass.orders.service import get_changed_order_payload


def request_order_creation(
        account_id: str,
        delivery_center_id: str,
        zone: str,
        environment: str,
        payment_method: str,
        allow_order_cancel: str,
        order_items: list,
        order_status: str,
        delivery_date: str,
        order_number: str = None,
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
        One of AR, BR, CA, CO, DO, MX, ZA, ES and US.
    environment : str
        One of DEV, SIT and UAT.
    allow_order_cancel : str
        One of `Y` or `N`.
    order_items : list
        List of SKUs
    order_number : str
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
    # Define url request
    if zone in ["CA", "US"]:
        request_headers = get_header_request(
            zone=zone,
            use_jwt_auth=True,
            account_id=account_id
        )

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
            "placementDate": (
                datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '+00:00'
            ),
            "status": order_status,
            "items": items,
            "empties": {
                "hasEmpties": has_empties
            },
            "subtotal": order_items.get("subTotal"),
            "total": order_items.get("subTotal"), # como pega esse campo?
            "vendor": {
                "accountId": account_id,
                "id": settings.vendor_id
            },
            "paymentMethod": "CASH"
        })
    else:
        request_headers = get_header_request(
            zone=zone,
            use_inclusion_auth=True
        )
        endpoint = "order-relay"
        is_v1 = True

        # Get body
        request_body = create_order_payload(
            account_id=account_id,
            payment_method=payment_method,
            delivery_center_id=delivery_center_id,
            allow_order_cancel=allow_order_cancel,
            order_items=order_items,
            order_status=order_status,
            delivery_date=delivery_date,
            is_v2=False,
            order_number=order_number
        )

    base_url = get_microservice_base_url(environment, is_v1)
    request_url = f"{base_url}/{endpoint}"

    # Send request
    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code in [200, 202]:
        if response.text:
            response = loads(response.text)

        return True

    print(
        f"{text.Red}\n"
        "[Order Service] Failure to create an order.\n"
        f"Response Status: {response.status_code}.\n"
        f"Response message {response.text}"
    )

    return False


def request_order_update(
        account_id: str,
        delivery_center_id: str,
        zone: str,
        environment: str,
        payment_method: str,
        allow_order_cancel: str,
        order_items: list,
        order_status: str,
        delivery_date: str,
        order_id: str,
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
        One of AR, BR, CA, CO, DO, MX, ZA, ES and US.
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
    if zone in ["CA", "US"]:
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
            "placementDate": (
                datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '+00:00'
            ),
            "status": order_status,
            "items": items,
            "empties": {
                "hasEmpties": has_empties
            },
            "subtotal": order_items.get("subTotal"),
            "total": order_items.get("subTotal"), # como pega esse campo?
            "vendor": {
                "accountId": account_id,
                "id": settings.vendor_id
            },
            "paymentMethod": "CASH"
        })
    else:
        request_headers = get_header_request(
            zone=zone,
            use_inclusion_auth=True
        )
        endpoint = "order-relay"
        is_v1 = True

        # Get body
        request_body = update_order_payload(
            order_id=order_id,
            payment_method=payment_method,
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
    response = place_request(
        request_method="PATCH",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )
    
    if response.status_code in [200, 202]:
        
        return response.text

    print(
        f"{text.Red}\n"
        "[Order Service] Failure to create an order.\n"
        f"Response Status: {response.status_code}.\n"
        f"Response message {response.text}"
    )

    return None

def create_order_payload(
        account_id: str,
        payment_method: str,
        delivery_center_id: str, 
        allow_order_cancel: str, 
        order_items: list, 
        order_status: str,
        delivery_date: str,
        order_number: str = None,
        is_v2: bool = False) -> str:
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
    order_number : str
    zone : bool
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

    if order_number:
        dict_values.update({'orderNumber': order_number})

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
            "paymentMethod": payment_method
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

    return json.dumps([json_data])


def update_order_payload(
        order_id: str,
        payment_method: str,
        account_id: str,
        delivery_center_id: str, 
        allow_order_cancel: str, 
        order_items: list, 
        order_status: str,
        delivery_date: str,
        is_v2: bool = False) -> str:
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
    zone : bool
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
        'items': items,
        'orderNumber': order_id
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
            "paymentMethod": payment_method
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

    return json.dumps([json_data])


def request_changed_order_creation(zone, environment, order_data) -> bool:
    """
    Change/Update order information through the Order Relay Service
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        order_data: order information

    Returns True or False message in case of failure
    """
    # Define headers
    request_headers = get_header_request(zone, False, False, True, False)

    # Define url request
    request_url = f"{get_microservice_base_url(environment)}/order-relay/"

    # Get body
    request_body = get_changed_order_payload(order_data)

    # Send request
    response = place_request(
        'POST', request_url, request_body, request_headers
    )
    if response.status_code == 202:
        return True

    print(
        f"{text.Red}- [Order Relay Service] Failure to change an order.\n"
        f"Response Status: {response.status_code}.\n"
        f"Response message: {response.text}.\n"
    )
    return False

def order_payment_method(account_id, zone, environment)-> str:
    """
    Get the available payment methods for the account and return one
    for being used on the order creation
    Args:
        account_id: POC number
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT

    Returns the selected payment method
    """
    response_data = check_account_exists_microservice(account_id, zone, environment)
    payment_list = response_data[0]['paymentMethods']

    if len(payment_list) == 1:
        payment_method, = payment_list
        return payment_method

    else:
        options = []

        for index, pay_item in enumerate(payment_list, 1):
            pay_option = f'{index}: {pay_item}'
            options.append(pay_option)

        check_option =  int(input(
                f'{text.Yellow}\n'
                f'Available payment methods for this POC: '+ f'{options}\n'
                f'Select the corresponding number: \n'
                        ))
        payment_method = payment_list[check_option -1]
        return payment_method
