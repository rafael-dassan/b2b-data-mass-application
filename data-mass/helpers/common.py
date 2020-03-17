from requests import request
from uuid import uuid1
from time import time
from json import dumps
import os
import sys
import json
from classes.text import text
from datetime import date, datetime, timedelta
from jsonpath_rw import Index, Fields
from jsonpath_rw_ext import parse
import logging

# Validate option menu selection
def validateOptionRequestSelection(option, isExtraStructure = "false"):
    if isExtraStructure == "false":
        switcher = {
            "0": "true",
            "1": "true",
            "2": "true",
            "3": "true",
            "4": "true",
            "5": "true",
            "6": "true",
            "7": "true",
            "8": "true",
            "9": "true",
            "10": "true",
            "11": "true"
        }

        value = switcher.get(option, "false")
        return value
        
    else:
        switcher = {
            "0": "true",
            "1": "true"
        }

        value = switcher.get(option, "false")
        return value

# Validate lenght of Account ID
def validateAccount(accountId):
    if len(accountId) < 10:
        return "false"
    else:
        return accountId

# Validate lenght of account name
def validateName(name):
    if len(name) == 0:
        return "false"
    else:
        return name

# Validate zone
def validateZone(isMiddleware, zone):
    if isMiddleware == "true":
        switcher = {
            "ZA": "true",
            "AR": "true",
            "CL": "true"
        }

        value = switcher.get(zone, "false")
        return value
    else:
        switcher = {
            "DO": "true",
            "ZA": "true",
            "AR": "true",
            "CL": "true",
            "BR": "true"
        }

        value = switcher.get(zone, "false")
        return value

# Validate account structure
def validateStructure(option):
    if option == "1" or option == "2" or option == "3" or option == "4":
        return "true"
    else:
        return "false"

# Validate environment
def validateEnvironment(environment):
    if environment == 'DEV' or environment == 'QA' or environment == 'UAT':
        return 'true'
    else:
        return "false"

# Place generic request
def place_request(request_type, request_url, request_body, request_headers):

    LOG_FILENAME = 'var/debug.log'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

    logging.debug('= Init LOG =')
    logging.debug('TYPE=' + request_type)
    logging.debug('HEADERS=' + json.dumps(request_headers))
    logging.debug('URL=' + request_url)
    logging.debug('BODY=' + request_body)
    logging.debug('= / Finish LOG =')
    
    response = request(
        request_type,
        request_url,
        data=request_body,
        headers=request_headers
    )

    return response

# Return JWT header request
def get_header_request(header_country, useJwtAuthorization="false", useRootAuthentication="false", useInclusionAuthentication="false", sku_product="false"):
    timezone = "UTC"

    header = {
        "Content-Type": "application/json",
        "country": header_country.upper(),
        "requestTraceId": str(uuid1()),
        "x-timestamp": str(int(round(time() * 1000))),
        "cache-control": "no-cache",
        "timezone": timezone
    }

    if useJwtAuthorization == "true":
        header['Authorization'] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3NlcnZpY2VzIiwiZXhwIjoxNTg1NjEyODAwLCJ1cGRhdGVkX2F0IjoxNTY1NzkxODI0LCJpYXQiOjE1NjU3OTE4MjQsIm5hbWUiOiJ0ZXN0ZUB0ZXN0ZS5jb20iLCJhY2NvdW50SUQiOiIwMDAwMTAwMDA0IiwidXNlcklEIjoiMTYiLCJyb2xlcyI6WyJST0xFX0NVU1RPTUVSIl19.GUc9ssFyXle0F0W6LUU2amvZ-hm7TFIDteR50WlQFUE"
    elif useRootAuthentication == "true":
        header['Authorization'] = "Basic cm9vdDpyb290"
    elif useInclusionAuthentication == "true":
        header['Authorization'] = "Basic cmVsYXk6TVVRd3JENVplSEtB"
    else:
        header['Authorization'] = "Basic cmVsYXk6cmVsYXk="
    
    if sku_product != "false":
        header['skuId'] = sku_product

    return header

# Return base URL for Middleware
def get_middleware_base_url(zone, environment, version_request):
    prefix_zone = zone.lower()

    if zone == "AR" or zone == "CL":
        prefix_zone = "las"
    
    prefix_environment = environment.lower()

    if environment == "UAT":
        prefix_environment = "test"

    return "https://b2b-" + prefix_zone.lower() + "-" + prefix_environment.lower() + ".azurewebsites.net/api/" + version_request + "/" + zone.upper()

