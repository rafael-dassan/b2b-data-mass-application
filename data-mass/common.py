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
import subprocess
from os import path

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

def validateDealType(deal_type):
    if deal_type == "1" or deal_type == "2" or deal_type == "3" or deal_type == "4":
        return "true"
    else:
        return "false"

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
            "BR": "true",
            "CO": "true"
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
    if environment == "DEV" or environment == "QA" or environment == "UAT":
        return "true"
    else:
        return "false"

# Place generic request
def place_request(request_type, request_url, request_body, request_headers):
    # Send request
    response = request(
        request_type,
        request_url,
        data=request_body,
        headers=request_headers
    )

    # Create dir and file paths
    dir_project = os.path.abspath(os.path.dirname(__file__))
    dir_logs = os.path.join(dir_project, "logs")
    file_debug = os.path.join(dir_logs, "debug.log")

    # If the logs directory does not exist, create it
    if path.exists(dir_logs) == False:
        subprocess.call(["mkdir", "-p", dir_logs])

    # If the debug.log file does not exist, create it
    if path.exists(file_debug) == False:
        subprocess.call(["touch", file_debug])

    # Log request data to debug.log file
    logging.basicConfig(filename=file_debug,level=logging.DEBUG)
    logging.debug("= Init LOG =")
    logging.debug("REQUEST TYPE= " + request_type)
    logging.debug("HEADERS= " + json.dumps(request_headers))
    logging.debug("URL= " + request_url)
    logging.debug("BODY= " + request_body)
    logging.debug("RESPONSE= " + str(response))
    logging.debug('= / Finish LOG =\n')
    
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
        print(text.White + str(2), text.Yellow + "Input products")
        print(text.White + str(3), text.Yellow + "Input credit")
        print(text.White + str(4), text.Yellow + "Input delivery window")
        if selectionStructure == "2":
            print(text.White + str(5), text.Yellow + "Input beer recommender")
            print(text.White + str(6), text.Yellow + "Input deals")
            print(text.White + str(7), text.Yellow + "Input combos")

        print(text.White + str(0), text.Yellow + "Close application")
        selection = input(text.White + "\nPlease select: ")
        while validateOptionRequestSelection(selection) == "false":
            print(text.Red + "\n- Invalid option\n")
            print(text.White + str(1), text.Yellow + "Create account")
            print(text.White + str(2), text.Yellow + "Input products")
            print(text.White + str(3), text.Yellow + "Input credit")
            print(text.White + str(4), text.Yellow + "Input delivery window")
            if selectionStructure == "2":
                print(text.White + str(5), text.Yellow + "Input deals")
                print(text.White + str(6), text.Yellow + "Input combos")

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

# Print deals menu
def printDealsMenu():
    print(text.White + "\nWhich type of deal do you want to create?")
    print(text.White + str(1), text.Yellow + "Input deal type discount")
    print(text.White + str(2), text.Yellow + "Input deal type stepped discount")
    print(text.White + str(3), text.Yellow + "Input deal type free good")
    print(text.White + str(4), text.Yellow + "Input deal type stepped free good")
    structure = input(text.White + "\nPlease select: ")
    while validateStructure(structure) == "false":
        print(text.Red + "\n- Invalid option")
        print(text.White + "\nWhich type of deal do you want to create?")
        print(text.White + str(1), text.Yellow + "Input deal type discount")
        print(text.White + str(2), text.Yellow + "Input deal type stepped discount")
        print(text.White + str(3), text.Yellow + "Input deal type free good")
        print(text.White + str(4), text.Yellow + "Input deal type stepped free good")

    return structure

# Print Discount type menu
def printDiscountTypeMenu():
    discount_type = input(text.White + "What type of discount do you want to apply (1. Percentage / 2. Fixed amount): ")
    while discount_type != "1" and discount_type != "2":
        print(text.Red + "\n- Invalid option")
        discount_type = input(text.White + "What type of discount do you want to apply (1. Percentage / 2. Fixed amount): ")

    switcher = {
        "1": "percentOff",
        "2": "amountOff"
    }

    value = switcher.get(discount_type, "true")

    return value

