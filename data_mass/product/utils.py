import json
from datetime import datetime
from distutils.util import strtobool
from json import dumps
from random import randint, uniform

import pkg_resources
from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.common import convert_json_to_string, update_value_to_json
from data_mass.menus.product_menu import (
    print_is_alcoholic_menu,
    print_is_narcotic_menu,
    print_is_returnable_menu
)

ZONES_DIFF_CONTRACT = ["AR", "PY", "US"]


def generate_random_price_ids(qtd):
    if qtd < 1:
        return []

    array_random_ids = set()
    while len(array_random_ids) < qtd:
        new_prefix = "DM" + str(randint(10000, 99999))
        array_random_ids.add(new_prefix)

    return list(array_random_ids)


def slice_array_products(quantity: int, products: list) -> list:
    """
    Slices a list of products, returning the first X elements

    Parameters
    ----------
    quantity : int
    products : list

    Returns
    -------
    list
        A new list.
    """
    return products[0:quantity]


def format_seconds_to_min_sec(seconds):
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i" % (minutes, seconds)


def generate_price_values(zone, product):
    """
    Generate random price values for a specific product
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        product: product information, such as name, brand name,\
        returnable, etc.
    Returns: new price values dict
    """

    # Generate random base price
    base_price = round(uniform(50, 2000), 2)
    deposit = None

    # Check if the SKU is returnable for ZA and DO
    # (the ones that have deposit value enabled in order summary)
    if zone == "ZA" or zone == "DO":
        if "container" in product and product.get("container", {}) is not None and product.get("container", {}).get("returnable"):
            deposit = (2 / 100) * base_price

    # Create dictionary with price values
    price_values = {
        "basePrice": base_price,
        "tax": randint(1, 5),
        "deposit": deposit,
        "quantityPerPallet": round(uniform(1, 2000), 2),
    }

    return price_values


def get_body_price_inclusion_microservice_request(
        delivery_center_id: str) -> dict:
    """
    Create body for product inclusion

    Parameters
    ----------
    delivery_center_id : str

    Returns
    -------
    dict
        A new body.
    """
    body_price_inclusion = dumps({
        "deliveryCenters": [delivery_center_id]
    })

    return body_price_inclusion


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


def get_item_input_data(zone: str):
    """
    Get input data from the user.

    Parameters
    ----------
    zone : str

    Returns
    -------
    dict
        A dictionary containing the customized product data
    """
    zone = zone.upper()
    sku_identifier = None

    if zone in ["CA", "US"]:
        vendor_item_id = input(f"{text.default_text_color}Vendor Item Id: ")

        if not vendor_item_id:
            vendor_item_id = "DM-{0}".format(str(randint(1, 100000)))
    else:
        sku_identifier = input(f"{text.default_text_color}SKU identifier: ")

        # Create random value for the SKU identifier if the entry is empty
        if not sku_identifier:
            sku_identifier = "DM-{0}".format(str(randint(1, 100000)))

    name = input(f"{text.default_text_color}Item name: ")
    brand_name = input(
        f"{text.default_text_color}"
        "Brand name (e.g., SKOL, PRESIDENTE): "
    ).upper()

    container_name = input(
        f"{text.default_text_color}"
        "Container name (e.g., BOTTLE, PET, CAN): "
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
                f"\n{text.Red}"
                "- The container size must be an integer value\n"
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
        "container": {
            "name": container_name,
            "size": container_size,
            "returnable": is_returnable,
            "unitOfMeasurement": container_unit_measurement
        },
        "salesRanking": randint(1, 100),
        "isNarcotic": is_narcotic,
        "isAlcoholic": is_alcoholic,
    }

    if zone in ["CA", "US"]:
        has_category = input(
            f"{text.default_text_color}"
            "Is uncategorized? y/N: "
        )

        while (has_category.upper() in ["Y", "N"]) is False:
            print(text.Red + "\n- Invalid option")
            has_category = input(
                f"\n{text.default_text_color}"
                "Is uncategorized? y/N: "
            )

        item_data.update({
            "sku": vendor_item_id,
            "sourceData": {
                "vendorItemId": vendor_item_id
            },
            "uncategorized": bool(strtobool(has_category))
        })

    return item_data


def display_items_information_zone(items: list):
    """
    Display items information zone.

    Parameters
    ----------
    items : list
    """
    list_items = []

    if items:
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


def get_body_price_microservice_request_v2(
        abi_id: str,
        sku_product: str,
        product_price_id: str,
        price_values: dict,
        zone: str = None) -> dict:
    """
    Create body for posting new product price rules (API version 2) \
    to the Pricing Engine Relay Service.

    Parameters
    ----------
    abi_id : str
        The account_id.
    sku_product : str
        The SKU unique identifier.
    product_price_id : str
        The price record unique identifier.
    price_values : dict
        The price values dict, including tax, base price and deposit.
    Returns
    -------
    dict
        The new price body.
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
