import json
from typing import Optional
from urllib.parse import urlencode

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

    if zone == "US":
        version = "v2"
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
    header_request = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        use_root_auth=False,
        use_inclusion_auth=False,
        sku_product=False,
        account_id=account_id
    )
    base_url = get_microservice_base_url(environment, False)

    if zone == "US":
        version = "v2"
        account_id = get_multivendor_account_id(account_id, zone, environment)
    else:
        version = "v1"

    request_url = (
        f"{base_url}"
        "/invoices-service"
        f"/{version}"
        f"?accountId={account_id}"
    )

    # Place request
    response = place_request("GET", request_url, "", header_request)
    invoice_info = json.loads(response.text)

    if response.status_code == 200:
        return invoice_info

    return None
