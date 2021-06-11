import json
from urllib.parse import urlencode
from uuid import uuid1

from data_mass.accounts import get_account_id
from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request
)
from data_mass.config import get_settings


def get_categories(
        zone: str,
        environment: str,
        service: str = "category",
        account_id: str = None) -> list:
    """
    Get categories.

    Parameters
    ----------
    zone : str
    environment : str
    service : str
        Service from which you will be consulted. One of [category, catalog].
    account_id : str
        If the chosen service is `catalog`, this parameter is required.\
        Default to `None`.

    Returns
    -------
    dict
        A dict with a list of categoires.
    """
    base_url = get_microservice_base_url(environment, False)
    header = get_header_request(zone)

    if service.lower() == "category":
        settings = get_settings()
        query = {
            "vendorId": settings.vendor_id
        }
        request_url = f"{base_url}/categories/?{urlencode(query)}"

    if service.lower() == "catalog":
        if account_id is not None:
            account_id = get_account_id(account_id, zone, environment)
            header.update({
                "accountId": account_id,
                "Accept-Language": "en"
            })

            query = {
                "categoryType": "WEB",
                "includeEmptyCategory": False,
                "projection": "SMALL",
                "page_size": 50,
                "depth": -1,
                "includeDiscount": False,
                "includeAllPromotions": False
            }
            request_url = (
                f"{base_url}"
                "/v1/catalog-service"
                "/catalog"
                "/categories"
                f"?{urlencode(query)}"
            )
        else:
            print(
                f"{text.Red}\n"
                'The parameter "account_id" is required '
                'when target service is catalog.\n'
            )

            return None

    response = place_request(
        request_method="GET",
        request_url=request_url,
        request_body="",
        request_headers=header
    )

    if response.status_code == 200:
        return json.loads(response.text)

    print(
        f"\n{text.Red}"
        "Error when retrieving categories.\n"
        f"Response status: {response.status_code}\n"
        f"Response message; {response.text}"
    )

    return None


def get_category_by_id(
        zone: str,
        environment: str,
        category_id: str,
        service: str = "category",
        account_id: str = None) -> dict:
    """
    Get a specific category.

    Parameters
    ----------
    zone : str
    environment : str
    service : str
        Service from which you will be consulted. One of [category, catalog].\
        Default to `category`.
    account_id : str
        If the chosen service is `catalog`, this parameter is required.\
        Default to `None`.

    Returns
    -------
    dict
        The catefory information.
    """
    base_url = get_microservice_base_url(environment, False)
    header = get_header_request(zone)

    if service.lower() == "category":
        settings = get_settings()
        query = {"vendorId": settings.vendor_id}
        request_url = (
            f"{base_url}"
            "/categories"
            f"/{category_id}"
            f"?{urlencode(query)}"
        )

    if service.lower() == "catalog":
        if account_id is not None:
            account_id = get_account_id(account_id, zone, environment)
            header.update({
                "accountId": account_id,
                "Accept-Language": "en"
            })

            query = {
                "includeEmptyCategory": False,
                "projection": "TREE",
                "page_size": 50,
                "depth": -1,
                "includeDiscount": False,
                "includeAllPromotions": False
            }
            request_url = (
                f"{base_url}"
                "/v1/catalog-service"
                "/catalog"
                "/categories"
                f"/{category_id}"
                f"?{urlencode(query)}"
            )
        else:
            print(
                f"{text.Red}\n"
                'The parameter "account_id" is required '
                'when target service is catalog.\n'
            )

            return None

    response = place_request(
        request_method="GET",
        request_url=request_url,
        request_body="",
        request_headers=header
    )

    if response.status_code == 200:
        return json.loads(response.text)

    print(
        f"{text.Red}\n"
        f'- [Category Service] Failure to get "{category_id}" category.\n'
        f"Response Status: {response.status_code}\n"
        f"Response message: {response.text}"
    )

    return None


def create_category(
        zone: str,
        environment: str,
        category_data: dict) -> dict:
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

    body = {
        "vendorCategoryId": category_data.get(
            "vendorCategoryId",
            str(uuid1())
        ),
        "enabled": category_data.get("enabled", True),
        "items": category_data.get("items", []),
        "name": category_data.get("name"),
        "type": category_data.get("type", "CATEGORY"),
        "parentId": category_data.get("parentId", 0)
    }

    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=json.dumps([body]),
        request_headers=header
    )

    if response.status_code in [200, 202]:
        content: dict = json.dumps(response.text)

        return content

    print(
        f"{text.Red}\n"
        f'- [Category Service] Failure to create category.\n'
        f"Response Status: {response.status_code}\n"
        f"Response message: {response.text}"
    )

    return None
