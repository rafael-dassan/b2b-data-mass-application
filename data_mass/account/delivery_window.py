import calendar
import json
import logging
from datetime import datetime, timedelta
from distutils.util import strtobool
from typing import Union

import pkg_resources

from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request,
    update_value_to_json,
    validate_user_entry_date
)

logger = logging.getLogger(__name__)

DATE_FORMAT = "%Y-%m-%d"


def get_microservice_payload_post_delivery_date(
        account_data: str,
        is_alternative_delivery_date: bool,
        dates_list: list,
        index: int) -> dict:
    """
    Create payload for delivery date.

    Parameters
    ----------
    account_data : str
    is_alternative_delivery_date : bool
    dates_list : list
    index : int

    Returns
    -------
    dict
        colect info and return an payload.
    """
    dict_values = {
        "alternative": is_alternative_delivery_date,
        "deliveryScheduleId": account_data["deliveryScheduleId"],
        "endDate": dates_list["endDate"],
        "expirationDate": dates_list["expirationDate"],
        "id": f'{index}_{account_data["accountId"]}',
        "startDate": dates_list["startDate"],
    }

    return dict_values


def get_microservice_delivery_fee_charge_relay(
        account_data: dict,
        include_delivery_cost: dict) -> dict:
    """
    Create payload for delivery fee for endpoint charge relay.

    Parameters
    ----------
    account_data : dict
    include_delivery_cost : dict

    Returns
    -------
    dict
        JSON payload for interest fee.
    """
    payment_method = account_data.get("paymentMethods", [])

    if "CREDIT_CARD_POS" in payment_method:
        change_charge_type = input(
            f'{text.default_text_color}Do you want to choose '
            '"PAYMENT_METHOD_FEE" as the type of the charge? [y/N]: '
        )

        while (change_charge_type.upper() in ["Y", "N"]) is False:
            print(text.Red + "\n- Invalid option")
            change_charge_type = input(
                f'{text.default_text_color}Do you want to choose '
                '"PAYMENT_METHOD_FEE" as the type of the charge? [y/N]: '
            )

    change_charge_type = strtobool(change_charge_type)

    dict_values = {
        "accounts": [account_data.get("accountId")],
        "charges": [{
            "chargeId": "CHARGE-01",
            "type": "DELIVERY_DATE_FEE",
            "conditions": {
                "alternativeDeliveryDate": True,
                "orderTotal": {
                    "maximumValue": include_delivery_cost.get("min_order_value")
                }
            },
            "output": {
                "scope": "ORDER",
                "applyTo": "TOTAL",
                "type": "AMOUNT",
                "value": include_delivery_cost.get("fee_value")
            }
        }]
    }

    if change_charge_type:
        charge, = dict_values.get("charges")
        charge.update({
            "type": "PAYMENT_METHOD_FEE",
            "conditions": {
                "paymentMethod": "CREDIT_CARD_POS"
            }
        })

        dict_values.update({"charges": [charge]})

    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/create_delivery_fee_charge-relay.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    # Update the delivery window values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    return json_object


def get_microservice_payload_post_delivery_fee(
        account_data: dict,
        include_delivery_cost: dict) -> dict:
    """
    Create payload for delivery fee.

    Parameters
    ----------
    account_data : dict
    include_delivery_cost : dict

    Returns
    -------
    dict
        JSON payload for interest fee.
    """
    dict_values = {
        "accounts[0]": account_data["accountId"],
        "interest[0].interestId": "ID00001",
        "interest[0].externalId": "NON_REGULAR_DELIVERY_DATE_FEE",
        "interest[0].scope": "order",
        "interest[0].conditions": {
            "alternativeDeliveryDate": True,
            "orderTotal": {
                "maximumValue": include_delivery_cost["min_order_value"]
            },
        },
        "interest[0].output": {
            "totalOutput": {
                "additionalAmount": include_delivery_cost["fee_value"]
            }
        },
    }

    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass", "data/create_delivery_fee_interest_payload.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    # Update the delivery window values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    return json_object


def create_delivery_window_microservice(
        zone: str,
        environment: str,
        account_data: dict,
        is_alternative_delivery_date: bool,
        option: str) -> bool:
    """
    Create delivery date in microservice.

    Parameters
    ----------
    zone : str
    environment : str
    account_data : dict
    is_alternative_delivery_date : bool
    option : str

    Returns
    -------
    bool
        Whenever a post request was successfully completed.
    """
    # Get headers
    request_headers = get_header_request(zone, False, True, False, False)

    if zone in ["CA", "US"]:
        v1 = False
    else:
        v1 = True

    # Get base URL
    ms_base_url = get_microservice_base_url(environment, v1)
    request_url = f"{ms_base_url}/account-relay/delivery-windows"

    # Return list of dates
    dates_list = return_dates_payload(option)
    if not dates_list:
        return False

    index = 0
    request_body = []
    while index <= (len(dates_list) - 1):
        # Force mixed values if it's is_alternative_delivery_date
        if is_alternative_delivery_date:
            if (index % 2) == 0:
                option_is_alternative_delivery_date = True
            else:
                option_is_alternative_delivery_date = False
        else:
            option_is_alternative_delivery_date = is_alternative_delivery_date

        # Get body request
        temporary_body = get_microservice_payload_post_delivery_date(
            account_data=account_data,
            is_alternative_delivery_date=option_is_alternative_delivery_date,
            dates_list=dates_list[index],
            index=index
        )
        request_body.append(temporary_body)
        index = index + 1

    # Place request
    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=json.dumps(request_body),
        request_headers=request_headers
    )

    if response.status_code in [200, 202]:
        return True

    print(
        f"{text.Red}"
        "- [Account Relay Service] Failure to create delivery window.\n"
        f"Response Status: {response.status_code}.\n"
        f"Response message: {response.text}"
    )
    return False


