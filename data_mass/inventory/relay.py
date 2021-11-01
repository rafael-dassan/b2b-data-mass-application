from json import dumps, loads
from typing import Optional, Union

import pkg_resources

from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request,
    update_value_to_json
)
from data_mass.enforcement import update_sku_limit_enforcement_microservice


def get_inventory_payload(
        products: list,
        delivery_center_id: str,
        sku_id: str,
        sku_quantity: int) -> dict:
    """
    Get inventory from microservice.

    Parameters
    ----------
    products : list
    delivery_center_id : str
    sku_id : str
    sku_quantity : int

    Returns
    -------
    dict
        The request body.
    """

    quantity = 999999
    if int(sku_quantity) >= 0:
        specific_quantity = int(sku_quantity)

    inventory_list = []

    len_inventory = len(products)

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
                    'sku': products.index(product),
                    'quantity': quantity
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
        skus_id: list,
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

    if zone in ["BR", "DO", "ZA"]:
        for sku_id in skus_id:
            update_sku_limit_enforcement_microservice(
                zone, 
                environment,
                account_id,
                sku_id,
                999999
            )
        # TODO: treat the status codes to check if some are not 202
        return True

    if zone in ["CA", "US"]:
        endpoint: str = f"inventory-relay/inventory/{delivery_center_id}"
        is_v1: bool = False

        request_body: dict = {"inventory": []}
        for sku_id in skus_id:
            request_body["inventory"].append({
                "vendorItemId": sku_id,
                "quantity": sku_quantity
            })
    else:
        is_v1: bool = True
        endpoint: str = "inventory-relay/add"

        request_body: dict = get_inventory_payload(
            products=skus_id,
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

    return handle_response(response)

def create_skus_from_products_or_sku_id(skus_id: list, sku_id: Optional[str]): 
    if(skus_id): 
        return skus_id
    else:
        return [sku_id]

def handle_response(response): 
    if response.status_code == 202:
        return True

    print(
        f'\n{text.Red}- '
        '[Inventory Relay Service] Failure to add stock for products. '
        f'Response Status: {response.status_code}. '
        f'Response message: {response.text}'
    )

    return False

def delete_inventory_for_delivery_center(
        zone: str,
        environment: str,
        delivery_center_id: str) -> Union[bool, str]:
    # Get headers
    request_headers = get_header_request(zone=zone, use_inclusion_auth=True)
    base_url = get_microservice_base_url(environment)

    # Get base URL
    request_url = f"{base_url}/inventory-relay/deliveryCenter/{delivery_center_id}"

    # Send request
    response = place_request(
        request_method="DELETE",
        request_url=request_url,
        request_body=None,
        request_headers=request_headers
    )

    if response.status_code == 202:
        return True

    return False
