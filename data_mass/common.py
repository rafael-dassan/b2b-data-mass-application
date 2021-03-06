# Standard library imports
import json
import logging
import os
import sys
import time as t
import warnings
from datetime import date, datetime
from time import time
from typing import Optional, Text
from urllib.parse import urlencode
from uuid import uuid1

import click
import jwt
import pkg_resources
import requests
from click.termui import prompt
from dateutil.parser import parse
from dotenv import load_dotenv
from jsonpath_rw import Fields, Index
from jsonpath_rw_ext import parse
from requests import request

from data_mass.classes.text import text
from data_mass.config import Settings, get_settings
from data_mass.logger import log_to_file
from data_mass.validations import (
    is_number,
    validate_environment,
    validate_option_request_selection,
    validate_structure,
    validate_supplier_menu_structure,
    validate_supplier_search_menu_structure,
    validate_zone_for_interactive_combos_ms,
    validate_zone_for_ms
)

logger = logging.getLogger(__name__)

PLEASE_SELECT = "\nPlease select: "
DATE_FORMAT = "%Y-%m-%d"
CLOSE_APPLICATION = "Close application"
INVALID_OPTION = "\n- Invalid option\n"
DATA_CREATION = "Data creation - "
ZONE_SELECTION = "Zone (e.g., AR, BR, CO): "

# Validate option menu selection
def validate_option_request_selection_for_structure_2(option):
    switcher = {
        '0': True,
        '1': True,
        '2': True
    }

    value = switcher.get(option, False)
    return value


def validate_zone_for_combos(zone):
    switcher = {
        'AR': True,
        'BR': True,
        'CA': True,
        'DO': True,
        'MX': True,
        "UY": True
    }

    value = switcher.get(zone, False)
    return value


def validate_zone_for_combos_dt(zone):
    switcher = {
        'BR': True,
        'DO': True,
        'AR': True,
        'CO': True,
        'ZA': True,
        'MX': True,
        'PE': True,
        'EC': True,
        'SV': True,
        "UY": True,
        "TZ": True
    }
    return switcher.get(zone, False)


# Validate environment to User creation
def validate_environment_user_creation(environment):
    switcher = {
        'DT': True,
        'SIT': True,
        'UAT': True
    }
    
    return switcher.get(environment, False)


# Place generic request
def place_request(request_method, request_url, request_body, request_headers):
    try:
        # Send request
        response = request(request_method, request_url, data=request_body, headers=request_headers)
    except requests.exceptions.RequestException as e:
        print(f'\n{text.Red}{str(e)}')
        finish_application()

    log_to_file(
        request_method=request_method,
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers,
        status_code=response.status_code,
        response_body=response.text,
    )

    return response


# Return JWT header request
def get_header_request(zone, use_jwt_auth=False, use_root_auth=False, use_inclusion_auth=False,
                       sku_product=False, account_id=None, jwt_app_claim=None, should_not_use_m2m=False):

    switcher = {
        'AR': 'America/Buenos_Aires',
        'BR': 'America/Sao_Paulo',
        'CA': 'America/Toronto',
        'CO': 'America/Bogota',
        'DO': 'America/Santo_Domingo',
        'EC': 'America/Guayaquil',
        'MX': 'America/Mexico_City',
        'PA': 'America/Panama',
        'PE': 'America/Lima',
        'PY': 'America/Asuncion',
        'SV': 'America/El_Salvador',
        'US': 'America/New_York',
        'UY': 'America/Montevideo',
        'ZA': 'Africa/Johannesburg',
        'TZ': 'Africa/Dar_es_Salaam'

    }
    timezone = switcher.get(zone.upper(), False)
    load_dotenv()
    header = {
        'User-Agent': 'BEES - Data Brew Framework Current user: ' + os.getenv('USER_EMAIL'),
        'Content-Type': 'application/json',
        'country': zone,
        'requestTraceId': str(uuid1()),
        'x-timestamp': str(int(round(time()))),
        'cache-control': 'no-cache',
        'timezone': timezone
    }

    if zone in ["CA", "US"] and not should_not_use_m2m:
        header['Authorization'] = get_jwt_token()
        header['Accept-Language'] = 'en'

    elif zone in ["SV", "UY"] and not should_not_use_m2m:
        header['Authorization'] = get_jwt_token()
        header['Accept-Language'] = 'es'

    elif zone in ["TZ"] and not should_not_use_m2m:
        header['Authorization'] = get_jwt_token()
        header['Accept-Language'] = 'EN-TZ'

    elif use_jwt_auth:
        header['Authorization'] = generate_hmac_jwt(
            zone=zone,
            account_id=account_id,
            app_claim=jwt_app_claim
        )
    elif use_root_auth:
        header['Authorization'] = 'Basic cm9vdDpyb290'
    elif use_inclusion_auth:
        header['Authorization'] = 'Basic cmVsYXk6TVVRd3JENVplSEtB'
    else:
        header['Authorization'] = 'Basic cmVsYXk6cmVsYXk='

    if sku_product:
        header['skuId'] = sku_product

    return header


