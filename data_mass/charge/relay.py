from json import dumps
from random import randint, uniform

from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request
)


def create_charge_global(
        account_id: str,
        zone: str,
        environment: str,
        **kwargs) -> bool:
    """
    Create charge.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str

    Returns
    -------
    bool
    """
    request_headers = get_header_request(zone=zone)
    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/charge-relay/v1"

    body = {
        "accounts": [account_id],
        "charges": [{
            "chargeId": kwargs.get("charge_id", f"DM-{randint(1, 999)}"),
            "type": kwargs.get("type", "PAYMENT_METHOD_FEE"),
            "conditions": {
                "paymentMethod": kwargs.get("payment_method")
            },
            "output": {
                "scope": "ORDER",
                "applyTo": "TOTAL",
                "type": kwargs.get("charge_type", "PERCENT"),
                "value": kwargs.get("value", round(uniform(9.99, 99.99), 2))
            }
        }]
    }

    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=dumps(body),
        request_headers=request_headers
    )

    if response.status_code == 202:
        return True

    return False