# Return base URL for Microservice
def get_microservice_base_url(environment):
    return "https://b2b-services-" + environment.lower() + ".westeurope.cloudapp.azure.com/v1"

# Clear terminal
def clearTerminal():
    os.system("clear")

# Kill application
def finishApplication():
    sys.exit()

# Print init menu
def printAvailableOptions(selectionStructure):
    if selectionStructure == "1" or selectionStructure == "2":
        print(text.White + str(1), text.Yellow + "Create account")
        print(text.White + str(2), text.Yellow + "Input products to an account")
        print(text.White + str(3), text.Yellow + "Input credit to an account")
        print(text.White + str(4), text.Yellow + "Input delivery window to an account")
        if selectionStructure == "2":
            print(text.White + str(5), text.Yellow + "Input discount by payment method")
            print(text.White + str(6), text.Yellow + "Input discount by delivery date")
            print(text.White + str(7), text.Yellow + "Input discount by SKU")
            print(text.White + str(8), text.Yellow + "Input free good selection")
            print(text.White + str(9), text.Yellow + "Input stepped discount")
            print(text.White + str(10), text.Yellow + "Input stepped free good")
            print(text.White + str(11), text.Yellow + "Input combos")
            

        print(text.White + str(0), text.Yellow + "Close application")
        selection = input(text.White + "\nPlease select: ")
        while validateOptionRequestSelection(selection) == "false":
            print(text.Red + "\n- Invalid option\n")
            print(text.White + str(1), text.Yellow + "Create account")
            print(text.White + str(2), text.Yellow + "Input products to an account")
            print(text.White + str(3), text.Yellow + "Input credit to an account")
            print(text.White + str(4), text.Yellow + "Input delivery window to an account")
            if selectionStructure == "2":
                print(text.White + str(5), text.Yellow + "Input discount by payment method")
                print(text.White + str(6), text.Yellow + "Input discount by delivery date")
                print(text.White + str(7), text.Yellow + "Input discount by SKU")
                print(text.White + str(8), text.Yellow + "Input free good selection")
                print(text.White + str(9), text.Yellow + "Input stepped discount")
                print(text.White + str(10), text.Yellow + "Input stepped free good")
                print(text.White + str(11), text.Yellow + "Input combos")

            print(text.White + str(0), text.Yellow + "Close application")
            selection = input(text.White + "\nPlease select: ")

    elif selectionStructure == "3":
        print(text.White + str(1), text.Yellow + "Open Browser")
        print(text.White + str(0), text.Yellow + "Close application")
        selection = input(text.White + "\nPlease select: ")
        while validateOptionRequestSelection(selection, "true") == "false":
            print(text.Red + "\n- Invalid option\n")
            print(text.White + str(1), text.Yellow + "Open Browser")
            print(text.White + str(0), text.Yellow + "Close application")
            selection = input(text.White + "\nPlease select: ")
    
    else:
        finishApplication()

    return selection

# Print welcome menu
def printWelcomeScript():
    print(text.White + "🄰🄽🅃🄰🅁🄲🅃🄸🄲🄰 🄰🅄🅃🄾🄼🄰🅃🄸🄾🄽 🅂🄲🅁🄸🄿🅃\n")

# Print structure menu
def printStructureMenu():
    print(text.White + str(1), text.Yellow + "Middleware (ZA, AR, CL)")
    print(text.White + str(2), text.Yellow + "MicroService")
    print(text.White + str(3), text.Yellow + "Extras")
    print(text.White + str(4), text.Yellow + "Close application")
    structure = input(text.White + "\nChoose which backend you want to run a service for: ")
    while validateStructure(structure) == "false":
        print(text.Red + "\n- Invalid option\n")
        print(text.White + str(1), text.Yellow + "Middleware (ZA, AR, CL)")
        print(text.White + str(2), text.Yellow + "MicroService")
        print(text.White + str(3), text.Yellow + "Extras")
        print(text.White + str(4), text.Yellow + "Close application")
        structure = input(text.White + "\nChoose which backend you want to run a service for: ")

    return structure

# Print Account ID menu
def printAccountIdMenu(zone):
    abi_id = input(text.White + "Account ID: ")
    while validateAccount(abi_id) == "false" and (zone == "BR" or zone == "DO"):
        print(text.Red + "\n- Account ID should not be empty or it must contain at least 10 characters")
        abi_id = input(text.White + "Account ID: ")

    return abi_id

