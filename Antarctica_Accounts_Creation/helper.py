from requests import request
from uuid import uuid1
from time import time
from json import dumps
import os
import sys
from classes.text import text
from datetime import date, datetime, timedelta

# Validate option menu selection
def validateOptionRequestSelection(option, isExtraStructure = 'false'):
    if isExtraStructure == 'false':
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
        }

        value = switcher.get(option, 'false')
        return value
        
    else:
        switcher = {
            '0': 'true',
            '1': 'true',
        }

        value = switcher.get(option, 'false')
        return value

# Validate lenght account id
def validateAccount(accountId):
    if len(accountId) > 10 or len(accountId) == 0:
        return 'false'
    else:
        return accountId.zfill(10)

# Validate lenght name account
def validateName(name):
    if len(name) == 0:
        return 'false'
    else:
        return name

# Validate zone account
def validateZone(isMiddleware, zone):
    if isMiddleware == 'true':
        switcher = {
            'DO': 'true',
            'ZA': 'true',
            'AR': 'true',
            'CL': 'true',
        }

        value = switcher.get(zone, 'false')
        return value
    else:
        switcher = {
            'DO': 'true',
            'ZA': 'true',
            'AR': 'true',
            'CL': 'true',
            'BR': 'true',
        }

        value = switcher.get(zone, 'false')
        return value

# Validate structure account
def validateStructure(option):
    if option == '1' or option == '2' or option == '3' or option == '4':
        return 'true'
    else:
        return 'false'

# Validate environment
def validateEnvironment(environment):
    if environment == 'QA' or environment == 'UAT':
        return 'true'
    else:
        return 'false'

# Place request generic
def place_request(request_type, request_url, request_body, request_headers):
    response = request(
        request_type,
        request_url,
        data=request_body,
        headers=request_headers
    )

    return response

