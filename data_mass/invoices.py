# Standard library imports
import json
import logging
from random import randint
from typing import Optional
from urllib.parse import urlencode

import pkg_resources

from data_mass.accounts import get_account_id
from data_mass.classes.text import text
# Local application imports
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

logger = logging.getLogger(__name__)

def create_invoice_request(zone, environment, order_id, status, order_details, order_items, account_id, invoice_id=None):
    # get data from Data Mass files
    if zone == "US":
        content: bytes = pkg_resources.resource_string(
            "data_mass",
            "data/create_invoice_payload_us.json"
        )
    else:
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
    elif zone == 'US':
        placement_date = order_placement_date
    else:
        placement_date = order_placement_date.split('+')[0] + 'Z'

    settings = get_settings()
    account_id = order_details.get('accountId')

    vendor_values = {
        'accountId': account_id,
        'id': settings.vendor_id,
        'invoiceId': invoice_id
    }

    dict_values = {
        'accountId': account_id,
        'channel': order_details.get('channel'),
        'invoiceId': invoice_id,
        'customerInvoiceNumber': invoice_id,
        'accountId': account_id,
        'date': placement_date,
        'interestAmount': order_details.get('interestAmount'),
        'discount': abs(order_details.get('discount')),
        'orderDate': placement_date,
        'orderId': order_id,
        'subtotal': order_details.get('subtotal'),
        'status': status,
        'tax': order_details.get('tax', 0),
        'total': order_details.get('total'),
        'poNumber': order_id,
        'paymentType': order_details.get('paymentMethod'),
        'itemsQuantity': order_details.get('itemsQuantity'),
        'vendor': vendor_values
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    set_to_dictionary(json_object, 'items', order_items)

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/invoices-relay'
    if zone == "US":
        request_url += "/v2"

    # Get headers
    request_headers = get_header_request(zone, False, False, True, False)

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return invoice_id
    else:
        print(text.Red + '\n- [Invoice Relay Service] Failure to create an invoice. Response Status: '
                         '{response_status}. Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return False


def create_invoice_v2(
        zone: str,
        environment: str,
        account_id: str,
        order_id: str,
        status: str,
        order_details: dict) -> Optional[dict]:
    """
    Create invoice.

    Parameters
    ----------
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
    order_placement_date = order_details.get('placementDate')
    placement_date = order_placement_date.split('+')[0] + 'Z'
    items = []
    
    for item in order_details.get("items", []):
        items.append({
            "discount": item.get("discount", 0.0),
            "price": item.get("price"),
            "quantity": item.get("quantity"),
            "subtotal": item.get("subtotal"),
            "tax": item.get("tax"),
            "total": item.get("total"),
            "vendorItemId": item.get("vendorItemId")
        })

    body = {
        "channel": order_details.get('channel'),
        "customerInvoiceNumber": invoice_id,
        "date": placement_date,
        "deleted": False,
        "discount": abs(order_details.get("discount")),
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
        "tax": order_details.get("tax"),
        "total": order_details.get("total"),
        "vendor": {
            "id": settings.vendor_id,
            "accountId": order_details.get("accountId"),
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

def update_invoice_request(zone, environment, account_id, invoice_id, payment_method, status):
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
    request_url = get_microservice_base_url(environment) + '/invoices-service'

    # Get headers
    request_headers = get_header_request(zone, True, False, False, False, account_id)

    # Create body
    request_body = convert_json_to_string(json_object)

    # Send request
    #TODO change to PATCH v2 as soon as available
    response = place_request('PATCH', request_url, request_body, request_headers)

    if response.status_code == 202:
        return True
    else:
        print(text.Red + '\n- [Invoice Service] Failure to update an invoice. Response Status: {response_status}. '
                         'Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return False


def check_if_invoice_exists(
        account_id: str,
        invoice_id: str,
        zone: str,
        environment: str) -> Optional[dict]:
    """
    Check if invoice exists on API.

    Parameters
    ----------
    account_id : str
    invoice_id : str
    zone : str
    environment : str

    Returns
    -------
    Optional[dict]
        The invoice data.
    """
    # Get header request
    request_headers = get_header_request(zone, True, False, False, False, account_id)
    
    if zone == "US":
        version = "v2"
        query = {"customerInvoiceNumber": invoice_id}
    else:
        version = "v1"
        query = {"invoiceId": invoice_id}
        
    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/invoices-service/{version}?{urlencode(query)}"

    # Place request
    response = place_request("GET", request_url, "", request_headers)

    json_data = json.loads(response.text)
    if response.status_code == 200 and len(json_data['data']) != 0:
        return json_data

    if response.status_code == 200 and len(json_data['data']) == 0:
        print(
            f"{text.Red}\n"
            f"- [Invoice Service] The invoice {invoice_id} does not exist"
        )

        return False

    print(
        f"{text.Red}\n"
        f"- [Invoice Service] Failure to retrieve the invoice {invoice_id}."
        f"Response status: {response.status_code}\n"
        f"Response message: {response.text}"
    )

    return False


def get_invoices(
        zone: str,
        account_id: str,
        environment: str) -> Optional[dict]:
    """
    Get invoice by id.

    Parameters
    ----------
    zone : str
    account_id : str
    environment : str

    Returns
    -------
    Optional[dict]
        The invoice data.
    """
    if zone == "US":
        version = "v2"
        account_id = get_account_id(account_id, zone, environment)
    else:
        version = "v1"

    header_request = get_header_request(zone, True, False, False, False, account_id)
    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/invoices-service/{version}?accountId={account_id}"

    # Place request
    response = place_request("GET", request_url, "", header_request)
    invoice_info = json.loads(response.text)

    if response.status_code == 200:
        return invoice_info

    return None


def delete_invoice_by_id(zone, environment, invoice_id):
    # Get base URL
    request_url = get_microservice_base_url(environment) + f'/invoices-relay/id/{invoice_id}'

    # Get headers
    request_headers = get_header_request(zone, False, False, True, False)

    # Send request
    response = place_request('DELETE', request_url, '', request_headers)

    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Invoice Relay Service] Failure to delete the invoice {invoice_id}. Response status: '
                         '{response_status}. Response message: {response_message}'
              .format(invoice_id=invoice_id, response_status=response.status_code, response_message=response.text))
        return False
