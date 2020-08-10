from json import loads
from requests import request
from uuid import uuid1
from time import time
import os
import sys
import json

from classes.text import text
from datetime import date, datetime
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
def validate_option_request_selection(selection):
    switcher = {
        '0': 'true',
        '1': 'true',
        '2': 'true',
        '3': 'true',
        '4': 'true',
        '5': 'true',
        '6': 'true',
        '7': 'true',
        '8': 'true',
        '9': 'true',
        '10': 'true',
        '11': 'true',
        '12': 'true'
    }

    value = switcher.get(selection, 'false')
    return value


# Validate option menu selection
def validate_option_request_selection_for_structure_3(option):
    switcher = {
        '0': 'true',
        '1': 'true',
        '2': 'true',
        '3': 'true'
    }

    value = switcher.get(option, 'false')
    return value


# Validate lenght of Account ID
def validate_account(account_id, zone):
    size_account_id = len(account_id)

    if size_account_id == 0:
        return 'error_0'
    elif (size_account_id > 0) and (is_number(account_id) == 'false'):
        return 'not_number'
    elif (zone == 'DO' or zone == 'BR') and (is_number(account_id) == 'true') and (size_account_id < 10):
        return 'error_10'
    elif is_number(account_id) == 'true':
        return 'true'


def validate_payments_method(payments_method, zone):
    size_payments_method = len(payments_method)

    if size_payments_method == 0:
        return 'error_0'
    elif (size_payments_method > 0) and (is_number(payments_method) == 'false'):
        return 'not_number'
    elif (int(payments_method) != 1) and (int(payments_method) != 2) and (int(payments_method) != 3):
        return 'not_payments_method'
    else:
        return 'true'


# Validate length of account name
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
    if isMiddleware == 'true':
        switcher = {
            'CL': 'true'
        }

        value = switcher.get(zone, 'false')
        return value
    else:
        switcher = {
            'DO': 'true',
            'ZA': 'true',
            'BR': 'true',
            'CO': 'true',
            'AR': 'true',
            'MX': 'true'
        }

        value = switcher.get(zone, 'false')
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


def validate_zone_data_searching_deals(zone):
    switcher = {
        'BR': 'true',
        'DO': 'true',
        'CO': 'true',
        'AR': 'true',
        'CL': 'true'
    }

    value = switcher.get(zone, 'false')
    return value


def validate_zone_for_rewards(zone):
    switcher = {
        'BR': 'true',
        'DO': 'true',
        'CO': 'true',
        'AR': 'true',
        'ZA': 'true'
    }

    value = switcher.get(zone, 'false')
    return value


def validate_zone_for_inventory(zone):
    switcher = {
        'ZA': 'true',
        'CO': 'true',
        'MX': 'true',
        'AR': 'true'
    }

    value = switcher.get(zone, 'false')
    return value


def validate_zone_for_deals(zone):
    switcher = {
        'BR': 'true',
        'DO': 'true',
        'CO': 'true',
        'MX': 'true',
        'AR': 'true',
        'ZA': 'true'
    }

    value = switcher.get(zone, 'false')
    return value


def validate_zone_for_combos(zone):
    switcher = {
        'BR': 'true',
        'DO': 'true'
    }

    value = switcher.get(zone, 'false')
    return value


def validate_zone_for_delivery_window(zone):
    switcher = {
        'BR': 'true',
        'DO': 'true',
        'ZA': 'true',
        'CO': 'true',
        'MX': 'true',
        'AR': 'true',
        'CL': 'true'
    }

    value = switcher.get(zone, 'false')
    return value


def validate_zone_for_ms(zone):
    switcher = {
        'BR': 'true',
        'DO': 'true',
        'ZA': 'true',
        'CO': 'true',
        'MX': 'true',
        'AR': 'true'
    }

    value = switcher.get(zone, 'false')
    return value


# Validate account structure
def validateStructure(option):
    if option == "1" or option == "2" or option == "3" or option == "4":
        return "true"
    else:
        return "false"


# Validate rewards
def validate_rewards(option):
    if option == '1' or option == '2' or option == '3' or option == '4':
        return 'true'
    else:
        return 'false'


# Validate deals
def validate_orders(option):
    if option == '1' or option == '2' or option == '3' or option == '4':
        return 'true'
    else:
        return 'false'


def validate_recommendation_type(option):
    if option == '1' or option == '2' or option == '3' or option == '4':
        return 'true'
    else:
        return 'false'


# Validate deals
def validate_deals(option):
    if option == "1" or option == "2" or option == "3" or option == "4" or option == "5":
        return "true"
    else:
        return "false"


