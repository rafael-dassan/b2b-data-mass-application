import json
from ast import literal_eval
from json import loads
from typing import Optional
from urllib.parse import urlencode

from data_mass.account.accounts import get_multivendor_account_id
from data_mass.classes.text import text
from data_mass.common import (
    finish_application,
    get_header_request,
    get_microservice_base_url,
    place_request
)
from data_mass.config import get_settings


def request_get_products_microservice(
        zone: str,
        environment: str,
        page_size: int = 100000) -> Optional[list]:
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

    return None


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
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        use_root_auth=False,
        use_inclusion_auth=False,
        sku_product=False,
        account_id=account_id
    )

    # Define base URL
    if zone == "US":
        account_id = get_multivendor_account_id(account_id, zone, environment)
        endpoint = "v1/catalog-service"
        v1 = False
    else:
        endpoint = "catalog-service"
        v1 = True

    base_url = get_microservice_base_url(environment, v1)
    query = {
        "accountId": account_id,
        "projection": "SMALL",
        "includeDiscount": False,
        "includeAllPromotions": False
    }

    request_url = f"{base_url}/{endpoint}/catalog/items?{urlencode(query)}"

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