# Return base URL for Microservice
def get_microservice_base_url(environment, is_v1=True):
    if environment == 'DEV':
        if is_v1:
            return 'https://bees-services-dev.eastus2.cloudapp.azure.com/v1'

        else:
            return "https://bees-services-dev.eastus2.cloudapp.azure.com/api"
    else:
        env_name = 'SIT' if (environment != 'SIT' and environment != 'UAT') else environment
        context = '/v1' if is_v1 else '/api'
        return f"https://services-{env_name.lower()}.bees-platform.dev{context}"


def get_magento_base_url(
        environment: str, country: str) -> str:
    """
    Returns base URL for Magento.

    Parameters
    ----------
    environment : str
        environment for dict selecting.
    country : str
        country for dict selecting.

    Returns
    -------
    str
        Base url for the inputed environment and zone.
    """
    magento_url = {
        'DT': {
            'AR': 'https://qa-dt-las-ar.abi-sandbox.net/',
            'BR': 'https://qa-dt-br.abi-sandbox.net',
            'CA': 'https://qa-dt-ca.abi-sandbox.net/',
            'CO': 'https://qa-dt-copec-co.abi-sandbox.net',
            'DO': 'https://qa-dt-dr.abi-sandbox.net',
            'MX': 'https://qa-dt-mx.abi-sandbox.net',
            'ZA': 'https://qa-dt-za.abi-sandbox.net'
        },
        'QA': {
            'AR': 'https://qa-ma-las.abi-sandbox.net',
            'BR': 'https://qa-ma-br.abi-sandbox.net',
            'CO': 'https://qa-m3-copec-co.abi-sandbox.net',
            'DO': 'https://qa-ma-dr.abi-sandbox.net',
            'EC': 'https://qa-m1-ec.abi-sandbox.net',
            'MX': 'https://qa-se-mx.abi-sandbox.net',
            'PE': 'https://qa-m1-pe.abi-sandbox.net',
            'ZA': 'https://qa-ma-za.abi-sandbox.net'
        },
        'SIT': {
            'AR': 'https://ar.sit.bees-platform.dev',
            'BR': 'https://br.sit.bees-platform.dev',
            'CA': 'https://ca.sit.bees-platform.dev',
            'CO': 'https://co.sit.bees-platform.dev',
            'DO': 'https://do.sit.bees-platform.dev',
            'EC': 'https://ec.sit.bees-platform.dev',
            'MX': 'https://mx.sit.bees-platform.dev',
            'PA': 'https://pa.sit.bees-platform.dev',
            'PE': 'https://pe.sit.bees-platform.dev',
            'PY': 'https://py.sit.bees-platform.dev',
            'SV': 'https://sv.sit.bees-platform.dev',
            'UY': 'https://uy.sit.bees-platform.dev',
            'ZA': 'https://za.sit.bees-platform.dev'
        },
        'UAT': {
            'AR': 'https://ar.uat.bees-platform.dev',
            'BR': 'https://br.uat.bees-platform.dev',
            'CA': 'https://ca.uat.bees-platform.dev',
            'CO': 'https://co.uat.bees-platform.dev',
            'DO': 'https://do.uat.bees-platform.dev',
            'EC': 'https://ec.uat.bees-platform.dev',
            'MX': 'https://mx.uat.bees-platform.dev',
            'PA': 'https://pa.uat.bees-platform.dev',
            'PE': 'https://pe.uat.bees-platform.dev',
            'PY': 'https://py.uat.bees-platform.dev',
            'SV': 'https://sv.uat.bees-platform.dev',
            'UY': 'https://uy.uat.bees-platform.dev',
            'ZA': 'https://za.uat.bees-platform.dev'
        }
    }
    return magento_url.get(environment).get(country)


