from random import randint

import pkg_resources
from requests import request

from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    get_new_token,
    remove_from_dictionary,
    set_to_dictionary
)
from data_mass.logger import log_to_file


def create_file_api(
    zone: str,
    environment: str,
    account_id: str,
    purpose: str,
    data: dict
) -> bool:
    """
    Create file through the File Management Service.
    Parameters
    ----------
    zone: str
        e.g., ZA, BR.
    environment: str
        e.g., DEV, SIT, UAT.
    account_id: str
        POC unique identifier.
    purpose: str
        e.g., invoice, bank-slip, credit-statement.
    data: dict
        Specific file data according to the purpose.

    Returns
    -------
    bool
        `False` in case of failure, otherwise, `True`.
    """
    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/files/random-file.pdf"
    )

    files = {"file": ("random-file.pdf", content, "application/pdf")}
    metadata = get_file_metadata(account_id, purpose, data)
    title = f"{randint(1, 100000)}-{purpose}-{account_id}"

    # Define headers
    request_headers = get_header_request(
        zone,
        True,
        False,
        False,
        False,
        account_id
    )
    set_to_dictionary(request_headers, "linkExpirationTime", str(-1))
    set_to_dictionary(request_headers, "metadata", metadata)
    set_to_dictionary(request_headers, "purpose", purpose)
    set_to_dictionary(request_headers, "title", title)
    set_to_dictionary(request_headers, "expiresAt", "")
    set_to_dictionary(request_headers, 'Authorization', get_new_token())
    remove_from_dictionary(request_headers, "Content-Type")

    # Define url request
    request_url = get_microservice_base_url(environment) + "/files/upload"

    # Send request
    response = request(
        "POST",
        request_url,
        files=files,
        headers=request_headers
    )
    log_to_file(
        request_method="POST",
        request_url=request_url,
        request_body="random-file.pdf",
        request_headers=request_headers,
        status_code=response.status_code,
        response_body=response.text,
    )

    if response.status_code == 200:
        return True

    print(
        f"{text.Red}"
        "- [File Management Service] Failure to create file.\n"
        f"Response Status: {response.status_code}\n"
        f"Response message: {response.text}"
    )

    return False


def get_file_metadata(account_id: str, purpose: str, data: dict) -> str:
    """
    Get metadata from a file.

    Parameters
    ----------
    account_id : str
    purpose : str
    data : dict

    Returns
    -------
    str
        `Purpose` property from metadata.
    """
    invoice_id = data.get("invoice_id")
    month = data.get("month")
    year = data.get("year")

    metadata = {
        "invoice": f"accountId:{account_id}, invoiceId:{invoice_id}",
        "bank-slip": f"accountId:{account_id}, invoiceId:{invoice_id}",
        "credit-statement": (
            f"accountId:{account_id}, "
            f"date:{month}/{year}, creditBalance:123.05"
        )
    }

    return metadata[purpose]
