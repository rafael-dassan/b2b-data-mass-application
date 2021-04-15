"""Rewards Challenges."""
import json
from datetime import timedelta, datetime, timezone
from random import randint, randrange
from typing import Optional, Union
from requests import Response

from data_mass.common import (
    convert_json_to_string,
    get_header_request,
    get_microservice_base_url,
    place_request,
    print_input_text,
    set_to_dictionary,
    update_value_to_json,
)

from data_mass.classes.text import text
from data_mass.rewards.utils import (
    create_product_list_from_zone,
    display_all_challenges_info,
    format_datetime_to_str,
    generate_id,
    get_payload,
)

APP_ADMIN = "membership"
DO_CHALLENGE_BASE_URL = (
    "https://b2bstaticwebsagbdev.blob.core.windows.net"
    "/challenge-uat/DO"
)


def create_take_photo_challenge(
        zone: str,
        environment: str,
        is_expired: Optional[bool] = False) -> [None, Response]:
    """
    Create Take Photo challenge.

    Parameters
    ----------
    zone : str
    environment : str
    is_expired : bool
        Default to False.

    Returns
    -------
    None or Response
        None if the request fails, else, the response from the service.
    """
    challenge_id = generate_id()

    if not is_expired:
        json_object = create_challenge_payload(
            challenge_id=challenge_id,
            execution_method='TAKE_PHOTO',
        )
    else:
        json_object = create_challenge_payload(
            challenge_id=challenge_id,
            execution_method='TAKE_PHOTO',
            start_date_timedelta=-30,
            end_date_timedelta=-1,
        )

    request_body = convert_json_to_string(json_object)

    return put_challenge(
        challenge_id=challenge_id,
        request_body=request_body,
        zone=zone,
        environment=environment,
    )


def create_mark_complete_challenge(
        zone: str,
        environment: str,
        is_expired: Optional[bool] = False) -> [None, Response]:
    """
    Create Mark Complete challenge.

    Parameters
    ----------
    zone : str
    environment : str
    is_expired : bool
        Default to False.

    Returns
    -------
    None or Response
        None if the request fails, else, the response from the service.
    """
    challenge_id = generate_id()

    if is_expired is False:
        json_object = create_challenge_payload(
            challenge_id=challenge_id,
            execution_method='MARK_COMPLETE'
        )
    else:
        json_object = create_challenge_payload(
            challenge_id=challenge_id,
            execution_method='MARK_COMPLETE',
            start_date_timedelta=-30,
            end_date_timedelta=-1,
        )

    request_body = convert_json_to_string(json_object)

    return put_challenge(
        challenge_id=challenge_id,
        request_body=request_body,
        zone=zone,
        environment=environment,
    )


def create_purchase_challenge(
        zone: str,
        environment: str,
        is_multiple: bool,
        is_expired: Optional[bool] = False) -> Union[None, Response]:
    """
    Create Purchase challenge.

    Parameters
    ----------
    zone : str
    environment : str
    is_multiple : bool
    is_expired : bool
        Default to False.

    Returns
    -------
    None or Response
        None if the request fails, else, the response from the service.
    """
    print((
        f"{text.Yellow}\n"
        "- [Products] Verifying the list of "
        f'available products for "{zone}" zone'
    ))

    zone_skus_list = create_product_list_from_zone(zone, environment)

    if zone_skus_list is None:
        return None

    if not zone_skus_list:
        print((
            f"{text.Red}\n"
            f"- [Rewards] There are no products available for {zone} zone"
        ))

        return None

    challenge_id = generate_id()
    execution_method = "PURCHASE" if not is_multiple else "PURCHASE_MULTIPLE"

    if not is_expired:
        json_object = create_challenge_payload(
            challenge_id=challenge_id,
            execution_method=execution_method,
            zone_skus_list=zone_skus_list
        )
    else:
        json_object = create_challenge_payload(
            challenge_id=challenge_id,
            execution_method=execution_method,
            zone_skus_list=zone_skus_list,
            start_date_timedelta=-30,
            end_date_timedelta=-1,
        )

    request_body = convert_json_to_string(json_object)

    return put_challenge(
        challenge_id=challenge_id,
        request_body=request_body,
        zone=zone,
        environment=environment
    )