def get_magento_user_registration_access_token(
        environment: str, country: str) -> str:
    """
    Returns Magento User Registration Integration Access Token.

    Parameters
    ----------
    environment : str
        environment for dict selecting.
    country : str
        country for dict selecting.

    Returns
    -------
    str
        An user registration access in Magento.
    """
    access_token = {
        'DT': {
            'AR': '0pj40segd3h67zjn68z9oj18xyx5yib8',
            'BR': 'qq8t0w0tvz7nbn4gxo5jh9u62gohvjrw',
            'CO': '2z0re32n00z159oui0az2j2dr42bx8m5',
            'DO': '56jqtzzto7tw9uox8nr3eckoeup53dt2',
            'MX': '40qrmhwv93ixeysxsw5hxrvjn6dstdim',
            'ZA': 'y4u1xqitth7k8y50ei5nlfm538sblk6j',
            'UY': 'Placeholder'
        },
        'QA': {
            'AR': '30lqki06nbdegugcmdb0ttm9yppnmoec',
            'BR': 'qq8t0w0tvz7nbn4gxo5jh9u62gohvjrw',
            'CO': '8mh6b9b6ft6m1cr5k7zm2jh4aljq4slx',
            'DO': '56jqtzzto7tw9uox8nr3eckoeup53dt2',
            'EC': 'kyhzpszn0bswbf17mlb409ldg14j58uv',
            'MX': 'w0mi88cajh0jbq0zrive3ht4eywc8xlm',
            'PE': 'hwv67q9d3zyy2u500n2x0r5g7mr2j5is',
            'ZA': 'yq2ed2ygbuiuysimjuir7cr86lbo3b90',
            'UY': 'Placeholder'
        },
        'SIT': {
            'AR': '30lqki06nbdegugcmdb0ttm9yppnmoec',
            'BR': 'qq8t0w0tvz7nbn4gxo5jh9u62gohvjrw',
            'CA': 'nhdzq8d4c59q1ofzsrpzlm2o7e2vdonf',
            'CO': 'walt5dp3keiq2du0f30kir21v13f3u0v',
            'DO': '56jqtzzto7tw9uox8nr3eckoeup53dt2',
            'EC': 'kyhzpszn0bswbf17mlb409ldg14j58uv',
            'MX': 'w0mi88cajh0jbq0zrive3ht4eywc8xlm',
            'PA': '28bfo54x45h9xajalu3hvl0a33dmo4z3',
            'PE': 'hwv67q9d3zyy2u500n2x0r5g7mr2j5is',
            'PY': '03ijjunt2djravu3kin3siirfdah0u7j',
            'ZA': 'nmvvuk58lc425a7p5l55orrkgh0jprr2',
            'UY': 'wfuqds2xd2ufmagho4qm2n9suc5qwuxk'
        },
        'UAT': {
            'AR': '30lqki06nbdegugcmdb0ttm9yppnmoec',
            'BR': 'qq8t0w0tvz7nbn4gxo5jh9u62gohvjrw',
            'CA': '1nb7d81mmwmsyd0i6n01fgrkyhmpj6k8',
            'CO': '8mh6b9b6ft6m1cr5k7zm2jh4aljq4slx',
            'DO': '56jqtzzto7tw9uox8nr3eckoeup53dt2',
            'EC': 'awtm7d9as0n9k1o5zi9fi90rtukxdmqh',
            'MX': 'kcsn7y80vvo2by9fluw2vq4r2a6pucfs',
            'PA': 'ovdnr3wfoh6nf0uh6h9ppoicp8jb15y0',
            'PE': '4z0crqq6yb6t5mip43i63tgntdll09vc',
            'PY': 'z3l3d1l09hxd9wy0jmnphfwj09o8iefn',
            'ZA': '31pdb0yht5kn3eld7gum021f6k984jh9',
            'UY': 'fjsmjuj8d022z19yn7sa196wcfsjp006'
        }
    }

    return access_token.get(environment).get(country)


def get_magento_datamass_access_token(
        environment: str, country: str) -> str:
    """
    Returns Magento Datamass Application Access Token.

    Parameters
    ----------
    environment : str
        environment for dict selecting.
    country : str
        country for dict selecting.

    Returns
    -------
    str
        The data-mass access token for Magento.
    """
    access_token = {
        'UAT': {
            'AR': 'a34o213zgisn67efeg0zbq04sqg667qk',
            'BR': '8z2z3y523hoqkcqci8q58afuoue81bns',
            'CA': 'kz18zssktxjrns2jyq1lbj7mufs3mj2h',
            'CO': 'meqei3q5ztreebdpb5vyej378mt2o8qy',
            'DO': 'js4gd8y9wkqogf7eo2s4uy6oys15lfkf',
            'EC': 'w9pphbvskd35206otky7cv1dobn0p1yb',
            'MX': 'lsnudq7uujr3svcbn0g0uxlt6vjqe9yj',
            'PA': 't1l4tdhvzrsk54qgm9b7wg0nty1ia0jr',
            'PE': 'xcgb5m0rl5pto116q4gxe1msd3zselq6',
            'PY': 'nju63hy7j5nhfzgaeah2y077anlpzs6o',
            'SV': 's2te8e0rzibmqj89cb4h2e4vduebe51o',
            'UY': 'Not ready for UAT',
            'ZA': '0seca4btewbr3e1opma4je2x8ftj57wx'
        },
        'SIT': {
            'AR': 'hzp6hw65oqiyeyv8ozfzunex0nc1rff8',
            'BR': 'q6yti2dxmhp0e2xjgyvtt72nziss6ptp',
            'CA': '93slxvujwumdkbpzb1qg4jf0zwrew1ud',
            'CO': 'new189lnml9xmcr3m9gc0j6oji6w2izr',
            'DO': 'tgqnjlqpfupf0i4zxcs2doqx409k1hyq',
            'EC': 'ybyiars1mhm5e4jyaq94s5csj1e77knp',
            'MX': '86pg36lug4ivrx3xh5b5qnemzy1gw6v8',
            'PA': '3bs7q1f5wtegt7vrgxumcv1plhjatf1d',
            'PE': 'lda0mjri507oqrm8xfofk6weifajn8cm',
            'PY': 'bgfrp38faxbpwnad7uoc2vqlprmv5nck',
            'SV': 'fqwj8frye6s4dpucnks6srh0l04xwk35',
            'UY': 'r9grukw8l2ck0r01mqo6bnlir6kyuysl',
            'ZA': 'fde80w10jbbaed1mrz6yg0pwy1vzfo48'
        }
    }
    return access_token.get(environment).get(country)



