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
from unicodedata import numeric
from os import path


def get_magento_user_v3_params(environment):
    if environment == "UAT":
        return get_magento_user_v3_params_uat()
    else:
        return get_magento_user_v3_params_dev()


def get_magento_user_v3_params_uat():
    b2b_server_name = "b2biamgbusuat1.b2clogin.com"
    b2b_path = "b2biamgbusuat1.onmicrosoft.com"
    b2b_signin_policy = "B2C_1A_AB2CSignin_DR_Dev_UAT"
    b2b_signup_policy = "B2C_1A_AB2CSignUp_DR_Dev_UAT"
    b2b_onboarding_policy = "B2C_1A_AB2COnboarding_DR_Dev_UAT"
    params = {
        "B2B_SERVER_NAME": b2b_server_name,
        "B2B_PATH": b2b_path,
        "REDIRECT_URL": "com.abi.Socio-Cerveceria://oauth/redirect",
        "CLIENT_ID": "2fb9932f-5ac2-4f9d-91d7-35ea363cde34",
        "B2B_SIGNIN_POLICY": b2b_signin_policy,
        "B2B_SIGNUP_POLICY": b2b_signup_policy,
        "B2B_ONBOARDING_POLICY": b2b_onboarding_policy,
        "OPT_SECRET": "1NcRfUjXn2r4u7x!A%D*G-KaPdSgVkYp",
        "OPT_INTERVAL": 600,
        "BASE_SIGNIN_URL": "https://{0}/{1}/{2}".format(b2b_server_name, b2b_path, b2b_signin_policy),
        "BASE_SIGNUP_URL": "https://{0}/{1}/{2}".format(b2b_server_name, b2b_path, b2b_signup_policy),
        "BASE_ONBOARDING_URL": "https://{0}/{1}/{2}".format(b2b_server_name, b2b_path, b2b_onboarding_policy)}
    return params


def get_magento_user_v3_params_dev():
    b2b_server_name = "b2biamgbusdev.b2clogin.com"
    b2b_path = "b2biamgbusdev.onmicrosoft.com"
    b2b_signin_policy = "B2C_1A_AB2CSIGNIN_DR"
    b2b_signup_policy = "B2C_1A_AB2CSIGNUP_DR"
    b2b_onboarding_policy = "B2C_1A_AB2CONBOARDING_DR"
    params = {
        "B2B_SERVER_NAME": b2b_server_name,
        "B2B_PATH": b2b_path,
        "REDIRECT_URL": "com.abi.Socio-Cerveceria://oauth/redirect",
        "CLIENT_ID": "496d9127-5493-4d0b-b98b-e3d8fb2e557e",
        "B2B_SIGNIN_POLICY": b2b_signin_policy,
        "B2B_SIGNUP_POLICY": b2b_signup_policy,
        "B2B_ONBOARDING_POLICY": b2b_onboarding_policy,
        "OPT_SECRET": "1NcRfUjXn2r4u7x!A%D*G-KaPdSgVkYp",
        "OPT_INTERVAL": 60,
        "BASE_SIGNIN_URL": "https://{0}/{1}/{2}".format(b2b_server_name, b2b_path, b2b_signin_policy),
        "BASE_SIGNUP_URL": "https://{0}/{1}/{2}".format(b2b_server_name, b2b_path, b2b_signup_policy),
        "BASE_ONBOARDING_URL": "https://{0}/{1}/{2}".format(b2b_server_name, b2b_path, b2b_onboarding_policy)}
    return params


# Validate option menu selection
def validateOptionRequestSelection(option):
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
    }

    value = switcher.get(option, "false")
    return value


# Validate option menu selection
def validate_option_request_selection_for_structure_3(option):
    switcher = {
        "0": "true",
        "1": "true",
        "2": "true"
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
            "BR": "true",
            "CO": "true"
        }

        value = switcher.get(zone, "false")
        return value

# Validate Country in User creation
def validateCountryInUserCreation(country):
    switcher = {
        "BR": "true",
        "DO": "true",
        "AR": "true",
        "CL": "true", 
        "ZA": "true",
        "CO": "true"
    }

    value = switcher.get(country, "false")
    return value

def validate_zone_for_inventory(zone):
    switcher = {
        "ZA": "true",
        "CO": "true",
        "MX": "true"
    }

    value = switcher.get(zone, "false")
    return value

