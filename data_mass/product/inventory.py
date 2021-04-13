import os
from json import dumps, load, loads
from typing import Optional

from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    convert_json_to_string,
    place_request,
    update_value_to_json,
)


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

    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/inventory-relay/add"

    request_body = get_inventory_payload(
        zone=zone,
        environment=environment,
        account_id=account_id,
        products=products,
        delivery_center_id=delivery_center_id,
        sku_id=sku_id,
        sku_quantity=sku_quantity
    )

    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=request_body,
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
        sku_quantity: int) -> str:
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
    str
        The request body.
    """
    get_inventory_response = get_delivery_center_inventory(
        environment=environment,
        zone=zone,
        account_id=account_id,
        delivery_center_id=delivery_center_id,
        products=products
    )

    if not get_inventory_response:
        print((
            f'{text.Red}\n'
            f'Error while trying to retrive inventory for "{delivery_center_id}".'
        ))
        exit()

    inv = get_inventory_response['inventory']
    
    quantity = 999999
    if int(sku_quantity) >= 0:
        specific_quantity = int(sku_quantity)

    inventory_list = []

    for product in products[:len(inv)]:
        if sku_id is not None:
            if sku_id == product:
                specific_inventory = {
                    'sku': sku_id,
                    'quantity': specific_quantity
                }
                inventory_list.append(specific_inventory)
            else:
                current_inventory = {
                    'sku': inv[products.index(product)]['sku'],
                    'quantity': inv[products.index(product)]['quantity']
                }
                inventory_list.append(current_inventory)
        else:
            default_inventory = {
                'sku': product,
                'quantity': quantity
            }
            inventory_list.append(default_inventory)

    # Create file path
    abs_path = os.path.abspath(os.path.dirname("__main__"))
    file_path = os.path.join(abs_path, 'data_mass/data/create_inventory_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = load(file)

    dict_values = {
        'fulfillmentCenterId': delivery_center_id,
        'inventory': inventory_list
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    return request_body


def display_inventory_by_account(inventory: list):
    """
    Display inventory on the screen.

    Parameters
    ----------
    inventory : list
    """
    inventory_info = []

    for item in inventory["inventory"]:
        inventory_values = {
            "sku": item["sku"],
            "quantity": item["quantity"]
        }

        inventory_info.append(inventory_values)

    print(text.default_text_color + '\nInventory/stock information ')
    print(tabulate(inventory_info, headers='keys', tablefmt='grid'))


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
    elif response.status_code == 404:
        return {}
    else:
        print((
            f'\n{text.Red}'
            '- [Inventory Service] Failure to retrieve inventory information. '
            f'Response Status: {response.status_code}. '
            f'Response message: {response.text}'
        ))

        return {}