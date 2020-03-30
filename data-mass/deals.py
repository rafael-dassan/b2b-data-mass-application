import sys
from json import dumps
from uuid import uuid1
from random import randint, uniform
from common import *

default_text_color = text.Cyan

def input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone, environment):
    account_group_id = list()
    sku_group_id = list()
    free_good_group_id = list()

    account = create_account_group(abi_id, zone, environment)
    account_group_id.append(account)

    sku = create_sku_group(deal_sku, zone, environment)
    sku_group_id.append(sku)

    if free_good_sku != []:
        free_good_group_id.append(sku)
    else:
        free_good_group_id = free_good_sku

    deal_id = "DM-" + str(randint(1, 100000))

    dict_values = {
        "accountGroupIds": account_group_id,
        "description": abi_id + " DEAL TYPE " + deal_type,
        "endDate": "2040-03-31T23:59:59.999Z",
        "freeGoodGroupIds": free_good_group_id,
        "id": deal_id,
        "promotionsRanking": 100,
        "score": 0,
        "skuGroupIds": sku_group_id,
        "startDate": "2019-03-04T00:00:00.000Z",
        "title": abi_id + " DEAL TYPE " + deal_type,
        "type": deal_type
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
        return list_dict_values

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

# Input discount business rules to Cart Calculation microservice
def input_discount_to_cart_calculation(deal_id, accounts, zone, environment, skus, discount_type, discount_value, minimum_quantity):
    # Get base URL
    request_url = get_microservice_base_url(environment) + "/cart-calculation-relay/deals"

    # Create body
    request_body = dumps({
        "accounts": accounts,
        "deals": [
        {
            "dealId": deal_id,
            "dealRules": {
                "dealSKURule": {
                    "skus": skus,
                    "minimumQuantity": minimum_quantity
                }
            },
            "dealOutput": {
                "dealOutputSKUDiscount": {
                    "skus": skus,
                    discount_type: discount_value
                }
            },
            "externalId": deal_id
        }
    ]})

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "false", "false")

    # Send request
    response = place_request("PUT", request_url, request_body, request_headers)

    if response.status_code == 202:
	    return "success"
    else:
        return response.status_code

def input_stepped_discount_to_cart_calculation(deal_id, accounts, zone, environment, skus, discount_type, index_range, discount_range):
    # Get base URL
    request_url = get_microservice_base_url(environment) + "/cart-calculation-relay/deals"

    # Create body
    request_body = dumps({
        "accounts": accounts,
        "deals": [
            {
                "dealId": deal_id,
                "dealRules": {
                    "dealSKUScaledRule": {
                        "skus": skus,
                        "ranges": [
                            {
                                "rangeIndex": 0,
                                "from": index_range[0],
                                "to": index_range[1]
                            },
                            {
                                "rangeIndex": 1,
                                "from": index_range[2],
                                "to": index_range[3]
                            }
                        ]
                    }
                },
                "dealOutput": {
                    "dealOutputSKUScaledDiscount": [
                        {
                            "rangeIndex": 0,
                            "skus": skus,
                            discount_type: discount_range[0],
                        },
                        {
                            "rangeIndex": 1,
                            "skus": skus,
                            discount_type: discount_range[1],
                        }
                    ]
                },
                "externalId": deal_id
            }
    ]})

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "false", "false")

    # Send request
    response = place_request("PUT", request_url, request_body, request_headers)

    if response.status_code == 202:
	    return "success"
    else:
        return response.status_code

def input_free_good_to_cart_calculation(deal_id, accounts, zone, environment, skus, minimum_quantity, quantity):
    # Get base URL
    request_url = get_microservice_base_url(environment) + "/cart-calculation-relay/deals"

    # Create body
    request_body = dumps({
        "accounts": accounts,
        "deals": [
            {
                "dealId": deal_id,
                "dealRules": {
                    "dealSKURule": {
                        "skus": skus,
                        "minimumQuantity": minimum_quantity
                    }
                },
                "dealOutput": {
                    "dealOutputFreeGoods": {
                        "skus": skus,
                        "quantity": quantity,
                        "measureUnit": "UNIT"
                    }
                },
                "externalId": deal_id
            }
    ]})

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "false", "false")

    # Send request
    response = place_request("PUT", request_url, request_body, request_headers)

    if response.status_code == 202:
	    return "success"
    else:
        return response.status_code

