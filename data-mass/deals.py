import sys
from json import dumps
from uuid import uuid1
from random import randint, uniform

# Custom
from helpers.common import *

def create_discount_auto(abi_id, sku_discount, zone, environment):
    account_group_id = list()
    sku_group_id = list()
    account = create_account_group(abi_id, zone, environment)
    account_group_id.append(account)
    sku = create_sku_group(sku_discount, zone, environment)
    sku_group_id.append(sku)
    deal_id = "DM-" + str(randint(1, 100000))

    dict_values = {
        "accountGroupIds": account_group_id,
        "description": abi_id + " DEAL TYPE DISCOUNT",
        "endDate": "2040-03-31T23:59:59.999Z",
        "id": deal_id,
        "promotionsRanking": 100,
        "score": 0,
        "skuGroupIds": sku_group_id,
        "startDate": "2019-03-04T00:00:00.000Z",
        "title": abi_id + " DEAL TYPE DISCOUNT",
        "type": "DISCOUNT"
    }

    # Create body
    list_dict_values = create_list(dict_values)
    request_body = convert_json_to_string(list_dict_values)

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "true", "false")

    # Get base URL
    request_url = get_microservice_base_url(environment) + "/promotion-relay/"

    # Send request
    response = place_request("POST", request_url, request_body, request_headers)

    if response.status_code != 202:
        return "false"
    else:
        return deal_id

def create_account_group(abi_id, zone, environment):
    accounts = list()
    accounts.append(abi_id)
    account_group_id = "DM-" + str(randint(1, 100000))

    dict_values = {
        "accountGroupId": account_group_id,
        "accounts": accounts
    }

    # Create body
    list_dict_values = create_list(dict_values)
    request_body = convert_json_to_string(list_dict_values)

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "true", "false")

    # Get base URL
    request_url = get_microservice_base_url(environment) + "/promotion-relay/account-group"

    # Send request
    response = place_request("POST", request_url, request_body, request_headers)

    if response.status_code != 202:
        print(text.Red + "\n- [Deals - Account Group] Something went wrong, please try again")
        finishApplication()
    else:
        return account_group_id

def create_sku_group(sku, zone, environment):
    skus = list()
    skus.append(sku)
    sku_group_id = "DM-" + str(randint(1, 100000))

    dict_values = {
        "skuGroupId": sku_group_id,
        "skus": skus
    }

    # Create body
    list_dict_values = create_list(dict_values)
    request_body = convert_json_to_string(list_dict_values)

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "true", "false")

    # Get base URL
    request_url = get_microservice_base_url(environment) + "/promotion-relay/sku-group"

    # Send request
    response = place_request("POST", request_url, request_body, request_headers)

    if response.status_code != 202:
        print(text.Red + "\n- [Deals - SKU Group] Something went wrong, please try again")
        finishApplication()
    else:
        return sku_group_id

def input_discount_by_sku(accounts, zone, environment, skus, type_discount, value_discount):
    request_url = get_microservice_base_url(environment) + "/cart-calculation-relay/deals"

    if type_discount == 1:
        strTypeDiscount = "percentOff"
    else:
        strTypeDiscount = "amountOff"

    request_body = dumps({
        "accounts": accounts,
        "deals": [
        {
            "dealId": "DM-" + str(randint(1, 100000)),
            "dealRules": {
                "dealSKURule": {
                    "skus": skus,
                    "minimumQuantity": 1
                }
            },
            "dealOutput": {
                "dealOutputSKUDiscount": {
                    "skus": skus,
                    strTypeDiscount: value_discount
                }
            },
            "externalId": "DM-" + str(randint(1, 100000)),
            "accumulationType": "UNIQUE"
        }
    ]})

    request_headers = get_header_request(zone, "false", "false", "false", "false")

    response = place_request("PUT", request_url, request_body, request_headers)

    if response.status_code == 202:
	    return "success"
    else:
        return response.status_code

# def create_promotion_discount(abi_id, zone, environment, title, description, sku, list_dates, promo_type):
#     request_body = define_promotion_payload(abi_id, zone, environment, title, description, sku, list_dates, promo_type)

#     # Get header request
#     request_headers = get_header_request(zone, "false", "true", "false", "false")

#     # Get base URL
#     request_url = get_microservice_base_url(environment) + "/"

#     # Send request
#     response = place_request("POST", request_url, request_body, request_headers)

#     if response.status_code != 202:
#         print(text.Red + "\n- [Deals] Something went wrong, please try again")

# def define_promotion_payload(abi_id, zone, environment, title, description, skus, list_dates, promo_type):
#     account_group_id = create_account_group(abi_id, zone, environment)
#     sku_group_id = create_sku_group(skus, zone, environment)

#     free_good_group_id = None
#     if (promo_type == "FREE_GOOD" or promo_type == "STEPPED_FREE_GOOD"):
#         free_good_group_id = create_free_good_group(skus, zone, environment)

#     # Create file path
#     path = os.path.abspath(os.path.dirname(__file__))
#     file_path = os.path.join(path, "data/create_promotion_payload.json")

#     # Load JSON file
#     with open(file_path) as file:
#         json_data = json.load(file)

#     dict_values = {
#         'accountGroupIds': account_group_id,
#         'description': description,
#         'endDate': list_dates['endDate'],
#         'freeGoodGroupIds': free_good_group_id,
#         'id': 'DM-' + str(randint(1, 100000)),
#         'skuGroupIds': sku_group_id,
#         'startDate': list_dates['startDate'],
#         'title': title,
#         'type': promo_type
#     }

#     for key in dict_values.keys():
#         json_object = update_value_to_json(json_data, key, dict_values[key])

#     # Create body
#     request_body = convert_json_to_string(json_object)

#     return request_body



def create_free_good_group(skus, zone, environment):
    free_good_group_id = "DM-" + str(randint(1, 100000))

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "data/create_sku_group_payload.json")

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'freeGoodGroupId': free_good_group_id,
        'skus': skus
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    print(request_body)

    # Get header request
    request_headers = get_header_request(zone, "false", "true", "false", "false")

    # Get base URL
    request_url = get_microservice_base_url(environment) + "/free-good-group"

    # Send request
    response = place_request("POST", request_url, request_body, request_headers)

    print(response.status_code)

    if response.status_code != 202:
        print(text.Red + "\n- [Deals - Free Good Group] Something went wrong, please try again")

    return free_good_group_id

