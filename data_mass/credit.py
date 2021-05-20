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
    request_headers.update({"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJCVVdYcTRLanhPMUwxdTFTaENJVVNrdEk5aXRreFJ0X1Zzb3luelVvVGFFIn0.eyJleHAiOjE2MjE0NjcxMTAsImlhdCI6MTYyMTQ2MzUxMCwianRpIjoiNTRmMTRjYTAtZDNjMy00ZDczLTljOWUtYjE4NTA5MDZmMGI0IiwiaXNzIjoiaHR0cDovL2tleWNsb2FrLXNlcnZpY2UvYXV0aC9yZWFsbXMvYmVlcy1yZWFsbSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiI3NGM2OThlOS01ZDE5LTRjM2ItODdiZC00ZDExNDM3MDhlOTciLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiI5MGFiMjNmOC03OTQ1LTRiODMtODllYy00NTFhNDVjNmE4NGQiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjbGllbnRJZCI6IjkwYWIyM2Y4LTc5NDUtNGI4My04OWVjLTQ1MWE0NWM2YTg0ZCIsImNsaWVudEhvc3QiOiIxMjcuMC4wLjEiLCJyb2xlcyI6WyJXcml0ZSIsIlJlYWQiXSwidmVuZG9ySWQiOiI1ODg3MGNiYy03ODA5LTRlMTgtYmE1OS05ODZiNDk5MmM4NDIiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzZXJ2aWNlLWFjY291bnQtOTBhYjIzZjgtNzk0NS00YjgzLTg5ZWMtNDUxYTQ1YzZhODRkIiwiY2xpZW50QWRkcmVzcyI6IjEyNy4wLjAuMSJ9.JMiHMPbs1zF8sA98F33Fqj6i2q2AUeTZE7H1U7khQH4GitzjVQPPt_dL4SdXnks0NUM-sKGz6zDLw97XucaWvj0iiY3jl0_6j4XYuA1yo7OF2oLHQ2djO_hyuCW1vkyIfV3yPsZtTpA5ahf4eGyUEZ9hSVWLsbD07ciYd5wok_jka_Vf3P1AYV3vSpI5_gaMHialUq-c7uHbkmEr-H5dcFS7sbdp2vzN8kY9vxq18Muk-LgNhOm5k27urg-APxnxcYRA_ERDlDJxo7mkwzaOO4Xc0cCcy7JFI89Xa1w8UgcDNl9SR_Gt0Xt2CXVInqdgDEKAKWp96wzi1JjsHJjJvQ"})

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