def validate_zone_for_deals(zone):
    switcher = {
        "BR": "true",
        "DO": "true",
        "CO": "true",
        "MX": "true"
    }

    value = switcher.get(zone, "false")
    return value

def validate_zone_for_ms(zone):
    switcher = {
        "BR": "true",
        "DO": "true",
        "ZA": "true",
        "CO": "true",
        "MX": "true"
    }

    value = switcher.get(zone, "false")
    return value

# Validate account structure
def validateStructure(option):
    if option == "1" or option == "2" or option == "3" or option == "4":
        return "true"
    else:
        return "false"

# Validate deals
def validate_deals(option):
    if option == "1" or option == "2" or option == "3" or option == "4" or option == "5":
        return "true"
    else:
        return "false"

# Validate environment
def validateEnvironment(environment):
    if environment == "DEV" or environment == "QA" or environment == "UAT":
        return "true"
    else:
        return "false"


# Validate environment to User creation
def validateEnvironmentInUserCreation(environment):
    if environment == "UAT" or environment == "SIT":
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
        if os.name == 'nt':
            os.makedirs(dir_logs)
        else:
            subprocess.call(["mkdir", "-p", dir_logs])

    # If the debug.log file does not exist, create it
    if path.exists(file_debug) == False:
        if os.name == 'nt':
            f = open(file_debug,"w+")
            f.close()
        else:
            subprocess.call(["touch", file_debug])

    # Log request data to debug.log file
    logging.basicConfig(filename=file_debug,level=logging.DEBUG)
    logging.debug("= Init LOG =")
    logging.debug("REQUEST TYPE= " + request_type)
    logging.debug("HEADERS= " + json.dumps(request_headers))
    logging.debug("URL= " + request_url)
    logging.debug("BODY= " + convert_json_to_string(request_body))
    logging.debug("RESPONSE= " + str(response))
    logging.debug("RESPONSE BODY= " + str(response.text))
    logging.debug('= / Finish LOG =\n')
    
    return response

# Return JWT header request
def get_header_request(header_country, useJwtAuthorization="false", useRootAuthentication="false", useInclusionAuthentication="false", sku_product="false"):
    
    switcher = {
        "ZA": "UTC",
        "AR": "America/Buenos_Aires",
        "DO": "America/Santo_Domingo",
        "BR": "America/Sao_Paulo",
        "CO": "America/Bogota",
        "PE": "America/Lima",
        "CL": "America/Santiago",
        "MX": "UTC"
    }
    timezone = switcher.get(header_country.upper(), "false")

    header = {
        "Content-Type": "application/json",
        "country": header_country.upper(),
        "requestTraceId": str(uuid1()),
        "x-timestamp": str(int(round(time() * 1000))),
        "cache-control": "no-cache",
        "timezone": timezone
    }

    if useJwtAuthorization == "true":
        header['Authorization'] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3NlcnZpY2VzIiwiZXhwIjoxNjA2Njk0NDAwLCJpYXQiOjE1MzY5NjMyNTcsInVwZGF0ZWRfYXQiOjE1MzY5NjMyNTcsIm5hbWUiOiJmaWxpcGVyaWJlaXJvKzFAY2lhbmR0LmNvbSIsImFjY291bnRJRCI6IjU1MDE1MCIsInVzZXJJRCI6IjExIiwicm9sZXMiOlsiUk9MRV9DVVNUT01FUiJdfQ.q1kb8Kb6OO9ewNo82WQdNwmrfgZtI_0dB9jq3j0XOUk"
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
def get_microservice_base_url(environment, is_v1="true"):
    if environment == "SIT":
        if is_v1 == "true":
            return "https://b2b-services-qa.westeurope.cloudapp.azure.com/v1"
        else:
            return "https://b2b-services-qa.westeurope.cloudapp.azure.com/api"

    elif is_v1 == "false":
        return "https://b2b-services-" + environment.lower() + ".westeurope.cloudapp.azure.com/api"
    else:
        return "https://b2b-services-" + environment.lower() + ".westeurope.cloudapp.azure.com/v1"