def default_delivery_window():
    list_delivery_dates = list()
    initial_date = datetime.now()
    initial_month = initial_date.strftime("%m")
    last_day_month = calendar.monthrange(
        int(initial_date.strftime("%Y")), int(initial_date.strftime("%m"))
    )[1]

    if int(initial_date.strftime("%d")) == last_day_month:
        initial_date = initial_date + timedelta(days=1)
        initial_month = initial_date.strftime("%m")
        last_day_month = calendar.monthrange(
            int(initial_date.strftime("%Y")),
            int(initial_date.strftime("%m")),
        )[1]

    while (int(initial_date.strftime("%d")) < last_day_month) and (
        int(initial_date.strftime("%m")) <= int(initial_month)
    ):
        clone_initial_date = initial_date
        clone_initial_date = clone_initial_date + timedelta(days=1)
        start_date = clone_initial_date.strftime(DATE_FORMAT)
        end_date = start_date
        expiration_date = initial_date.strftime(DATE_FORMAT) + "T20:00:00Z"

        list_delivery_dates.append(
            {
                "startDate": start_date,
                "endDate": end_date,
                "expirationDate": expiration_date,
            }
        )
        initial_date = initial_date + timedelta(days=2)
    return list_delivery_dates


def delivery_window_specific():
    
    start_date = validate_user_entry_date(
        text=f"{text.LightYellow}Date (YYYY-mm-dd)"
    )
    while not start_date:
        print(f"{text.Red}\nNo delivery window date was inputed.")
        start_date = validate_user_entry_date(
            text=f"{text.LightYellow}Date"
        )
    date = datetime.strptime(start_date, DATE_FORMAT).date()
    list_delivery_dates = [
        {
            "startDate": date.strftime(DATE_FORMAT),
            "endDate": date.strftime(DATE_FORMAT),
            "expirationDate": date.strftime(DATE_FORMAT) + "T20:00:00Z",
        }
    ]
    return list_delivery_dates

    
def delivery_window_range():
    
    date_begin = validate_user_entry_date(
        text=f"{text.LightYellow}Begin Date (YYYY-mm-dd)"
    )
    date_end = validate_user_entry_date(
        text=f"{text.LightYellow}End Date (YYYY-mm-dd)"
    )

    while not date_begin or not date_end:
        print("\nNo delivery window begin or end date was inputed.")
        date_begin = validate_user_entry_date()
        date_end = validate_user_entry_date()

    datetime_begin = datetime.strptime(date_begin, DATE_FORMAT).date()
    datetime_end = datetime.strptime(date_end, DATE_FORMAT).date()

    list_delivery_dates = list()
    while datetime_begin <= datetime_end:
        start_date = datetime_begin.strftime(DATE_FORMAT)
        end_date = start_date
        expiration_date = (
            datetime_begin.strftime(DATE_FORMAT) + "T20:00:00Z"
        )

        list_delivery_dates.append(
            {
                "startDate": start_date,
                "endDate": end_date,
                "expirationDate": expiration_date,
            }
        )
        datetime_begin = datetime_begin + timedelta(days=2)
    return list_delivery_dates


def return_dates_payload(option: str) -> list:
    """
    Execute user option and returns a list of dates.

    Parameters
    ----------
    option : prompt
        prompt to user option.

    Returns
    -------
    list
        list of delivery dates
    """
    options = {
        "1": default_delivery_window,
        "2": delivery_window_specific,
        "3": delivery_window_range
    }
    dates = options.get(option)()
    return dates


def create_delivery_fee_microservice(
    zone: str,
    environment: str,
    account_data: dict,
    include_delivery_cost: dict) -> bool:
    """
    Create delivery fee (interest) in microservice.

    Parameters
    ----------
    zone : str
    environment : str
    account_data : dict
    include_delivery_cost : dict

    Returns
    -------
    bool
        True if creation is okay and False if fail.
    """
    charge_relay_countries = ["AR", "BR", "CO", "DO", "EC", "MX", "PE", "ZA"]
    
    # Get base URL
    base_url = get_microservice_base_url(environment)
    if zone in charge_relay_countries:
        request_url = f"{base_url}/charge-relay/v1"
        request_body = get_microservice_delivery_fee_charge_relay(
            account_data, include_delivery_cost
        )
    else:
        request_url = f"{base_url}/cart-calculation-relay/v2/interest"
        request_body = get_microservice_payload_post_delivery_fee(
            account_data, include_delivery_cost
        )
    request_headers = get_header_request(zone=zone)

    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=json.dumps(request_body),
        request_headers=request_headers
    )
    if response.status_code != 202:
        print(
            f"{text.Red}\n"
            "- [Pricing Engine Relay Service] Failure to add delivery cost.\n"
            f"Response Status: {response.status_code}.\n"
            f"Response message: {response.text}."
        )
        return False

    return True