def clear_terminal():
    """
    Clears the terminal
    """
    os.system('clear')


def finish_application():
    """
    Kills the application
    """
    sys.exit()


def print_available_options(selection_structure):
    """
    Print the init menu for user selection

    Args:
        selection_structure ([str]): the option selected by the user

    Returns:
        [str]: the selected option by the user
    """
    if selection_structure == '1':
        print(text.default_text_color + str(0), text.Yellow + CLOSE_APPLICATION)
        print(text.default_text_color + str(1), text.Yellow + 'Account')
        print(text.default_text_color + str(2), text.Yellow + 'Product')
        print(text.default_text_color + str(3), text.Yellow + 'Orders')
        print(text.default_text_color + str(4), text.Yellow + 'Deals')
        print(text.default_text_color + str(5), text.Yellow + 'Input combos')
        print(text.default_text_color + str(6), text.Yellow + 'Invoice')
        print(text.default_text_color + str(7), text.Yellow + 'Create rewards')
        print(text.default_text_color + str(8), text.Yellow + 'Create credit statement')
        print(text.default_text_color + str(9), text.Yellow + 'Categories (Multivendor)')
        selection = input(text.default_text_color + '\nPlease select: ')
        while not validate_option_request_selection(selection):
            print(text.Red + INVALID_OPTION)
            print(text.default_text_color + str(0), text.Yellow + CLOSE_APPLICATION)
            print(text.default_text_color + str(1), text.Yellow + 'Account')
            print(text.default_text_color + str(2), text.Yellow + 'Product')
            print(text.default_text_color + str(3), text.Yellow + 'Orders')
            print(text.default_text_color + str(4), text.Yellow + 'Deals')
            print(text.default_text_color + str(5), text.Yellow + 'Input combos')
            print(text.default_text_color + str(6), text.Yellow + 'Invoice')
            print(text.default_text_color + str(7), text.Yellow + 'Create rewards')
            print(text.default_text_color + str(8), text.Yellow + 'Create credit statement')
            print(text.default_text_color + str(9), text.Yellow + 'Categories')
            selection = input(text.default_text_color + PLEASE_SELECT)
    elif selection_structure == '2':
        print(text.default_text_color + str(0), text.Yellow + CLOSE_APPLICATION)
        print(text.default_text_color + str(1), text.Yellow + 'Order simulation via Microservice')
        print(text.default_text_color + str(2), text.Yellow + 'POC information')
        print(text.default_text_color + str(3), text.Yellow + 'Product information')
        print(text.default_text_color + str(4), text.Yellow + 'Deals information by account')
        print(text.default_text_color + str(5), text.Yellow + 'Order information by account')
        print(text.default_text_color + str(6), text.Yellow + 'Recommender information by account')
        print(text.default_text_color + str(7), text.Yellow + 'Retrieve available invoices')
        print(text.default_text_color + str(8), text.Yellow + 'SKUs for Reward Shopping')
        selection = input(text.default_text_color + PLEASE_SELECT)
        while not validate_option_request_selection(selection):
            print(text.Red + INVALID_OPTION)
            print(text.default_text_color + str(0), text.Yellow + CLOSE_APPLICATION)
            print(text.default_text_color + str(1), text.Yellow + 'Order simulation via Microservice')
            print(text.default_text_color + str(2), text.Yellow + 'POC information')
            print(text.default_text_color + str(3), text.Yellow + 'Product information')
            print(text.default_text_color + str(4), text.Yellow + 'Deals information')
            print(text.default_text_color + str(5), text.Yellow + 'Order information by account')
            print(text.default_text_color + str(6), text.Yellow + 'Recommender information by account')
            print(text.default_text_color + str(7), text.Yellow + 'Retrieve available invoices')
            print(text.default_text_color + str(8), text.Yellow + 'SKUs for Reward Shopping')
            selection = input(text.default_text_color + PLEASE_SELECT)
    elif selection_structure == '3':
        print(text.default_text_color + str(0), text.Yellow + CLOSE_APPLICATION)
        print(text.default_text_color + str(1), text.Yellow + 'Generate GET token')
        print(text.default_text_color + str(2), text.Yellow + 'Generate Root token')
        print(text.default_text_color + str(3), text.Yellow + 'Generate Inclusion token')
        print(text.default_text_color + str(4), text.Yellow + 'Generate Basic token')
        selection = input(text.default_text_color + PLEASE_SELECT)
        while not validate_option_request_selection(selection):
            print(text.Red + INVALID_OPTION)
            print(text.default_text_color + str(0), text.Yellow + CLOSE_APPLICATION)
            print(text.default_text_color + str(1), text.Yellow + 'Generate GET token')
            print(text.default_text_color + str(2), text.Yellow + 'Generate Root token')
            print(text.default_text_color + str(3), text.Yellow + 'Generate Inclusion token')
            print(text.default_text_color + str(4), text.Yellow + 'Generate Basic token')
            selection = input(text.default_text_color + PLEASE_SELECT)
    elif selection_structure == '4':
        print(text.default_text_color + str(0), text.Yellow + CLOSE_APPLICATION)
        print(text.default_text_color + str(1), text.Yellow + 'List categories')
        print(text.default_text_color + str(2), text.Yellow + 'Associate product to category')
        print(text.default_text_color + str(3), text.Yellow + 'Create category')
        selection = input(text.default_text_color + PLEASE_SELECT)
        while not validate_option_request_selection(selection):
            print(text.Red + INVALID_OPTION)
            print(text.default_text_color + str(0), text.Yellow + CLOSE_APPLICATION)
            print(text.default_text_color + str(1), text.Yellow + 'List categories')
            print(text.default_text_color + str(2), text.Yellow + 'Associate product to category')
            print(text.default_text_color + str(3), text.Yellow + 'Create category')
            selection = input(text.default_text_color + PLEASE_SELECT)
    elif selection_structure == '5':
        print(text.default_text_color + str(0), text.Yellow + CLOSE_APPLICATION)
        print(text.default_text_color + str(1), text.Yellow + 'Create User')
        print(text.default_text_color + str(2), text.Yellow + 'Delete User')
        selection = input(text.default_text_color + PLEASE_SELECT)
        while not validate_option_request_selection_for_structure_2(selection):
            print(text.Red + INVALID_OPTION)
            print(text.default_text_color + str(0), text.Yellow + CLOSE_APPLICATION)
            print(text.default_text_color + str(1), text.Yellow + 'Create User')
            print(text.default_text_color + str(2), text.Yellow + 'Delete User')
            selection = input(text.default_text_color + PLEASE_SELECT)
    elif selection_structure == '6':
        print(text.default_text_color + str(0), text.Yellow + CLOSE_APPLICATION)
        print(text.default_text_color + str(1), text.Yellow + 'Create Attribute')
        print(text.default_text_color + str(2), text.Yellow + 'Create Category')
        print(text.default_text_color + str(3), text.Yellow + 'Create association between attribute and category')
        print(text.default_text_color + str(4), text.Yellow + 'Delete Attribute')
        print(text.default_text_color + str(5), text.Yellow + 'Edit Attribute Type')
        print(text.default_text_color + str(6), text.Yellow + 'Create Product')
        selection = input(text.default_text_color + PLEASE_SELECT)
        while not validate_supplier_menu_structure(selection):
            print(text.Red + INVALID_OPTION)
            print(text.default_text_color + str(0), text.Yellow + CLOSE_APPLICATION)
            print(text.default_text_color + str(1), text.Yellow + 'Create Attribute')
            print(text.default_text_color + str(2), text.Yellow + 'Create Category')
            print(text.default_text_color + str(3), text.Yellow + 'Create association between attribute and category')
            print(text.default_text_color + str(4), text.Yellow + 'Delete Attribute')
            print(text.default_text_color + str(5), text.Yellow + 'Edit Attribute Type')
            print(text.default_text_color + str(6), text.Yellow + 'Create Product')
            selection = input(text.default_text_color + PLEASE_SELECT)
    elif selection_structure == '7':
        print(text.default_text_color + str(0), text.Yellow + CLOSE_APPLICATION)
        print(text.default_text_color + str(1), text.Yellow + 'Search a specific attribute')
        print(text.default_text_color + str(2), text.Yellow + 'Search all attributes')
        print(text.default_text_color + str(3), text.Yellow + 'Search a specific category')
        print(text.default_text_color + str(4), text.Yellow + 'Search all category')
        selection = input(text.default_text_color + PLEASE_SELECT)
        while not validate_supplier_search_menu_structure(selection):
            print(text.Red + INVALID_OPTION)
            print(text.default_text_color + str(0), text.Yellow + CLOSE_APPLICATION)
            print(text.default_text_color + str(1), text.Yellow + 'Search a specific attribute')
            print(text.default_text_color + str(2), text.Yellow + 'Search all attributes')
            print(text.default_text_color + str(3), text.Yellow + 'Search a specific category')
            print(text.default_text_color + str(4), text.Yellow + 'Search all category')
            selection = input(text.default_text_color + PLEASE_SELECT)
    else:
        finish_application()

    return selection