# Return base URL for Magento
def get_magento_base_url(environment, country):
    magento_url = {
        "UAT": {
            "BR": "https://test-br.abi-sandbox.net",
            "DO": "https://test-conv-micerveceria.abi-sandbox.net",
            "AR": "https://migration-test-conv-quilmes.abi-sandbox.net",
            "CL": "https://test-conv-cl-mitienda.abi-sandbox.net",
            "ZA": "https://test-conv-sabconnect.abi-sandbox.net",
            "CO": "https://test-copec-co.abi-sandbox.net"
        },
        "SIT": {
            "BR": "https://sit-br.abi-sandbox.net",
            "DO": "https://sit-dr.abi-sandbox.net",
            "AR": "https://sit-las-ar.abi-sandbox.net",
            "CL": "https://sit-las-ch.abi-sandbox.net",
            "ZA": "https://sit-za.abi-sandbox.net",
            "CO": "https://sit-copec-co.abi-sandbox.net"
        }
    }

    return magento_url.get(environment).get(country)


def get_region_id(country):
    region_id = {
        "BR": "PT_BR",
        "DO": "ES_DO",
        "AR": "ES_AR",
        "CL": "ES_CL",
        "ZA": "EN_ZA",
        "CO": "ES_CO"
    }
    return region_id.get(country)


# Return base URL for Azure IAM
def get_azure_iam_base_url(environment, country):
    iam_url = {
        "UAT": {
            "DO": "https://b2biamgbusuat1.b2clogin.com/b2biamgbusuat1.onmicrosoft.com"
        },
        "DEV": {
            "DO": "https://b2biamgbusdev.b2clogin.com/b2biamgbusdev.onmicrosoft.com"
        }
    }

    return iam_url.get(environment).get(country)


# Returns Magento User Registration Integration Access Token
def get_magento_access_token(environment, country):
    access_token = {
        "UAT": {
            "BR": "qq8t0w0tvz7nbn4gxo5jh9u62gohvjrw",
            "DO": "56jqtzzto7tw9uox8nr3eckoeup53dt2",
            "AR": "30lqki06nbdegugcmdb0ttm9yppnmoec",
            "CL": "30lqki06nbdegugcmdb0ttm9yppnmoec",
            "ZA": "31pdb0yht5kn3eld7gum021f6k984jh9",
            "CO": "8mh6b9b6ft6m1cr5k7zm2jh4aljq4slx"
        },
        "SIT": {
            "BR": "qq8t0w0tvz7nbn4gxo5jh9u62gohvjrw",
            "DO": "56jqtzzto7tw9uox8nr3eckoeup53dt2",
            "AR": "30lqki06nbdegugcmdb0ttm9yppnmoec",
            "CL": "30lqki06nbdegugcmdb0ttm9yppnmoec",
            "ZA": "nmvvuk58lc425a7p5l55orrkgh0jprr2",
            "CO": "walt5dp3keiq2du0f30kir21v13f3u0v"
        }
    }

    return access_token.get(environment).get(country)


# Clear terminal
def clearTerminal():
    os.system("clear")

# Kill application
def finishApplication():
    sys.exit()

# Print init menu
def printAvailableOptions(selectionStructure):
    if selectionStructure == "1" or selectionStructure == "2":
        print(text.default_text_color + str(1), text.Yellow + "Create account")
        print(text.default_text_color + str(2), text.Yellow + "Input products")
        print(text.default_text_color + str(3), text.Yellow + "Input credit")
        print(text.default_text_color + str(4), text.Yellow + "Input delivery window")
        if selectionStructure == "1":
            print(text.default_text_color + str(5), text.Yellow + "(Beta) - Check Simulation Service")
        elif selectionStructure == "2":
            print(text.default_text_color + str(5), text.Yellow + "Input recommended products")
            print(text.default_text_color + str(6), text.Yellow + "Input inventory to product")
            print(text.default_text_color + str(7), text.Yellow + "Input deals")
            print(text.default_text_color + str(8), text.Yellow + "Input combos")
            print(text.default_text_color + str(9), text.Yellow + "Create User IAM")
            print(text.default_text_color + str(10), text.Yellow + "(Beta) - Check Simulation Service")

        print(text.default_text_color + str(0), text.Yellow + "Close application")
        selection = input(text.default_text_color + "\nPlease select: ")
        while validateOptionRequestSelection(selection) == "false":
            print(text.Red + "\n- Invalid option\n")
            print(text.default_text_color + str(1), text.Yellow + "Create account")
            print(text.default_text_color + str(2), text.Yellow + "Input products")
            print(text.default_text_color + str(3), text.Yellow + "Input credit")
            print(text.default_text_color + str(4), text.Yellow + "Input delivery window")
            if selectionStructure == "1":
                print(text.default_text_color + str(5), text.Yellow + "(Beta) - Check Simulation Service")
            elif selectionStructure == "2":
                print(text.default_text_color + str(5), text.Yellow + "Input recommended products")
                print(text.default_text_color + str(6), text.Yellow + "Input inventory to product")
                print(text.default_text_color + str(7), text.Yellow + "Input deals")
                print(text.default_text_color + str(8), text.Yellow + "Input combos")
                print(text.default_text_color + str(9), text.Yellow + "Create User IAM")
                print(text.default_text_color + str(10), text.Yellow + "(Beta) - Check Simulation Service")
            
            print(text.default_text_color + str(0), text.Yellow + "Close application")
            selection = input(text.default_text_color + "\nPlease select: ")
    elif selectionStructure == "3":
        print(text.default_text_color + str(1), text.Yellow + "Create User")
        print(text.default_text_color + str(2), text.Yellow + "Associate Account to user")

        print(text.default_text_color + str(0), text.Yellow + "Close application")
        selection = input(text.default_text_color + "\nPlease select: ")
        while validate_option_request_selection_for_structure_3(selection) == "false":
            print(text.default_text_color + str(1), text.Yellow + "Create User")
            print(text.default_text_color + str(2), text.Yellow + "Associate Account to user")

            print(text.default_text_color + str(0), text.Yellow + "Close application")
            selection = input(text.default_text_color + "\nPlease select: ")
    elif selectionStructure == "4":
        return "4"
    else:
        finishApplication()

    return selection

