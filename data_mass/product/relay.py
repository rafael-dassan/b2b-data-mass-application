import concurrent.futures
import json
from datetime import datetime
from random import randint, uniform
from typing import Optional, Union

import pkg_resources

from data_mass.classes.text import text
from data_mass.common import (
    convert_json_to_string,
    get_header_request,
    get_microservice_base_url,
    place_request,
    update_value_to_json
)
from data_mass.menus.product_menu import print_product_quantity_menu
from data_mass.product.service import check_item_enabled
from data_mass.product.utils import (
    generate_price_values,
    generate_random_price_ids,
    get_body_price_inclusion_microservice_request,
    get_body_price_microservice_request_v2,
    slice_array_products
)

ZONES_NEW_ENDPOINT = ["AR", "PY", "PA"]


def request_post_price_microservice(
        account_id: str,
        zone: str,
        environment: str,
        sku_product: str,
        product_price_id: str,
        price_values: dict) -> bool:
    """
    Define price for a specific product via \
    Pricing Engine Relay Service.

    Parameters
    ----------
    account_id : str
        POC unique identifier.
    zone : str
        e.g., AR, BR, CO, DO, MX, ZA or US.
    environment : str
        e.g., DEV, SIT or UAT.
    sku_product : str
        SKU unique identifier.
    product_price_id : str
        Price record unique identifier.
    price_values : str
        Price values dict, including tax, base price and deposit.

    Returns
    -------
    `True` in case of successful response or \
    `False` in case of failure.
    """
    request_headers = get_header_request(zone)
    base_url = get_microservice_base_url(environment, False)

    if zone in ZONES_NEW_ENDPOINT:
        request_url = f"{base_url}/price-relay/v1"
        request_body = get_body_price_microservice_request_v2(
            abi_id=account_id,
            sku_product=sku_product,
            product_price_id=product_price_id,
            price_values=price_values,
            zone=zone
        )
    elif zone == "US":
        request_url = f"{base_url}/price-relay/v2"
        request_body = get_body_price_microservice_request_v2_us(
            account_id=account_id,
            sku_product=sku_product,
            product_price_id=product_price_id,
            price_values=price_values
        )
    else:
        request_url = f"{base_url}/cart-calculation-relay/v2/prices"
        request_body = get_body_price_microservice_request_v2(
            abi_id=account_id,
            sku_product=sku_product,
            product_price_id=product_price_id,
            price_values=price_values
        )

    # Send request
    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 202:
        return True

    print(
        f"{text.Red}\n- [Pricing Engine Relay Service] "
        f"Failure to define price for the SKU {sku_product}.\n"
        f"Status: {response.status_code}\n"
        f"Response message: {response.text}\n"
    )

    return False


def get_body_price_microservice_request_v2_us(
        account_id: str,
        sku_product: str,
        product_price_id: str,
        price_values: dict):
    """
    Create body por posting new product price rules for us.

    Parameters
    ----------
    account_id : str
    sku_product : str
    product_price_id : str
    price_values : dict

    Returns
    -------
    str
        The request body.
    """
    content = {
        "vendorAccountIds": [account_id],
        "prices": [{
            "vendorItemId": str(randint(1, 99999)),
            "sku": sku_product,
            "basePrice": price_values.get("basePrice"),
            "measureUnit": "CS",
            "minimumPrice": 0,
            "deposit": price_values.get("deposit"),
            "quantityPerPallet": price_values.get("quantityPerPallet"),
            "promotionalPrice": {
                "price": round(uniform(10.99, 99.99), 2),
                "externalId": "ZTPM",
                "validUntil": "2021-12-31"
            },
            "measureUnitConversion": {
                "6PACK": 6,
                "CASE": 30,
                "LITER": 1
            },
            "taxes": [{
                "taxId": product_price_id,
                "type": "$",
                "value": str(price_values.get("tax")),
                "taxBaseInclusionIds": [],
                "hidden": False
            }]
        }]
    }

    body = json.dumps(content)

    return body


def add_products_to_account_microservice(
    abi_id, zone, environment, delivery_center_id, all_products_zone
):
    # Get desired product quantity to be associated
    product_qty = print_product_quantity_menu(all_products_zone)

    # Builds a list of products to be posted,\
    # along with their generated random IDs for price and inclusion
    products_data = list(
        zip(
            generate_random_price_ids(product_qty),
            slice_array_products(product_qty, all_products_zone),
        )
    )

    # Associate products to an account
    result = request_post_products_account_microservice(
        abi_id, zone, environment, delivery_center_id, products_data
    )

    return result