def print_welcome_script():
    print(text.Bold + text.White + text.BackgroundDarkGray)
    print("                                    ")
    print("                                    ")
    print("          DATA-MASS SCRIPT          ")
    print("                                    ")
    print("                                    ")
    print(text.default_text_color + text.ResetAll + text.Bold + "\n")


def print_structure_menu():
    print(text.default_text_color + str(1), text.Yellow + DATA_CREATION + text.White + 'Microservice')
    print(text.default_text_color + str(2), text.Yellow + 'Data searching - ' + text.White + 'Microservice')    
    print(text.default_text_color + str(3), text.Yellow + 'Token generator - ' + text.White + 'Microservice')
    print(text.default_text_color + str(4), text.Yellow + DATA_CREATION + text.White + 'Magento')
    print(text.default_text_color + str(5), text.Yellow + DATA_CREATION + text.White + 'IAM')
    print(text.default_text_color + str(6), text.Yellow + DATA_CREATION + text.White + 'Supplier/PIM')
    print(text.default_text_color + str(7), text.Yellow + 'Data searching - ' + text.White + 'Supplier/PIM')    
    print(text.default_text_color + str(8), text.Yellow + CLOSE_APPLICATION)
    structure = input(text.default_text_color + '\nPlease choose an option: ')
    while validate_structure(structure) is False:
        print(text.Red + INVALID_OPTION)
        print(text.default_text_color + str(1), text.Yellow + 'Data creation - Microservice')
        print(text.default_text_color + str(2), text.Yellow + 'Data searching - Microservice') 
        print(text.default_text_color + str(3), text.Yellow + 'Token generator - Microservice')
        print(text.default_text_color + str(4), text.Yellow + 'Data creation - Magento')
        print(text.default_text_color + str(5), text.Yellow + 'Data creation - IAM')
        print(text.default_text_color + str(6), text.Yellow + 'Data creation - Supplier/PIM')
        print(text.default_text_color + str(7), text.Yellow + 'Data searching - Supplier/PIM')
        print(text.default_text_color + str(8), text.Yellow + CLOSE_APPLICATION)
        structure = input(text.default_text_color + '\nPlease choose an option: ')

    return structure


