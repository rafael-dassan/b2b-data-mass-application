import concurrent.futures
import json
import os
from ast import literal_eval
from datetime import datetime
from distutils.util import strtobool
from json import dumps, loads
from random import randint, sample, uniform
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import click
import pkg_resources
from tabulate import tabulate

from data_mass.accounts import get_multivendor_account_id
from data_mass.classes.text import text
from data_mass.common import (
    convert_json_to_string,
    create_list,
    finish_application,
    get_header_request,
    get_microservice_base_url,
    place_request,
    update_value_to_json
)
from data_mass.config import get_settings
from data_mass.menus.product_menu import (
    print_is_alcoholic_menu,
    print_is_narcotic_menu,
    print_is_returnable_menu,
    print_product_quantity_menu
)

ZONES_NEW_ENDPOINT = ["AR", "PY", "PA"]
ZONES_DIFF_CONTRACT = ["AR", "PY", "US"]
TEXT_GREEN = text.Green


def generate_random_price_ids(qtd):
    if qtd < 1:
        return []

    array_random_ids = set()
    while len(array_random_ids) < qtd:
        new_prefix = "DM" + str(randint(10000, 99999))
        array_random_ids.add(new_prefix)

    return list(array_random_ids)


# Slices a list of products, returning the first X elements
def slice_array_products(quantity, products):
    return products[0:quantity]


def format_seconds_to_min_sec(seconds):
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i" % (minutes, seconds)