# Print welcome menu
def printWelcomeScript():
    print(text.BackgroundLightYellow + text.Bold + text.Black)
    print("╭──────────────────────────────────╮")
    print("│ 🐝                               │")
    print("│   ANTARCTICA AUTOMATION SCRIPT   │")
    print("│                               🐝 │")
    print("╰──────────────────────────────────╯") 
    print(text.BackgroundDefault + text.ResetBold + text.default_text_color + "\n")

# Print structure menu
def printStructureMenu():
    print(text.default_text_color + str(1), text.Yellow + "Middleware")
    print(text.default_text_color + str(2), text.Yellow + "MicroService")
    print(text.default_text_color + str(3), text.Yellow + "Magento")

    print(text.default_text_color + str(4), text.Yellow + "Close application")
    structure = input(text.default_text_color + "\nChoose which backend you want to run a service for: ")
    while validateStructure(structure) == "false":
        print(text.Red + "\n- Invalid option\n")
        print(text.default_text_color + str(1), text.Yellow + "Middleware")
        print(text.default_text_color + str(2), text.Yellow + "MicroService")
        print(text.default_text_color + str(3), text.Yellow + "Magento")
        print(text.default_text_color + str(4), text.Yellow + "Close application")
        structure = input(text.default_text_color + "\nChoose which backend you want to run a service for: ")

    return structure

# Print deals menu
def printDealsMenu():
    print(text.default_text_color + "\nWhich type of deal do you want to create?")
    print(text.default_text_color + str(1), text.Yellow + "Input deal type discount")
    print(text.default_text_color + str(2), text.Yellow + "Input deal type stepped discount")
    print(text.default_text_color + str(3), text.Yellow + "Input deal type free good")
    print(text.default_text_color + str(4), text.Yellow + "Input deal type stepped free good")
    print(text.default_text_color + str(5), text.Yellow + "Input deal type stepped discount with quantity")
    structure = input(text.default_text_color + "\nPlease select: ")
    while validate_deals(structure) == "false":
        print(text.Red + "\n- Invalid option")
        print(text.default_text_color + "\nWhich type of deal do you want to create?")
        print(text.default_text_color + str(1), text.Yellow + "Input deal type discount")
        print(text.default_text_color + str(2), text.Yellow + "Input deal type stepped discount")
        print(text.default_text_color + str(3), text.Yellow + "Input deal type free good")
        print(text.default_text_color + str(4), text.Yellow + "Input deal type stepped free good")
        print(text.default_text_color + str(5), text.Yellow + "Input deal type stepped discount with quantity")

    return structure

