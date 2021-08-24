from json import dumps, loads
from typing import Optional

import pkg_resources

from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request,
    update_value_to_json
)
from data_mass.inventory.service import (
    get_delivery_center_inventory,
    get_delivery_center_inventory_v2
)


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

    inventory = get_inventory_response.get('inventory', {})

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
    json_data = loads(content.decode("utf-8"))

    dict_values = {
        'fulfillmentCenterId': delivery_center_id,
        'inventory': inventory_list
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    return json_object


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

    if zone in ["CA", "US"]:
        endpoint: str = f"inventory-relay/inventory/{delivery_center_id}"
        is_v1: bool = False

        request_body: dict = {"inventory": []}
        for product in products:
            request_body["inventory"].append({
                "vendorItemId": product,
                "quantity": sku_quantity
            })
    else:
        is_v1: bool = True
        endpoint: str = "inventory-relay/add"

        request_body: dict = get_inventory_payload(
            zone=zone,
            environment=environment,
            account_id=account_id,
            products=products,
            delivery_center_id=delivery_center_id,
            sku_id=sku_id,
            sku_quantity=sku_quantity
        )

    base_url = get_microservice_base_url(environment, is_v1)
    request_url = f"{base_url}/{endpoint}"

    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=dumps(request_body),
        request_headers=request_headers
    )

    if response.status_code == 202:
        return True

    print(
        f'\n{text.Red}- '
        '[Inventory Relay Service] Failure to add stock for products. '
        f'Response Status: {response.status_code}. '
        f'Response message: {response.text}'
    )

    return False