def request_post_price_microservice(
        account_id: str,
        zone: str,
        environment: str,
        sku_product: str,
        product_price_id: str,
        price_values: dict) -> bool:
    """
    Define price for a specific product via Pricing Engine Relay Service

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
    `True` in case of successful response or `False` in case of failure.
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
        request_url = "https://bees-services-sit.eastus2.cloudapp.azure.com/api/price-relay/v2"
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


def generate_price_values(zone, product):
    """
    Generate random price values for a specific product
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        product: product information, such as name, brand name, returnable, etc.
    Returns: new price values dict
    """

    # Generate random base price
    base_price = round(uniform(50, 2000), 2)
    deposit = None

    # Check if the SKU is returnable for ZA and DO (the ones that have deposit value enabled in order summary)
    if zone == "ZA" or zone == "DO":
        if "container" in product and product["container"]["returnable"] is True:
            deposit = (2 / 100) * base_price

    # Create dictionary with price values
    price_values = {
        "basePrice": base_price,
        "tax": randint(1, 5),
        "deposit": deposit,
        "quantityPerPallet": round(uniform(1, 2000), 2),
    }

    return price_values


# Add products in microservice account
def add_products_to_account_microservice(
    abi_id, zone, environment, delivery_center_id, all_products_zone
):
    # Get desired product quantity to be associated
    product_qty = print_product_quantity_menu(all_products_zone)

    # Builds a list of products to be posted, along with their generated random IDs for price and inclusion
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


def request_get_products_microservice(
        zone: str,
        environment: str,
        page_size: int = 100000) -> list:
    """
    Get all available products for a specific zone via Item Service.

    Parameters
    ----------
    zone : str
        One of `[AR, BR, CO, DO, MX, ZA, US]`.
    environment : str
        e.g., DEV, SIT, UAT.
    page_size : int
        Page size for searching products in the microservice.\
        Default to `100000`.

    Returns
    -------
    list
        array of items in case of success or `false` in case of failure
    """
    # Get headers
    request_headers = get_header_request(zone, True, False, False, False)

    # Get base URL
    if zone == "US":
        base_url = get_microservice_base_url(environment)

        request_url = (
            f"{base_url}"
            "/items/?"
            "includeDeleted=false"
            "&includeDisabled=false"
            f"&pageSize={page_size}"
        )
    else:
        base_url = get_microservice_base_url(environment)
        request_url = (
            f"{base_url}"
            "/items/?"
            "includeDeleted=false"
            "&includeDisabled=false"
            f"&pageSize={page_size}"
        )

    # Send request
    response = place_request("GET", request_url, "", request_headers)
    json_data = loads(response.text)

    if response.status_code == 200:
        return json_data["items"]

    print(
        f"{text.Red}"
        "\n- [Item Service] Failure to retrieve products.\n"
        f"Response Status: {response.status_code}.\n"
        f"Response message: {response.text}\n"
    )

    return []


# Make the necessary requests to add a product in a microservice-based zone
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

    return "success"


# Post requests for product price creation and product inclusion
def request_post_products_account_microservice(
    account_id, zone, environment, delivery_center_id, products_data
):
    results = list()
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
        text.default_text_color
        + "{}\n- Products added: {} / failed: {}. Completed in {} seconds.".format(
            text.Green, results.count("success"), results.count(False), lapsed
        )
    )

    return "success"


def request_post_price_inclusion_microservice(
    zone, environment, sku_product, delivery_center_id
):
    """
    Create product association to an account via Product Assortment Relay Service
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        sku_product: SKU unique identifier
        delivery_center_id: POC's unique delivery center
    Returns: `success` in case of successful response or `false` in case of failure
    """

    # Get headers
    request_headers = get_header_request(zone, False, False, True, sku_product)
    base_url = get_microservice_base_url(environment)

    # Get base URL
    request_url = f"{base_url}/product-assortment-relay/inclusion"

    # Get body request
    request_body = get_body_price_inclusion_microservice_request(delivery_center_id)

    # Send request
    response = place_request("POST", request_url, request_body, request_headers)
    if response.status_code == 202:
        return "success"

    print(
        text.Red
        + "\n- [Product Assortment Relay Service] Failure to associate the SKU {sku}. Response status: "
        "{response_status}. Response message: {response_message}".format(
            sku=sku_product,
            response_status=response.status_code,
            response_message=response.text,
        )
    )

    return False


# Create body for product inclusion
def get_body_price_inclusion_microservice_request(delivery_center_id):
    body_price_inclusion = dumps({"deliveryCenters": [delivery_center_id]})

    return body_price_inclusion


def request_get_offers_microservice(
        account_id: str,
        zone: str,
        environment: str) -> dict:
    """
    Get available SKUs for a specific account via Catalog Service
    Projection: SMALL
    Args:
        account_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
    Returns:
        json_data: new json object in case of success
        not_found: if there is no product association for an account
        false: if there is any error coming from the microservice
    """
    # Get headers
    headers = get_header_request(zone, True, False, False, False, account_id)
    base_url = get_microservice_base_url(environment, False)

    if zone == "US":
        account_id = get_multivendor_account_id(account_id, zone, environment)

        request_url = (
            f"{base_url}/v1"
            "/catalog-service"
            "/catalog"
            f"/items?accountId={account_id}"
            "&projection=SMALL"
        )
    else:
        request_url = (
            f"{base_url}"
            "/catalog-service"
            f"/catalog?accountId={account_id}"
            "&projection=SMALL"
        )

    # Send request
    response = place_request("GET", request_url, "", headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        return "not_found"
    elif response.status_code == 500:
        response_message = literal_eval(response.text)

        if "404 Not Found" in response_message.get("message"):
            return "not_found"
    else:
        print(
            text.Red
            + "\n- [Catalog Service] Failure to get a list of available SKUs. Response Status: "
            "{response_status}. Response message: {response_message}".format(
                response_status=response.status_code, response_message=response.text
            )
        )
        return False


def check_item_enabled(sku, zone, environment):
    """
    Check if a SKU is enabled via Item Service
    Args:
        sku: product unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
    Returns:
        json_data: new json object in case of success
        not_found: if the product is disabled
        False: if there is any error coming from the microservice
    """
    # Get base URL
    base_url = get_microservice_base_url(environment, False)

    if zone == "US":
        settings = get_settings()
        query = {
            "vendorId": settings.vendor_id,
            "vendorItemIds": sku,
            "includeDisabled": False
        }

        request_url = f"{base_url}/items/items?{urlencode(query)}"
    else:
        request_url = f"{base_url}/items/{sku}?includeDisabled=false"

    # Get headers
    request_headers = get_header_request(zone, True, False, False, False)

    # Send request
    response = place_request("GET", request_url, "", request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        if zone == "US":
            item, = json_data.get("items")

            return item.get("sku")

        return json_data["sku"]

    if response.status_code == 404:
        print(
            text.Red
            + "\n- [Item Service] SKU {sku} not found for country {country}".format(
                sku=sku, country=zone
            )
        )
        return False

    print(
        text.Red
        + "\n- [Item Service] Failure to update an item. Response Status: {response_status}. Response "
        "message: {response_message}".format(
            response_status=response.status_code, response_message=response.text
        )
    )
    return False


def request_get_products_by_account_microservice(account_id, zone, environment):
    """
    Get available SKUs for a specific account via Catalog Service
    Projection: LIST
    Args:
        account_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
    Returns:
        json_data: new json object in case of success
        not_found: if there is no product association for an account
        false: if there is any error coming from the microservice
    """

    # Define headers
    request_headers = get_header_request(zone, True, False, False, False, account_id)

    # Define base URL
    if zone == "US":
        account_id = get_multivendor_account_id(account_id, zone, environment)
        endpoint = "v1/catalog-service"
        v1 = False
    else:
        endpoint = "catalog-service"
        v1 = True

    base_url = get_microservice_base_url(environment, v1)
    request_url = f"{base_url}/{endpoint}/catalog/items?accountId={account_id}&projection=SMALL&includeDiscount=False&includeAllPromotions=False"

    # Send request
    response = place_request("GET", request_url, "", request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        return "not_found"
    else:
        print(
            text.Red
            + "\n- [Catalog Service] Failure to get a list of available SKUs. Response Status: "
            "{response_status}. Response message: {response_message}".format(
                response_status=response.status_code, response_message=response.text
            )
        )
        return False


def get_body_price_microservice_request_v2(
    abi_id: str,
    sku_product: str,
    product_price_id: str,
    price_values: dict,
    zone: str = None,
):
    """
    Create body for posting new product price rules (API version 2) to the Pricing Engine Relay Service
    Args:
        abi_id: account_id
        sku_product: SKU unique identifier
        product_price_id: price record unique identifier
        price_values: price values dict, including tax, base price and deposit
    Returns: new price body
    """
    
    # Create dictionary with price values
    dict_values = {
        "accounts": [abi_id],
        "prices[0].sku": sku_product,
        "prices[0].basePrice": price_values.get("basePrice"),
        "prices[0].deposit": price_values.get("deposit"),
        "prices[0].quantityPerPallet": price_values.get("quantityPerPallet"),
        "prices[0].taxes[0].taxId": product_price_id,
        "prices[0].taxes[0].value": str(price_values.get("tax")),
        "prices[0].validFrom": datetime.now().strftime("%Y-%m-%d"),
    }
    
    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/create_sku_price_payload_v2.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    if zone not in ZONES_DIFF_CONTRACT:
        del json_data["prices"][0]["validFrom"]
        del json_data["prices"][0]["consignment"]

    # Update the price values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    put_price_microservice_body = convert_json_to_string(json_object)

    return put_price_microservice_body


def request_get_account_product_assortment(
    account_id, zone, environment, delivery_center_id
):
    """
    Get product association for a specific account via Product Assortment Service
    Args:
        account_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        delivery_center_id: POC's delivery center unique identifier
    Returns: array of SKUs in case of success and `false` in case of failure
    """
    # Get headers
    headers = get_header_request(zone, True, False, False, False, account_id)

    # Get base URL
    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/product-assortment/?accountId={account_id}&deliveryCenterId={delivery_center_id}"

    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/product-assortment/?accountId={account_id}&deliveryCenterId={delivery_center_id}"

    response = place_request("GET", request_url, "", headers)
    json_data = loads(response.text)
    skus = json_data["skus"]
    if response.status_code == 200 and len(json_data) != 0:
        return skus
    elif response.status_code == 200 and len(skus) == 0:
        return "not_found"
    else:
        print(
            text.Red
            + "\n- [Product Assortment Service] Failure to get product association. Response Status: "
            "{response_status}. Response message: {response_message}".format(
                response_status=response.status_code, response_message=response.text
            )
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


def delete_item_v2(
        zone: str,
        environment: str,
        vendor_item_id: str) -> bool:
    """
    Delete a item from microservice.

    Parameters
    ----------
    zone : str
    environment : str
    vendor_item_id : str

    Returns
    -------
    bool
        Whnenever a deletions works it out.
    """
    request_headers = get_header_request(zone, False, True, False)

    # Get base URL
    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/item-relay/v2/items"

def get_item_input_data(zone: str):
    """
    Get input data from the user
    Returns: a dictionary containing the customized product data
    """
    zone = zone.upper()
    sku_identifier = None

    if zone == "US":
        vendor_item_id = input(f"{text.default_text_color}Vendor Item Id: ")

        if not vendor_item_id:
            vendor_item_id = "DM-{0}".format(str(randint(1, 100000)))
    else:
        sku_identifier = input("{0}SKU identifier: ".format(text.default_text_color))

        # Create random value for the SKU identifier if the entry is empty
        if not sku_identifier:
            sku_identifier = "DM-{0}".format(str(randint(1, 100000)))

    name = input("{0}Item name: ".format(text.default_text_color))
    brand_name = input(
        "{0}Brand name (e.g., SKOL, PRESIDENTE): ".format(text.default_text_color)
    ).upper()

    container_name = input(
        "{0}Container name (e.g., BOTTLE, PET, CAN): ".format(text.default_text_color)
    ).upper()

    # Validate container size input data
    while True:
        try:
            container_size = int(
                input("{0}Container size: ".format(text.default_text_color))
            )
            break
        except ValueError:
            print(
                "\n{0}- The container size must be an integer value\n".format(text.Red)
            )

    container_unit_measurement = input(
        "{0}Container unit of measurement (e.g., ML, OZ): ".format(
            text.default_text_color
        )
    ).upper()
    is_returnable = print_is_returnable_menu()
    is_narcotic = print_is_narcotic_menu()
    is_alcoholic = print_is_alcoholic_menu()

    # Create item dictionary
    item_data = {
        "sku": sku_identifier,
        "name": name,
        "brandName": brand_name,
        "subBrandName": brand_name,
        "package.id": str(randint(1, 1000)),
        "container.name": container_name,
        "container.size": container_size,
        "container.returnable": is_returnable,
        "container.unitOfMeasurement": container_unit_measurement,
        "salesRanking": randint(1, 100),
        "isNarcotic": is_narcotic,
        "isAlcoholic": is_alcoholic,
    }

    if zone == "US":
        has_category = input(f"{text.default_text_color}Is uncategorized? y/N: ")

        while (has_category.upper() in ["Y", "N"]) is False:
            print(text.Red + "\n- Invalid option")
            has_category = input(f"\n{text.default_text_color}Is uncategorized? y/N: ")

        item_data.update({
            "sku": vendor_item_id,
            "sourceData": {
                "vendorItemId": vendor_item_id
            },
            "uncategorized": bool(strtobool(has_category))
        })

    return item_data


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
                "unitOfMeasurement": product_data["container.unitOfMeasurement"]
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
            "container.unitOfMeasurement": product_data.get("container.unitOfMeasurement"),
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


def display_product_information(product_offers):
    """
    Display item information
    Args:
        product_offers: product data by account
    Returns: a table containing the available item information
    """
    product_information = list()

    for product in product_offers:
        product_values = {
            "SKU": product.get("sku"),
            "Name": product.get("sourceData", {}).get("vendorItemId"),
            "Price": product.get("price"),
            "Stock Available": product.get("stockAvailable"),
        }
        product_information.append(product_values)

    print(text.default_text_color + "\nProduct Information By Account")
    print(tabulate(product_information, headers="keys", tablefmt='fancy_grid'))
    

def get_sku_name(
        zone: str,
        environment: str,
        sku_id: str) -> str:
    """
    Get SKU by name.

    Parameters
    ----------
    zone : str
    environment : str
    sku_id : str

    Returns
    -------
    str
        The SKU name.
    """
    headers = get_header_request(zone, True)

    # Get url base
    base_url = get_microservice_base_url(environment, False)
    request_url = (
        f"{base_url}"
        "/items"
        f"/{sku_id}"
        "?includeDisabled=false"
    )

    # Place request
    response = place_request("GET", request_url, "", headers)
    json_data = loads(response.text)

    if response.status_code == 200 and json_data:
        return json_data["itemName"]

    return None


def display_items_information_zone(items):
    list_items = list()
    if len(items) != 0:
        for i in range(len(items)):
            dict_values = {
                "SKU": items[i]["sku"],
                "Name": items[i]["itemName"],
                "Description": items[i]["description"],
                "Brand Name": items[i]["brandName"],
                "Returnable": items[i]["container"]["returnable"],
            }
            list_items.append(dict_values)
    else:
        dict_values = {"Products": "None"}
        list_items.append(dict_values)

    print(text.default_text_color + "\nProduct Information By Zone")
    print(tabulate(list_items, headers="keys", tablefmt='fancy_grid'))


def get_sku_price(account_id, combo_item, zone, environment):
    # Get base URL
    request_url = (
        get_microservice_base_url(environment)
        + "/cart-calculator/prices?accountID="
        + account_id
    )

    # Get header request
    request_headers = get_header_request(zone, True, False, False, False, account_id)

    # Send request
    response = place_request("GET", request_url, "", request_headers)

    json_data = json.loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        for my_dict in json_data:
            if my_dict["sku"] == combo_item:
                return my_dict["price"]
    else:
        print(
            text.Red + "\n- [Pricing Engine Service] Failure to get price. Response "
            "status: {response_status}. Response message: {response_message}".format(
                response_status=response.status_code, response_message=response.text
            )
        )
        finish_application()


def request_empties_discounts_creation(
    account_id, zone, environment, empty_sku, discount_value
):
    # Define headers
    request_headers = get_header_request(zone)

    # Get base URL
    if zone != "US":
        request_url = (
            get_microservice_base_url(environment, False)
            + "/cart-calculation-relay/v2/prices"
        )
    else:
       request_url = "https://bees-services-sit.eastus2.cloudapp.azure.com/api/price-relay/v2"


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
    response = place_request("PUT", request_url, request_body, request_headers)

    if response.status_code == 202:
        return "success"
    else:
        print(
            text.Red
            + "\n- [Pricing Engine Relay Service] Failure to define price for the empty SKU {sku}. Response "
            "status: {response_status}. Response message: {response_message}".format(
                sku=empty_sku,
                response_status=response.status_code,
                response_message=response.text,
            )
        )
        return False


def get_items_associated_account(
    account_id: str,
    zone: str,
    environment: str,
    qty_lists: int = 1,
) -> List:
    """
    Get items associated in the POC.

    Parameters
    ----------
    account_id : str
        POC unique identifier
    zone : str
        e.g., AR, BR, DO, etc
    environment : str
        e.g., DEV, SIT, UAT
    qty_lists : int
        value to identify quantity of lists with skus.

    Returns
    -------
    Union[List, List[List]]
        list of dict with sku and quantity of products
        associated in the account.
        List of lists with dict of sku and quantity of products.
    """
    product_offers = request_get_offers_microservice(
        account_id=account_id,
        zone=zone,
        environment=environment
    )
    if not product_offers or product_offers == "not_found":
        print(
            f"{text.Red}"
            f"\n- [Catalog Service] - There is no product associated: "
            f"with the account {account_id}"
        )
        return []

    unique_sku = {item['sku'] for item in product_offers}
    unique_sku = sample(list(unique_sku), len(unique_sku))
    print(
        f"{TEXT_GREEN}"
        f"The account has {len(unique_sku)} products associated!"
    )
    quantity = click.prompt(
        f"{text.default_text_color}"
        "Quantity of products you want to include in this order",
        type=click.IntRange(1, len(unique_sku)),
    )
    if qty_lists > 1:
        items_list = [
            generate_list_skus(unique_sku,quantity) for _ in range(qty_lists)
        ]
    else:
        items_list = generate_list_skus(items=unique_sku, qty_items=quantity)
    return items_list


def generate_list_skus(
    items: list,
    qty_items:int,
) -> List:
    items_list = []
    for sku in sample(items, qty_items):
        data = {"sku": sku, "itemQuantity": randint(0, 10)}
        items_list.append(data)
    return items_list