# Print combos menu
def printCombosMenu():
    print(text.default_text_color + "\nWhich type of combo do you want to create?")
    print(text.default_text_color + str(1), text.Yellow + "Input combo type discount")
    print(text.default_text_color + str(2), text.Yellow + "Input combo type free good")
    print(text.default_text_color + str(3), text.Yellow + "Input combo with only free goods")
    structure = input(text.default_text_color + "\nPlease select: ")
    while validateComboStructure(structure) == "false":
        print(text.Red + "\n- Invalid option")
        print(text.default_text_color + "\nWhich type of combo do you want to create?")
        print(text.default_text_color + str(1), text.Yellow + "Input combo type discount")
        print(text.default_text_color + str(2), text.Yellow + "Input combo type free good")
        print(text.default_text_color + str(3), text.Yellow + "Input combo with only free goods")
        structure = input(text.default_text_color + "\nPlease select: ")

    return structure

# Validate combo type structure
def validateComboStructure(option):
    if option != "1" or option != "2" or option != "3":
        return "true"
    else:
        return "false"

# Print Discount type menu
def print_discount_type_menu():
    discount_type = input(text.default_text_color + "What type of discount do you want to apply (1. Percentage / 2. Fixed amount): ")
    while discount_type != "1" and discount_type != "2":
        print(text.Red + "\n- Invalid option")
        discount_type = input(text.default_text_color + "What type of discount do you want to apply (1. Percentage / 2. Fixed amount): ")

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
                discount_value = float(input(text.default_text_color + "Discount percentage (%): "))
                break
            except ValueError:
                print(text.Red + "\n- Invalid value")
    else:
        while True:
            try:
                discount_value = float(input(text.default_text_color + "Discount amount: "))
                break
            except ValueError:
                print(text.Red + "\n- Invalid value")

    return discount_value

# Print range index menu
def print_index_range_menu(indexs=4):
    index_list = list()

    for x in range(indexs):
        range_index = input(text.default_text_color + "Range index #" + str(x) + ": ")
        while range_index == "" or int(range_index) <= 0:
            print(text.Red + "\n- Range index must be greater than 0")
            range_index = input(text.default_text_color + "\nRange index #" + str(x) + ": ")

        index_list.append(range_index)
    
    return index_list

# Print discount range menu
def print_discount_range_menu(indexs=2):
    index_list = list()

    for x in range(indexs):
        discount_value = input(text.default_text_color + "Discount value for index #" + str(x) + ": ")
        while discount_value == "" or float(discount_value) <= 0:
            print(text.Red + "\n- Discount value must be greater than 0")
            discount_value = input(text.default_text_color + "\nDiscount value for index #" + str(x) + ": ")

        index_list.append(discount_value)

    return index_list

# Print quantity range menu
def printQuantityRangeMenu():
    index_list = list()

    for x in range(2):
        quantity_value = input(text.default_text_color + "SKU quantity for index #" + str(x) + ": ")
        while quantity_value == "" or int(quantity_value) <= 0:
            print(text.Red + "\n- SKU quantity must be greater than 0")
            quantity_value = input(text.default_text_color + "\nSKU quantity for index #" + str(x) + ": ")

        index_list.append(quantity_value)

    return index_list


# Print minimum quantity menu
def printMinimumQuantityMenu():
    minimum_quantity = input(text.default_text_color + "Desired quantity needed to buy to get a discount/free good: ")
    while minimum_quantity == "" or int(minimum_quantity) <= 0:
            print(text.Red + "\n- Minimum quantity must be greater than 0")
            minimum_quantity = input(text.default_text_color + "Desired quantity needed to buy to get a discount/free good: ")

    return minimum_quantity

# Print quantity menu
def printQuantityMenu():
    quantity = input(text.default_text_color + "Desired quantity of free goods to offer: ")
    while quantity == "" or int(quantity) <= 0:
        print(text.Red + "\n- SKU quantity must be greater than 0")
        quantity = input(text.default_text_color + "Desired quantity of free goods to offer: ")

    return quantity

# Print Account ID menu
#   validate_string_account -- For microservices, a character number pattern was determined 
#       for account creation, however not all zones use this pattern (e.g. AR, CH, CO). 
#       Therefore, for simulation, this parameter was created to allow using accounts that do not 
#       follow this pattern of more than 10 characters
def print_account_id_menu(validate_string_account='true'):
    while True:
        try:
            abi_id = int(input(text.default_text_color + 'Account ID: '))
            if validate_string_account == 'true':
                while validateAccount(str(abi_id)) == 'false':
                    print(text.Red + '\n- Account ID should not be empty and it must contain at least 10 characters')
                    abi_id = int(input(text.default_text_color + '\nAccount ID: '))
            break
        except ValueError:
            print(text.Red + '\n- The account ID must be Numeric\n')

    return str(abi_id)


