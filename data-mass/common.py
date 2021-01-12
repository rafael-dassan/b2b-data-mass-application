# Standard library imports
import json
import os
import sys
from datetime import date
import time as t
from time import time
from uuid import uuid1

# Third party imports
from jsonpath_rw import Index, Fields
from jsonpath_rw_ext import parse
from requests import request
from tabulate import tabulate
import jwt

# Local application imports
from classes.text import text
from logs.log import log_to_file
from validations import is_number, validate_zone_for_ms, validate_environment, \
    validate_structure, validate_rewards, validate_zone_for_interactive_combos_ms, \
    validate_option_request_selection


# Validate option menu selection
def validate_option_request_selection_for_structure_2(option):
    switcher = {
        '0': 'true',
        '1': 'true',
        '2': 'true'
    }

    value = switcher.get(option, 'false')
    return value


# Validate Country in User creation
def validateCountryInUserCreation(country):
    switcher = {
        "AR": "true",
        "BR": "true",
        "CO": "true",
        "DO": "true",
        "MX": "true",
        "ZA": "true"
    }

    value = switcher.get(country, "false")
    return value


def validate_zone_for_inventory(zone):
    switcher = {
        'ZA': 'true',
        'CO': 'true',
        'MX': 'true',
        'AR': 'true',
        'PE': 'true',
        'EC': 'true'
    }

    value = switcher.get(zone, 'false')
    return value


def validate_zone_for_combos(zone):
    switcher = {
        'BR': 'true',
        'DO': 'true',
        'MX': 'true'
    }

    value = switcher.get(zone, 'false')
    return value


def validate_zone_for_combos_dt(zone):
    switcher = {
        'BR': 'true',
        'DO': 'true',
        'AR': 'true',
        'CO': 'true',
        'ZA': 'true',
        'MX': 'true',
        'PE': 'true',
        'EC': 'true'
    }

    value = switcher.get(zone, 'false')
    return value


# Validate environment to User creation
def validateEnvironmentInUserCreation(environment):
    switcher = {
        'DT': 'true',
        'SIT': 'true',
        'UAT': 'true'
    }
    
    return switcher.get(environment, 'false')


# Place generic request
def place_request(request_method, request_url, request_body, request_headers):
    # Send request
    response = request(
        request_method,
        request_url,
        data=request_body,
        headers=request_headers
    )

    log_to_file(request_method, request_url, request_body, request_headers, response.status_code, response.text)

    return response


# Return JWT header request
def get_header_request(header_country, use_jwt_auth='false', use_root_auth='false', use_inclusion_auth='false',
                       sku_product='false', account_id=None):

    switcher = {
        'ZA': 'UTC',
        'AR': 'America/Buenos_Aires',
        'DO': 'America/Santo_Domingo',
        'BR': 'America/Sao_Paulo',
        'CO': 'America/Bogota',
        'PE': 'America/Lima',
        'EC': 'America/Guayaquil',
        'MX': 'UTC'
    }
    timezone = switcher.get(header_country.upper(), 'false')

    header = {
        'User-Agent': 'BEES - Data Mass App',
        'Content-Type': 'application/json',
        'country': header_country.upper(),
        'requestTraceId': str(uuid1()),
        'x-timestamp': str(int(round(time() * 1000))),
        'cache-control': 'no-cache',
        'timezone': timezone
    }

    if use_jwt_auth == 'true':
        header['Authorization'] = generate_hmac_jwt(account_id)
    elif use_root_auth == 'true':
        header['Authorization'] = 'Basic cm9vdDpyb290'
    elif use_inclusion_auth == 'true':
        header['Authorization'] = 'Basic cmVsYXk6TVVRd3JENVplSEtB'
    else:
        header['Authorization'] = 'Basic cmVsYXk6cmVsYXk='

    if sku_product != 'false':
        header['skuId'] = sku_product

    return header


# Return base URL for Microservice
def get_microservice_base_url(environment, is_v1='true'):
    if environment == 'DEV':
        if is_v1 == 'true':
            return 'https://bees-services-dev.eastus2.cloudapp.azure.com/v1'
        else:
            return 'https://bees-services-dev.eastus2.cloudapp.azure.com/api'
    else:
        env_name = 'SIT' if (environment != 'SIT' and environment != 'UAT') else environment
        context = '/v1' if (is_v1 == 'true') else '/api'
        return 'https://services-' + env_name.lower() + '.bees-platform.dev' + context


