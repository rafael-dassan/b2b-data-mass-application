# Standard library imports
import json
import os
from typing import Union

import pkg_resources

from data_mass.classes.text import text
from data_mass.common import (
    convert_json_to_string,
    create_list,
    get_header_request,
    get_microservice_base_url,
    place_request,
    update_value_to_json
)


def add_credit_to_account_microservice(
    account_id: str,
    zone: str,
    environment: str,
    credit: Union[str, int] = 5000,
    balance: Union[str, int] = 1500) -> bool:
    """
    Include credit for account in microservice.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str
    credit : str
    balance : str

    Returns
    -------
    bool
        Whenever was possible to add credit to an account.
    """
    request_headers = get_header_request(zone, False, True, False, False)
    from os import environ
    request_headers.update({"Authorization": environ["TOKEN"]})

    ms_base_url = get_microservice_base_url(environment)
    
    # Create dictionary with credit values
    dict_values = {
        "available": credit,
        "balance": balance,
        "total": credit + balance
    }
    
    if zone == "US":
        payload_path = "data/create_credit_us_payload.json"
        request_url = f"{ms_base_url}/credit-relay"
        dict_values.update({"vendorAccountId": account_id})
    else:
        request_url = f"{ms_base_url}/account-relay/credits"
        payload_path = "data/create_credit_payload.json"
        dict_values.update({"accountId": account_id})

    # TODO: check that you are always receiving an empty string
    if credit == "":
        credit = 5000

    # TODO: check that you are always receiving an empty string
    if balance == "":
        balance = 15000
    
    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        payload_path
    )
    body: dict = json.loads(content.decode("utf-8"))
    body.update(dict_values)

    # Send request
    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=json.dumps([body]),
        request_headers=request_headers
    )

    if response.status_code == 202:
        return True

    print(
        f"{text.Red}"
        f"[Account Relay Service] Failure to add credit to the account {account_id}.\n"
        f"Response Status: {response.status_code}."
        f"Response message: {response.text}"
    )

    return False