# Print account name menu
def printNameMenu():
    name = input(text.default_text_color + "Account name: ")
    while validateName(name) == "false":
        print(text.Red + "\n- The account name should not be empty")
        name = input(text.default_text_color + "Account name: ")

    return name

# Print zone menu
def printZoneMenu(isMiddleware="true"):
    if isMiddleware == "true":
        zone = input(text.default_text_color + "Zone (ZA): ")
        while validateZone("true", zone.upper()) == "false":
            print(text.Red + "\n- Invalid option\n")
            zone = input(text.default_text_color + "Zone (ZA): ")
    else:
        zone = input(text.default_text_color + "Zone (ZA, DO, BR): ")
        while validateZone("false", zone.upper()) == "false":
            print(text.Red + "\n- Invalid option\n")
            zone = input(text.default_text_color + "Zone (ZA, DO, BR): ")

    return zone.upper()

# Print zone menu for Microservice
def print_zone_menu_for_ms():
    zone = input(text.default_text_color + "Zone (BR, DO, ZA, CO, MX): ")
    while validate_zone_for_ms(zone.upper()) == "false":
        print(text.Red + "\n- Invalid option\n")
        zone = input(text.default_text_color + "Zone (BR, DO, ZA, CO, MX): ")

    return zone.upper()

# Print zone menu for inventory
def print_zone_menu_for_inventory():
    zone = input(text.default_text_color + "Zone (ZA, CO, MX): ")
    while validate_zone_for_inventory(zone.upper()) == "false":
        print(text.Red + "\n- Invalid option\n")
        zone = input(text.default_text_color + "Zone (ZA, CO, MX): ")

    return zone.upper()

# Print zone menu for deals
def print_zone_menu_for_deals():
    zone = input(text.default_text_color + "Zone (BR, DO, CO, MX): ")
    while validate_zone_for_deals(zone.upper()) == "false":
        print(text.Red + "\n- Invalid option\n")
        zone = input(text.default_text_color + "Zone (BR, DO, CO, MX): ")

    return zone.upper()

# Print country menu for User creation
def printCountryMenuInUserCreation():
    country = input(text.default_text_color + "Country (BR, DO, AR, CL, ZA, CO): ")
    while validateCountryInUserCreation(country.upper()) == "false":
        print(text.Red + "\n- Invalid option\n")
        country = input(text.default_text_color + "Country (BR, DO, AR, CL, ZA, CO): ")

    return country.upper()

# Print environment menu
def printEnvironmentMenu():
    environment = input(text.default_text_color + "Environment (DEV, QA, UAT): ")
    while validateEnvironment(environment.upper()) == 'false':
        print(text.Red + '\n- Invalid option')
        environment = input(text.default_text_color + "Environment (DEV, QA, UAT): ")

    return environment.upper()

# Print environment menu for User creation
def printEnvironmentMenuInUserCreation():
    environment = input(text.default_text_color + "Environment (UAT, SIT): ")
    while validateEnvironmentInUserCreation(environment.upper()) == 'false':
        print(text.Red + '\n- Invalid option')
        environment = input(text.default_text_color + "Environment (UAT, SIT): ")

    return environment.upper()

# Print payment method menu
def printPaymentMethodMenu(zone):
    payment_cash = ["CASH"]

    if zone == "BR":
        paymentMethod = input(text.default_text_color + "Choose the payment method (1. CASH / 2. BANK SLIP / 3. CASH, BANK SLIP): ")
        while paymentMethod == "" or (int(paymentMethod) != 1 and int(paymentMethod) != 2 and int(paymentMethod) != 3):
            print(text.Red + "\n- Invalid option\n")
            paymentMethod = input(text.default_text_color + "Choose the payment method (1. CASH / 2. BANK SLIP / 3. CASH, BANK SLIP): ")
        
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
        paymentMethod = input(text.default_text_color + "Choose the payment method (1. CASH / 2. CREDIT / 3. CASH, CREDIT): ")
        while paymentMethod == "" or (int(paymentMethod) != 1 and int(paymentMethod) != 2 and int(paymentMethod) != 3):
            print(text.Red + "\n- Invalid option\n")
            paymentMethod = input(text.default_text_color + "Choose the payment method (1. CASH / 2. CREDIT / 3. CASH, CREDIT): ")

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
    startDeliveryDate = input(text.default_text_color + "Enter the start date to apply the discount (YYYY-mm-dd): ")
    while validateDate(startDeliveryDate) == "false":
        print(text.Red + "\n- Invalid date\n")
        startDeliveryDate = input(text.default_text_color + "Enter the start date to apply the discount (YYYY-mm-dd): ")

    endDeliveryDate = input(text.default_text_color + "Enter the end date to apply the discount (YYYY-mm-dd): ")
    while validateDate(endDeliveryDate) == "false":
        print(text.Red + "\n- Invalid date\n")
        endDeliveryDate = input(text.default_text_color + "Enter the end date to apply the discount(YYYY-mm-dd): ")
    
    listDeliveryWindowDates.append({'startDate':startDeliveryDate, 'endDate':endDeliveryDate})

    return listDeliveryWindowDates