# Return base URL for Magento
def get_magento_base_url(environment, country):
    magento_url = {
        'DT': {
            'AR': 'https://qa-dt-las-ar.abi-sandbox.net/',
            'BR': 'https://qa-dt-br.abi-sandbox.net',
            'CO': 'https://qa-dt-copec-co.abi-sandbox.net',
            'DO': 'https://qa-dt-dr.abi-sandbox.net',
            'MX': 'https://qa-dt-mx.abi-sandbox.net',
            'ZA': 'https://qa-dt-za.abi-sandbox.net'
        },
        'SIT': {
            'AR': 'https://ar.sit.bees-platform.dev',
            'BR': 'https://br.sit.bees-platform.dev',
            'CO': 'https://co.sit.bees-platform.dev',
            'DO': 'https://do.sit.bees-platform.dev',
            'EC': 'https://ec.sit.bees-platform.dev',
            'MX': 'https://mx.sit.bees-platform.dev',
            'PE': 'https://pe.sit.bees-platform.dev',
            'ZA': 'https://za.sit.bees-platform.dev'
        },
        'UAT': {
            'AR': 'https://ar.uat.bees-platform.dev',
            'BR': 'https://br.uat.bees-platform.dev',
            'CO': 'https://co.uat.bees-platform.dev',
            'DO': 'https://do.uat.bees-platform.dev',
            'EC': 'https://ec.uat.bees-platform.dev',
            'MX': 'https://mx.uat.bees-platform.dev',
            'PE': 'https://pe.uat.bees-platform.dev',
            'ZA': 'https://za.uat.bees-platform.dev'
        }
    }

    return magento_url.get(environment).get(country)


def get_region_id(country):
    region_id = {
        'BR': 'PT_BR',
        'DO': 'ES_DO',
        'AR': 'ES_AR',
        'ZA': 'EN_ZA',
        'CO': 'ES_CO'
    }
    return region_id.get(country)


# Returns Magento User Registration Integration Access Token
def get_magento_user_registration_access_token(environment, country):
    access_token = {
        'DT': {
            'AR': '0pj40segd3h67zjn68z9oj18xyx5yib8',
            'BR': 'qq8t0w0tvz7nbn4gxo5jh9u62gohvjrw',
            'CO': '2z0re32n00z159oui0az2j2dr42bx8m5',
            'DO': '56jqtzzto7tw9uox8nr3eckoeup53dt2',
            'MX': '40qrmhwv93ixeysxsw5hxrvjn6dstdim',
            'ZA': 'y4u1xqitth7k8y50ei5nlfm538sblk6j'
        },
        'SIT': {
            'AR': '30lqki06nbdegugcmdb0ttm9yppnmoec',
            'BR': 'qq8t0w0tvz7nbn4gxo5jh9u62gohvjrw',
            'CO': 'walt5dp3keiq2du0f30kir21v13f3u0v',
            'DO': '56jqtzzto7tw9uox8nr3eckoeup53dt2',
            'EC': 'kyhzpszn0bswbf17mlb409ldg14j58uv',
            'MX': 'w0mi88cajh0jbq0zrive3ht4eywc8xlm',
            'PE': 'hwv67q9d3zyy2u500n2x0r5g7mr2j5is',
            'ZA': 'nmvvuk58lc425a7p5l55orrkgh0jprr2'
        },
        'UAT': {
            'AR': '30lqki06nbdegugcmdb0ttm9yppnmoec',
            'BR': 'qq8t0w0tvz7nbn4gxo5jh9u62gohvjrw',
            'CO': '8mh6b9b6ft6m1cr5k7zm2jh4aljq4slx',
            'DO': '56jqtzzto7tw9uox8nr3eckoeup53dt2',
            'EC': 'awtm7d9as0n9k1o5zi9fi90rtukxdmqh',
            'MX': 'kcsn7y80vvo2by9fluw2vq4r2a6pucfs',
            'PE': '4z0crqq6yb6t5mip43i63tgntdll09vc',
            'ZA': '31pdb0yht5kn3eld7gum021f6k984jh9'
        }
    }

    return access_token.get(environment).get(country)