def input_stepped_free_good_to_cart_calculation(deal_id, accounts, zone, environment, skus, index_range, quantity_range):
    # Get base URL
    request_url = get_microservice_base_url(environment) + "/cart-calculation-relay/deals"

    # Create body
    request_body = dumps({
        "accounts": accounts,
        "deals": [
            {
                "dealId": deal_id,
                "dealRules": {
                    "dealSKUScaledRule": {
                        "skus": skus,
                        "ranges": [
                            {
                                "rangeIndex": 0,
                                "from": index_range[0],
                                "to": index_range[1]
                            },
                            {
                                "rangeIndex": 1,
                                "from": index_range[2],
                                "to": index_range[3]
                            }
                        ]
                    }
                },
                "dealOutput": {
                    "dealOutputScaledFreeGoods": [
                        {
                            "rangeIndex": 0,
                            "skus": skus,
                            "quantity": quantity_range[0],
                            "measureUnit": "UNIT"
                        },
                        {
                            "rangeIndex": 1,
                            "skus": skus,
                            "quantity": quantity_range[1],
                            "measureUnit": "UNIT"
                        }
                    ]
                },
                "externalId": deal_id
            }
    ]})

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "false", "false")

    # Send request
    response = place_request("PUT", request_url, request_body, request_headers)

    if response.status_code == 202:
	    return "success"
    else:
        return response.status_code

def input_discount_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone, environment):
    free_good_sku = []
    minimum_quantity = printMinimumQuantityMenu()
    discount_type = printDiscountTypeMenu()
    discount_value = printDiscountValueMenu(discount_type)
    promotion_response = input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone.upper(), environment.upper())
    cart_response = input_discount_to_cart_calculation(promotion_response[0]["id"], accounts, zone.upper(), environment.upper(), skus, discount_type, discount_value, minimum_quantity)

    if promotion_response == "false" and cart_response != "success":
        print(text.Red + "\n- [Deals] Something went wrong, please try again")
    else:
        print(text.Green + "\n- Deal successfully registered")
        print(default_text_color + "\n- Deal ID: " + promotion_response[0]["id"])
        print(default_text_color + "- Buy at least " + str(minimum_quantity) + " of " + deal_sku + " and get " + str(discount_value) + " " + str(discount_type) + " discount")

def input_stepped_discount_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone, environment):
    free_good_sku = []
    index_range = printIndexRangeMenu()
    discount_type = printDiscountTypeMenu()
    discount_range = printDiscountRangeMenu()
    promotion_response = input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone.upper(), environment.upper())
    cart_response = input_stepped_discount_to_cart_calculation(promotion_response[0]["id"], accounts, zone.upper(), environment.upper(), skus, discount_type, index_range, discount_range)

    if promotion_response == "false" and cart_response != "success":
        print(text.Red + "\n- [Deals] Something went wrong, please try again")
    else:
        print(text.Green + "\n- Deal successfully registered")
        print(default_text_color + "\n- Deal ID: " + promotion_response[0]["id"])
        print(default_text_color + "- Buy from " + str(index_range[0]) + " to " + str(index_range[1]) + " of " + deal_sku + " and get " + str(discount_range[0]) + " " + str(discount_type) + " discount")
        print(default_text_color + "- Buy from " + str(index_range[2]) + " to " + str(index_range[3]) + " of " + deal_sku + " and get " + str(discount_range[1]) + " " + str(discount_type) + " discount")

def input_free_good_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone, environment):
    free_good_sku = deal_sku
    minimum_quantity = printMinimumQuantityMenu()
    quantity = printQuantityMenu()
    promotion_response = input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone.upper(), environment.upper())
    cart_response = input_free_good_to_cart_calculation(promotion_response[0]["id"], accounts, zone.upper(), environment.upper(), skus, minimum_quantity, quantity)

    if promotion_response == "false" and cart_response != "success":
        print(text.Red + "\n- [Deals] Something went wrong, please try again")
    else:
        print(text.Green + "\n- Deal successfully registered")
        print(default_text_color + "\n- Deal ID: " + promotion_response[0]["id"])
        print(default_text_color + "- Buy at least " + str(minimum_quantity) + " of " + deal_sku + " and get " + str(quantity) + " of " + deal_sku + " for free")

def input_stepped_free_good_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone, environment):
    free_good_sku = deal_sku
    index_range = printIndexRangeMenu()
    quantity_range = printQuantityRangeMenu()
    promotion_response = input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone.upper(), environment.upper())
    cart_response = input_stepped_free_good_to_cart_calculation(promotion_response[0]["id"], accounts, zone.upper(), environment.upper(), skus, index_range, quantity_range)

    if promotion_response == "false" and cart_response != "success":
        print(text.Red + "\n- [Deals] Something went wrong, please try again")
    else:
        print(text.Green + "\n- Deal successfully registered")
        print(default_text_color + "\n- Deal ID: " + promotion_response[0]["id"])
        print(default_text_color + "- Buy from " + str(index_range[0]) + " to " + str(index_range[1]) + " of " + deal_sku + " and get " + str(quantity_range[0]) + " of " + deal_sku + " for free")
        print(default_text_color + "- Buy from " + str(index_range[2]) + " to " + str(index_range[3]) + " of " + deal_sku + " and get " + str(quantity_range[1]) + " of " + deal_sku + " for free")