# Print Discount value menu
def printDiscountValueMenu(discount_type):
    if discount_type == "percentOff":
        while True:
            try:
                discount_value = float(input(text.White + "Discount percentage (%): "))
                break
            except ValueError:
                print(text.Red + "\n- Invalid value")
    else:
        while True:
            try:
                discount_value = float(input(text.White + "Discount amount: "))
                break
            except ValueError:
                print(text.Red + "\n- Invalid value")

    return discount_value

# Print range index menu
def printIndexRangeMenu():
    index_list = list()

    for x in range(4):
        range_index = input(text.White + "Range index #" + str(x) + ": ")
        while range_index == "" or int(range_index) <= 0:
            print(text.Red + "\n- Range index must be greater than 0")
            range_index = input(text.White + "\nRange index #" + str(x) + ": ")

        index_list.append(range_index)
    
    return index_list

# Print discount range menu
def printDiscountRangeMenu():
    index_list = list()

    for x in range(2):
        discount_value = input(text.White + "Discount value for index #" + str(x) + ": ")
        while discount_value == "" or float(discount_value) <= 0:
            print(text.Red + "\n- Discount value must be greater than 0")
            discount_value = input(text.White + "\nDiscount value for index #" + str(x) + ": ")

        index_list.append(discount_value)

    return index_list

# Print quantity range menu
def printQuantityRangeMenu():
    index_list = list()

    for x in range(2):
        quantity_value = input(text.White + "SKU quantity for index #" + str(x) + ": ")
        while quantity_value == "" or int(quantity_value) <= 0:
            print(text.Red + "\n- SKU quantity must be greater than 0")
            quantity_value = input(text.White + "\nSKU quantity for index #" + str(x) + ": ")

        index_list.append(quantity_value)

    return index_list

# Print minimum quantity menu
def printMinimumQuantityMenu():
    minimum_quantity = input(text.White + "Desired quantity needed to buy to get a discount/free good: ")
    while minimum_quantity == "" or int(minimum_quantity) <= 0:
            print(text.Red + "\n- Minimum quantity must be greater than 0")
            minimum_quantity = input(text.White + "Desired quantity needed to buy to get a discount/free good: ")

    return minimum_quantity

# Print quantity menu
def printQuantityMenu():
    quantity = input(text.White + "Desired quantity of free goods to offer: ")
    while quantity == "" or int(quantity) <= 0:
        print(text.Red + "\n- SKU quantity must be greater than 0")
        quantity = input(text.White + "Desired quantity of free goods to offer: ")

    return quantity

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
        zone = input("Zone (ZA, AR, CL, DO, BR, CO): ")
        while validateZone("false", zone.upper()) == "false":
            print(text.Red + "\n- Invalid option\n")
            zone = input(text.White + "Zone (ZA, AR, CL, DO, BR, CO): ")

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
        while paymentMethod == "" or (int(paymentMethod) != 1 and int(paymentMethod) != 2 and int(paymentMethod) != 3):
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
        while paymentMethod == "" or (int(paymentMethod) != 1 and int(paymentMethod) != 2 and int(paymentMethod) != 3):
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

def printMinimumOrderMenu():
    option_type = input(text.White + "Minimum order type (1. Poduct quantity / 2. Order volume / 3. Order total): ")
    while option_type == "" or (int(option_type) != 1 and int(option_type) != 2 and int(option_type) != 3): 
        print(text.Red + "\n- Invalid option\n")
        option_type = input(text.White + "Minimum order type (1. Poduct quantity / 2. Order volume / 3. Order total): ")

    switcher = {
        "1": "PRODUCT_QUANTITY",
        "2": "ORDER_VOLUME",
        "3": "ORDER_TOTAL"
    }

    minimum_order_type = switcher.get(option_type, "false")

    option_value = input(text.White + "Minimum order value: ")
    while option_value == "" or int(option_value) <= 0:
        print(text.Red + "\n- SKU quantity must be greater than 0\n")
        option_value = input(text.White + "Minimum order value: ")

    minimum_order_values = list()
    minimum_order_values.append(minimum_order_type)
    minimum_order_values.append(option_value)

    return minimum_order_values

# Validate the option to finish application
def validateYesOrNotOption(option):
    if option == "Y" or option == "N":
        return "true"
    else:
        return "false"

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

def create_list(*items):
    """Returns a list containing given items.
    The returned list can be assigned both to ``${scalar}`` and ``@{list}``
    variables.
    """
    return list(items)