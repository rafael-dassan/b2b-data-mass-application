import json
from random import randint
from typing import Optional

import pkg_resources

from data_mass.classes.text import text
from data_mass.common import (
    convert_json_to_string,
    create_list,
    get_header_request,
    get_microservice_base_url,
    place_request,
    set_to_dictionary,
    update_value_to_json
)
from data_mass.config import get_settings


def create_invoice_request(
        zone: str,
        environment: str,
        order_id: str,
        status: str,
        order_details: dict,
        order_items: dict,
        invoice_id: str = None) -> str:
    """
    Create Invoice.

    Parameters
    ----------
    zone : str
    environment : str
    order_id : str
    status : str
    order_details : dict
    order_items : dict
    invoice_id : str, optional
        The invoice_id, by default None.

    Returns
    -------
    str
        The invoice id that was just created.
    """
    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/create_invoice_payload.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    if invoice_id is None:
        invoice_id = 'DM-' + str(randint(1, 100000))

    order_placement_date = order_details.get('placementDate')

    if zone == 'DO':
        placement_date = order_placement_date.split('T')[0] + 'T00:00:00Z'
    else:
        placement_date = order_placement_date.split('+')[0] + 'Z'

    dict_values = {
        'accountId': order_details.get('accountId'),
        'channel': order_details.get('channel'),
        'date': placement_date,
        'interestAmount': order_details.get('interestAmount'),
        'orderDate': placement_date,
        'orderId': order_id,
        'subtotal': order_details.get('subtotal'),
        'invoiceId': invoice_id,
        'status': status,
        'tax': order_details.get('tax'),
        'total': order_details.get('total'),
        'poNumber': order_id,
        'paymentType': order_details.get('paymentMethod'),
        'discount': abs(order_details.get('discount')),
        'itemsQuantity': order_details.get('itemsQuantity')
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    set_to_dictionary(json_object, 'items', order_items)

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/invoices-relay'

    # Get headers
    request_headers = get_header_request(zone, False, False, True, False)

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    # Send request
    response = place_request(
        request_method='POST',
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 202:
        return invoice_id

    print(
        f"{text.Red}\n"
        "- [Invoice Relay Service] Failure to create an invoice.\n"
        f"Response Status: {response.status_code}\n"
        f"Response message: {response.text}"
    )

    return False


def create_invoice_multivendor(
        vendor_account_id: str,
        zone: str,
        environment: str,
        order_id: str,
        status: str,
        order_details: dict) -> Optional[dict]:
    """
    Create invoice.

    Parameters
    ----------
    vendor_account_id : str
    zone : str
    environment : str
    order_id : str
    status : str
    order_details : dict

    Returns
    -------
    Optional[dict]
        The invoice response.
    """
    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/invoices-relay/v2"
    request_headers = get_header_request(zone)
    settings = get_settings()

    invoice_id = f"DM-{str(randint(1, 100000))}"
    order_placement_date = order_details.get("placementDate")
    placement_date = order_placement_date.split('+')[0]
    items = []

    if "Z" not in placement_date:
        placement_date += "Z"

    for item in order_details.get("items", []):
        # For some reason, `discount` and `tax` are not required when \
        # creating an new Order, but it's required when creating an Invoice.
        # Since dict's `get` method does not return a default \
        # value when a key's value is `None` \
        # (only when the key does not exists), and `json.loads()` \
        # turns `null` into `None`, we should change it manually.
        discount = item.get("discount")
        tax = item.get("tax")

        items.append({
            "discount": 0.0 if discount is None else discount,
            "price": item.get("price"),
            "quantity": item.get("quantity"),
            "subtotal": item.get("subtotal"),
            "tax": 0 if tax is None else tax,
            "total": item.get("total"),
            "vendorItemId": item.get("vendorItemId")
        })

    body = {
        "channel": order_details.get('channel'),
        "customerInvoiceNumber": invoice_id,
        "date": placement_date,
        "deleted": False,
        "discount": abs(order_details.get("discount", 0)),
        "dueDate": placement_date,
        "fileAvailable": False,
        "items": items,
        "itemsQuantity": order_details.get("itemsQuantity"),
        "orderDate": placement_date,
        "orderId": order_id,
        "parentOrderNumber": None,
        "paymentType": order_details.get("paymentMethod"),
        "poNumber": order_id,
        "status": status,
        "subtotal": order_details.get("subtotal"),
        "tax": order_details.get("tax", 0),
        "total": order_details.get("total"),
        "vendor": {
            "id": settings.vendor_id,
            "accountId": vendor_account_id,
            "invoiceId": invoice_id
        }
    }

    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=json.dumps([body]),
        request_headers=request_headers
    )

    if response.status_code == 202:
        return invoice_id

    print(
        f"{text.Red}\n"
        "- [Invoice Relay Service] Failure to create an invoice."
        f"Response Status: {response.status_code}\n"
        f"Response message: {response.text}"
    )

    return False


def update_invoice_request(
        zone: str,
        environment: str,
        account_id: str,
        invoice_id: str,
        payment_method: str,
        status: str) -> bool:
    """
    Update Invoice.

    Parameters
    ----------
    zone : str
    environment : str
    account_id : str
    invoice_id : str
    payment_method : str
    status : str

    Returns
    -------
    bool
        Whenever an invoice was successfully updated.
    """
    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/update_invoice_status.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    dict_values = {
        'invoiceId': invoice_id,
        'paymentType': payment_method,
        'status': status
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Get base URL
    base_url = get_microservice_base_url(environment)
    request_url = f'{base_url}/invoices-service'

    # Get headers
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        use_root_auth=False,
        use_inclusion_auth=False,
        sku_product=False,
        account_id=account_id
    )

    # Create body
    request_body = convert_json_to_string(json_object)

    # Send request
    # TODO change to PATCH v2 as soon as available
    response = place_request(
        request_method='PATCH',
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 202:
        return True

    print(
        f"{text.Red}\n"
        "- [Invoice Service] Failure to update an invoice.\n"
        f"Response Status: {response.status_code}.\n"
        f"Response message: {response.text}"
    )

    return False


def delete_invoice_by_id(
        zone: str,
        environment: str,
        invoice_id: str) -> bool:
    """
    Delete invoice by id.

    Parameters
    ----------
    zone : str
    environment : str
    invoice_id : str

    Returns
    -------
    bool
        Whenever an invoice is successfully deleted.
    """
    # Get base URL
    base_url = get_microservice_base_url(environment)
    request_url = f'{base_url}/invoices-relay/id/{invoice_id}'

    # Get headers
    request_headers = get_header_request(zone, False, False, True, False)

    # Send request
    response = place_request("DELETE", request_url, "", request_headers)

    if response.status_code == 202:
        return True

    print(
        f"{text.Red}\n"
        f"[Invoice Relay Service]Failure to delete the invoice {invoice_id}\n"
        f"Response status: {response.status_code}"
        f"Response message: {response.text}'"
    )

    return False
