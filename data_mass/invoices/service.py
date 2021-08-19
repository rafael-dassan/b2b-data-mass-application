import json
from typing import Optional
from urllib.parse import urlencode

from tabulate import tabulate

from data_mass.account.accounts import get_multivendor_account_id
from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request
)


def check_if_invoice_exists(
        account_id: str,
        invoice_id: str,
        zone: str,
        environment: str) -> Optional[dict]:
    """
    Check if invoice exists on API.

    Parameters
    ----------
    account_id : [str
    invoice_id : str
    zone : str
    environment : str

    Returns
    -------
    Optional[dict]
        The invoice data.
    """
    # Get header request
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        use_root_auth=False,
        use_inclusion_auth=False,
        sku_product=False,
        account_id=account_id
    )

    if zone in ["CA", "US"]:
        version = "v2"
    else:
        version = "v1"

    query = {"customerInvoiceNumber": invoice_id}
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
    header_request = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        use_root_auth=False,
        use_inclusion_auth=False,
        sku_product=False,
        account_id=account_id
    )
    base_url = get_microservice_base_url(environment, False)

    if zone in ["CA", "US"]:
        version = "v2"
    else:
        version = "v1"

    request_url = (
        f"{base_url}"
        "/invoices-service"
        f"/{version}"
    )

    # Place request
    response = place_request("GET", request_url, "", header_request)
    invoice_info = json.loads(response.text)

    if response.status_code == 200:
        return invoice_info

    return None


def print_invoices(
        invoice_info: dict,
        status: list,
        account_id: str,
        zone: str = None,
        environment: str = None):
    """
    Print invoices.

    Parameters
    ----------
    invoice_info : dict
    status : list
    account_id : str
    zone : str
        Defaults by `None`.
    environment : str
        Defaults by `None`.
    """
    invoices = []

    if zone in ["CA", "US"]:
        key = "vendorItemId"
        account_id = get_multivendor_account_id(account_id, zone, environment)
    else:
        key = "sku"

    for invoice in invoice_info.get("data", []):
        products = [item.get(key) for item in invoice.get("items")]

        if invoice.get("status") in status and account_id == invoice.get("accountId"):
            invoices.append({
                "Invoice ID": invoice.get("invoiceId"),
                "Customer Invoice Number": invoice.get("customerInvoiceNumber"),
                "Product Quantity": invoice.get("itemsQuantity", 0),
                "Sub Total": invoice.get("subtotal"),
                "Tax": invoice.get("tax"),
                "Discount": invoice.get("discount"),
                "Total": invoice.get("total"),
                key: ", ".join(products)
            })

    if invoices:
        print(text.default_text_color + '\nInvoice Information By Account  -  Status:' + status[1])
        print(tabulate(invoices, headers='keys', tablefmt='fancy_grid'))
    else:
        print(text.Red + '\nThere is no invoices with the status of ' + status[1] + ' for this account')
        