# Validate environment
def validateEnvironment(environment):
    if environment == 'DEV' or environment == 'SIT' or environment == 'UAT':
        return 'true'
    else:
        return 'false'


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
            f = open(file_debug, "w+")
            f.close()
        else:
            subprocess.call(["touch", file_debug])

    # Log request data to debug.log file
    logging.basicConfig(filename=file_debug, level=logging.DEBUG, format='%(asctime)s :: %(levelname)s :: %(message)s')
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger('chardet.charsetprober').setLevel(logging.WARNING)
    logging.debug("Initializing rerquest...")
    logging.debug("Request method: " + request_type)
    logging.debug("Request headers: " + json.dumps(request_headers))
    logging.debug("Request URL: " + request_url)
    logging.debug("Request body: " + request_body)
    logging.debug("Response code: " + str(response.status_code))
    logging.debug("Response body: " + response.text)
    logging.debug("Request finished!\n")

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

    if zone == 'AR' or zone == 'CL':
        prefix_zone = 'las'

    prefix_environment = environment.lower()

    if environment == 'UAT':
        prefix_environment = 'test'
    elif environment == 'SIT':
        prefix_environment = 'qa'

    return 'https://b2b-' + prefix_zone.lower() + '-' + prefix_environment.lower() + '.azurewebsites.net/api/' + version_request + '/' + zone.upper()


# Return base URL for Microservice
def get_microservice_base_url(environment, is_v1='true'):
    if environment == 'DEV':
        if is_v1 == 'true':
            return 'https://b2b-services-dev.westeurope.cloudapp.azure.com/v1'
        else:
            return 'https://b2b-services-dev.westeurope.cloudapp.azure.com/api'

    elif is_v1 == 'false':
        return 'https://services-' + environment.lower() + '.bees-platform.dev/api'
    else:
        return 'https://services-' + environment.lower() + '.bees-platform.dev/v1'


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
def get_magento_user_registration_access_token(environment, country):
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