def product_post_requests_microservice(
        product_data: dict,
        account_id: str,
        zone: str,
        environment: str,
        delivery_center_id: str) -> bool:
    """
    Create prices for customers.

    Parameters
    ----------
    product_data : dict
    account_id : str
    zone : str
    environment : str
    delivery_center_id : str

    Returns
    -------
    bool
        Whenever the request is successful or not.
    """
    index, product = product_data
    price_values = generate_price_values(zone, product)

    # Call product association via Product Assortment Relay Service
    product_inclusion_ms_result = request_post_price_inclusion_microservice(
        zone=zone,
        environment=environment,
        sku_product=product["sku"],
        delivery_center_id=delivery_center_id
    )

    if not product_inclusion_ms_result:
        return False

    # Call price inclusion via Pricing Engine Relay Service
    price_inclusion_result = request_post_price_microservice(
        account_id=account_id,
        zone=zone,
        environment=environment,
        sku_product=product["sku"],
        product_price_id=index,
        price_values=price_values
    )

    if not price_inclusion_result:
        return False

    return True


def request_post_products_account_microservice(
        account_id: str,
        zone: str,
        environment: str,
        delivery_center_id: str,
        products_data: dict) -> bool:
    """
    Post requests for product price creation and product inclusion.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str
    delivery_center_id : str
    products_data : dict

    Returns
    -------
    bool
        Whenever product creation is carried out successfully or not.
    """
    results = []
    last = datetime.now()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                product_post_requests_microservice,
                product_data,
                account_id,
                zone,
                environment,
                delivery_center_id,
            )
            for product_data in products_data
        ]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    now = datetime.now()
    lapsed = (now - last).seconds

    print(
        f"{text.default_text_color}\n"
        f"{text.Green}- Products added: "
        f"{results.count(True)} / failed: {results.count(False)}. "
        f"Completed in {lapsed} seconds."
    )

    return True


def request_post_price_inclusion_microservice(
        zone: str,
        environment: str,
        sku_product: str,
        delivery_center_id: str) -> Union[bool, str]:
    """
    Create product association to an account via \
    Product Assortment Relay Service.

    Parameters
    ----------
    zone : str
        e.g., AR, BR, CO, DO, MX, ZA.
    environment : str
        e.g., DEV, SIT, UAT.
    sku_product : str
        SKU unique identifier.
    delivery_center_id : str
        POC's unique delivery center.

    Returns
    -------
    Union[bool, str]
        `success` in case of successful response or `false` in \
        case of failure
    """

    # Get headers
    request_headers = get_header_request(zone, False, False, True, sku_product)
    base_url = get_microservice_base_url(environment)

    # Get base URL
    request_url = f"{base_url}/product-assortment-relay/inclusion"

    # Get body request
    request_body = get_body_price_inclusion_microservice_request(
        delivery_center_id
    )

    # Send request
    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 202:
        return "success"

    print(
        f"{text.Red}\n"
        "- [Product Assortment Relay Service] "
        f"Failure to associate the SKU {sku_product}."
        f"\nResponse status: {response.status_code}"
        f"Response message: {response.text}"
    )

    return False


def create_product(
        zone: str,
        environment: str,
        product_data: dict) -> dict:
    """
    Create or update an product via Item Relay Service.

    Parameters
    ----------
    zone : str
        e.g., AR, BR, CO, DO, MX, ZA.
    environment : str
        e.g., DEV, SIT, UAT.
    product_data : str
        All necessary and relevant SKU data.

    Returns
    -------
    dict
        `product_data in case of success or `None` in case of failure.
    """
    # Define headers
    request_headers = get_header_request(zone, False, True, False)

    # Get base URL
    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/item-relay/items"

    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/create_item_payload.json"
    )
    body: dict = json.loads(content.decode("utf-8"))
    body.update(product_data)

    # Place request
    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=json.dumps([body]),
        request_headers=request_headers
    )

    if response.status_code == 202:
        key = "vendorItemId" if zone == "US" else "sku"

        update_item_response = set_item_enabled(
            zone,
            environment,
            product_data
        )
        get_item_response = check_item_enabled(
            product_data.get(key),
            zone,
            environment
        )

        if update_item_response and get_item_response:
            return product_data

    print(
        f"\n{text.Red}- [Item Relay Service] Failure to update an item.\n"
        f"Response Status: {response.status_code}.\n"
        f"Response message: {response.text}\n"
    )

    return None