# Print combos menu
def print_combos_menu():
    print(text.default_text_color + '\nWhich type of combo do you want to create?')
    print(text.default_text_color + str(1), text.Yellow + 'Input combo type discount')
    print(text.default_text_color + str(2), text.Yellow + 'Input combo type free good')
    print(text.default_text_color + str(3), text.Yellow + 'Input combo type digital trade')
    print(text.default_text_color + str(4), text.Yellow + 'Input combo with only free goods')
    print(text.default_text_color + str(5), text.Yellow + 'Reset combo consumption to zero')
    structure = input(text.default_text_color + PLEASE_SELECT)
    while not validate_combo_structure(structure):
        print(text.Red + INVALID_OPTION)
        print(text.default_text_color + '\nWhich type of combo do you want to create?')
        print(text.default_text_color + str(1), text.Yellow + 'Input combo type discount')
        print(text.default_text_color + str(2), text.Yellow + 'Input combo type free good')
        print(text.default_text_color + str(3), text.Yellow + 'Input combo type digital trade')
        print(text.default_text_color + str(4), text.Yellow + 'Input combo with only free goods')
        print(text.default_text_color + str(5), text.Yellow + 'Reset combo consumption to zero')
        structure = input(text.default_text_color + PLEASE_SELECT)

    return structure


# Validate combo type structure
def validate_combo_structure(option):
    options = ['1', '2', '3', '4', '5']
    if option in options:
        return True
    else:
        return False


# Print zone menu for Microservice
def print_zone_menu_for_ms():
    zone = input(text.default_text_color + ZONE_SELECTION)
    save_environment_zone_to_env(zone)
    while not validate_zone_for_ms(zone.upper()):
        print(text.Red + f'\n- {zone.upper()} is not a valid zone\n')
        zone = input(text.default_text_color + ZONE_SELECTION)
        save_environment_zone_to_env(zone)

    return zone.upper()


# For interactive combos
def print_zone_for_interactive_combos_menu_for_ms():
    zone = input(text.default_text_color + ZONE_SELECTION)
    save_environment_zone_to_env(zone)
    while not validate_zone_for_interactive_combos_ms(zone.upper()):
        print(text.Red + f'\n- {zone.upper()} is not a valid zone\n')
        zone = input(text.default_text_color + ZONE_SELECTION)
        save_environment_zone_to_env(zone)

    return zone.upper() 


# Print environment menu
def print_environment_menu():
    environment = input(text.default_text_color + 'Environment (DEV, SIT, UAT): ')
    save_environment_to_env(environment)
    while validate_environment(environment.upper()) is False:
        print(text.Red + f'\n- {environment.upper()} is not a valid environment\n')
        environment = input(text.default_text_color + 'Environment (DEV, SIT, UAT): ')
        save_environment_to_env(environment)

    return environment.upper() 