# Print account name menu
def printNameMenu():
    name = input(text.White + "Account name: ")
    while validateName(name) == "false":
        print(text.Red + "\n- The account name should not be empty")
        name = input(text.White + "Account name: ")

    return name

# Print zone menu
def printZoneMenu(isMiddleware="true"):
    if isMiddleware == "true":
        zone = input("Zone (ZA, AR, CL): ")
        while validateZone("true", zone.upper()) == "false":
            print(text.Red + "\n- Invalid option\n")
            zone = input(text.White + "Zone (ZA, AR, CL): ")
    else:
        zone = input("Zone (ZA, AR, CL, DO, BR): ")
        while validateZone("false", zone.upper()) == "false":
            print(text.Red + "\n- Invalid option\n")
            zone = input(text.White + "Zone (ZA, AR, CL, DO, BR): ")

    return zone

# Print environment menu
def printEnvironmentMenu():
    environment = input("Environment (DEV, QA, UAT): ")
    while validateEnvironment(environment.upper()) == 'false':
        print(text.Red + '\n- Invalid option')
        environment = input(text.White + "Environment (DEV, QA, UAT): ")

    return environment

# Print payment method menu
def printPaymentMethodMenu(zone):
    payment_cash = ["CASH"]

    if zone == "BR":
        paymentMethod = input(text.White + "Choose the payment method (1. CASH / 2. BANK SLIP / 3. CASH, BANK SLIP): ")
        while (int(paymentMethod) != 1 and int(paymentMethod) != 2 and int(paymentMethod) != 3):
            print(text.Red + "\n- Invalid option\n")
            paymentMethod = input(text.White + "Choose the payment method (1. CASH / 2. BANK SLIP / 3. CASH, BANK SLIP): ")
        
        payment_credit = ["BANK_SLIP"]
        payment_list = ["CASH", "BANK_SLIP"]

        switcher = {
            "1": payment_cash,
            "2": payment_credit,
            "3": payment_list
        }

        value = switcher.get(paymentMethod, "false")
        return value

    elif zone == "DO":
        paymentMethod = input(text.White + "Choose the payment method (1. CASH / 2. CREDIT / 3. CASH, CREDIT): ")
        while (int(paymentMethod) != 1 and int(paymentMethod) != 2 and int(paymentMethod) != 3):
            print(text.Red + "\n- Invalid option\n")
            paymentMethod = input(text.White + "Choose the payment method (1. CASH / 2. CREDIT / 3. CASH, CREDIT): ")

        payment_credit = ["CREDIT"]
        payment_list = ["CASH", "CREDIT"]
        
        switcher = {
            "1": payment_cash,
            "2": payment_credit,
            "3": payment_list
        }

        value = switcher.get(paymentMethod, "false")
        return value

    else:
        return payment_cash

# Print range delivery date menu
def printDeliveryDateMenu():
    listDeliveryWindowDates = list()
    startDeliveryDate = input(text.White + "Enter the start date to apply the discount (YYYY-mm-dd): ")
    while validateDate(startDeliveryDate) == "false":
        print(text.Red + "\n- Invalid date\n")
        startDeliveryDate = input(text.White + "Enter the start date to apply the discount (YYYY-mm-dd): ")

    endDeliveryDate = input(text.White + "Enter the end date to apply the discount (YYYY-mm-dd): ")
    while validateDate(endDeliveryDate) == "false":
        print(text.Red + "\n- Invalid date\n")
        endDeliveryDate = input(text.White + "Enter the end date to apply the discount(YYYY-mm-dd): ")
    
    listDeliveryWindowDates.append({'startDate':startDeliveryDate, 'endDate':endDeliveryDate})

    return listDeliveryWindowDates

# Validate date
def validateDate(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return "false"

def update_value_to_json(json_object, json_path, new_value):
    """Update value to JSON using JSONPath
    Arguments:
        - json_object: json as a dictionary object.
        - json_path: jsonpath expression
        - new_value: value to update
    Return new json_object
    """
    json_path_expr = parse(json_path)
    for match in json_path_expr.find(json_object):
        path = match.path
        if isinstance(path, Index):
            match.context.value[match.path.index] = new_value
        elif isinstance(path, Fields):
            match.context.value[match.path.fields[0]] = new_value
    return json_object

def convert_json_to_string(json_object):
    """Convert JSON object to string
    Arguments:
        - json_object: json as a dictionary object.
    Return new json_string
    """
    return json.dumps(json_object)