def create_challenge_payload(
        challenge_id: str,
        execution_method: str,
        zone_skus_list: Optional[list] = None,
        start_date_timedelta: Optional[float] = 0,
        end_date_timedelta: Optional[float] = 180) -> Union[None, Response]:
    """
    Create challenge payload.

    Parameters
    ----------
    challenge_id : str
    execution_method : str
    zone_skus_list : list
        Default to None.
    start_date_timedelta : int
        Default to 0.
    end_date_timedelta : int
        Default to 180.

    Returns
    -------
    None or Response
        None if the request fails, else, the response from the service.
    """
    challenge_payload_template = get_payload(
        file_path='../data/create_rewards_challenges_payload.json'
    )

    start_date = datetime.now(timezone.utc) + \
        timedelta(days=start_date_timedelta)
    start_date = format_datetime_to_str(start_date)

    end_date = datetime.now(timezone.utc) + timedelta(days=end_date_timedelta)
    end_date = format_datetime_to_str(end_date)

    dict_challenge = {
        "title": f"DM-{challenge_id}({execution_method})",
        "description": f"{execution_method} challenge created by data-mass",
        "points": randrange(500, 5000, 100),
        "startDate": start_date,
        "endDate": end_date,
        "executionMethod": execution_method
    }

    for key, value in dict_challenge.items():
        json_object = update_value_to_json(
            challenge_payload_template,
            key,
            value
        )

    if execution_method == "TAKE_PHOTO":
        good_photo = (
            f"{DO_CHALLENGE_BASE_URL}"
            "/good-examples-photo-challenge/cooler_cerveza_ok.png"
        )
        bad_photo = (
            f"{DO_CHALLENGE_BASE_URL}"
            "/bad-examples-photo-challenge/cooler_cerveza_nok.png"
        )

        set_to_dictionary(json_object, 'goodPhotoSample', good_photo)
        set_to_dictionary(json_object, 'badPhotoSample', bad_photo)

    if execution_method in ["PURCHASE", "PURCHASE_MULTIPLE"]:
        sku_count = 4 if len(zone_skus_list) > 4 else len(zone_skus_list)

        # TODO
        challenge_sku_list = list()
        for i in range(sku_count):
            dict_challenge_sku = {
                'sku': zone_skus_list[i],
                'quantity': randint(2, 5)
            }
            challenge_sku_list.append(dict_challenge_sku)

        set_to_dictionary(json_object, 'skus', challenge_sku_list)

    return json_object