# Print environment menu for User creation
def print_environment_menu_user_creation():
    environment = input(text.default_text_color + "Environment (e.g., SIT, UAT): ")
    save_environment_to_env(environment)
    while not validate_environment_user_creation(environment.upper()):
        print(text.Red + f"\n- {environment} is not a valid environment")
        environment = input(text.default_text_color + "Environment (e.g., SIT, UAT): ")
        save_environment_to_env(environment)

    return environment.upper() 


# Print user name menu
def print_input_email():
    email = input(text.default_text_color + "User email/UserPhone: ")
    while len(email) == 0:
        print(text.Red + "\n- The user email should not be empty")
        email = input(text.default_text_color + "User email/UserPhone: ")

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


def validate_yes_no_change_date(
    question: str = "New Date entry for Delivery Date? y/N: "
    ):
    """
    Validate user input for change date.

    Parameters
    ----------
    question: str, optional
        Verify if user would change the date,
        by default "New Date entry for Delivery Date? y/N:"

    Returns
    -------
    str
        Y or N depending on user input.
    """
    option = input(f'{text.default_text_color}{question}')

    while (option.upper() in ["Y", "N"]) is False:
        print(text.Red + INVALID_OPTION)
        option = input(f'\n{text.default_text_color}{question}')

    if option.upper() == "Y": 
        return option.upper()

    return option.upper()


def validate_user_entry_date(text:str = "New Date entry"):
    """
    Validate user input for date using format of Y-m-d.

    Parameters
    ----------
    text: str, optional
        Validate user input date and print the passed,
        by default "New Date entry"

    Returns
    -------
    str
        str valid date.
    """
    date = prompt(text, type=click.DateTime(formats=[DATE_FORMAT]))

    new_date = str(datetime.date(date))
    return new_date


def validate_country_menu_in_user_create_iam(zone):
    switcher = {
        "AR": True,
        "BR": True,
        "CA": True,
        "CO": True,
        "DO": True,
        "EC": True,
        "MX": True,
        "PE": True,
        "PA": True,
        "SV": True,
        "US": True,
        "UY": True,
        "ZA": True,
        "TZ": True
    }
    return switcher.get(zone, False)


def validate_environment_menu_in_user_create_iam(environment):
    switcher = {
        'QA': True,
        'SIT': True,
        'UAT': True
    }
    return switcher.get(environment, False)


def print_environment_menu_in_user_create_iam():
    """Print Environment Menu to Create User IAM
        Requirements:
        - QA
        - SIT
        - UAT
    """
    environment = input(text.default_text_color + 'Environment (QA, SIT, UAT): ')
    while not validate_environment_menu_in_user_create_iam(environment.upper()):
        print(text.Red + INVALID_OPTION)
        environment = input(text.default_text_color + 'Environment (QA, SIT, UAT): ')
    return environment.upper()