# Returns Magento Datamass Application Access Token
def get_magento_datamass_access_token(environment, country):
    access_token = {
        'UAT': {
            'BR': '8z2z3y523hoqkcqci8q58afuoue81bns',
            'DO': 'js4gd8y9wkqogf7eo2s4uy6oys15lfkf',
            'AR': 'a34o213zgisn67efeg0zbq04sqg667qk',
            'ZA': '0seca4btewbr3e1opma4je2x8ftj57wx',
            'CO': 'meqei3q5ztreebdpb5vyej378mt2o8qy',
            'MX': 'bqzqcmx3opvntxtwijh98s4kmb21pi8j',
            'EC': 'w9pphbvskd35206otky7cv1dobn0p1yb',
            'PE': 'xcgb5m0rl5pto116q4gxe1msd3zselq6'
        },
        'SIT': {
            'BR': 'q6yti2dxmhp0e2xjgyvtt72nziss6ptp',
            'DO': 'tgqnjlqpfupf0i4zxcs2doqx409k1hyq',
            'AR': 'hzp6hw65oqiyeyv8ozfzunex0nc1rff8',
            'ZA': 'fde80w10jbbaed1mrz6yg0pwy1vzfo48',
            'CO': 'new189lnml9xmcr3m9gc0j6oji6w2izr',
            'MX': '86pg36lug4ivrx3xh5b5qnemzy1gw6v8',
            'EC': 'ybyiars1mhm5e4jyaq94s5csj1e77knp',
            'PE': 'lda0mjri507oqrm8xfofk6weifajn8cm'
        }
    }

    return access_token.get(environment).get(country)

# Clear terminal
def clear_terminal():
    os.system('clear')


# Kill application
def finish_application():
    sys.exit()


# Print init menu
def print_available_options(selection_structure):
    if selection_structure == '1':
        print(text.default_text_color + str(0), text.Yellow + 'Close application')
        print(text.default_text_color + str(1), text.Yellow + 'Account')
        print(text.default_text_color + str(2), text.Yellow + 'Product')
        print(text.default_text_color + str(3), text.Yellow + 'Orders')
        print(text.default_text_color + str(4), text.Yellow + 'Deals')
        print(text.default_text_color + str(5), text.Yellow + 'Input combos')
        print(text.default_text_color + str(6), text.Yellow + 'Invoice')
        print(text.default_text_color + str(7), text.Yellow + 'Create rewards')
        print(text.default_text_color + str(8), text.Yellow + 'Create credit statement')
        selection = input(text.default_text_color + '\nPlease select: ')
        while validate_option_request_selection(selection) == 'false':
            print(text.Red + '\n- Invalid option\n')
            print(text.default_text_color + str(0), text.Yellow + 'Close application')
            print(text.default_text_color + str(1), text.Yellow + 'Account')
            print(text.default_text_color + str(2), text.Yellow + 'Product')
            print(text.default_text_color + str(3), text.Yellow + 'Orders')
            print(text.default_text_color + str(4), text.Yellow + 'Deals')
            print(text.default_text_color + str(5), text.Yellow + 'Input combos')
            print(text.default_text_color + str(6), text.Yellow + 'Invoice')
            print(text.default_text_color + str(7), text.Yellow + 'Create rewards')
            print(text.default_text_color + str(8), text.Yellow + 'Create credit statement')
            selection = input(text.default_text_color + '\nPlease select: ')
    elif selection_structure == '2':
        print(text.default_text_color + str(0), text.Yellow + 'Close application')
        print(text.default_text_color + str(1), text.Yellow + 'Order simulation via Microservice')
        print(text.default_text_color + str(2), text.Yellow + 'POC information')
        print(text.default_text_color + str(3), text.Yellow + 'Product information')
        print(text.default_text_color + str(4), text.Yellow + 'Deals information by account')
        print(text.default_text_color + str(5), text.Yellow + 'Order information by account')
        print(text.default_text_color + str(6), text.Yellow + 'Recommender information by account')
        print(text.default_text_color + str(7), text.Yellow + 'Retrieve available invoices')
        print(text.default_text_color + str(8), text.Yellow + 'SKUs for Reward Shopping')
        selection = input(text.default_text_color + '\nPlease select: ')
        while validate_option_request_selection(selection) == 'false':
            print(text.Red + '\n- Invalid option\n')
            print(text.default_text_color + str(0), text.Yellow + 'Close application')
            print(text.default_text_color + str(1), text.Yellow + 'Order simulation via Microservice')
            print(text.default_text_color + str(2), text.Yellow + 'POC information')
            print(text.default_text_color + str(3), text.Yellow + 'Product information')
            print(text.default_text_color + str(4), text.Yellow + 'Deals information')
            print(text.default_text_color + str(5), text.Yellow + 'Order information by account')
            print(text.default_text_color + str(6), text.Yellow + 'Recommender information by account')
            print(text.default_text_color + str(7), text.Yellow + 'Retrieve available invoices')
            print(text.default_text_color + str(8), text.Yellow + 'SKUs for Reward Shopping')
            selection = input(text.default_text_color + '\nPlease select: ')
    elif selection_structure == '3':
        print(text.default_text_color + str(0), text.Yellow + 'Close application')
        print(text.default_text_color + str(1), text.Yellow + 'List categories')
        print(text.default_text_color + str(2), text.Yellow + 'Associate product to category')
        print(text.default_text_color + str(3), text.Yellow + 'Create category')
        selection = input(text.default_text_color + '\nPlease select: ')
        while validate_option_request_selection(selection) == 'false':
            print(text.Red + '\n- Invalid option\n')
            print(text.default_text_color + str(0), text.Yellow + 'Close application')
            print(text.default_text_color + str(1), text.Yellow + 'List categories')
            print(text.default_text_color + str(2), text.Yellow + 'Associate product to category')
            print(text.default_text_color + str(3), text.Yellow + 'Create category')
            selection = input(text.default_text_color + '\nPlease select: ')
    elif selection_structure == '4':
        print(text.default_text_color + str(0), text.Yellow + 'Close application')
        print(text.default_text_color + str(1), text.Yellow + 'Create User')
        print(text.default_text_color + str(2), text.Yellow + 'Delete User')
        selection = input(text.default_text_color + '\nPlease select: ')
        while validate_option_request_selection_for_structure_2(selection) == 'false':
            print(text.Red + '\n- Invalid option\n')
            print(text.default_text_color + str(0), text.Yellow + 'Close application')
            print(text.default_text_color + str(1), text.Yellow + 'Create User')
            print(text.default_text_color + str(2), text.Yellow + 'Delete User')
            selection = input(text.default_text_color + '\nPlease select: ')
    else:
        finish_application()

    return selection


