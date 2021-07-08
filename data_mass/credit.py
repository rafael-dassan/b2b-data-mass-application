import json
import os
from typing import Union

from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request
)


def add_credit_to_account_microservice(
    account_id: str,
    zone: str,
    environment: str,
    credit: int = 0,
    balance: int = 0,
    consumption: int = 0,
    payment_term: str = None,
    overdue: int = 0,
    total: int = 0
) -> bool:
    """
    Include credit for account in microservice

    Parameters
    ----------
    account_id : str
        POC unique identifier
    zone : str
        country used in the operation e.g., AR, BR, DO, etc.
    environment : str
        envorinment used in the operation e.g., DEV, SIT, UAT.
    credit_info : dict

    Returns
    -------
    bool
        `True` if there were success in POST method, \
        else print the failure and return False.
    """
    request_headers = get_header_request(zone=zone, use_root_auth=True)

    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/account-relay/credits"

    dict_values = {
        "accountId": account_id,
        "available": credit,
        "balance": balance,
        "consumption": consumption,
        "overdue": overdue,
        "paymentTerms": payment_term,
        "total": total
    }

    request_body = json.dumps(dict_values)

    response = place_request(
        request_method='POST',
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 202:
        return True

    print(
        f"{text.Red}\n- [Account Relay Service] "
        f"Failure to add credit to the account {account_id}. "
        f"Response Status: {str(response.status_code)}. "
        f"Response message: {response.text}"
    )
    return False
