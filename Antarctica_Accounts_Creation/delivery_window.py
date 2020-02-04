import sys
from json import dumps
import time
from datetime import date, datetime, timedelta
import calendar

#Custom
from helper import *

# Create delivery window on middleware
def create_delivery_window_middleware(abi_id, zone, environment):
    
    listDates = returnDatesPayload()
    # Define headers
    headers = get_header_request(zone, 'false', 'true')

    # Define URL Middleware
    url = get_middleware_base_url(zone, environment, "v5") + "/delivery-windows"

    # Body request
    request_body = dumps({
        "deliveryScheduleId": "{account_id}".format(account_id=abi_id),
        "endDate": "{end_date}".format(end_date=listDates['endDate']),
        "expirationDate": "{expiration_date}".format(expiration_date=listDates['expirationDate']),
        "id": "{account_id}".format(account_id=abi_id),
        "startDate": "{start_date}".format(start_date=listDates['startDate'])
    })

    # Send request
    response = place_request("POST", url, request_body, headers)
    
    if response.status_code == 202:
        return 'success'
    else:
        return response.status_code

# Create payload for delivery date
def get_microservice_payload_post_delivery_date(zone, accountId, environment, accountData, isAlternativeDeliveryDate, listDates):
    request_body = dumps({
        "alternative": isAlternativeDeliveryDate,
        "deliveryScheduleId": accountData['deliveryScheduleId'],
        "endDate": listDates['endDate'],
        "expirationDate": listDates['expirationDate'],
        "id": accountData['accountId'],
        "startDate": listDates['startDate']
    })

    return request_body

# Create delivery date in microservice
def create_delivery_window_microservice(accountId, zone, environment, accountData, isAlternativeDeliveryDate):
    
    # Define headers
    request_headers = get_header_request(zone, 'false', 'true')

    # Define url request
    request_url = get_microservice_base_url(environment) + "/account-relay/delivery-windows"

    # Return list of dates
    listDates = returnDatesPayload()

    # Get body request
    request_body = get_microservice_payload_post_delivery_date(zone, accountId, environment, accountData, isAlternativeDeliveryDate, listDates)

    # Place request
    response = place_request("POST", request_url, request_body, request_headers)
    if response.status_code == 202:
        return 'success'
    else:
        return response.status_code

# Validate alternative delivery date creation
def validateAlternativeDeliveryDate(option):
    if option == '' or (option != 'Y' and option != 'N'):
        return 'false'
    else:
        return 'true'

# Return payload next date for delivery date
def returnDatesPayload():
    today = datetime.now()
    next_date = datetime.strptime(today.strftime("%Y/%m/%d"), "%Y/%m/%d")
    next_date = next_date + timedelta(days=1)
    baseLastDayMonth = next_date
    next_date = next_date.strftime("%Y-%m-%d")
    start_date = next_date
    expiration_date = next_date + "T23:59:59Z"
    last_day_month = calendar.monthrange(
        int(baseLastDayMonth.strftime("%Y")), int(baseLastDayMonth.strftime("%m")))[1]
    end_date = datetime.strptime(baseLastDayMonth.strftime("%Y/%m/%d"), "%Y/%m/%d")
    end_date = end_date.strftime("%Y-%m") + "-" + str(last_day_month)
    return {'startDate': start_date, 'endDate': end_date, 'expirationDate': expiration_date}