# Print welcome menu
def print_welcome_script():
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
    print(text.default_text_color + str(2), text.Yellow + 'Data searching - Microservice')
    print(text.default_text_color + str(3), text.Yellow + 'Data creation - Magento')
    print(text.default_text_color + str(4), text.Yellow + 'Data creation - IAM')
    print(text.default_text_color + str(5), text.Yellow + 'Close application')
    structure = input(text.default_text_color + '\nPlease choose an option: ')
    while validate_structure(structure) is False:
        print(text.Red + '\n- Invalid option\n')
        print(text.default_text_color + str(1), text.Yellow + 'Data creation - Microservice')
        print(text.default_text_color + str(2), text.Yellow + 'Data searching - Microservice')
        print(text.default_text_color + str(3), text.Yellow + 'Data creation - Magento')
        print(text.default_text_color + str(4), text.Yellow + 'Data creation - IAM')
        print(text.default_text_color + str(5), text.Yellow + 'Close application')
        structure = input(text.default_text_color + '\nPlease choose an option: ')

    return structure


# Print rewards menu
def print_rewards_menu():
    print(text.default_text_color + str(1), text.Yellow + 'Create new program')
    print(text.default_text_color + str(2), text.Yellow + 'Update Initial Balance of a program')
    print(text.default_text_color + str(3), text.Yellow + 'Update DT Combos')
    print(text.default_text_color + str(4), text.Yellow + 'Enroll POC to a program')
    print(text.default_text_color + str(5), text.Yellow + 'Input Challenges to zone')
    print(text.default_text_color + str(6), text.Yellow + 'Input Redeem Products to account')
    print(text.default_text_color + str(7), text.Yellow + 'Unenroll a POC from a program')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_rewards(structure) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + str(1), text.Yellow + 'Create new program')
        print(text.default_text_color + str(2), text.Yellow + 'Update Initial Balance of a program')
        print(text.default_text_color + str(3), text.Yellow + 'Update DT Combos')
        print(text.default_text_color + str(4), text.Yellow + 'Enroll POC to a program')
        print(text.default_text_color + str(5), text.Yellow + 'Input Challenges to zone')
        print(text.default_text_color + str(6), text.Yellow + 'Input Redeem Products to account')
        print(text.default_text_color + str(7), text.Yellow + 'Unenroll a POC from a program')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure

