from json import dumps
from datetime import timedelta
import calendar
from common import *


# Create payload for delivery date
def get_microservice_payload_post_delivery_date(account_data, is_alternative_delivery_date, dates_list):
    request_body = dumps({
        'alternative': is_alternative_delivery_date,
        'deliveryScheduleId': account_data['deliveryScheduleId'],
        'endDate': dates_list['endDate'],
        'expirationDate': dates_list['expirationDate'],
        'id': account_data['accountId'],
        'startDate': dates_list['startDate']
    })

    return request_body


# Create delivery date in microservice
def create_delivery_window_microservice(abi_id, zone, environment, account_data, is_alternative_delivery_date):
    # Define headers
    request_headers = get_header_request(zone, 'false', 'true')

    # Define url request
    request_url = get_microservice_base_url(environment) + '/account-relay/delivery-windows'

    # Return list of dates
    dates_list = return_dates_payload()

    # Get body request
    request_body = get_microservice_payload_post_delivery_date(account_data, is_alternative_delivery_date, dates_list)

    # Place request
    response = place_request('POST', request_url, request_body, request_headers)
    if response.status_code == 202:
        return 'success'
    else:
        return response.status_code


# Validate alternative delivery date creation
def validate_alternative_delivery_date(option):
    if option == '' or (option != 'Y' and option != 'N'):
        return 'false'
    else:
        return 'true'


# Return payload next date for delivery date
def return_dates_payload():
    today = datetime.now()
    next_date = datetime.strptime(today.strftime('%Y/%m/%d'), '%Y/%m/%d')
    next_date = next_date + timedelta(days=1)
    base_last_day_month = next_date
    next_date = next_date.strftime('%Y-%m-%d')
    start_date = next_date
    expiration_date = next_date + 'T23:59:59Z'
    last_day_month = calendar.monthrange(
        int(base_last_day_month.strftime('%Y')), int(base_last_day_month.strftime('%m')))[1]
    end_date = datetime.strptime(base_last_day_month.strftime('%Y/%m/%d'), '%Y/%m/%d')
    end_date = end_date.strftime('%Y-%m') + '-' + str(last_day_month)
    return {'startDate': start_date, 'endDate': end_date, 'expirationDate': expiration_date}
