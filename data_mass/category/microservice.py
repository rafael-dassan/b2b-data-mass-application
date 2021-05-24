import json
from typing import List, Union

from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request
)


def get_categories(
        zone: str,
        environment: str,
        vendor_id: str) -> list:
    """
    Get categories.

    Parameters
    ----------
    zone : str
    environment : str
    vendor_id : str

    Returns
    -------
    bool
        Whenever the request completed successfully.
    """
    base_url = get_microservice_base_url("environment")
    request_url = f"{base_url}/categories/?vendorId={vendor_id}"
    header = get_header_request(zone)

    response = place_request(
        request_method="GET",
        request_url=request_url,
        request_body="",
        request_headers=header
    )

    if response.status_code == 202:
        return json.loads(response.content)

    return []


def get_category_by_id(
        zone: str,
        environment: str,
        category_id: str) -> dict:
    """
    Get a specific category.

    Parameters
    ----------
    zone : str
    environment : str
    vendor_id : str

    Returns
    -------
    bool
        Whenever the request completed successfully.
    """
    base_url = get_microservice_base_url("environment")
    request_url = f"{base_url}/categories/{category_id}"
    header = get_header_request(zone)

    response = place_request(
        request_method="GET",
        request_url=request_url,
        request_body="",
        request_headers=header
    )

    if response.status_code == 200:
        content: dict = json.dumps(response.content)

        return content

    print("Generic print here.")
    return {}


def create_categories(
        zone: str,
        environment: str,
        categories: Union[List[dict], dict],
        asynchronous: bool = False) -> dict:
    """
    Get categories.

    Parameters
    ----------
    zone : str
    environment : str
    vendor_id : str
    asynchronous : bool
        Create or update a list of categories.\
        This request is asynchronous and it will\
        be placed upon a queue for a \
        post processor consumption. Default to `False`.

    Returns
    -------
    bool
        Whenever the request completed successfully.
    """
    endpoint = "categories/batch"

    if asynchronous:
        is_v1 = True
        endpoint = "category-relay-service"

    base_url = get_microservice_base_url("environment", is_v1)
    request_url = f"{base_url}/{endpoint}"
    header = get_header_request(zone)

    if isinstance(categories, dict):
        categories = [categories]

    response = place_request(
        request_method="GET",
        request_url=request_url,
        request_body=json.loads(categories),
        request_headers=header
    )

    if response.status_code == 200:
        content: dict = json.dumps(response.content)

        return content

    print("Generic print here.")

    return {}
