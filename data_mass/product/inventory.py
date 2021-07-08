import json
import os
from json import dumps, load, loads
from typing import Optional
from urllib.parse import urlencode

import pkg_resources
from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.common import (
    convert_json_to_string,
    get_header_request,
    get_microservice_base_url,
    place_request,
    update_value_to_json
)
from data_mass.config import get_settings


def request_inventory_creation(
        zone: str,
        environment: str,
        account_id: str,
        delivery_center_id: str,
        products: list,
        sku_id: Optional[str] = None,
        sku_quantity: Optional[int] = 0) -> bool:
    """
    Create a new inventory on the microservice.

    Parameters
    ----------
    zone : str
    environment : str
    account_id : str
    delivery_center_id : str
    products : list
    sku_id : str
    sku_quantity : int

    Returns
    -------
    bool
        Whenever a request is succeded or not.
    """

    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=False,
        use_root_auth=False,
        use_inclusion_auth=True
    )
    
    if zone == "US":
        endpoint: str = f"inventory-relay/inventory/{delivery_center_id}"
        is_v1: bool = False

        response: dict = get_delivery_center_inventory_v2(
            account_id=account_id,
            zone=zone,
            environment=environment,
            delivery_center_id=delivery_center_id
        )

        request_body: dict = {"inventory": []}
        for inventory in response:
            for product in inventory.get("inventories", []):
                if product.get("vendorItemId") == sku_id:
                    product.update({"quantity": int(sku_quantity)})

                request_body["inventory"].append(product)
    else:
        request_body = get_inventory_payload(
            zone=zone,
            environment=environment,
            account_id=account_id,
            products=products,
            delivery_center_id=delivery_center_id,
            sku_id=sku_id,
            sku_quantity=sku_quantity
        )
        is_v1 = True
        endpoint = "inventory-relay/add"

    base_url = get_microservice_base_url(environment, is_v1)
    request_url = f"{base_url}/{endpoint}"

    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=json.dumps(request_body),
        request_headers=request_headers
    )

    if response.status_code == 202:
        return True
    else:
        print((
            f'\n{text.Red}- '
            '[Inventory Relay Service] Failure to add stock for products. '
            f'Response Status: {response.status_code}. '
            f'Response message: {response.text}'
        ))

        return False


def get_inventory_payload(
        zone: str,
        environment: str,
        account_id: str,
        products: list,
        delivery_center_id: str,
        sku_id: str,
        sku_quantity: int) -> dict:
    """
    Get inventory from microservice.

    Parameters
    ----------
    zone : str
    environment : str
    account_id : str
    products : list
    delivery_center_id : str
    sku_id : str
    sku_quantity : int

    Returns
    -------
    dict
        The request body.
    """
    get_inventory_response = get_delivery_center_inventory(
        environment=environment,
        zone=zone,
        account_id=account_id,
        delivery_center_id=delivery_center_id,
        products=products
    )

    inventory = get_inventory_response['inventory'] if get_inventory_response else {}

    quantity = 999999
    if int(sku_quantity) >= 0:
        specific_quantity = int(sku_quantity)

    inventory_list = []

    len_inventory = len(inventory) if inventory else len(products)

    for product in products[:len_inventory]:
        if sku_id is not None:
            if sku_id == product:
                specific_inventory = {
                    'sku': sku_id,
                    'quantity': specific_quantity
                }
                inventory_list.append(specific_inventory)
            else:
                current_inventory = {
                    'sku': inventory[products.index(product)]['sku'],
                    'quantity': inventory[products.index(product)]['quantity']
                }
                inventory_list.append(current_inventory)
        else:
            default_inventory = {
                'sku': product,
                'quantity': quantity
            }
            inventory_list.append(default_inventory)
    
    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/create_inventory_payload.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    dict_values = {
        'fulfillmentCenterId': delivery_center_id,
        'inventory': inventory_list
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    return json_object


def display_inventory_by_account(inventory: list, zone: str = None):
    """
    Display inventory on the screen.

    Parameters
    ----------
    inventory : list
    """
    inventory_info = []

    if zone == "US":
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
        query = f"{urlencode(query)}&deliveryCenters={delivery_center_id}"

    request_url = f"{base_url}/inventory/inventories?{query}"
    
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
        return None

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
        return None

    print(
        f'\n{text.Red}'
        '- [Inventory Service] Failure to retrieve inventory information. '
        f'Response Status: {response.status_code}. '
        f'Response message: {response.text}'
    )

    return None
