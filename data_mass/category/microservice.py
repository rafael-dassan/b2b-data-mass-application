import json
from typing import List, Union

from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request
)


def get_categories(zone: str, environment: str) -> list:
    """
    Get categories.

    Parameters
    ----------
    zone : str
    environment : str

    Returns
    -------
    bool
        Whenever the request completed successfully.
    """
    base_url = get_microservice_base_url(environment, False)
    request_url = (
        f"{base_url}"
        "/categories"
        "/?vendorId=00fcdd80-274a-42be-8eae-0676856736f1"
    )
    header = get_header_request(zone)

    response = place_request(
        request_method="GET",
        request_url=request_url,
        request_body="",
        request_headers=header
    )

    if response.status_code == 200:
        return json.loads(response.content)

    print(
        f"\n{text.Red}"
        "Error when retrieving categories.\n"
        f"Response status: {response.status_code}\n"
        f"Response message; {response.text}"
    )

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

    Returns
    -------
    bool
        Whenever the request completed successfully.
    """
    base_url = get_microservice_base_url(environment)
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
        categories: Union[List[dict], dict]) -> dict:
    """
    Get categories.

    Parameters
    ----------
    zone : str
    environment : str

    Returns
    -------
    bool
        Whenever the request completed successfully.
    """

    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/category-relay-service"
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


def generate_categories_data() -> dict:
    """
    Pass
    """
    pass