# Returns Magento Datamass Application Access Token
def get_magento_datamass_access_token(environment, country):
    access_token = {
        "UAT": {
            "BR": "8z2z3y523hoqkcqci8q58afuoue81bns",
            "DO": "js4gd8y9wkqogf7eo2s4uy6oys15lfkf",
            "AR": "a34o213zgisn67efeg0zbq04sqg667qk",
            "CL": "a34o213zgisn67efeg0zbq04sqg667qk",
            "ZA": "0seca4btewbr3e1opma4je2x8ftj57wx",
            "CO": "meqei3q5ztreebdpb5vyej378mt2o8qy"
        },
        "SIT": {
            "BR": "q6yti2dxmhp0e2xjgyvtt72nziss6ptp",
            "DO": "tgqnjlqpfupf0i4zxcs2doqx409k1hyq",
            "AR": "hzp6hw65oqiyeyv8ozfzunex0nc1rff8",
            "CL": "hzp6hw65oqiyeyv8ozfzunex0nc1rff8",
            "ZA": "fde80w10jbbaed1mrz6yg0pwy1vzfo48",
            "CO": "bl9cnb3ngb7almxml6rmvma3lyl8b1st"
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
def print_available_options(selection_structure):
    if selection_structure == '1':
        print(text.default_text_color + str(0), text.Yellow + 'Close application')
        print(text.default_text_color + str(1), text.Yellow + 'Create account')
        print(text.default_text_color + str(2), text.Yellow + 'Input products')
        print(text.default_text_color + str(3), text.Yellow + 'Input credit')
        print(text.default_text_color + str(4), text.Yellow + 'Input delivery window')
        print(text.default_text_color + str(5), text.Yellow + 'Input recommended products')
        print(text.default_text_color + str(6), text.Yellow + 'Input inventory to product')
        print(text.default_text_color + str(7), text.Yellow + 'Input orders to account')
        print(text.default_text_color + str(8), text.Yellow + 'Input deals')
        print(text.default_text_color + str(9), text.Yellow + 'Input combos')
        print(text.default_text_color + str(10), text.Yellow + 'Create item')
        print(text.default_text_color + str(11), text.Yellow + 'Create invoice')
        print(text.default_text_color + str(12), text.Yellow + 'Create rewards')

        selection = input(text.default_text_color + '\nPlease select: ')
        while validate_option_request_selection(selection) == 'false':
            print(text.Red + '\n- Invalid option\n')
            print(text.default_text_color + str(0), text.Yellow + 'Close application')
            print(text.default_text_color + str(1), text.Yellow + 'Create account')
            print(text.default_text_color + str(2), text.Yellow + 'Input products')
            print(text.default_text_color + str(3), text.Yellow + 'Input credit')
            print(text.default_text_color + str(4), text.Yellow + 'Input delivery window')
            print(text.default_text_color + str(5), text.Yellow + 'Input recommended products')
            print(text.default_text_color + str(6), text.Yellow + 'Input inventory to product')
            print(text.default_text_color + str(7), text.Yellow + 'Input orders to account')
            print(text.default_text_color + str(8), text.Yellow + 'Input deals')
            print(text.default_text_color + str(9), text.Yellow + 'Input combos')
            print(text.default_text_color + str(10), text.Yellow + 'Create item')
            print(text.default_text_color + str(11), text.Yellow + 'Create invoice')
            print(text.default_text_color + str(12), text.Yellow + 'Create rewards')

            selection = input(text.default_text_color + '\nPlease select: ')

    elif selection_structure == '2':
        print(text.default_text_color + str(0), text.Yellow + 'Close application')
        print(text.default_text_color + str(1), text.Yellow + 'Order simulation via Microservice')
        print(text.default_text_color + str(2), text.Yellow + 'Order simulation via Middleware')
        print(text.default_text_color + str(3), text.Yellow + 'POC information')
        print(text.default_text_color + str(4), text.Yellow + 'Product information')
        print(text.default_text_color + str(5), text.Yellow + 'Deals information by account')
        print(text.default_text_color + str(6), text.Yellow + 'Order information by account')
        print(text.default_text_color + str(7), text.Yellow + 'Recommender information by account')
        selection = input(text.default_text_color + '\nPlease select: ')
        while validate_option_request_selection(selection) == 'false':
            print(text.Red + '\n- Invalid option\n')
            print(text.default_text_color + str(0), text.Yellow + 'Close application')
            print(text.default_text_color + str(1), text.Yellow + 'Order simulation via Microservice')
            print(text.default_text_color + str(2), text.Yellow + 'Order simulation via Middleware')
            print(text.default_text_color + str(3), text.Yellow + 'POC information')
            print(text.default_text_color + str(4), text.Yellow + 'Product information')
            print(text.default_text_color + str(5), text.Yellow + 'Deals information')
            print(text.default_text_color + str(6), text.Yellow + 'Order information by account')
            print(text.default_text_color + str(7), text.Yellow + 'Recommender information by account')
            selection = input(text.default_text_color + '\nPlease select: ')

    elif selection_structure == '3':
        print(text.default_text_color + str(0), text.Yellow + 'Close application')
        print(text.default_text_color + str(1), text.Yellow + 'Create User')
        print(text.default_text_color + str(2), text.Yellow + 'Create User IAM')
        print(text.default_text_color + str(3), text.Yellow + 'Associate Account to user')
        print(text.default_text_color + str(4), text.Yellow + 'List Categories')
        print(text.default_text_color + str(5), text.Yellow + 'Associate Product to category')
        print(text.default_text_color + str(6), text.Yellow + 'Create Category')

        selection = input(text.default_text_color + '\nPlease select: ')
        while validate_option_request_selection(selection) == 'false':
            print(text.Red + '\n- Invalid option\n')
            print(text.default_text_color + str(0), text.Yellow + 'Close application')
            print(text.default_text_color + str(1), text.Yellow + 'Create User')
            print(text.default_text_color + str(2), text.Yellow + 'Create User IAM')
            print(text.default_text_color + str(3), text.Yellow + 'Associate Account to user')
            print(text.default_text_color + str(4), text.Yellow + 'List Categories')
            print(text.default_text_color + str(5), text.Yellow + 'Associate Product to category')
            print(text.default_text_color + str(6), text.Yellow + 'Create Category')

            selection = input(text.default_text_color + '\nPlease select: ')
    else:
        finishApplication()

    return selection


# Print welcome menu
def printWelcomeScript():
    print(text.BackgroundLightYellow + text.Bold + text.Black)
    print("╭──────────────────────────────────╮")
    print("│ 🝝                               │")
    print("│   ANTARCTICA AUTOMATION SCRIPT   │")
    print("│                               🝝 │")
    print("╰──────────────────────────────────╯")
    print(text.BackgroundDefault + text.ResetBold + text.default_text_color + "\n")


# Print structure menu
def print_structure_menu():
    print(text.default_text_color + str(1), text.Yellow + 'Data creation - Microservice')
    print(text.default_text_color + str(2), text.Yellow + 'Data searching - Microservice/MDW')
    print(text.default_text_color + str(3), text.Yellow + 'Data creation - Magento')
    print(text.default_text_color + str(4), text.Yellow + 'Close application')

    structure = input(text.default_text_color + '\nChoose which backend you want to run a service for: ')
    while validateStructure(structure) == 'false':
        print(text.Red + '\n- Invalid option\n')
        print(text.default_text_color + str(1), text.Yellow + 'Data creation - Microservice')
        print(text.default_text_color + str(2), text.Yellow + 'Data searching - Microservice/MDW')
        print(text.default_text_color + str(3), text.Yellow + 'Data creation - Magento')
        print(text.default_text_color + str(4), text.Yellow + 'Close application')
        structure = input(text.default_text_color + '\nChoose which backend you want to run a service for: ')

    return structure


# Print rewards menu
def print_rewards_menu():
    print(text.default_text_color + str(1), text.Yellow + 'Create new program')
    print(text.default_text_color + str(2), text.Yellow + 'Update Balance of a Program')
    print(text.default_text_color + str(3), text.Yellow + 'Enroll POC to a Reward program')
    print(text.default_text_color + str(4), text.Yellow + 'Input Challenges to Zone')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_rewards(structure) == 'false':
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + str(1), text.Yellow + 'Create new program')
        print(text.default_text_color + str(2), text.Yellow + 'Update Balance of a Program')
        print(text.default_text_color + str(3), text.Yellow + 'Enroll POC to a Reward program')
        print(text.default_text_color + str(4), text.Yellow + 'Input Challenges to Zone')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure


# Print orders menu
def print_orders_menu():
    print(text.default_text_color + '\nWhich type of order do you want to create?')
    print(text.default_text_color + str(1), text.Yellow + 'Input Active Order')
    print(text.default_text_color + str(2), text.Yellow + 'Input Cancelled Order')
    print(text.default_text_color + str(3), text.Yellow + 'Input Changed Order')
    print(text.default_text_color + str(4), text.Yellow + 'Input Delivered Order')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_orders(structure) == 'false':
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nWhich type of order do you want to create?')
        print(text.default_text_color + str(1), text.Yellow + 'Input Active Order')
        print(text.default_text_color + str(2), text.Yellow + 'Input Cancelled Order')
        print(text.default_text_color + str(3), text.Yellow + 'Input Changed Order')
        print(text.default_text_color + str(4), text.Yellow + 'Input Delivered Order')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure


# Print deals menu
def print_deals_menu():
    print(text.default_text_color + "\nWhich type of deal do you want to create?")
    print(text.default_text_color + str(1), text.Yellow + "Input deal type discount")
    print(text.default_text_color + str(2), text.Yellow + "Input deal type stepped discount")
    print(text.default_text_color + str(3), text.Yellow + "Input deal type free good")
    print(text.default_text_color + str(4), text.Yellow + "Input deal type stepped free good")
    print(text.default_text_color + str(5), text.Yellow + "Input deal type stepped discount with quantity")
    structure = input(text.default_text_color + "\nPlease select: ")
    while validate_deals(structure) == 'false':
        print(text.Red + "\n- Invalid option")
        print(text.default_text_color + "\nWhich type of deal do you want to create?")
        print(text.default_text_color + str(1), text.Yellow + "Input deal type discount")
        print(text.default_text_color + str(2), text.Yellow + "Input deal type stepped discount")
        print(text.default_text_color + str(3), text.Yellow + "Input deal type free good")
        print(text.default_text_color + str(4), text.Yellow + "Input deal type stepped free good")
        print(text.default_text_color + str(5), text.Yellow + "Input deal type stepped discount with quantity")
        structure = input(text.default_text_color + "\nPlease select: ")

    return structure


# Print combos menu
def print_combos_menu():
    print(text.default_text_color + '\nWhich type of combo do you want to create?')
    print(text.default_text_color + str(1), text.Yellow + 'Input combo type discount')
    print(text.default_text_color + str(2), text.Yellow + 'Input combo type free good')
    print(text.default_text_color + str(3), text.Yellow + 'Input combo with only free goods')
    print(text.default_text_color + str(4), text.Yellow + 'Reset combo consumption to zero')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_combo_structure(structure) == 'false':
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nWhich type of combo do you want to create?')
        print(text.default_text_color + str(1), text.Yellow + 'Input combo type discount')
        print(text.default_text_color + str(2), text.Yellow + 'Input combo type free good')
        print(text.default_text_color + str(3), text.Yellow + 'Input combo with only free goods')
        print(text.default_text_color + str(4), text.Yellow + 'Reset combo consumption to zero')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure


# Validate combo type structure
def validate_combo_structure(option):
    if option == '1' or option == '2' or option == '3' or option == '4':
        return 'true'
    else:
        return 'false'


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
def print_discount_value_menu(discount_type):
    if discount_type == 'percentOff':
        while True:
            try:
                discount_value = float(input(text.default_text_color + 'Discount percentage (%): '))
                break
            except ValueError:
                print(text.Red + '\n- Invalid value')
    else:
        while True:
            try:
                discount_value = float(input(text.default_text_color + 'Discount amount: '))
                break
            except ValueError:
                print(text.Red + '\n- Invalid value')

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
def print_quantity_range_menu():
    index_list = list()

    for x in range(2):
        quantity_value = input(text.default_text_color + 'SKU quantity for index #' + str(x) + ': ')
        while quantity_value == '' or int(quantity_value) <= 0:
            print(text.Red + '\n- SKU quantity must be greater than 0')
            quantity_value = input(text.default_text_color + '\nSKU quantity for index #' + str(x) + ': ')

        index_list.append(quantity_value)

    return index_list


# Print minimum quantity menu
def print_minimum_quantity_menu():
    minimum_quantity = input(text.default_text_color + 'Desired quantity needed to buy to get a discount/free good: ')
    while minimum_quantity == '' or int(minimum_quantity) <= 0:
        print(text.Red + '\n- Minimum quantity must be greater than 0')
        minimum_quantity = input(text.default_text_color + 'Desired quantity needed to buy to get a discount/free '
                                                           'good: ')

    return minimum_quantity


# Print quantity menu
def print_quantity_menu():
    quantity = input(text.default_text_color + 'Desired quantity of free goods to offer: ')
    while quantity == '' or int(quantity) <= 0:
        print(text.Red + '\n- SKU quantity must be greater than 0')
        quantity = input(text.default_text_color + 'Desired quantity of free goods to offer: ')

    return quantity


def print_account_id_menu_create_account(zone):
    abi_id = input(text.default_text_color + 'Account ID: ')
    attempt = 0
    while validate_account(str(abi_id), zone) != 'true' and attempt < 3:
        if validate_account(str(abi_id), zone) == 'error_0':
            print(text.Red + '\n- Account ID should not be empty')
            abi_id = input(text.default_text_color + 'Account ID: ')
        if validate_account(str(abi_id), zone) == 'error_10':
            print(text.Red + '\n- Account ID must contain at least 10 characters')
            abi_id = input(text.default_text_color + 'Account ID: ')
        elif validate_account(str(abi_id), zone) == 'not_number':
            print(text.Red + '\n- The account ID must be Numeric')
            abi_id = input(text.default_text_color + 'Account ID: ')
        attempt = attempt + 1
    if attempt >= 3:
        return 'false'
    else:
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


def print_zone_menu_data_searching_deals():
    zone = input(text.default_text_color + 'Zone (AR, BR, CL, CO, DO): ')
    while validate_zone_data_searching_deals(zone.upper()) == 'false':
        print(text.Red + '\n- Invalid option\n')
        zone = input(text.default_text_color + 'Zone (AR, BR, CL, CO, DO): ')

    return zone.upper()


# Print zone menu for Delivery Window
def print_zone_menu_for_delivery_window():
    zone = input(text.default_text_color + 'Zone (AR, CL, BR, DO, ZA, CO, MX): ')
    while validate_zone_for_delivery_window(zone.upper()) == 'false':
        print(text.Red + '\n- Invalid option\n')
        zone = input(text.default_text_color + 'Zone (AR, CL, BR, DO, ZA, CO, MX): ')

    return zone.upper()


# Print zone menu for Microservice
def print_zone_menu_for_ms():
    zone = input(text.default_text_color + 'Zone (AR, BR, DO, ZA, CO, MX): ')
    while validate_zone_for_ms(zone.upper()) == 'false':
        print(text.Red + '\n- Invalid option\n')
        zone = input(text.default_text_color + 'Zone (AR, BR, DO, ZA, CO, MX): ')

    return zone.upper()


# Print zone menu for rewards
def print_zone_menu_for_rewards():
    zone = input(text.default_text_color + 'Zone (BR, DO, CO, AR, ZA): ')
    while validate_zone_for_rewards(zone.upper()) == 'false':
        print(text.Red + '\n- Invalid option\n')
        zone = input(text.default_text_color + 'Zone (BR, DO, CO, AR, ZA): ')

    return zone.upper()


# Print zone menu for inventory
def print_zone_menu_for_inventory():
    zone = input(text.default_text_color + "Zone (AR, ZA, CO, MX): ")
    while validate_zone_for_inventory(zone.upper()) == "false":
        print(text.Red + "\n- Invalid option\n")
        zone = input(text.default_text_color + "Zone (AR, ZA, CO, MX): ")

    return zone.upper()


# Print zone menu for deals
def print_zone_menu_for_deals():
    zone = input(text.default_text_color + 'Zone (AR, BR, CO, DO, MX, ZA): ')
    while validate_zone_for_deals(zone.upper()) == 'false':
        print(text.Red + '\n- Invalid option\n')
        zone = input(text.default_text_color + 'Zone (AR, BR, CO, DO, MX, ZA): ')

    return zone.upper()


# Print zone menu for combos
def print_zone_menu_for_combos():
    zone = input(text.default_text_color + 'Zone (BR, DO): ')
    while validate_zone_for_combos(zone.upper()) == 'false':
        print(text.Red + '\n- Invalid option\n')
        zone = input(text.default_text_color + 'Zone (BR, DO): ')

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
    environment = input(text.default_text_color + 'Environment (DEV, SIT, UAT): ')
    while validateEnvironment(environment.upper()) == 'false':
        print(text.Red + '\n- Invalid option')
        environment = input(text.default_text_color + 'Environment (DEV, SIT, UAT): ')

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
    payment_cash = ['CASH']

    if zone == 'BR':
        payment_method = input(text.default_text_color + 'Choose the payment method (1. CASH / 2. BANK SLIP / 3. CASH, BANK SLIP): ')
        while validate_payments_method(payment_method, zone) != 'true':
            if validate_payments_method(payment_method, zone) == 'error_0':
                print(text.Red + '\n- Payments Method should not be empty')
                payment_method = input(text.default_text_color + 'Choose the payment method (1. CASH / 2. BANK SLIP / 3. CASH, BANK SLIP): ')
            elif validate_payments_method(payment_method, zone) == 'not_number':
                print(text.Red + '\n- Payments Method should be numeric')
                payment_method = input(text.default_text_color + 'Choose the payment method (1. CASH / 2. BANK SLIP / 3. CASH, BANK SLIP): ')
            elif validate_payments_method(payment_method, zone) == 'not_payments_method':
                print(text.Red + '\n- Payments Method should be 1, 2 or 3')
                payment_method = input(text.default_text_color + 'Choose the payment method (1. CASH / 2. BANK SLIP / 3. CASH, BANK SLIP): ')

        payment_credit = ['BANK_SLIP']
        payment_list = ['CASH', 'BANK_SLIP']

        switcher = {
            '1': payment_cash,
            '2': payment_credit,
            '3': payment_list
        }

        value = switcher.get(payment_method, 'false')
        return value

    elif zone == 'DO' or zone == 'CO':
        payment_method = input(text.default_text_color + 'Choose the payment method (1. CASH / 2. CREDIT / 3. CASH, CREDIT): ')
        while validate_payments_method(payment_method, zone) != 'true':
            if validate_payments_method(payment_method, zone) == 'error_0':
                print(text.Red + '\n- Payments Method should not be empty')
                payment_method = input(
                    text.default_text_color + 'Choose the payment method (1. CASH / 2. CREDIT / 3. CASH, CREDIT): ')
            elif validate_payments_method(payment_method, zone) == 'not_number':
                print(text.Red + '\n- Payments Method should be numeric')
                payment_method = input(
                    text.default_text_color + 'Choose the payment method (1. CASH / 2. CREDIT / 3. CASH, CREDIT): ')
            elif validate_payments_method(payment_method, zone) == 'not_payments_method':
                print(text.Red + '\n- Payments Method should be 1, 2 or 3')
                payment_method = input(
                    text.default_text_color + 'Choose the payment method (1. CASH / 2. CREDIT / 3. CASH, CREDIT): ')

        payment_credit = ['CREDIT']
        payment_list = ['CASH', 'CREDIT']

        switcher = {
            '1': payment_cash,
            '2': payment_credit,
            '3': payment_list
        }

        value = switcher.get(payment_method, 'false')
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

    listDeliveryWindowDates.append({'startDate': startDeliveryDate, 'endDate': endDeliveryDate})

    return listDeliveryWindowDates


def printMinimumOrderMenu():
    option_type = input(text.default_text_color + 'Minimum order type (1. Poduct quantity / 2. Order volume / 3. Order total): ')
    while option_type == '' or (int(option_type) != 1 and int(option_type) != 2 and int(option_type) != 3):
        print(text.Red + '\n- Invalid option\n')
        option_type = input(
            text.default_text_color + 'Minimum order type (1. Poduct quantity / 2. Order volume / 3. Order total): ')

    switcher = {
        '1': 'PRODUCT_QUANTITY',
        '2': 'ORDER_VOLUME',
        '3': 'ORDER_TOTAL'
    }

    minimum_order_type = switcher.get(option_type, 'false')

    option_value = input(text.default_text_color + 'Minimum order value: ')
    while option_value == '' or int(option_value) <= 0:
        print(text.Red + '\n- SKU quantity must be greater than 0\n')
        option_value = input(text.default_text_color + 'Minimum order value: ')

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
    if zone == 'BR':
        state = 'RS'

    elif zone == 'DO':
        state = 'STO DGO'

    elif zone == 'ZA':
        state = 'Free State'

    elif zone == 'CO':
        state = 'San Alberto'

    elif zone == 'MX':
        state = 'Cidade do México'

    elif zone == 'AR':
        state = 'Corrientes'

    elif zone == 'CL':
        state = 'Los Lagos'

    return state


# Validate the option to finish application
def validate_yes_no_option(option):
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


def is_blank(str):
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

def print_input_number_with_default(input_text, default_value = 0):
    """Validate input number with default value"""
    while(True):
        input_number = input("{default_text_color}{input_text} - [default: {default_value}]: ".format(
            default_text_color=text.default_text_color,
            input_text=input_text, default_value=default_value)).strip() or str(default_value)

        if input_number.lstrip("-").isdigit():
            return int(input_number)


def print_input_number(input_text):
    """Validate input number"""
    while(True):
        input_number = input("{default_text_color}{input_text}: ".format(
            default_text_color=text.default_text_color,
            input_text=input_text)).strip()

        if input_number.lstrip("-").isdigit():
            return int(input_number)


def print_input_text(input_text):
    """Validate input text"""
    while(True):
        input_str = input("{default_text_color}{input_text}: ".format(
            default_text_color=text.default_text_color,
            input_text=input_text)).strip()

        if not is_blank(input_str):
            return input_str


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
def print_zone_simulation_menu(is_middleware='true'):
    if is_middleware == 'true':
        zone = input(text.default_text_color + 'Zone (CL): ')
        while validateZone('true', zone.upper()) == 'false':
            print(text.Red + '\n- Invalid option\n')
            zone = input(text.default_text_color + 'Zone (CL): ')
    else:
        zone = input(text.default_text_color + 'Zone (AR, ZA, DO, BR, CO, MX): ')
        while validateZone('false', zone.upper()) == 'false':
            print(text.Red + '\n- Invalid option\n')
            zone = input(text.default_text_color + 'Zone (AR, ZA, DO, BR, CO, MX): ')

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
    if zone == 'BR':
        payment_choice = input(text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - BANK_SLIP ')
        while payment_choice != '1' and payment_choice != '2':
            print(text.Red + '\n- Invalid option\n')
            payment_choice = input(text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - BANK_SLIP ')

        if payment_choice == '1':
            payment_method = 'CASH'
        else:
            payment_method = 'BANK_SLIP'

    elif zone == 'DO' and zone == 'CO':
        payment_choice = input(text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - CREDIT ')
        while payment_choice != '1' and payment_choice != '2':
            print(text.Red + '\n- Invalid option\n')
            payment_choice = input(text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - CREDIT ')

        if payment_choice == '1':
            payment_method = 'CASH'
        else:
            payment_method = 'CREDIT'
    else:
        payment_method = 'CASH'

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
        temp_index = temp_index + 1
        list_term_periods = {
            'days': temp_index
        }

        term_periods.append(list_term_periods)

    list_payment_term = {
        'type': 'BANK_SLIP',
        'termPeriods': term_periods
    }

    payment_term.append(list_payment_term)
    return payment_term


def set_to_dictionary(dictionary, *key_value_pairs, **items):
    """Adds the given ``key_value_pairs`` and ``items`` to the ``dictionary``.
    Giving items as ``key_value_pairs`` means giving keys and values
    as separate arguments:
    | Set To Dictionary | ${D1} | key | value | second | ${2} |
    =>
    | ${D1} = {'a': 1, 'key': 'value', 'second': 2}
    | Set To Dictionary | ${D1} | key=value | second=${2} |
    The latter syntax is typically more convenient to use, but it has
    a limitation that keys must be strings.
    If given keys already exist in the dictionary, their values are updated.
    """

    if len(key_value_pairs) % 2 != 0:
        raise ValueError('Adding data to a dictionary failed. There '
                         'should be even number of key-value-pairs.')
    for i in range(0, len(key_value_pairs), 2):
        dictionary[key_value_pairs[i]] = key_value_pairs[i + 1]
    dictionary.update(items)
    return dictionary


def print_order_id_menu():
    order_id = input(text.default_text_color + 'Order ID: ')

    while True:
        size_order_id = len(order_id)
        if size_order_id == 0:
            print(text.Red + '\n- Order ID should not be empty')
        elif size_order_id != 0:
            break
        order_id = input(text.default_text_color + 'Order ID: ')
    return order_id


def print_recommendation_type_menu():
    print(text.default_text_color + '\nWhich recommendation use case do you want to add?')
    print(text.default_text_color + str(1), text.Yellow + 'Quick order')
    print(text.default_text_color + str(2), text.Yellow + 'Up sell')
    print(text.default_text_color + str(3), text.Yellow + 'Forgotten items')
    print(text.default_text_color + str(4), text.Yellow + 'Standard recommendations (all use cases)')
    option = input(text.default_text_color + '\nPlease select: ')
    while validate_recommendation_type(option) == 'false':
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nWhich recommendation use case do you want to add?')
        print(text.default_text_color + str(1), text.Yellow + 'Quick order')
        print(text.default_text_color + str(2), text.Yellow + 'Up sell')
        print(text.default_text_color + str(3), text.Yellow + 'Forgotten items')
        print(text.default_text_color + str(4), text.Yellow + 'Standard recommendations (all use cases)')
        option = input(text.default_text_color + '\nPlease select: ')

    switcher = {
        '1': 'QUICK_ORDER',
        '2': 'CROSS_SELL_UP_SELL',
        '3': 'FORGOTTEN_ITEMS',
        '4': 'ALL'
    }

    recommendation_type = switcher.get(option, 'false')

    return recommendation_type


def check_if_order_exists(abi_id, zone, environment, order_id):
    # Get header request
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/order-service/v1?orderIds=' + order_id + '&accountId=' + abi_id

    # Place request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        if order_id == '':
            print(text.Red + '\n- [Order Service] The account ' + abi_id + ' does not have orders')
        else:
            print(text.Red + '\n- [Order Service] The order ' + order_id + ' does not exist')
        return 'false'
    else:
        print(text.Red + '\n- [Order Service] Failure to retrieve order information. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


# Validate account sub-menus
def validate_accounts(option):
    if option == '1' or option == '2':
        return 'true'
    else:
        return 'false'


# Validate order sub-menus
def validate_order_sub_menu(option):
    if option == '1' or option == '2':
        return 'true'
    else:
        return 'false'


def print_get_account_menu():
    print(text.default_text_color + '\nWhich option to retrieve account do you want?')
    print(text.default_text_color + str(1), text.Yellow + 'All information from one account')
    print(text.default_text_color + str(2), text.Yellow + 'All accounts active in the zone')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_accounts(structure) == 'false':
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nWhich option to retrieve account do you want?')
        print(text.default_text_color + str(1), text.Yellow + 'All information from one account')
        print(text.default_text_color + str(2), text.Yellow + 'All accounts active in the zone')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure


def validate_get_products(option):
    if option == '1' or option == '2' or option == '3':
        return 'true'
    else:
        return 'false'


def print_get_products_menu():
    print(text.default_text_color + '\nWhich option to retrieve products information do you want?')
    print(text.default_text_color + str(1), text.Yellow + 'Products information by account')
    print(text.default_text_color + str(2), text.Yellow + 'Products inventory information by account')
    print(text.default_text_color + str(3), text.Yellow + 'Products information by zone')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_get_products(structure) == 'false':
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nWhich option to retrieve products information do you want?')
        print(text.default_text_color + str(1), text.Yellow + 'Products information by account')
        print(text.default_text_color + str(2), text.Yellow + 'Products inventory information by account')
        print(text.default_text_color + str(3), text.Yellow + 'Products information by zone')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure


def print_get_order_menu():
    print(text.default_text_color + '\nWhich option to retrieve orders do you want?')
    print(text.default_text_color + str(1), text.Yellow + 'Specific order information by account')
    print(text.default_text_color + str(2), text.Yellow + 'All order information by account')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_order_sub_menu(structure) == 'false':
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nWhich option to retrieve orders do you want?')
        print(text.default_text_color + str(1), text.Yellow + 'Specific order information by account')
        print(text.default_text_color + str(2), text.Yellow + 'All order information by account')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure


def validate_invoice_status(option):
    if option == '1' or option == '2':
        return 'true'
    else:
        return 'false'


def invoice_status_menu():
    status = input(
        text.default_text_color + 'Do you want to create the invoice with which status: 1. CLOSED or 2. OPEN: ')
    while validate_invoice_status(status) == 'false':
        print(text.Red + '\n- Invalid option')
        status = input(
            text.default_text_color + 'Do you want to create the invoice with which status: 1. CLOSED or 2. OPEN: ')
    if status == '1':
        return 'CLOSED'
    else:
        return 'OPEN'


def print_combo_id_menu():
    combo_id = input(text.default_text_color + 'Combo ID: ')

    while len(combo_id) == 0:
        print(text.Red + '\n- Combo ID should not be empty')
        combo_id = input(text.default_text_color + 'Combo ID: ')
    return combo_id


def validate_option_sku(option):
    if option == '1' or option == '2':
        return 'true'
    else:
        return 'false'


def print_option_sku(zone):
    if zone == 'DO':
        option = input(text.default_text_color + 'Do you want to input this type of deal to a specific SKU (1. YES or 2. NO): ')

        while validate_option_sku(option) != 'true':
            print(text.Red + '\n- Invalid option')
            option = input(
                text.default_text_color + 'Do you want to input this type of deal to a specific SKU (1. YES or 2. NO): ')
        return option


def check_account_exists_microservice(abi_id, zone, environment):
    # Get header request
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/accounts?accountId=' + abi_id

    # Place request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        return json_data
    else:
        print(
            text.Red + '\n- [Account Relay Service] Failure to found the account. Response Status: '
            + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def validate_if_account_exist(account_id, zone, environment):
    account = check_account_exists_microservice(account_id, zone, environment)
    if account == 'false':
        return 'error_api'
    elif len(account) == 0:
        return 'not_exist'
    elif len(account) != 0:
        return 'true'


def print_account_id_menu(zone, environment):
    abi_id = input(text.default_text_color + 'Account ID: ')
    attempt = 0
    while validate_account(str(abi_id), zone) != 'true' and attempt < 3 \
            or validate_if_account_exist(abi_id, zone, environment) != 'true':
        attempt = attempt + 1
        if validate_account(str(abi_id), zone) == 'error_0':
            print(text.Red + '\n- Account ID should not be empty')
            if attempt >= 3:
                return 'false'
            else:
                abi_id = input(text.default_text_color + 'Account ID: ')
        elif validate_account(str(abi_id), zone) == 'error_10':
            print(text.Red + '\n- Account ID must contain at least 10 characters')
            if attempt >= 3:
                return 'false'
            else:
                abi_id = input(text.default_text_color + 'Account ID: ')
        elif validate_account(str(abi_id), zone) == 'not_number':
            print(text.Red + '\n- The account ID must be Numeric')
            if attempt >= 3:
                return 'false'
            else:
                abi_id = input(text.default_text_color + 'Account ID: ')
        elif validate_if_account_exist(abi_id, zone, environment) == 'not_exist':
            print(text.Red + '\n- The account ID not exist')
            if attempt >= 3:
                return 'false'
            else:
                abi_id = input(text.default_text_color + 'Account ID: ')

        elif validate_if_account_exist(abi_id, zone, environment) == 'error_api':
            if attempt >= 3:
                return 'false'
            else:
                abi_id = input(text.default_text_color + 'Account ID: ')
    return str(abi_id)