# Menu for payment method simulation
def print_payment_method_simulation_menu(zone):
    if zone == 'BR':
        payment_choice = input(
            text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - BANK_SLIP ')
        while payment_choice != '1' and payment_choice != '2':
            print(text.Red + INVALID_OPTION)
            payment_choice = input(
                text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - BANK_SLIP ')

        if payment_choice == '1':
            payment_method = 'CASH'
        else:
            payment_method = 'BANK_SLIP'

    elif zone == 'DO' and zone == 'CO' or zone == 'EC' or zone == 'PE':
        payment_choice = input(text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - CREDIT ')
        while payment_choice != '1' and payment_choice != '2':
            print(text.Red + INVALID_OPTION)
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
    first_date = first_date.strftime(DATE_FORMAT)
    last_date = date(date.today().year, 12, 31)
    last_date = last_date.strftime(DATE_FORMAT)
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
        return False
    else:
        return True


# Print zone menu for credit statement
def print_zone_credit_statement():
    zone = input(text.default_text_color + 'Zone (ZA): ')
    while not validate_zone_for_credit_statement(zone):
        print(text.Red + INVALID_OPTION)
        zone = input(text.default_text_color + 'Zone (ZA): ')

    return zone.upper()


def validate_month(month):
    switcher = {
        '01': True,
        '02': True,
        '03': True,
        '04': True,
        '05': True,
        '06': True,
        '07': True,
        '08': True,
        '09': True,
        '10': True,
        '11': True,
        '12': True
    }

    value = switcher.get(month, False)
    return value


def print_month_credit_statement():
    month = input(text.default_text_color + 'Which month do you want to create the document? (please put the number '
                                            'referent the month): ')
    if int(month) < 10:
        month = '0' + month

    while not validate_month(month):
        print(text.Red + INVALID_OPTION)
        month = input(text.default_text_color + 'Which month do you want to create the document? (please put the number'
                                                'referent the month): ')

    return month


def validate_years_credit_statement(year):
    if len(year) == 0:
        return 'error_0'
    elif (len(year) > 0) and not is_number(year):
        return 'not_number'
    elif len(year) < 4:
        return 'error_4'
    elif is_number(year):
        return True


def print_year_credit_statement():
    which_year = 'Which year do you want to create the document?: '
    year = input(text.default_text_color + which_year)

    while validate_years_credit_statement(year) != True:
        if validate_years_credit_statement(year) == 'error_0':
            print(text.Red + '\n- Year should not be empty')
            year = input(text.default_text_color + which_year)
        if validate_years_credit_statement(year) == 'error_4':
            print(text.Red + '\n- Year must contain at least 4 characters')
            year = input(text.default_text_color + which_year)
        elif validate_years_credit_statement(year) == 'not_number':
            print(text.Red + '\n- The year must be Numeric')
            year = input(text.default_text_color + which_year)

    return year


def validate_invoice_id(invoice_id):
    size_invoice_id = len(invoice_id)

    if size_invoice_id == 0:
        return 'error_0'
    else:
        return True


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


def generate_hmac_jwt(zone, account_id, app_claim=None, expire_months=1):
    now = int(t.time())
    expire_in = now + (2592000 * expire_months)
    
    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/create_jwt_payload.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    dict_values = {
        'exp': expire_in,
        'iat': now,
        'country': zone,
        'accounts': [account_id]
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])
    
    if app_claim is not None:
        set_to_dictionary(json_object, 'app', app_claim)
        if app_claim == 'adminportal':
            set_to_dictionary(json_object, 'scopes', ["Membership"])
    
    encoded = jwt.encode(json_object, '20735d31-46b5-411d-af02-47897a01c0c9', algorithm='HS256')
    return f'Bearer {encoded}'


def generate_erp_token(expire_months=1):
    now = int(t.time())
    expire_in = now + (2592000 * expire_months)
    
    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/create_erp_token_payload.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    dict_values = {
        'exp': expire_in,
        'iat': now
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    encoded = jwt.encode(json_object, '20735d31-46b5-411d-af02-47897a01c0c9', algorithm='HS256')
    return f'Bearer {encoded}'


# Return base URL for Supplier
def get_supplier_base_url(environment):
    if environment == 'LOCAL':
        return 'http://localhost:8080/graphql'
    else:
        return 'https://services-' + environment.lower()+'.bees-platform.dev/api/product-taxonomy-service/graphql'


def get_header_request_supplier():
    header = {
       'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3Nlcn'
                        'ZpY2VzIiwiZXhwIjoxODkzNDU2MDAwLCJpYXQiOjE1MTYyMzkwMjIsInVwZGF0ZWRfYXQiOjExMTExMTEsInJvbGVzIjpbI'
                        'lJPTEVfQ1VTVE9NRVIiXX0.oDALscasXTa2Zt209Hjmydk9GT7ErsdxI4c1D4q9kNA',
       'requestTraceId': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
    }

    return header


def get_jwt_token():
    """
    checks if there is any token, if it exists and has expired,\
    a new one must be created.

    Returns
    -------
    str
        The jwt token.
    """
    access_token: Optional[str] = None

    try:
        access_token = os.environ["TOKEN"]
    except KeyError:
        pass

    if access_token is None or token_has_expired():
        access_token = get_new_token()
        os.environ["TOKEN"] = access_token

    return access_token
    

def token_has_expired() -> bool:
    """
    Check if the current token has expired.
    
    Returns
    -------
    bool
        Whenever a token has expired or not.
    """
    current_time = round(t.time())

    try:
        expiration_date = os.environ["EXPIRATION_TIME"]
    except KeyError:
        return True

    if current_time > int(expiration_date):
        return True

    return False


def resources_warning():
    """
    Shows `ResourcesWarning` when using US features.
    """
    message = \
    """
    Data Mass does not have persistent data creation power for
    services that make use of live-call.

    All returned data (if any) is mocked. If there is a need for any
    specific data, we suggest that you notify the migration team.
    """
    warnings.filterwarnings(action="once")
    warnings.warn(
        f"{text.Red}{message}",
        ResourceWarning, stacklevel=2
    )

def get_confirmation_option(option, callbackFunction): 
    option = option.upper()
    isInvalidOption = option != '' and (option != 'Y' and option != 'N')
    if(isInvalidOption):
        print('Invalid option, please try again')
        return callbackFunction()
    else: 
        return option == 'Y'

def save_environment_to_env(environment):
    os.environ['environment_env']=environment.upper()
    
def save_environment_zone_to_env(zone):
    os.environ['zone_env']=zone.upper() 


def get_new_token():
    env = os.environ['environment_env']
    email = os.environ['USER_EMAIL']
    zone = os.environ['zone_env']
    header: dict = {
        "Content-Type": "application/x-www-form-urlencoded",
        "requestTraceId": str(uuid1()),
    }
    request_url: str = f"https://services-{env}.bees-platform.dev/data-brew-server/token/create?email={email}&zone={zone}"

    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body="",
        request_headers=header
    )
    content: dict = json.loads(response.content)
    token = content.get("token", None)

    os.environ["EXPIRATION_TIME"] = str(round(t.time() + 1800))
    
    return f"Bearer {token}"
