import sys
from json import dumps
from uuid import uuid1
from random import randint, uniform
from common import *
from classes.text import text

def input_combo_type_discount(abi_id, zone, environment, combo_item, discount_value):
    combo_id = "DM-" + str(randint(1, 100000))
    accounts = list()
    accounts.append(abi_id)
    
    # Get base URL
    request_url = get_microservice_base_url(environment) + "/combo-relay/accounts"
    
    original_price = get_sku_price(abi_id, combo_item, zone, environment)
    price = round(original_price - original_price * (discount_value/100), 2)
    score = randint(1, 100)

    # Create body
    request_body = dumps({
        "accounts": accounts,
        "combos": [
            {
                "description": "Combo " + combo_id + " type discount",
                "discountPercentOff": discount_value,
                "endDate": "2045-02-28T00:00:00Z",
                "id": combo_id,
                "image": "http://www.ab-inbev.com/b2b/files/combo-icon.png",
                "items": [
                    {
                        "quantity": 1,
                        "sku": combo_item
                    }
                ],
                "limit": {
                    "daily": 500,
                    "monthly": 500
                },
                "originalPrice": original_price,
                "price": price,
                "score": score,
                "startDate": "2019-02-01T00:00:00Z",
                "title": "Combo " + combo_id + " type discount",
                "type": "D"
            }
        ]
    })

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "true", "false")

    # Send request
    response = place_request("POST", request_url, request_body, request_headers)

    if response.status_code == 201:
        print(text.Green + "\n- Combo successfully registered")
        print(text.White + "\n- Combo ID: " + combo_id)
        update_combo_consumption(abi_id, zone, environment, combo_id)
        return "success"
    else:
        return response.status_code

def input_combo_type_free_good(abi_id, zone, environment, combo_item, combo_free_good):
    combo_id = "DM-" + str(randint(1, 100000))
    accounts = list()
    accounts.append(abi_id)

    # Get base URL
    request_url = get_microservice_base_url(environment) + "/combo-relay/accounts"

    price = get_sku_price(abi_id, combo_item, zone, environment)
    score = randint(1, 100)

    # Create body
    request_body = dumps({
        "accounts": accounts,
        "combos": [
            {
                "description": "Combo " + combo_id + " type free good",
                "discountPercentOff": 0,
                "endDate": "2045-02-28T00:00:00Z",
                "id": combo_id,
                "image": "http://www.ab-inbev.com/b2b/files/combo-icon.png",
                "freeGoods": {
                    "quantity": 1,
                    "skus": combo_free_good
                },
                "items": [
                    {
                        "quantity": 1,
                        "sku": combo_item
                    }
                ],
                "limit": {
                    "daily": 500,
                    "monthly": 500
                },
                "originalPrice": price,
                "price": price,
                "score": score,
                "startDate": "2019-02-01T00:00:00Z",
                "title": "Combo " + combo_id + " type free good",
                "type": "FG"
            }
        ]
    })

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "true", "false")

    # Send request
    response = place_request("POST", request_url, request_body, request_headers)

    if response.status_code == 201:
        print(text.Green + "\n- Combo successfully registered")
        print(text.White + "\n- Combo ID: " + combo_id)
        update_combo_consumption(abi_id, zone, environment, combo_id)
        return "success"
    else:
        return response.status_code

def input_combo_free_good_only(abi_id, zone, environment, combo_free_good):
    combo_id = "DM-" + str(randint(1, 100000))
    accounts = list()
    accounts.append(abi_id)
    score = randint(1, 100)

    # Get base URL
    request_url = get_microservice_base_url(environment) + "/combo-relay/accounts"
    
    # Create body
    request_body = dumps({
        "accounts": accounts,
        "combos": [
            {
                "description": "Combo " + combo_id + " with only free goods",
                "discountPercentOff": 0,
                "endDate": "2045-02-28T00:00:00Z",
                "id": combo_id,
                "image": "http://www.ab-inbev.com/b2b/files/combo-icon.png",
                "freeGoods": {
                    "quantity": 1,
                    "skus": combo_free_good
                },
                "limit": {
                    "daily": 500,
                    "monthly": 500
                },
                "originalPrice": 0,
                "price": 0,
                "score": score,
                "startDate": "2019-02-01T00:00:00Z",
                "title": "Combo " + combo_id + " with only free goods",
                "type": "FG"
            }
        ]
    })

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "true", "false")

    # Send request
    response = place_request("POST", request_url, request_body, request_headers)

    if response.status_code == 201:
        print(text.Green + "\n- Combo successfully registered")
        print(text.White + "\n- Combo ID: " + combo_id)
        update_combo_consumption(abi_id, zone, environment, combo_id)
        return "success"
    else:
        return response.status_code

# Turn combo quantity available
def update_combo_consumption(abi_id, zone, environment, combo_id):
    # Get base URL
    request_url = get_microservice_base_url(environment) + "/combo-relay/consumption"
    
    request_body = dumps([{
        "accountId": abi_id,
        "combos": [
            {
                "comboId": combo_id,
                "consumedLimit": {
                    "daily": 0,
                    "monthly": 0
                }
            }
        ]
    }])

    request_headers = get_header_request(zone, "false", "false", "true", "false")

    response = place_request("POST", request_url, request_body, request_headers)

    if response.status_code != 201:
        print(text.Red + "\n- [Combo] Something went wrong while updating the combo consumption")