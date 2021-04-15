"""Transactions Rewards."""
from json import loads
from random import randint
from typing import Union
from requests import Response

from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    convert_json_to_string,
    place_request,
    print_input_number
)
from data_mass.rewards.utils import get_rewards_combos_by_account

APP_ADMIN = "membership"


def create_redemption(
        account_id: str,
        zone: str,
        environment: str) -> Union[None, Response]:
    """
    Create REDEMPTION transaction for an account.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str

    Returns
    -------
    Response or None
        None if account does not contain any reward combo, else, \
        the http response.
    """
    rewards_combos_response = get_rewards_combos_by_account(
        account_id=account_id,
        zone=zone,
        environment=environment
    )

    if rewards_combos_response is None:
        return None

    json_rewards_combos = loads(rewards_combos_response.text)

    combo_id = json_rewards_combos["combos"][0]["id"]
    order_id = f"DM-{account_id}{str(randint(100,900))}"

    dict_redemption = {
        "combos": [{
            "comboId": combo_id,
            "quantity": 1
        }],
        "orderId": order_id
    }

    body = convert_json_to_string(dict_redemption)

    return post_redemption(
        account_id=account_id,
        zone=zone,
        environment=environment,
        request_body=body
    )


def create_rewards_offer(
        account_id: str,
        zone: str,
        environment: str) -> Response:
    """
    Create REWARDS_OFFER transaction for an account.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str

    Returns
    -------
    Response
        The http response.
    """
    points_amount = print_input_number(
        "\nPlease inform the points amount (greater than zero)"
    )

    while int(points_amount) <= 0:
        print(text.Red + "\nInvalid value!! Must be greater than zero!!")
        points_amount = print_input_number(
            "\nPlease inform the new balance amount (greater than zero)"
        )

    dict_rewards_offer = {
        "points": int(points_amount),
        "campaignId": f"DM-{str(randint(100,900))}",
        "description": "DM-Bonus for customers signing up to Rewards Program"
    }

    body = convert_json_to_string(dict_rewards_offer)

    return post_rewards_offer(
        account_id=account_id,
        zone=zone,
        environment=environment,
        request_body=body,
    )


def create_points_removal(
        account_id: str,
        zone: str,
        environment: str) -> Response:
    """
    Create POINTS_REMOVAL transaction for an account.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str

    Returns
    -------
    Response
        The http response.
    """
    points_amount = print_input_number(
        "\nPlease inform the points amount (greater than zero)"
    )

    while int(points_amount) <= 0:
        print(text.Red + '\nInvalid value!! Must be greater than zero!!')

        # TODO
        _ = print_input_number(
            "\nPlease inform the new balance amount (greater than zero)"
        )

    dict_points_removal = {
        "points": int(points_amount),
        "description": "DM Transaction to remove the balance from a POC."
    }

    body = convert_json_to_string(dict_points_removal)

    return post_points_removal(
        account_id=account_id,
        zone=zone,
        environment=environment,
        request_body=body,
    )


def post_rewards_offer(
        account_id: str,
        zone: str,
        environment: str,
        request_body: str) -> Response:
    """
    Create a Rewards Offer.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str
    request_body : str

    Returns
    -------
    Response
        The http response.
    """
    jwt_app_claim = f"{APP_ADMIN}-{zone.lower()}"
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        account_id=account_id,
        jwt_app_claim=jwt_app_claim,
    )

    base_url = get_microservice_base_url(environment, False)
    request_url = (
        f"{base_url}"
        f"/rewards-service/rewards/{account_id}"
        "/transaction/rewards-offer"
    )

    response = place_request(
        request_method='POST',
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 201:
        print((
            f"{text.Green}\n"
            "[Rewards] The REWARDS_OFFER transaction was successfully "
            f"created for the account {account_id}"
        ))
    elif response.status_code == 404:
        print((
            f"{text.Red}\n"
            f'- [Rewards] The account "{account_id}" '
            "is not enrolled to any rewards program."
            'Please use the menu option "Enroll POC to a program" '
            "to enroll this account to a rewards program."
        ))
    else:
        print((
            f"{text.Red}\n"
            "- [Rewards] Failure when creating a REWARDS_OFFER transaction "
            f'for account "{account_id}"\n'
            f'- Response Status: "{str(response.status_code)}"\n'
            f'Response message "{response.text}"'
        ))

    return response


def post_redemption(
        account_id: str,
        zone: str,
        environment: str,
        request_body: str) -> Response:
    """
    Create Redemption on the service.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str
    request_body : str

    Returns
    --------
    Response
        The http response.
    """
    jwt_app_claim = f"{APP_ADMIN}-{zone.lower()}"
    base_url = get_microservice_base_url(environment, False)
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        jwt_app_claim=jwt_app_claim
    )
    request_url = (
        f"{base_url}"
        "/rewards-service/rewards"
        "/{account_id}"
        "/transaction/redemption"
    )

    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers,
    )

    if response.status_code == 201:
        print((
            f"{text.Green}\n"
            "- [Rewards] The REDEMPTION transaction was"
            f" successfully created for the account {account_id}."
        ))

    elif response.status_code == 404:
        print((
            f"{text.Red}\n"
            f"- [Rewards] The account {account_id} is not enrolled to "
            "any rewards program.\n"
            'Please use the menu option "Enroll POC to a program" '
            "to enroll this account to a rewards program."
        ))
    else:
        print((
            f"{text.Red }\n"
            "- [Rewards] Failure when creating a REDEMPTION "
            f"transaction for account {account_id}.\n"
            f"- Response Status: {str(response.status_code)}\n"
            f"- Response message {response.text}."
        ))

    return response


def post_points_removal(
        account_id: str,
        zone: str,
        environment: str,
        request_body: str) -> Response:
    """
    Post points removal.

    Parameters
    ----------
    account_id : str
    zone : str
    environment : str
    request_body : str

    Returns
    -------
    Response
        The http response.
    """
    jwt_app_claim = f"{APP_ADMIN}-{zone.lower()}"
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        account_id=account_id,
        jwt_app_claim=jwt_app_claim
    )

    base_url = get_microservice_base_url(environment, False)
    request_url = (
        f"{base_url}"
        f"/rewards-service/rewards/{account_id}"
        "/transaction/points-removal"
    )

    response = place_request(
        request_method='POST',
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers,
    )

    if response.status_code == 201:
        print((
            f"{text.Green}\n"
            "- [Rewards] The POINTS_REMOVAL transaction was "
            f'successfully created for the account "{account_id}"'
        ))
    elif response.status_code == 404:
        print((
            f"{text.Red}\n"
            f'- [Rewards] The account "{account_id}" '
            "is not enrolled to any rewards program.\n"
            'Please use the menu option "Enroll POC to a program" '
            "to enroll this account to a rewards program."
        ))
    else:
        print((
            f"{text.Red}\n"
            "- [Rewards] Failure when creating a POINTS_REMOVAL "
            f'transaction for account "{account_id}".\n'
            f'Response Status: "{str(response.status_code)}"\n'
            f'- Response message "{response.text}".'
        ))

    return response