# Return jwt header request
def get_header_request(header_country, useJwtAuthorization='false', useRootAuthentication = 'false', useInclusionAuthentication = 'false', sku_product='false'):
    timezone = "UTC"
    header = {
        "Content-Type": "application/json",
        "country": header_country.upper(),
        "requestTraceId": str(uuid1()),
        "x-timestamp": str(int(round(time() * 1000))),
        "cache-control": "no-cache",
        "timezone": timezone
    }

    if useJwtAuthorization == 'true':
        header['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3NlcnZpY2VzIiwiZXhwIjoxNTg1NjEyODAwLCJ1cGRhdGVkX2F0IjoxNTY1NzkxODI0LCJpYXQiOjE1NjU3OTE4MjQsIm5hbWUiOiJ0ZXN0ZUB0ZXN0ZS5jb20iLCJhY2NvdW50SUQiOiIwMDAwMTAwMDA0IiwidXNlcklEIjoiMTYiLCJyb2xlcyI6WyJST0xFX0NVU1RPTUVSIl19.GUc9ssFyXle0F0W6LUU2amvZ-hm7TFIDteR50WlQFUE'
    elif useRootAuthentication == 'true':
        header['Authorization'] = 'Basic cm9vdDpyb290'
    elif useInclusionAuthentication == 'true':
        header['Authorization'] = 'Basic cmVsYXk6TVVRd3JENVplSEtB'
    else:
        header['Authorization'] = 'Basic cmVsYXk6cmVsYXk='
    
    if sku_product != 'false':
        header['skuId'] = sku_product

    return header

# Return base url for middleware
def get_middleware_base_url(zone, environment, version_request):
    prefix_zone = zone.lower()
    if zone == 'DO':
        prefix_zone = 'dr'
    elif zone == 'AR' or zone == 'CL':
        prefix_zone = 'las'
    
    prefix_environment = environment.lower()
    if environment == "UAT":
        prefix_environment = "test"

    return "https://b2b-" + prefix_zone.lower() + "-" + prefix_environment.lower() + ".azurewebsites.net/api/" + version_request + "/" + zone.upper()

# Return base url for microservice
def get_microservice_base_url(environment):
    return "https://b2b-services-" + environment.lower() + ".westeurope.cloudapp.azure.com/v1"

# Payload Middleware ZA account
def get_middleware_payload_za_account(accountId, name, environment):
    null = None
    return dumps({
        "accountId": accountId,
        "deliveryAddress": {
            "address": "ERVEN 14-18",
            "city": "CHAMDOR - ROODEKRANS",
            "state": "Free State",
            "zipcode": "9301"
        },
        "deliveryCenterId": accountId,
        "deliveryScheduleId": accountId,
        "liquorLicense": [
            {
                "description": null,
                "expirationDate": "2022-12-31",
                "number": "GAU/" + accountId,
                "status": "VALID",
                "type": "PERMANENT"
            }
        ],
        "minimumOrder": {
            "type": "PRODUCT_QUANTITY",
            "value": 5
        },
        "name": name,
        "owner": {
            "email": accountId + "@mailinator.com",
            "firstName": name,
            "lastName": environment.upper(),
            "phone": 11999999999
        },
        "paymentMethods": [
            "CASH"
        ],
        "priceListId": accountId,
        "salesRepresentative": {
            "email": "N/A",
            "name": "DORINAH",
            "phone": "072 726 1722"
        },
        "status": "ACTIVE",
        "taxId": accountId
    })

# Payload Middleware DR account
def get_middleware_payload_dr_account(accountId, name, environment):
    null = None
    return dumps({
        "accountId": accountId,
        "deliveryAddress": {
            "address": "ROSA DUARTE:43504 Esq.13,  LOS MINAS SUR",
            "city": "STO DGO  ESTE",
            "state": "STO DGO",
            "zipcode": null
        },
        "deliveryCenterId": accountId,
        "deliveryScheduleId": accountId,
        "liquorLicense": null,
        "minimumOrder": null,
        "paymentTerms": null,
        "name": name,
        "owner": {
            "email": accountId + "@mailinator.com",
            "firstName": name,
            "lastName": environment.upper(),
            "phone": 11999999999
        },
        "paymentMethods": [
            "CASH",
            "CREDIT"
        ],
        "priceListId": accountId,
        "salesRepresentative": {
            "email": "micerveceria@cnd.com.do",
            "name": "TINKA",
            "phone": "0227721277"
        },
        "segment": "16",
        "subSegment": "00011",
        "status": "ACTIVE",
        "taxId": accountId
    })

# Payload Middleware AR account
def get_middleware_payload_ar_account(accountId, name, environment):
    null = None
    return dumps({
        "accountId": accountId,
        "deliveryAddress": {
            "address": "AVDA ALVAREZ THOMAS 1073, CAPITAL FEDERA",
            "city": "CAPITAL FEDERAL",
            "state": "CAPITAL FEDERAL",
            "zipcode": "C1427CCK"
        },
        "deliveryCenterId": accountId,
        "deliveryScheduleId": accountId,
        "liquorLicense": [
            {
                "description": null,
                "expirationDate": "2020-12-31",
                "number": accountId,
                "status": "VALID",
                "type": "PERMANENT"
            }
        ],
        "minimumOrder": {
            "type": "PRODUCT_QUANTITY",
            "value": 5
        },
        "name": name,
        "owner": {
            "email": accountId + "@mailinator.com",
            "firstName": name,
            "lastName": environment.upper(),
            "phone": 11999999999
        },
        "paymentMethods": [
            "CASH"
        ],
        "priceListId": accountId,
        "salesRepresentative": {
            "email": null,
            "name": "ARAMAYO JAVIER",
            "phone": null
        },
        "status": "ACTIVE",
        "taxId": accountId
    })

# Payload Middleware CL account
def get_middleware_payload_cl_account(accountId, name, environment):
    null = None
    return dumps({
        "accountId": accountId,
        "deliveryAddress": {
            "address": "SANTA PETRONILA 230, ESTACION CTRAL.",
            "city": "ESTACION CTRAL.",
            "state": "METROPOLITANA",
            "zipcode": null
        },
        "deliveryCenterId": accountId,
        "deliveryScheduleId": accountId,
        "liquorLicense": [
            {
                "description": null,
                "expirationDate": "2020-12-31",
                "number": accountId,
                "status": "VALID",
                "type": "PERMANENT"
            }
        ],
        "minimumOrder": {
            "type": "PRODUCT_QUANTITY",
            "value": 5
        },
        "name": name,
        "owner": {
            "email": accountId + "@mailinator.com",
            "firstName": name,
            "lastName": environment.upper(),
            "phone": 11999999999
        },
        "paymentMethods": [
            "CASH"
        ],
        "priceListId": accountId,
        "salesRepresentative": {
            "email": null,
            "name": "GENERICO MESA 8",
            "phone": "08102221234"
        },
        "status": "ACTIVE",
        "taxId": accountId
    })

# Payload Microservice ZA account
def get_microservice_payload_za_account(accountId, name, environment):
    null = None
    return dumps({
        "accountId": accountId,
        "channel": null,
        "deliveryAddress": {
            "address": "ERVEN 14-18",
            "city": "CHAMDOR - ROODEKRANS",
            "latitude": null,
            "longitude": null,
            "state": "Free State",
            "zipcode": "9301"
        },
        "deliveryCenterId": accountId,
        "deliveryRegion": null,
        "deliveryRoute": null,
        "deliveryScheduleId": accountId,
        "erpSalesCenter": null,
        "liquorLicense": [],
        "maximumOrder": {
            "paymentMethods": "CASH",
            "type": "ORDER_TOTAL",
            "value": 10000
        },
        "minimumOrder": null,
        "name": name,
        "owner": {
            "email": accountId + "@mailinator.com",
            "firstName": name,
            "lastName": environment.upper(),
            "phone": 11999999999
        },
        "paymentMethods": [
            "CASH"
        ],
        "paymentTerms": null,
        "potential": null,
        "priceListId": accountId,
        "salesRepresentative": {
            "email": "N/A",
            "name": "DORINAH",
            "phone": "072 726 1722"
        },
        "salesRoute": null,
        "segment": "16",
        "status": "ACTIVE",
        "subSegment": "00011",
        "taxId": accountId
    })

# Payload Microservice DR account
def get_microservice_payload_dr_account(accountId, name, environment):
    null = None
    return dumps({
        "accountId": accountId,
        "channel": null,
        "deliveryAddress": {
            "address": "ROSA DUARTE:43504 Esq.13,  LOS MINAS SUR",
            "city": "STO DGO  ESTE",
            "latitude": null,
            "longitude": null,
            "state": "STO DGO",
            "zipcode": null
        },
        "deliveryCenterId": accountId,
        "deliveryRegion": null,
        "deliveryRoute": null,
        "deliveryScheduleId": accountId,
        "erpSalesCenter": null,
        "liquorLicense": [],
        "maximumOrder": {
            "paymentMethods": "CASH",
            "type": "ORDER_TOTAL",
            "value": 10000
        },
        "minimumOrder": null,
        "name": name,
        "owner": {
            "email": accountId + "@mailinator.com",
            "firstName": name,
            "lastName": environment.upper(),
            "phone": 11999999999
        },
        "paymentMethods": [
            "CASH",
            "CREDIT"
        ],
        "paymentTerms": null,
        "potential": null,
        "priceListId": accountId,
        "salesRepresentative": {
            "email": "micerveceria@cnd.com.do",
            "name": "TINKA",
            "phone": "0227721277"
        },
        "salesRoute": null,
        "segment": "16",
        "status": "ACTIVE",
        "subSegment": "00011",
        "taxId": accountId
    })

# Payload Microservice AR account
def get_microservice_payload_ar_account(accountId, name, environment):
    null = None
    return dumps({
        "accountId": accountId,
        "channel": null,
        "deliveryAddress": {
            "address": "AVDA ALVAREZ THOMAS 1073, CAPITAL FEDERA",
            "city": "CAPITAL FEDERAL",
            "latitude": null,
            "longitude": null,
            "state": "CAPITAL FEDERAL",
            "zipcode": "C1427CCK"
        },
        "deliveryCenterId": accountId,
        "deliveryRegion": null,
        "deliveryRoute": null,
        "deliveryScheduleId": accountId,
        "erpSalesCenter": null,
        "liquorLicense": [],
        "maximumOrder": {
            "paymentMethods": "CASH",
            "type": "ORDER_TOTAL",
            "value": 10000
        },
        "minimumOrder": null,
        "name": name,
        "owner": {
            "email": accountId + "@mailinator.com",
            "firstName": name,
            "lastName": environment.upper(),
            "phone": 11999999999
        },
        "paymentMethods": [
            "CASH"
        ],
        "paymentTerms": null,
        "potential": null,
        "priceListId": accountId,
        "salesRepresentative": {
            "email": null,
            "name": "ARAMAYO JAVIER",
            "phone": null
        },
        "salesRoute": null,
        "segment": "16",
        "status": "ACTIVE",
        "subSegment": "00011",
        "taxId": accountId
    })

# Payload Microservice CL account
def get_microservice_payload_cl_account(accountId, name, environment):
    null = None
    return dumps({
        "accountId": accountId,
        "channel": null,
        "deliveryAddress": {
            "address": "SANTA PETRONILA 230, ESTACION CTRAL.",
            "city": "ESTACION CTRAL.",
            "latitude": null,
            "longitude": null,
            "state": "METROPOLITANA",
            "zipcode": null
        },
        "deliveryCenterId": accountId,
        "deliveryRegion": null,
        "deliveryRoute": null,
        "deliveryScheduleId": accountId,
        "erpSalesCenter": null,
        "liquorLicense": [],
        "maximumOrder": {
            "paymentMethods": "CASH",
            "type": "ORDER_TOTAL",
            "value": 10000
        },
        "minimumOrder": null,
        "name": name,
        "owner": {
            "email": accountId + "@mailinator.com",
            "firstName": name,
            "lastName": environment.upper(),
            "phone": 11999999999
        },
        "paymentMethods": [
            "CASH"
        ],
        "paymentTerms": null,
        "potential": null,
        "priceListId": accountId,
        "salesRepresentative": {
            "email": null,
            "name": "GENERICO MESA 8",
            "phone": "08102221234"
        },
        "salesRoute": null,
        "segment": "16",
        "status": "ACTIVE",
        "subSegment": "00011",
        "taxId": accountId
    })

# Payload Microservice BR account
def get_microservice_payload_br_account(accountId, name, environment):
    null = None
    return dumps({
        "accountId": accountId,
        "channel": null,
        "deliveryAddress": {
            "address": "RUA VEREADOR MARIO PEZZI, 770, EXPOSICAO",
            "city": "CAXIAS DO SUL",
            "latitude": null,
            "longitude": null,
            "state": "RS",
            "zipcode": "95084-180"
        },
        "deliveryCenterId": accountId,
        "deliveryRegion": null,
        "deliveryRoute": null,
        "deliveryScheduleId": accountId,
        "erpSalesCenter": null,
        "liquorLicense": [],
        "maximumOrder": {
            "paymentMethods": "CASH",
            "type": "ORDER_TOTAL",
            "value": 10000
        },
        "minimumOrder": null,
        "name": name,
        "owner": {
            "email": accountId + "@mailinator.com",
            "firstName": name,
            "lastName": null,
            "phone": "(54) 3333-3333"
        },
        "paymentMethods": [
            "BANK_SLIP",
            "CASH"
        ],
        "paymentTerms": [{
            "type": "BANK_SLIP",
            "termPeriods": [{
                "days": 1
            },
            {
                "days": 2
            },
            {
                "days": 3
            },
            {
                "days": 4
            },
            {
                "days": 5
            },
            {
                "days": 6
            },
            {
                "days": 7
            },
            {
                "days": 8
            },
            {
                "days": 9
            },
            {
                "days": 10
            },
            {
                "days": 11
            },
            {
                "days": 12
            },
            {
                "days": 13
            },
            {
                "days": 14
            },
            {
                "days": 15
            },
            {
                "days": 18
            },
            {
                "days": 20
            },
            {
                "days": 21
            }]
        }],
        "potential": null,
        "priceListId": accountId,
        "salesRepresentative": {
            "email": null,
            "name": "VD AS CDD CAXIAS **cpf inext**",
            "phone": "(00) 0000-0000"
        },
        "salesRoute": null,
        "segment": "16",
        "status": "ACTIVE",
        "subSegment": "00011",
        "taxId": accountId
    })

# Return middleware payload create account
# (DO, ZA, AR, CL)
def get_middleware_payload_create_account(zone, accountId, name, environment):
    switcher = {
        'DO': get_middleware_payload_dr_account,
        'ZA': get_middleware_payload_za_account,
        'AR': get_middleware_payload_ar_account,
        'CL': get_middleware_payload_cl_account,
    }

    function = switcher.get(zone, "")
    if function != '':
        return function(accountId, name, environment)

# Return microservice payload create account
# (DO, ZA, AR, CL, BR)
def get_microservice_payload_create_account(zone, accountId, name, environment):
    switcher = {
        'DO': get_microservice_payload_dr_account,
        'ZA': get_microservice_payload_za_account,
        'AR': get_microservice_payload_ar_account,
        'CL': get_microservice_payload_cl_account,
        'BR': get_microservice_payload_br_account,
    }

    function = switcher.get(zone, "")
    if function != '':
        return function(accountId, name, environment)

# Clear terminal
def clearTerminal():
    os.system('clear')

# kill application
def finishApplication():
    sys.exit()

# Print init menu application
def printAvailableOptions(selectionStructure):
    if selectionStructure == '1' or selectionStructure == '2':
        print(text.White + str(1), text.Yellow + "Create Account" + text.ResetAll)
        print(text.White + str(2), text.Yellow + "Input Products In Account" + text.ResetAll)
        print(text.White + str(3), text.Yellow + "Input Credit In Account" + text.ResetAll)
        print(text.White + str(4), text.Yellow + "Input Delivery Window In Account" + text.ResetAll)
        if selectionStructure == '2':
            print(text.White + str(5), text.Yellow + "Input Discount By Payment Method" + text.ResetAll)
            print(text.White + str(6), text.Yellow + "Input Discount By Delivery Date" + text.ResetAll)
            print(text.White + str(7), text.Yellow + "Input Discount By Sku" + text.ResetAll)
            print(text.White + str(8), text.Yellow + "Input Free Goods Selection" + text.ResetAll)

        print(text.White + str(0), text.White + text.BackgroundRed + "Exit" + text.ResetAll)
        selection = input("Please select: ")
        while validateOptionRequestSelection(selection) == 'false':
            print(text.Red + '\n- Invalid option')
            print(text.White + str(1), text.Yellow + "Create Account" + text.ResetAll)
            print(text.White + str(2), text.Yellow + "Input Products In Account" + text.ResetAll)
            print(text.White + str(3), text.Yellow + "Input Credit In Account" + text.ResetAll)
            print(text.White + str(4), text.Yellow + "Input Delivery Window In Account" + text.ResetAll)
            if selectionStructure == '2':
                print(text.White + str(5), text.Yellow + "Input Discount By Payment Method" + text.ResetAll)
                print(text.White + str(6), text.Yellow + "Input Discount By Delivery Date" + text.ResetAll)
                print(text.White + str(7), text.Yellow + "Input Discount By Sku" + text.ResetAll)
                print(text.White + str(8), text.Yellow + "Input Free Goods Selection" + text.ResetAll)

            print(text.White + str(0), text.White + text.BackgroundRed + "Exit" + text.ResetAll)
            selection = input("Please select: ")

    elif selectionStructure == '3':
        print(text.White + str(1), text.Yellow + "Open Browser" + text.ResetAll)
        print(text.White + str(0), text.White + text.BackgroundRed + "Exit" + text.ResetAll)
        selection = input("Please select: ")
        while validateOptionRequestSelection(selection, 'true') == 'false':
            print(text.Red + '\n- Invalid option')
            print(text.White + str(1), text.Yellow + "Open Browser" + text.ResetAll)
            print(text.White + str(0), text.White + text.BackgroundRed + "Exit" + text.ResetAll)
            selection = input("Please select: ")
    
    else:
        finishApplication()

    return selection

# Print welcome menu application
def printWelcomeScript():
    print(text.White + " 🄰🄽🅃🄰🅁🄲🅃🄸🄲🄰 🄰🅄🅃🄾🄼🄰🅃🄸🄾🄽 🅂🄲🅁🄸🄿🅃 " + text.ResetAll)
    print(text.White + "Choose which backend you want to run a service for" + text.ResetAll)

# Print structure menu application
def printStructureMenu():
    print(text.White + str(1), text.Yellow + "Middleware (ZA, DO, AR, CH)" + text.ResetAll)
    print(text.White + str(2), text.Yellow + "MicroService" + text.ResetAll)
    print(text.White + str(3), text.Yellow + "Extras" + text.ResetAll)
    print(text.White + str(4), text.Yellow + "Close application" + text.ResetAll)
    structure = input(text.White + "Choose which backend you want to run a service for: " + text.ResetAll)
    while validateStructure(structure) == 'false':
        print(text.Red + '\n- Invalid option')
        print(text.White + str(1), text.Yellow + "Middleware (ZA, DO, AR, CH)" + text.ResetAll)
        print(text.White + str(2), text.Yellow + "MicroService" + text.ResetAll)
        print(text.White + str(3), text.Yellow + "Extras" + text.ResetAll)
        print(text.White + str(4), text.Yellow + "Close application" + text.ResetAll)
        structure = input(text.White + "Choose which backend you want to run a service for: " + text.ResetAll)

    return structure

# Print account id menu application
def printAccountIdMenu():
    abi_id = input("ID AB-Inbev (Must contain 10 characters): ")
    while validateAccount(abi_id) == 'false':
        print(text.Red + '\n- Account ID not be empty or must contain 10 characters')
        abi_id = input(text.White + "ID AB-Inbev (Must contain 10 characters): ")

    return abi_id

# Print name menu application
def printNameMenu():
    name = input("Account Name: ")
    while validateName(name) == 'false':
        print(text.Red + '\n- Account Name not be empty')
        name = input(text.White + "Account Name: ")

    return name

# Print zone menu application
def printZoneMenu(isMiddleware='true'):
    if isMiddleware == 'true':
        zone = input("Zone (DO, ZA, AR, CL): ")
        while validateZone('true', zone.upper()) == 'false':
            print(text.Red + '\n- Invalid option')
            zone = input(text.White + "Zone (DO, ZA, AR, CL): ")
    else:
        zone = input("Zone (DO, ZA, AR, CL, BR): ")
        while validateZone('false', zone.upper()) == 'false':
            print(text.Red + '\n- Invalid option')
            zone = input(text.White + "Zone (DO, ZA, AR, CL, BR): ")

    return zone

# Print environment menu application
def printEnvironmentMenu():
    environment = input("Environment (QA, UAT): ")
    while validateEnvironment(environment.upper()) == 'false':
        print(text.Red + '\n- Invalid option')
        environment = input(text.White + "Environment (QA, UAT): ")

    return environment

# Print payment method menu application
def printPaymentMethodMenu(zone):
    if zone == 'BR':
        paymentMethod = input(text.White + "What payment method want apply this rule (1- CASH, 2- BANK SLIP): ")
        while (int(paymentMethod) != 1 and int(paymentMethod) != 2):
            print(text.Red + '\n- Invalid option')
            paymentMethod = input(text.White + "What payment method want apply this rule (1- CASH, 2- BANK SLIP): ")
        
        switcher = {
            '1': 'CASH',
            '2': 'BANK-SLIP',
        }

        value = switcher.get(paymentMethod, 'false')
        return value
    elif zone == 'DR':
        paymentMethod = input(text.White + "What payment method want apply this rule (1- CASH, 2- BANK SLIP): ")
        while (int(paymentMethod) != 1 and int(paymentMethod) != 2):
            print(text.Red + '\n- Invalid option')
            paymentMethod = input(text.White + "What payment method want apply this rule (1- CASH, 2- CREDIT): ")
        
        switcher = {
            '1': 'CASH',
            '2': 'CREDIT',
        }

        value = switcher.get(paymentMethod, 'false')
        return value
    else:
        return 'CASH'

# Print range delivery date menu
def printDeliveryDateMenu():
    listDeliveryWindowDates = list()
    startDeliveryDate = input(text.White + "Enter the start date to apply the discount(format required YYYY-mm-dd): ")
    while validateDate(startDeliveryDate) == 'false':
        print(text.Red + '\n- Invalid date')
        startDeliveryDate = input(text.White + "Enter the start date to apply the discount(format required YYYY-mm-dd): ")

    endDeliveryDate = input(text.White + "Enter the end date to apply the discount(format required YYYY-mm-dd): ")
    while validateDate(endDeliveryDate) == 'false':
        print(text.Red + '\n- Invalid date')
        endDeliveryDate = input(text.White + "Enter the end date to apply the discount(format required YYYY-mm-dd): ")
    
    listDeliveryWindowDates.append({'startDate':startDeliveryDate, 'endDate':endDeliveryDate})

    return listDeliveryWindowDates

# Validate if string it's a date
def validateDate(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return 'false'
