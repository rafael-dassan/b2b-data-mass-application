"""Handle Product Creation on Magento Service."""
from requests import Response

from data_mass.common import (
    convert_json_to_string,
    get_magento_base_url,
    get_magento_datamass_access_token,
    place_request
    )


def enable_product(country: str, environment: str, product_sku: str):
    """
    Enable product.

    Parameters
    ----------
    country: str
        One of BR, DO, AR, ZA or CO.
    environment: str
        One of UAT or SIT.
    product_sku: str
        The product SKU.

    Returns
    -------
    bool
        Whenever a product has been successfully enabled.
    """
    response = request_enable_product(country, environment, product_sku)
    if response.status_code == 200:
        return True

    return False


def request_enable_product(
        country: str,
        environment: str,
        product_sku: str) -> Response:
    """
    Enable Product on Magento.

    Parameters
    ----------
    country : str
    environment : str
    product_sku : str

    Returns
    -------
    Response
        The response.
    """
    # Get header request
    base_rul = get_magento_base_url(environment, country)
    url = f"{base_rul}/rest/V1/products/{product_sku}"

    # Get base URL
    access_token = get_magento_datamass_access_token(environment, country)

    # Get header request
    headers = {
        "Content-Type": "application/json",
        "x-access-token": access_token
    }

    data = {
        "product": {
            "sku": product_sku,
            "status": 1
        }
    }

    # Send request
    data = convert_json_to_string(data)
    response = place_request(
        request_method="PUT",
        request_url=url,
        request_body=data,
        request_headers=headers
    )

    return response