def printMinimumOrderMenu():
    option_type = input(text.default_text_color + "Minimum order type (1. Poduct quantity / 2. Order volume / 3. Order total): ")
    while option_type == "" or (int(option_type) != 1 and int(option_type) != 2 and int(option_type) != 3): 
        print(text.Red + "\n- Invalid option\n")
        option_type = input(text.default_text_color + "Minimum order type (1. Poduct quantity / 2. Order volume / 3. Order total): ")

    switcher = {
        "1": "PRODUCT_QUANTITY",
        "2": "ORDER_VOLUME",
        "3": "ORDER_TOTAL"
    }

    minimum_order_type = switcher.get(option_type, "false")

    option_value = input(text.default_text_color + "Minimum order value: ")
    while option_value == "" or int(option_value) <= 0:
        print(text.Red + "\n- SKU quantity must be greater than 0\n")
        option_value = input(text.default_text_color + "Minimum order value: ")

    minimum_order_values = list()
    minimum_order_values.append(minimum_order_type)
    minimum_order_values.append(option_value)

    return minimum_order_values


# Print user name menu
def print_input_email():
    email = input(text.default_text_color + "User email: ")
    while len(email) == 0:
        print(text.Red + "\n- The user email should not be empty")
        email = input(text.default_text_color + "User email: ")

    return email


# Print user password menu
def print_input_password():
    password = input(text.default_text_color + "User password: ")
    while len(password) == 0:
        print(text.Red + "\n- The user password should not be empty")
        password = input(text.default_text_color + "User password: ")

    return password


# Print user phone menu
def print_input_phone():
    return input(text.default_text_color + "User phone (optional): ")


# Validate State in registration flow
def validate_state(zone):
    if (zone == "BR"):
        state = "RS"
    
    elif (zone == "DO"):
        state = "STO DGO"

    elif (zone == "ZA"):
        state = "Free State"
    
    elif (zone == "CO"):
        state = "SAN ALBERTO"
    
    elif (zone == "MX"):
        state = "Cidade do México"

    else:
        state = "CAPITAL FEDERAL"
            
    return state

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

def get_sku_price(abi_id, combo_item, zone, environment):
    # Get base URL
    request_url = get_microservice_base_url(environment) + "/cart-calculator/prices?accountID=" + abi_id

    # Get header request
    request_headers = get_header_request(zone, "true", "false", "false", "false")

    # Get body request
    request_body = ""

    # Send request
    response = place_request("GET", request_url, request_body, request_headers)

    if response.status_code == 200 and response.text != "":
        json_data = json.loads(response.text)
        for dict in json_data:
            if dict["sku"] == combo_item:
                return dict["price"]
    else:
        print(text.Red + "\n- [Pricing Engine] Something went wrong when searching for prices")
        finishApplication()

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

def is_blank (str):
    return not (str and str.strip())    

def print_input_tax_id():
    """Validate tax_id
    Requirements:
        - Not empty
    """
    tax_id = input(text.default_text_color + "Tax ID: ")
    while is_blank(tax_id):
        print(text.Red + "\n- The tax ID should not be empty")
        tax_id = input(text.default_text_color + "Tax ID: ")
    return tax_id

def print_input_username():
    """Validate username
    Requirements:
        - Not empty
    """
    username = input(text.default_text_color + "Username: ")
    while is_blank(username):
        print(text.Red + "\n- The Username should not be empty")
        username = input(text.default_text_color + "Username: ")
    return username