def put_challenge(
        challenge_id: str,
        request_body: str,
        zone: str,
        environment: str) -> Union[None, Response]:
    """
    Make a challenge on the service.

    Parameters
    ----------
    challenge_id : str
    request_body : str
    zone : str
    environment : str

    Returns
    -------
    None or Response
        None if the request fails, else, the response from the service.
    """
    jwt_app_claim = f"{APP_ADMIN}-{zone.lower()}"
    base_url = get_microservice_base_url(environment, False)
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        jwt_app_claim=jwt_app_claim
    )
    request_url = f"{base_url}/rewards-service/challenges/{challenge_id}"
    response = place_request(
        request_method='PUT',
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 200:
        print((
            f"{text.Green}\n"
            f"- [Rewards] The challenge {challenge_id}"
            f" was successfully created."
        ))

    else:
        print((
            f"{text.Red}\n"
            '- [Rewards] Failure when creating the challenge '
            f'"{challenge_id}"\n'
            f"- Response Status: {str(response.status_code)}.\n"
            f"- Response message {response.text}."
        ))

    return response


def remove_challenge(zone: str, environment: str):
    """
    Remove challenge.

    Parameters
    ----------
    zone : str
    environment : str
    """
    response_all_challenges = get_all_challenges(zone, environment)

    # TODO: if there's no challenge, skip input text
    if response_all_challenges is None:
        print("There's no challenge avaliable.")

    json_all_challenges = json.loads(response_all_challenges.text)
    display_all_challenges_info(json_all_challenges)

    challenge_id = print_input_text('\nPlease inform the Challenge ID')
    delete_challenge(challenge_id, zone, environment)


def delete_challenge(
        challenge_id: str,
        zone: str,
        environment: str) -> Response:
    """
    Delete a challenge.

    Parameters
    ----------
    challenge_id : str
    zone : str
    environment :  str

    Returns
    -------
    Response
        The response data.
    """
    jwt_app_claim = f"{APP_ADMIN}-{zone.lower()}"
    base_url = get_microservice_base_url(environment, False)
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        jwt_app_claim=jwt_app_claim
    )
    request_url = f"{base_url}/rewards-service/challenges/{challenge_id}"
    response = place_request(
        request_method='DELETE',
        request_url=request_url,
        request_body="",
        request_headers=request_headers
    )

    if response.status_code == 204:
        print((
            f"{text.Green}\n"
            f'- [Rewards] The challenge "{challenge_id}" '
            "was successfully deleted."
        ))

    elif response.status_code == 404:
        print((
            f"{text.Red}\n"
            f'- [Rewards] The challenge "{challenge_id}" was not found.'
        ))

    else:
        print((
            f"{text.Red}\n"
            '- [Rewards] Failure when deleting the '
            f'challenge "{challenge_id}"\n'
            f"- Response Status: {str(response.status_code)}.\n"
            f"- Response message {response.text}"
        ))

    return response


def get_all_challenges(zone: str, environment: str) -> Union[None, Response]:
    """
    Get all challenges for the zone.

    Parameters
    ----------
    zone : str
    environment : str

    Returns
    -------
    Union[None, Response]
        None if the specific challenge does not exists, else, \
        all challenges.
    """
    jwt_app_claim = f"{APP_ADMIN}-{zone.lower()}"
    base_url = get_microservice_base_url(environment, False)
    header_request = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        jwt_app_claim=jwt_app_claim
    )
    request_url = f"{base_url}/rewards-service/challenges"
    response = place_request(
        request_method="GET",
        request_url=request_url,
        request_body="",
        request_headers=header_request
    )

    if response.status_code == 200:
        json_data = json.loads(response.text)
        if len(json_data) > 0:
            return response

        print((
            f"{text.Red}\n"
            "- [Rewards] There are no challenges "
            f'available in "{zone}"" zone.'
        ))

    else:
        print((
            f"{text.Red}\n"
            "- [Rewards] Failure when getting all"
            f' challenges in "{zone}" zone.\n'
            f"- Response Status: {str(response.status_code)}.\n"
            f"- Response message {response.text}"
        ))

    return None


def get_specific_challenge(
        challenge_id: str,
        zone: str,
        environment: str) -> Union[None, Response]:
    """
    Get an specific challenge for the zone.

    Parameters
    ----------
    challenge_id : str
    zone : str
    environment = str

    Returns
    -------
    Union[None, Response]
        None if the specific challenge does not exists, else, \
        the challenge details.
    """
    base_url = get_microservice_base_url(environment, False)
    jwt_app_claim = f"{APP_ADMIN}-{zone.lower()}"

    header_request = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        jwt_app_claim=jwt_app_claim,
    )
    request_url = f"{base_url}/rewards-service/challenges/{challenge_id}"
    response = place_request(
        request_method="GET",
        request_url=request_url,
        request_body="",
        request_headers=header_request
    )

    if response.status_code == 200:
        return response

    if response.status_code == 404:
        print((
            f"{text.Red}\n"
            f'- [Rewards] The challenge "{challenge_id}" was not found.'
        ))
    else:
        print((
            f"{text.Red}\n"
            "- [Rewards] Failure when getting the challenge "
            f'"{challenge_id}"" information.\n'
            f"- Response Status: {str(response.status_code)}.\n"
            f"- Response message {response.text}"
        ))

    return None
