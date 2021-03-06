from json import dumps, loads
from urllib.parse import urlencode

from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request
)
from data_mass.config import get_settings


def get_delivery_center_inventory_v2(
        account_id: str,
        zone: str,
        environment: str,
        delivery_center_id: str = None) -> dict:
    """
    Get inventory from a specific Delivery Center.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str
    delivery_center_id : str
        Default by `None`.

    Returns
    -------
    dict
        List of all Delivery Center inventory.
    """
    header = get_header_request(zone)
    base_url = get_microservice_base_url(environment, False)
    settings = get_settings()

    query = {"vendorId": settings.vendor_id}

    if delivery_center_id:
        query.update({"deliveryCenters": delivery_center_id})

    request_url = f"{base_url}/inventory/inventories?{urlencode(query)}"

    response = place_request(
        request_method="GET",
        request_url=request_url,
        request_body="",
        request_headers=header
    )

    if response.status_code == 200:
        data = loads(response.text)
        return data

    if response.status_code == 404:
        return {}

    print(
        f'\n{text.Red}'
        '- [Inventory Service] Failure to retrieve inventory information. '
        f'Response Status: {response.status_code}. '
        f'Response message: {response.text}'
    )

    return None


def get_delivery_center_inventory(
        environment: str,
        zone: str,
        account_id: str,
        delivery_center_id: str,
        products: list) -> dict:
    """
    Get inventory from a specific Delivery Center.

    Paramaters
    ----------
    environment : str
    zone : st
    account_id : str
    delivery_center_id : str
    products : list

    Returns
    -------
    list
        List of all Delivery Center inventory.
    """
    body = {
        "fulfillmentCenterId": delivery_center_id,
        "skus": products
    }

    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        account_id=account_id
    )

    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/inventory/"
    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=dumps(body),
        request_headers=request_headers
    )

    json_data = loads(response.text)

    if response.status_code == 200:
        return json_data

    if response.status_code == 404:
        return {}

    print(
        f'\n{text.Red}'
        '- [Inventory Service] Failure to retrieve inventory information. '
        f'Response Status: {response.status_code}. '
        f'Response message: {response.text}'
    )

    return {}


def display_inventory_by_account(inventory: list, zone: str = None):
    """
    Display inventory on the screen.

    Parameters
    ----------
    inventory : list
    """
    inventory_info = []

    if zone in ["CA", "US"]:
        inventory = inventory[0]

        for item in inventory["inventories"]:
            inventory_values = {
                "vendorItemId": item["vendorItemId"],
                "quantity": item["quantity"]
            }

            inventory_info.append(inventory_values)
    else:
        for item in inventory["inventory"]:
            inventory_values = {
                "sku": item["sku"],
                "quantity": item["quantity"]
            }

            inventory_info.append(inventory_values)

    print(text.default_text_color + '\nInventory/stock information ')
    print(tabulate(inventory_info, headers='keys', tablefmt='fancy_grid'))
