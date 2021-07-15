# Standard library imports
import calendar
import json
import logging
import os
import sys
from datetime import datetime, timedelta

import pkg_resources
from PyQt5.QtWidgets import QApplication

from data_mass.classes.text import text
from data_mass.classes.window import window
# Local application imports
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request,
    update_value_to_json
)

logger = logging.getLogger(__name__)


# Create payload for delivery date
def get_microservice_payload_post_delivery_date(account_data, is_alternative_delivery_date, dates_list, index):
    # Create dictionary with delivery window values
    dict_values = {
        'alternative': is_alternative_delivery_date,
        'deliveryScheduleId': account_data['deliveryScheduleId'],
        'endDate': dates_list['endDate'],
        'expirationDate': dates_list['expirationDate'],
        'id': str(index) + "_" + account_data['accountId'],
        'startDate': dates_list['startDate']
    }
    
    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/create_delivery_window_payload.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    # Update the delivery window values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])
    
    return json_object

def get_microservice_delivery_fee_charge_relay(account_data, include_delivery_cost):
    dict_values = {
        'accounts': [account_data['accountId']],
        'charges' : [{
            'chargeId' : 'CHARGE-01',
            'type' : 'DELIVERY_DATE_FEE',
            'output' : {
                'scope' : 'ORDER',
                'applyTo' : 'BASE_PRICE',
                'type' : 'AMOUNT',
                'value' : include_delivery_cost['fee_value']
            }
        }]        
    }

    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/create_delivery_fee_charge-relay.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    # Update the delivery window values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])
    
    return json_object

# Create payload for delivery fee
def get_microservice_payload_post_delivery_fee(account_data, include_delivery_cost):
    # Create dictionary with interest amount values
    dict_values = {
        'accounts[0]': account_data['accountId'],
        'interest[0].interestId': 'ID00001',
        'interest[0].externalId': 'NON_REGULAR_DELIVERY_DATE_FEE',
        'interest[0].scope': 'order',
        'interest[0].conditions': {
            'alternativeDeliveryDate': True,
            'orderTotal': {
                'maximumValue': include_delivery_cost['min_order_value']
            }
        },
        'interest[0].output': {
            'totalOutput': {
                'additionalAmount': include_delivery_cost['fee_value']
            }
        }
    }
    
    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/create_delivery_fee_interest_payload.json"
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

    if zone == "US":
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
            account_data,
            option_is_alternative_delivery_date,
            dates_list[index],
            index
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


# Return payload next date for delivery date
def return_dates_payload(option):
    if option == '1':
        list_delivery_dates = list()
        initial_date = datetime.now()
        initial_month = initial_date.strftime('%m')
        last_day_month = calendar.monthrange(int(initial_date.strftime('%Y')), int(initial_date.strftime('%m')))[1]

        if int(initial_date.strftime('%d')) == last_day_month:
            initial_date = initial_date + timedelta(days=1)
            initial_month = initial_date.strftime('%m')
            last_day_month = calendar.monthrange(int(initial_date.strftime('%Y')), int(initial_date.strftime('%m')))[1]

        while (int(initial_date.strftime('%d')) < last_day_month) and (int(initial_date.strftime('%m'))<= int(initial_month)):
            clone_initial_date = initial_date
            clone_initial_date = clone_initial_date + timedelta(days=1)
            start_date = clone_initial_date.strftime('%Y-%m-%d')
            end_date = start_date
            expiration_date = initial_date.strftime('%Y-%m-%d') + 'T20:00:00Z'

            list_delivery_dates.append({'startDate': start_date, 'endDate': end_date, 'expirationDate': expiration_date})
            initial_date = initial_date + timedelta(days=2)
        return list_delivery_dates
    else:
        date_list = delivery_window_selector()
        if not date_list:
            print("\nNo delivery window end date was selected.")
            return False
        else:
            datetime_object = datetime.strptime(date_list[0], "%B")
            month_number = datetime_object.month
            today = datetime.today()
            date_datetime_object = datetime(int(today.year), month_number, int(date_list[1]))
            initial_date = today
            list_delivery_dates = list()

            while initial_date < date_datetime_object:
                clone_initial_date = initial_date
                clone_initial_date = clone_initial_date + timedelta(days=1)
                start_date = clone_initial_date.strftime('%Y-%m-%d')
                end_date = start_date
                expiration_date = initial_date.strftime('%Y-%m-%d') + 'T20:00:00Z'

                list_delivery_dates.append(
                    {'startDate': start_date, 'endDate': end_date, 'expirationDate': expiration_date})
                initial_date = initial_date + timedelta(days=2)
            return list_delivery_dates


# Create delivery fee (interest) in microservice
def create_delivery_fee_microservice(zone, environment, account_data, include_delivery_cost):
    # Get headers
    request_headers = get_header_request(zone, False, False, False, False)

    charge_relay_countries = ["AR", "BR", "CO", "DO", "EC", "MX", "PE", "ZA"]
    
    # Get base URL
    if zone in charge_relay_countries:
        request_url = get_microservice_base_url(environment) + '/charge-relay/v1'
        request_body = get_microservice_delivery_fee_charge_relay(account_data, include_delivery_cost)
    else:
        request_url = get_microservice_base_url(environment) + '/cart-calculation-relay/v2/interest'
        request_body = get_microservice_payload_post_delivery_fee(account_data, include_delivery_cost)
    
    # Place request
    response = place_request('PUT', request_url, json.dumps(request_body), request_headers)
    if response.status_code != 202:
        print(text.Red + '\n- [Pricing Engine Relay Service] Failure to add delivery cost. Response Status: '
                         '{response_status}. Response message: {response_message}'
              .format(response_status=str(response.status_code), response_message=response.text))
        return False

    return 'success'


def delivery_window_selector():

    # create pyqt5 app
    app = QApplication(sys.argv)

    # create the instance of window
    Window = window()
    app.exec()
    selected_dates = getattr(Window, 'dates')
    sys.is_finalizing()
    if selected_dates:
        return selected_dates
    else:
        return False
