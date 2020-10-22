# Standard library imports
import os
import json
import calendar
from datetime import timedelta, datetime

# Local application imports
from common import update_value_to_json, get_header_request, get_microservice_base_url, place_request
from classes.text import text


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

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_delivery_window_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

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
            'alternativeDeliveryDate': 'true',
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

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_delivery_fee_interest_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Update the delivery window values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])
    
    return json_object


# Create delivery date in microservice
def create_delivery_window_microservice(zone, environment, account_data, is_alternative_delivery_date):
    # Get headers
    request_headers = get_header_request(zone, 'false', 'true', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/account-relay/delivery-windows'

    # Return list of dates
    dates_list = return_dates_payload()

    index = 0
    request_body = list()
    while index <= (len(dates_list) - 1):
        # Force mixed values if it's is_alternative_delivery_date
        if is_alternative_delivery_date == 'true':
            if (index % 2) == 0:
                option_is_alternative_delivery_date = 'true'
            else:
                option_is_alternative_delivery_date = 'false'
        else:
            option_is_alternative_delivery_date = is_alternative_delivery_date

        # Get body request
        temporary_body = get_microservice_payload_post_delivery_date(account_data, option_is_alternative_delivery_date,
                                                                     dates_list[index], index)
        request_body.append(temporary_body)
        index = index + 1
    
    # Place request
    response = place_request('POST', request_url, json.dumps(request_body), request_headers)
    if response.status_code != 202:
        print(text.Red + '\n- [Account Relay Service] Failure to add delivery window to account. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'

    return 'success'


# Validate alternative delivery date option
def validate_alternative_delivery_date(option):
    if option == '' or (option != 'Y' and option != 'N'):
        return 'false'
    else:
        return 'true'


# Return payload next date for delivery date
def return_dates_payload():
    list_delivery_dates = list()
    initial_date = datetime.now()
    initial_month = initial_date.strftime('%m')
    last_day_month = calendar.monthrange(int(initial_date.strftime('%Y')), int(initial_date.strftime('%m')))[1]

    if int(initial_date.strftime('%d')) == last_day_month:
        initial_date = initial_date + timedelta(days=1)
        initial_month = initial_date.strftime('%m')
        last_day_month = calendar.monthrange(int(initial_date.strftime('%Y')), int(initial_date.strftime('%m')))[1]
        
    while (int(initial_date.strftime('%d')) < last_day_month) and (int(initial_date.strftime('%m'))
                                                                   <= int(initial_month)):
        clone_initial_date = initial_date
        clone_initial_date = clone_initial_date + timedelta(days=1)
        start_date = clone_initial_date.strftime('%Y-%m-%d')
        end_date = start_date
        expiration_date = initial_date.strftime('%Y-%m-%d') + 'T20:00:00Z'

        list_delivery_dates.append({'startDate': start_date, 'endDate': end_date, 'expirationDate': expiration_date})
        initial_date = initial_date + timedelta(days=2)
    
    return list_delivery_dates


# Create delivery fee (interest) in microservice
def create_delivery_fee_microservice(zone, environment, account_data, include_delivery_cost):
    # Get headers
    request_headers = get_header_request(zone, 'false', 'false', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/cart-calculation-relay/v2/interest'

    # Get body request
    request_body = get_microservice_payload_post_delivery_fee(account_data, include_delivery_cost)
    
    # Place request
    response = place_request('PUT', request_url, json.dumps(request_body), request_headers)
    if response.status_code != 202:
        print(text.Red + '\n- [Pricing Engine Relay Service] Failure to add delivery cost. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'

    return 'success'