# Print combos menu
def print_combos_menu():
    print(text.default_text_color + '\nWhich type of combo do you want to create?')
    print(text.default_text_color + str(1), text.Yellow + 'Input combo type discount')
    print(text.default_text_color + str(2), text.Yellow + 'Input combo type free good')
    print(text.default_text_color + str(3), text.Yellow + 'Input combo type digital trade')
    print(text.default_text_color + str(4), text.Yellow + 'Input combo with only free goods')
    print(text.default_text_color + str(5), text.Yellow + 'Reset combo consumption to zero')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_combo_structure(structure) == 'false':
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nWhich type of combo do you want to create?')
        print(text.default_text_color + str(1), text.Yellow + 'Input combo type discount')
        print(text.default_text_color + str(2), text.Yellow + 'Input combo type free good')
        print(text.default_text_color + str(3), text.Yellow + 'Input combo type digital trade')
        print(text.default_text_color + str(4), text.Yellow + 'Input combo with only free goods')
        print(text.default_text_color + str(5), text.Yellow + 'Reset combo consumption to zero')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure


# Validate combo type structure
def validate_combo_structure(option):
    options = ['1', '2', '3', '4', '5']
    if option in options:
        return 'true'
    else:
        return 'false'


# Print zone menu for Microservice
def print_zone_menu_for_ms():
    zone = input(text.default_text_color + 'Zone (AR, BR, DO, ZA, CO, MX, PE, EC): ')
    while validate_zone_for_ms(zone.upper()) == 'false':
        print(text.Red + '\n- Invalid option\n')
        zone = input(text.default_text_color + 'Zone (AR, BR, DO, ZA, CO, MX, PE, EC): ')

    return zone.upper()

# For interactive combos
def print_zone_for_interactive_combos_menu_for_ms():
    zone = input(text.default_text_color + 'Zone (BR, CO, AR): ')
    while validate_zone_for_interactive_combos_ms(zone.upper()) == 'false':
        print(text.Red + '\n- Invalid option\n')
        zone = input(text.default_text_color + 'Zone (BR, CO, AR): ')

    return zone.upper()

# Print zone menu for combos
def print_zone_menu_for_combos(combo_type=''):
    if combo_type == 'DT':
        zone = input(text.default_text_color + 'Zone (BR, DO, AR, CO, ZA, MX, PE, EC): ')
        while validate_zone_for_combos_dt(zone.upper()) == 'false':
            print(text.Red + '\n- Invalid option\n')
            zone = input(text.default_text_color + 'Zone (BR, DO, AR, CO, ZA, MX, PE, EC): ')
    else:
        zone = input(text.default_text_color + 'Zone (BR, DO, MX): ')
        while validate_zone_for_combos(zone.upper()) == 'false':
            print(text.Red + '\n- Invalid option\n')
            zone = input(text.default_text_color + 'Zone (BR, DO, MX): ')

    return zone.upper()


# Print country menu for User creation
def printCountryMenuInUserCreation():
    country = input(text.default_text_color + "Country (AR, BR, CO, DO, MX, ZA): ")
    while validateCountryInUserCreation(country.upper()) == "false":
        print(text.Red + "\n- Invalid option\n")
        country = input(text.default_text_color + "Country (AR, BR, CO, DO, MX, ZA): ")

    return country.upper()


# Print environment menu
def print_environment_menu():
    environment = input(text.default_text_color + 'Environment (DEV, SIT, UAT): ')
    while validate_environment(environment.upper()) is False:
        print(text.Red + '\n- Invalid option')
        environment = input(text.default_text_color + 'Environment (DEV, SIT, UAT): ')

    return environment.upper()


# Print environment menu for User creation
def printEnvironmentMenuInUserCreation():
    environment = input(text.default_text_color + "Environment (DT, SIT, UAT): ")
    while validateEnvironmentInUserCreation(environment.upper()) == 'false':
        print(text.Red + '\n- Invalid option')
        environment = input(text.default_text_color + "Environment (DT, SIT, UAT): ")

    return environment.upper()


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


