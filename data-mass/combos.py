import sys
from json import dumps
from uuid import uuid1
from random import randint, uniform

# Custom
from helper import *
from classes.text import text

#Input combo simple
def inputComboDiscount(accounts, zone, environment, skuCombo):

    request_url = get_microservice_base_url(environment) + '/combo-relay/accounts'
    idComboDiscount = 'AntD-' + str(randint(1, 100000))
    price = round(uniform(1, 2000), 2)
    originalPrice = round(price / 2, 2)
    score = randint(1, 100)
    discountPercent = randint(1, 25)
    comboDescription = str("Combo Antarctica " + accounts[0] + " Discount")
    request_body = dumps({
        "accounts": accounts,
        "combos": [
            {
                "description": comboDescription,
                "discountPercentOff": discountPercent,
                "endDate": "2045-02-28T00:00:00Z",
                "id": str(idComboDiscount),
                "image": "http://www.ab-inbev.com/b2b/files/combo-icon.png",
                "items": [
                    {
                        "quantity": 100,
                        "sku": skuCombo
                    }
                ],
                "limit": {
                    "daily": 1000,
                    "monthly": 1000
                },
                "originalPrice": originalPrice,
                "price": price,
                "score": score,
                "startDate": "2019-02-01T00:00:00Z",
                "title": comboDescription,
                "type": "D"
            }
        ]
    })

    request_headers = get_header_request(zone, 'false', 'false', 'true')

    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 201:
        print(' -- Skus included on combo -- ')
        print(skuCombo)
        print(' -- Discount Percent-- ')
        print(discountPercent)
        turnComboAvailable(accounts, zone, environment, idComboDiscount)
        return 'success'
    else:
        return response.status_code

#Input combo with free goods
def inputComboWithFreeGoods(accounts, zone, environment, skuCombo, skusFreeGoods):

    request_url = get_microservice_base_url(environment) + '/combo-relay/accounts'
    idComboWithFreeGoods = 'AntWF-' + str(randint(1, 100000))
    price = round(uniform(1, 2000), 2)
    originalPrice = round(price / 2, 2)
    score = randint(1, 100)
    discountPercent = randint(1, 25)
    comboDescription = str("Combo Antarctica " + accounts[0] + " With FreeGoods")
    request_body = dumps({
        "accounts": accounts,
        "combos": [
            {
                "description": comboDescription,
                "discountPercentOff": discountPercent,
                "endDate": "2045-02-28T00:00:00Z",
                "id": str(idComboWithFreeGoods),
                "image": "http://www.ab-inbev.com/b2b/files/combo-icon.png",
                "freeGoods": {
                    "quantity": 1,
                    "skus": skusFreeGoods
                },
                "items": [
                    {
                        "quantity": 100,
                        "sku": skuCombo
                    }
                ],
                "limit": {
                    "daily": 1000,
                    "monthly": 1000
                },
                "originalPrice": originalPrice,
                "price": price,
                "score": score,
                "startDate": "2019-02-01T00:00:00Z",
                "title": comboDescription,
                "type": "FG"
            }
        ]
    })

    request_headers = get_header_request(zone, 'false', 'false', 'true')

    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 201:
        print(' -- Skus included on combo -- ')
        print(skuCombo)
        print(' -- Discount Percent-- ')
        print(discountPercent)
        print(' -- Skus free goods included on combo -- ')
        print(skusFreeGoods)
        turnComboAvailable(accounts, zone, environment, idComboWithFreeGoods)
        return 'success'
    else:
        return response.status_code

#Input combo only free goods
def inputComboOnlyFreeGoods(accounts, zone, environment, skusFreeGoods):

    request_url = get_microservice_base_url(environment) + '/combo-relay/accounts'
    idComboOnlyFreeGoods = 'AntOF-' + str(randint(1, 100000))
    price = round(uniform(1, 2000), 2)
    originalPrice = round(price / 2, 2)
    score = randint(1, 100)
    discountPercent = randint(1, 25)
    comboDescription = str("Combo Antarctica " + accounts[0] + " Only FreeGoods")
    request_body = dumps({
        "accounts": accounts,
        "combos": [
            {
                "description": comboDescription,
                "discountPercentOff": discountPercent,
                "endDate": "2045-02-28T00:00:00Z",
                "id": str(idComboOnlyFreeGoods),
                "image": "http://www.ab-inbev.com/b2b/files/combo-icon.png",
                "freeGoods": {
                    "quantity": 1,
                    "skus": skusFreeGoods
                },
                "limit": {
                    "daily": 1000,
                    "monthly": 1000
                },
                "originalPrice": originalPrice,
                "price": price,
                "score": score,
                "startDate": "2019-02-01T00:00:00Z",
                "title": comboDescription,
                "type": "FG"
            }
        ]
    })

    request_headers = get_header_request(zone, 'false', 'false', 'true')

    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 201:
        print(' -- Discount Percent-- ')
        print(discountPercent)
        print(' -- Skus free goods included on combo -- ')
        print(skusFreeGoods)
        turnComboAvailable(accounts, zone, environment, idComboOnlyFreeGoods)
        return 'success'
    else:
        return response.status_code

#Turn combo quantity available
def turnComboAvailable(accounts, zone, environment, idCombo):
    accountId = accounts[0]
    request_url = get_microservice_base_url(environment) + '/combo-relay/consumption'
    request_body = dumps([{
        "accountId": str(accountId),
        "combos": [
            {
                "comboId": str(idCombo),
                "consumedLimit": {
                    "daily": 0,
                    "monthly": 0
                }
            }
        ]
    }])

    request_headers = get_header_request(zone, 'false', 'false', 'true')

    response = place_request('POST', request_url, request_body, request_headers)
    if response.status_code == 201:
        print(text.Green + '-- Combo ' + idCombo + ' are available')
    else:
        print(text.Red + '-- [Combo] Something went wrong in turn combo ' + idCombo + ' available')