def create_product_v2(
        zone: str,
        environment: str,
        product_data: dict,
        vendor_item_id: Optional[str] = None) -> dict:
    """
    Create product using ms version 2.

    Parameters
    ----------
    zone : str
    environment : str
    product_data : dict
    vendor_item_id : str, optional
        Required if the target zone is US.

    Returns
    -------
    dict
        The API response.
    """
    request_headers = get_header_request(zone, False, True, False)

    # Get base URL
    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/item-relay/v2/items"

    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/update_item_payload_v2.json"
    )
    body: dict = json.loads(content.decode("utf-8"))

    product_data.update({
        "sku": product_data.get("sku"),
        "name": product_data.get("name"),
        "brandId": str(randint(1, 1000)),
        "package": {
            "count": 1,
            "id": "01",
            "itemCount": 12,
            "name": "CD",
            "pack": "string"
        },
        "container": {
            "name": product_data["container.name"],
            "size": product_data["container.size"],
            "returnable": product_data["container.returnable"],
            "unitOfMeasurement": product_data["container.unitOfMeasurement"]
        },
        "uncategorized": product_data.get("uncategorized", False)
    })
    body.update(product_data)

    # Place request
    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=json.dumps([body]),
        request_headers=request_headers
    )
    if response.status_code == 202:
        update_item_response = set_item_enabled(
            zone,
            environment,
            product_data
        )
        get_item_response = check_item_enabled(
            product_data.get("sku"),
            zone,
            environment
        )

        if update_item_response and get_item_response:
            return product_data
    print(
        f"\n{text.Red}- [Item Relay Service] Failure to update an item.\n"
        f"Response Status: {response.status_code}.\n"
        f"Response message: {response.text}\n"
    )

    return None


def set_item_enabled(
        zone: str,
        environment: str,
        product_data: dict) -> bool:
    """
    Update an item via Item Service.

    Parameters
    ----------
    zone : str
        One of `[AR, BR, CO, DO, MX, ZA]`.
    environment : str
        One of `[DEV, SIT, UAT]`.
    product_data : str
        All necessary and relevant SKU data.

    Returns
    -------
    Whenever the item is updated successfully or not.
    """
    request_headers = get_header_request(zone, True, False, False)
    body = {}
    sku = product_data.get("sku")

    # Get base URL
    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/items/{sku}"

    if zone == "US":
        request_url = f"{base_url}/item-relay/v2/items"
        payload_path = "data/update_item_payload_v2.json"

        product_data.update({
            "sku": product_data.get("sku"),
            "name": product_data.get("name"),
            "brandId": str(randint(1, 1000)),
            "package": {
                "count": 1,
                "id": "01",
                "itemCount": 12,
                "name": "CD",
                "pack": "string"
            },
            "container": {
                "name": product_data["container.name"],
                "size": product_data["container.size"],
                "returnable": product_data["container.returnable"],
                "unitOfMeasurement":
                    product_data["container.unitOfMeasurement"]
            }
        })
    else:
        # get data from Data Mass files
        payload_path = "data/update_item_payload.json"
        content: bytes = pkg_resources.resource_string(
            "data_mass",
            payload_path
        )

        body: dict = json.loads(content.decode("utf-8"))
        product_data.update({
            "itemName": product_data.get("name"),
            "package.packageId": product_data.get("package.id"),
            "container.name": product_data.get("container.name"),
            "container.itemSize": product_data.get("container.size"),
            "container.unitOfMeasurement": product_data.get(
                "container.unitOfMeasurement"
            ),
            "description": product_data.get("name"),
            "salesRanking": product_data.get("salesRanking"),
        })

    body.update(product_data)

    # send as list of object or just object?
    body = json.dumps([body]) if zone == "US" else json.dumps(body)

    # Place request
    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=body,
        request_headers=request_headers
    )

    if response.status_code in [200, 202]:
        return True

    print(
        f"{text.Red}\n"
        + "- [Item Service] Failure to update an item.\n"
        f"Response Status: {response.status_code}.\n"
        f"Response message: {response.text}\n"
    )

    return False


def request_empties_discounts_creation(
        account_id: str,
        zone: str,
        environment: str,
        empty_sku: str,
        discount_value: float) -> bool:
    """
    Create empties discounts.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str
    empty_sku : str
    discount_value : float

    Returns
    -------
    bool
        Whenever empties discounts creation is carried out \
        successfully or not.
    """
    # Define headers
    request_headers = get_header_request(zone)

    # Get base URL
    if zone != "US":
        request_url = (
            get_microservice_base_url(environment, False)
            + "/cart-calculation-relay/v2/prices"
        )
    else:
        request_url = (
            "https://bees-services-sit.eastus2.cloudapp.azure.com"
            "/api/price-relay/v2"
        )

    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/create_empties_discounts_payload.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    dict_values = {
        "accounts": [account_id],
        "prices[0].sku": empty_sku,
        "prices[0].basePrice": discount_value,
        "prices[0].minimumPrice": discount_value,
    }

    # Update JSON values
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Place request
    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 202:
        return True

    print(
        f"{text.Red}\n"
        "- [Pricing Engine Relay Service] "
        f"Failure to define price for the empty SKU {empty_sku}.\n"
        f"status: {response.status_code}."
        f"Response message: {response.text}"
    )

    return False
