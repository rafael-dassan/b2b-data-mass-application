import json
from uuid import uuid1
from typing import Optional

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
        content: str = json.dumps(response.text)

        return content

    print(
        f"{text.Red}\n"
        f'- [Category Service] Failure to create category.\n'
        f"Response Status: {response.status_code}\n"
        f"Response message: {response.text}"
    )

    return None