def print_input_number_with_default(input_text, default_value=0):
    """Validate input number with default value"""
    while (True):
        input_number = input("{default_text_color}{input_text} - [default: {default_value}]: ".format(
            default_text_color=text.default_text_color,
            input_text=input_text, default_value=default_value)).strip() or str(default_value)

        if input_number.lstrip("-").isdigit():
            return int(input_number)


def print_input_number(input_text):
    """Validate input number"""
    while (True):
        input_number = input("{default_text_color}{input_text}: ".format(
            default_text_color=text.default_text_color,
            input_text=input_text)).strip()

        if input_number.lstrip("-").isdigit():
            return int(input_number)


def print_input_text(input_text):
    """Validate input text"""
    while (True):
        input_str = input("{default_text_color}{input_text}: ".format(
            default_text_color=text.default_text_color,
            input_text=input_text)).strip()

        if not is_blank(input_str):
            return input_str


def validate_country_menu_in_user_create_iam(zone):
    switcher = {
        'BR': 'true',
        'CO': 'true',
        'DO': 'true',
        'MX': 'true',
        'EC': 'true',
        'PE': 'true',
        'ZA': 'true',
        'AR': 'true'
    }
    return switcher.get(zone, 'false')


def validate_environment_menu_in_user_create_iam(environment):
    switcher = {
        'SIT': 'true',
        'UAT': 'true'
    }
    return switcher.get(environment, 'false')


def print_country_menu_in_user_create_iam():
    """Print Country Menu to Create User IAM
    Requirements:
        - BR
        - CO
        - DO
        - MX
        - EC
        - PE
        - ZA
        - AR
    """
    zone = input(text.default_text_color + 'Zone (BR, CO, DO, EC, MX, PE, ZA, AR): ')
    while validate_country_menu_in_user_create_iam(zone.upper()) == 'false':
        print(text.Red + '\n- Invalid option\n')
        zone = input(text.default_text_color + 'Zone (BR, CO, DO, EC, MX, PE, ZA, AR): ')
    return zone.upper()


def print_environment_menu_in_user_create_iam():
    """Print Environment Menu to Create User IAM
        Requirements:
        - SIT
        - UAT
    """
    environment = input(text.default_text_color + 'Environment (SIT, UAT): ')
    while validate_environment_menu_in_user_create_iam(environment.upper()) == 'false':
        print(text.Red + '\n- Invalid option')
        environment = input(text.default_text_color + 'Environment (SIT, UAT): ')
    return environment.upper()