def validate_country_menu_in_user_create_iam(country):
    switcher = {
        "DO": "true"
    }
    return switcher.get(country, "false")

def validate_environment_menu_in_user_create_iam(environment):
    switcher = {
        "DEV": "true",
        "UAT": "true"
    }
    return switcher.get(environment, "false")

def print_country_menu_in_user_create_iam():
    """Print Country Menu to Create User IAM
    Requirements:
        - DR 
    """
    country = input(text.default_text_color + "Country (DO): ")
    while validate_country_menu_in_user_create_iam(country.upper()) == "false":
        print(text.Red + "\n- Invalid option\n")
        country = input(text.default_text_color + "Country (DO): ")
    return country.upper()

def print_environment_menu_in_user_create_iam():
    """Print Environment Menu to Create User IAM
        Requirements:
        - DEV
        - UAT
    """
    environment = input(text.default_text_color + "Environment (DEV, UAT): ")
    while validate_environment_menu_in_user_create_iam(environment.upper()) == 'false':
        print(text.Red + '\n- Invalid option')
        environment = input(text.default_text_color + "Environment (DEV, UAT): ")
    return environment.upper()

# Print zone simulation menu
def print_zone_simulation_menu(is_middleware="true"):
    if is_middleware == "true":
        zone = input(text.default_text_color + "Zone (AR, CL): ")
        while validateZone("true", zone.upper()) == "false":
            print(text.Red + "\n- Invalid option\n")
            zone = input(text.default_text_color + "Zone (AR, CL): ")
    else:
        zone = input(text.default_text_color + "Zone (ZA, DO, BR, CO): ")
        while validateZone("false", zone.upper()) == "false":
            print(text.Red + "\n- Invalid option\n")
            zone = input(text.default_text_color + "Zone (ZA, DO, BR, CO): ")

    return zone.upper()

# Validate zone simulation
def validate_zone_simulation_service(is_middleware, zone):
    if is_middleware == "true":
        switcher = {
            "AR": "true",
            "CL": "true"
        }

        value = switcher.get(zone, "false")
        return value
    else:
        switcher = {
            "DO": "true",
            "ZA": "true",
            "BR": "true"
        }

        value = switcher.get(zone, "false")
        return value

# Validate if value is a number
def is_number(s):
    try:
        float(s)
        return "true"
    except ValueError:
        pass
 
    try:
        numeric(s)
        return "true"
    except (TypeError, ValueError):
        pass
 
    return "false"

# Menu for payment method simulation
def print_payment_method_simulation_menu(zone):
    if zone == "BR":
        payment_choice = input(text.default_text_color + "Select payment method for simulation: 1 - CASH, 2 - BANK_SLIP ")
        while payment_choice != "1" and payment_choice != "2":
            print(text.Red + "\n- Invalid option\n")
            payment_choice = input(text.default_text_color + "Select payment method for simulation: 1 - CASH, 2 - BANK_SLIP ")

        if payment_choice == "1":
            payment_method = "CASH"
        else:
            payment_method = "BANK_SLIP"

    elif zone == "DO" and zone == "CO":
        payment_choice = input(text.default_text_color + "Select payment method for simulation: 1 - CASH, 2 - CREDIT ")
        while payment_choice != "1" and payment_choice != "2":
            print(text.Red + "\n- Invalid option\n")
            payment_choice = input(text.default_text_color + "Select payment method for simulation: 1 - CASH, 2 - CREDIT")

        if payment_choice == "1":
            payment_method = "CASH"
        else:
            payment_method = "CREDIT"
    else:
        payment_method = "CASH"
    
    return payment_method

# Return first and last day in the year
def return_first_and_last_date_year_payload():
    first_date = date(date.today().year, 1, 1)
    first_date = first_date.strftime("%Y-%m-%d")
    last_date = date(date.today().year, 12, 31)
    last_date = last_date.strftime("%Y-%m-%d")
    return {'startDate': first_date, 'endDate': last_date}

# Return payment term value for BANK_SLIP payment method
def return_payment_term_bank_slip():
    payment_term = []
    term_periods = []

    temp_index = 0
    while temp_index < 5:
        temp_index = temp_index+1
        list_term_periods = {
            'days':temp_index
        }

        term_periods.append(list_term_periods)
    
    list_payment_term = {
        "type":"BANK_SLIP",
        "termPeriods":term_periods
    }

    payment_term.append(list_payment_term)
    return payment_term