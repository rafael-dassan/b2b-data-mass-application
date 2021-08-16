import json
from typing import List, Optional
from urllib.parse import urlencode

from data_mass.account.accounts import get_multivendor_account_id
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
        account_id: str = None) -> Optional[list]:
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
            account_id = get_multivendor_account_id(
                vendor_account_id=account_id,
                zone=zone,
                environment=environment
            )

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
        account_id: str = None) -> Optional[dict]:
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
        The category information.
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
            account_id = get_multivendor_account_id(
                vendor_account_id=account_id,
                zone=zone,
                environment=environment
            )

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

            return False

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

    return False