# Menu for payment method simulation
def print_payment_method_simulation_menu(zone):
    if zone == 'BR':
        payment_choice = input(
            text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - BANK_SLIP ')
        while payment_choice != '1' and payment_choice != '2':
            print(text.Red + '\n- Invalid option\n')
            payment_choice = input(
                text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - BANK_SLIP ')

        if payment_choice == '1':
            payment_method = 'CASH'
        else:
            payment_method = 'BANK_SLIP'

    elif zone == 'DO' and zone == 'CO' or zone == 'EC' or zone == 'PE':
        payment_choice = input(text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - CREDIT ')
        while payment_choice != '1' and payment_choice != '2':
            print(text.Red + '\n- Invalid option\n')
            payment_choice = input(
                text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - CREDIT ')

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


def print_combo_id_menu():
    combo_id = input(text.default_text_color + 'Combo ID: ')

    while len(combo_id) == 0:
        print(text.Red + '\n- Combo ID should not be empty')
        combo_id = input(text.default_text_color + 'Combo ID: ')
    return combo_id


def validate_zone_for_credit_statement(zone):
    if zone.upper() != 'ZA':
        return 'false'
    else:
        return 'true'


# Print zone menu for credit statement
def print_zone_credit_statement():
    zone = input(text.default_text_color + 'Zone (ZA): ')
    while validate_zone_for_credit_statement(zone) == 'false':
        print(text.Red + '\n- Invalid option\n')
        zone = input(text.default_text_color + 'Zone (ZA): ')

    return zone.upper()


def validate_month(month):
    switcher = {
        '01': 'true',
        '02': 'true',
        '03': 'true',
        '04': 'true',
        '05': 'true',
        '06': 'true',
        '07': 'true',
        '08': 'true',
        '09': 'true',
        '10': 'true',
        '11': 'true',
        '12': 'true'
    }

    value = switcher.get(month, 'false')
    return value


def print_month_credit_statement():
    month = input(text.default_text_color + 'Which month do you want to create the document? (please put the number '
                                            'referent the month): ')
    if int(month) < 10:
        month = '0' + month

    while validate_month(month) == 'false':
        print(text.Red + '\n- Invalid option\n')
        month = input(text.default_text_color + 'Which month do you want to create the document? (please put the number'
                                                'referent the month): ')

    return month


def validate_years_credit_statement(year):
    if len(year) == 0:
        return 'error_0'
    elif (len(year) > 0) and (is_number(year) == 'false'):
        return 'not_number'
    elif len(year) < 4:
        return 'error_4'
    elif is_number(year) == 'true':
        return 'true'


def print_year_credit_statement():
    year = input(text.default_text_color + 'Which year do you want to create the document?: ')

    while validate_years_credit_statement(year) != 'true':
        if validate_years_credit_statement(year) == 'error_0':
            print(text.Red + '\n- Year should not be empty')
            year = input(text.default_text_color + 'Which year do you want to create the document?: ')
        if validate_years_credit_statement(year) == 'error_4':
            print(text.Red + '\n- Year must contain at least 4 characters')
            year = input(text.default_text_color + 'Which year do you want to create the document?: ')
        elif validate_years_credit_statement(year) == 'not_number':
            print(text.Red + '\n- The year must be Numeric')
            year = input(text.default_text_color + 'Which year do you want to create the document?: ')

    return year


def print_invoices(invoice_info, status):
    invoice_list = list()
    for i in invoice_info['data']:
        if i['status'] == status[0] or i['status'] == status[1]:
            invoice_values = {
                'Invoice ID': i['invoiceId'],
                'Product Quantity': i['itemsQuantity'],
                'Sub Total': i['subtotal'],
                'Tax': i['tax'],
                'Discount': i['discount'],
                'Total': i['total']
            }
            for j in range(i['itemsQuantity']):
                invoice_values.setdefault('SKU', []).append(i['items'][j-1]['sku'])
            invoice_list.append(invoice_values)
        else:
            continue
    if bool(invoice_list):
        print(text.default_text_color + '\nInvoice Information By Account  -  Status:' + status[1])
        print(tabulate(invoice_list, headers='keys', tablefmt='grid'))
    else:
        print(text.Red + '\nThere is no invoices with the status of ' + status[1] + ' for this account')


def validate_invoice_id(invoice_id):
    size_invoice_id = len(invoice_id)

    if size_invoice_id == 0:
        return 'error_0'
    else:
        return 'true'


def block_print():
    # Overwrite standard output (stdout)
    sys.stdout = open(os.devnull, 'w')


def find_values(key, json_str):
    """
    Find values in a dictionary
    Args:
        key: dict key
        json_str: json object
    Returns: None if the key does not exist or the key's value in case of success
    """

    results = list()

    def _decode_dict(a_dict):
        try:
            results.append(a_dict[key])
        except KeyError:
            pass
        return a_dict

    json.loads(json_str, object_hook=_decode_dict)

    if len(results) == 0:
        return 'None'
    else:
        return results[0]


def remove_from_dictionary(dictionary, *keys):
    """Removes the given ``keys`` from the ``dictionary``.

    If the given ``key`` cannot be found from the ``dictionary``, it
    is ignored.

    Example:
    | Remove From Dictionary | ${D3} | b | x | y |
    =>
    | ${D3} = {'a': 1, 'c': 3}
    """
    if is_string(dictionary) or isinstance(dictionary, (int, float)):
        raise TypeError("Expected argument to be a dictionary or dictionary-like, got %s instead.")

    for key in keys:
        if key in dictionary:
            dictionary.pop(key)


def is_string(item):
    return isinstance(item, str)


def generate_hmac_jwt(account_id, expire_months=1):
    now = int(t.time())
    expire_in = now + (2592000 * expire_months)

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/create_jwt_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'exp': expire_in,
        'iat': now,
        'accounts': [account_id]
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    encoded = jwt.encode(json_object, '20735d31-46b5-411d-af02-47897a01c0c9', algorithm='HS256')
    return 'Bearer {0}'.format(encoded)
