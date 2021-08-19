import json
from typing import Optional
from uuid import uuid1

from data_mass.category.service import get_category_by_id
from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request
)


def create_category(
        zone: str,
        environment: str,
        category_data: dict) -> Optional[dict]:
    """
    Create/Update category via Category API.

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
    header.update({"Accept-Language": "en"})
    parent_id = category_data.get("parentId")

    if not parent_id:
        parent_id = None

    body = {
        "vendorCategoryId": category_data.get(
            "vendorCategoryId",
            str(uuid1())
        ),
        "enabled": category_data.get("enabled", True),
        "items": category_data.get("items", []),
        "name": category_data.get("name"),
        "categories": [],
        "type": "CATEGORY",
        "parentId": parent_id
    }

    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=json.dumps([body]),
        request_headers=header
    )

    if response.status_code in [200, 202]:
        return True

    print(
        f"{text.Red}\n"
        f'- [Category Service] Failure to create category.\n'
        f"Response Status: {response.status_code}\n"
        f"Response message: {response.text}"
    )

    return False


def associate_product_to_category(
        zone: str,
        environment: str,
        items: list,
        category_id: str) -> bool:
    """
    Associate product to a category.

    Parameters
    ----------
    zone : str
    environment : str
    vendor_item_id : str
    category_id : str, optional
        By default `1011`.

    Returns
    -------
    bool
        Whenever the association was completed successfully or not.
    """
    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/category-relay-service"
    header = get_header_request(zone)
    category = get_category_by_id(zone, environment, category_id)

    if not category:
        return False

    category.update({"items": items})

    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=json.dumps([category]),
        request_headers=header
    )

    if response.status_code in [200, 202]:
        return True

    print(
        f"{text.Red}\n"
        f'- [Category Service] Failure to associate product.\n'
        f"Response Status: {response.status_code}\n"
        f"Response message: {response.text}"
    )

    return False
