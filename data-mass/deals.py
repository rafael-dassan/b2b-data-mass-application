from json import dumps, loads
from random import randint
from common import *
from tabulate import tabulate


def input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone, environment):
    account_group_id = list()
    sku_group_id = list()
    free_good_group_id = list()

    account = create_account_group(abi_id, zone, environment)
    account_group_id.append(account)

    sku = create_sku_group(deal_sku, zone, environment)
    sku_group_id.append(sku)

    if free_good_sku != []:
        free_good = create_free_good_group(deal_sku, zone, environment)
        free_good_group_id.append(free_good)
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


def create_free_good_group(sku, zone, environment):
    skus = list()
    skus.append(sku)
    free_good_group_id = "DM-" + str(randint(1, 100000))

    dict_values = {
        "freeGoodGroupId": free_good_group_id,
        "skus": skus
    }

    # Create body
    list_dict_values = create_list(dict_values)
    request_body = convert_json_to_string(list_dict_values)

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "true", "false")

    # Get base URL
    request_url = get_microservice_base_url(environment) + "/promotion-relay/free-good-group"

    # Send request
    response = place_request("POST", request_url, request_body, request_headers)

    if response.status_code != 202:
        print(text.Red + "\n- [Deals - Free Good Group] Something went wrong, please try again")
        finishApplication()
    else:
        return free_good_group_id


# Input discount business rules to Cart Calculation microservice
def input_discount_to_cart_calculation(deal_id, accounts, zone, environment, skus, discount_type, discount_value, minimum_quantity):
    product_sku = skus[0]['sku']
    
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
                    "skus": [product_sku],
                    "minimumQuantity": minimum_quantity
                }
            },
            "dealOutput": {
                "dealOutputSKUDiscount": {
                    "skus": [product_sku],
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

def input_stepped_discount_with_qtd_to_cart_calculation(deal_id, accounts, zone, environment, skus, quantity, index_range, discount_type, discount_range):
    product_sku = skus[0]['sku']
    
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
                        "skus": [product_sku],
                        "ranges": [
                            {
                                "rangeIndex": 0,
                                "from": index_range[0],
                                "to": index_range[1]
                            }
                        ]
                    }
                },
                "dealOutput": {
                    "dealOutputSKUScaledDiscount": [
                        {
                            "rangeIndex": 0,
                            "skus": [product_sku],
                            discount_type: discount_range[0],
                            "maxQuantity": quantity
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

def input_stepped_discount_to_cart_calculation(deal_id, accounts, zone, environment, skus, discount_type, index_range, discount_range):
    product_sku = skus[0]['sku']
    
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
                        "skus": [product_sku],
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
                            "skus": [product_sku],
                            discount_type: discount_range[0],
                        },
                        {
                            "rangeIndex": 1,
                            "skus": [product_sku],
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
    product_sku = skus[0]['sku']
    
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
                        "skus": [product_sku],
                        "minimumQuantity": minimum_quantity
                    }
                },
                "dealOutput": {
                    "dealOutputFreeGoods": {
                        "skus": [product_sku],
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
    product_sku = skus[0]['sku']

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
                        "skus": [product_sku],
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
                            "skus": [product_sku],
                            "quantity": quantity_range[0],
                            "measureUnit": "UNIT"
                        },
                        {
                            "rangeIndex": 1,
                            "skus": [product_sku],
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
    discount_type = print_discount_type_menu()
    discount_value = printDiscountValueMenu(discount_type)

    promotion_response = input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone.upper(), environment.upper())

    if zone == "CO" or zone == "MX":
        cart_response = input_discount_to_cart_calculation_v2(promotion_response, accounts, zone.upper(), environment.upper(), skus, discount_type, discount_value, minimum_quantity)
    else:
        cart_response = input_discount_to_cart_calculation(promotion_response, accounts, zone.upper(), environment.upper(), skus, discount_type, discount_value, minimum_quantity)

    if promotion_response == "false" or cart_response != "success":
        print(text.Red + "\n- [Deals] Something went wrong, please try again")
    else:
        print(text.Green + "\n- Deal successfully registered")
        print(text.default_text_color + "\n- Deal ID: " + promotion_response)
        print(text.default_text_color + "- Buy at least " + str(minimum_quantity) + " of " + deal_sku + " and get " + str(discount_value) + " " + str(discount_type) + " discount")

def input_stepped_discount_with_qtd_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone, environment):
    free_good_sku = []
    index_range = print_index_range_menu(2)
    discount_type = print_discount_type_menu()
    discount_range = print_discount_range_menu(1)
    quantity = input(text.default_text_color + "Quantity: ")

    promotion_response = input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone.upper(), environment.upper())

    if zone == "CO" or zone == "MX":
        cart_response = input_stepped_discount_with_qtd_to_cart_calculation_v2(promotion_response, accounts, zone.upper(), environment.upper(), skus, quantity, index_range, discount_type, discount_range)
    else:
        cart_response = input_stepped_discount_with_qtd_to_cart_calculation(promotion_response, accounts, zone.upper(), environment.upper(), skus, quantity, index_range, discount_type, discount_range)

    if promotion_response == "false" or cart_response != "success":
        print(text.Red + "\n- [Deals] Something went wrong, please try again")
    else:
        print(text.Green + "\n- Deal successfully registered")
        print(text.default_text_color + "\n- Deal ID: " + promotion_response)
        print(text.default_text_color + "- Buy from " + str(index_range[0]) + " to " + str(index_range[1]) + " of " + deal_sku + " and get " + str(discount_range[0]) + " " + str(discount_type) + " discount in " + quantity + " items ")

def input_stepped_discount_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone, environment):
    free_good_sku = []
    index_range = print_index_range_menu()
    discount_type = print_discount_type_menu()
    discount_range = print_discount_range_menu()

    promotion_response = input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone.upper(), environment.upper())

    if zone == "CO" or zone == "MX":
        cart_response = input_stepped_discount_to_cart_calculation_v2(promotion_response, accounts, zone.upper(), environment.upper(), skus, discount_type, index_range, discount_range)
    else:
        cart_response = input_stepped_discount_to_cart_calculation(promotion_response, accounts, zone.upper(), environment.upper(), skus, discount_type, index_range, discount_range)

    if promotion_response == "false" or cart_response != "success":
        print(text.Red + "\n- [Deals] Something went wrong, please try again")
    else:
        print(text.Green + "\n- Deal successfully registered")
        print(text.default_text_color + "\n- Deal ID: " + promotion_response)
        print(text.default_text_color + "- Buy from " + str(index_range[0]) + " to " + str(index_range[1]) + " of " + deal_sku + " and get " + str(discount_range[0]) + " " + str(discount_type) + " discount")
        print(text.default_text_color + "- Buy from " + str(index_range[2]) + " to " + str(index_range[3]) + " of " + deal_sku + " and get " + str(discount_range[1]) + " " + str(discount_type) + " discount")

def input_free_good_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone, environment):
    free_good_sku = deal_sku
    minimum_quantity = printMinimumQuantityMenu()
    quantity = printQuantityMenu()

    promotion_response = input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone.upper(), environment.upper())

    if zone == "CO" or zone == "MX" or zone == "AR":
        cart_response = input_free_good_to_cart_calculation_v2(promotion_response, accounts, zone.upper(), environment.upper(), skus, minimum_quantity, quantity)
    else:
        cart_response = input_free_good_to_cart_calculation(promotion_response, accounts, zone.upper(), environment.upper(), skus, minimum_quantity, quantity)

    if promotion_response == "false" or cart_response != "success":
        print(text.Red + "\n- [Deals] Something went wrong, please try again")
    else:
        print(text.Green + "\n- Deal successfully registered")
        print(text.default_text_color + "\n- Deal ID: " + promotion_response)
        print(text.default_text_color + "- Buy at least " + str(minimum_quantity) + " of " + deal_sku + " and get " + str(quantity) + " of " + deal_sku + " for free")

def input_stepped_free_good_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone, environment):
    free_good_sku = deal_sku
    index_range = print_index_range_menu()
    quantity_range = printQuantityRangeMenu()

    promotion_response = input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone.upper(), environment.upper())
    
    if zone == "CO" or zone == "MX":
        cart_response = input_stepped_free_good_to_cart_calculation_v2(promotion_response, accounts, zone.upper(), environment.upper(), skus, index_range, quantity_range)
    else:
        cart_response = input_stepped_free_good_to_cart_calculation(promotion_response, accounts, zone.upper(), environment.upper(), skus, index_range, quantity_range)

    if promotion_response == "false" or cart_response != "success":
        print(text.Red + "\n- [Deals] Something went wrong, please try again")
    else:
        print(text.Green + "\n- Deal successfully registered")
        print(text.default_text_color + "\n- Deal ID: " + promotion_response)
        print(text.default_text_color + "- Buy from " + str(index_range[0]) + " to " + str(index_range[1]) + " of " + deal_sku + " and get " + str(quantity_range[0]) + " of " + deal_sku + " for free")
        print(text.default_text_color + "- Buy from " + str(index_range[2]) + " to " + str(index_range[3]) + " of " + deal_sku + " and get " + str(quantity_range[1]) + " of " + deal_sku + " for free")

#Input free goods in cart calculation relay using v2 deals contract
def input_free_good_to_cart_calculation_v2(deal_id, accounts, zone, environment, skus, minimum_quantity, quantity):
    product_sku = skus[0]['sku']
    
    # Get base URL
    request_url = get_microservice_base_url(environment, "false") + "/cart-calculation-relay/v2/deals"

    dates_payload = return_first_and_last_date_year_payload()

    accumulation_type = ""
    if zone == "AR":
        accumulation_type = "UNIQUE"

    #Inputs for default payload of simple free goods for cart calculation v2
    dict_values = {
        "accounts": accounts,
        "deals[0].dealId": deal_id,
        "deals[0].externalId": deal_id,
        "deals[0].accumulationType": accumulation_type,
        "deals[0].conditions.simulationDateTime[0].startDate": dates_payload['startDate'],
        "deals[0].conditions.simulationDateTime[0].endDate": dates_payload['endDate'],
        "deals[0].conditions.lineItem.skus": [product_sku],
        "deals[0].conditions.lineItem.minimumQuantity": minimum_quantity,
        "deals[0].output.freeGoods.proportion": minimum_quantity,
        "deals[0].output.freeGoods.freeGoods[0].skus[0].sku": product_sku,
        "deals[0].output.freeGoods.freeGoods[0].skus[0].price": skus[0]['price'],
        "deals[0].output.freeGoods.freeGoods[0].quantity": quantity,
        "deals[0].output.freeGoods.freeGoods[1].skus[0].sku": skus[1]['sku'],
        "deals[0].output.freeGoods.freeGoods[1].skus[0].price": skus[1]['price'],
        "deals[0].output.freeGoods.freeGoods[1].skus[1].sku": skus[2]['sku'],
        "deals[0].output.freeGoods.freeGoods[1].skus[1].price": skus[2]['price'],
        "deals[0].output.freeGoods.freeGoods[1].quantity": quantity,
    }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "data/input_simple_freegoods_v2_payload.json")

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "false", "false")

    # Send request
    response = place_request("PUT", request_url, request_body, request_headers)

    if response.status_code == 202:
	    return "success"
    else:
        return response.status_code

#Use deals v2 contract for register stepped free goods on
#cart calculator relay
def input_stepped_free_good_to_cart_calculation_v2(deal_id, accounts, zone, environment, skus, index_range, quantity_range):
    product_sku = skus[0]['sku']
    
    # Get base URL
    request_url = get_microservice_base_url(environment, "false") + "/cart-calculation-relay/v2/deals"

    dates_payload = return_first_and_last_date_year_payload()

    #Inputs for default payload of stepped free goods for cart calculation v2
    dict_values = {
        "accounts": accounts,
        "deals[0].dealId": deal_id,
        "deals[0].externalId": deal_id,
        "deals[0].conditions.simulationDateTime[0].startDate": dates_payload['startDate'],
        "deals[0].conditions.simulationDateTime[0].endDate": dates_payload['endDate'],
        "deals[0].conditions.scaledLineItem.skus": [product_sku],
        "deals[0].conditions.scaledLineItem.ranges[0].from": index_range[0],
        "deals[0].conditions.scaledLineItem.ranges[0].to": index_range[1],
        "deals[0].conditions.scaledLineItem.ranges[1].from": index_range[2],
        "deals[0].conditions.scaledLineItem.ranges[1].to": index_range[3],
        "deals[0].output.scaledFreeGoods.ranges[0].freeGoods[0].skus[0].sku": product_sku,
        "deals[0].output.scaledFreeGoods.ranges[0].freeGoods[0].quantity": quantity_range[0],
        "deals[0].output.scaledFreeGoods.ranges[0].proportion": quantity_range[0],
        "deals[0].output.scaledFreeGoods.ranges[1].freeGoods[0].skus[0].sku": product_sku,
        "deals[0].output.scaledFreeGoods.ranges[1].freeGoods[0].quantity": quantity_range[1],
        "deals[0].output.scaledFreeGoods.ranges[1].proportion": quantity_range[1],
    }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "data/input_stepped_freegods_v2_payload.json")

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "false", "false")

    # Send request
    response = place_request("PUT", request_url, request_body, request_headers)

    if response.status_code == 202:
	    return "success"
    else:
        return response.status_code

# Input deals v2 discount business rules to Cart Calculation microservice
def input_discount_to_cart_calculation_v2(deal_id, accounts, zone, environment, skus, discount_type, discount_value, minimum_quantity):
    product_sku = skus[0]['sku']
    
    if discount_type == "percentOff":
        discount_type = "%"
    else:
        discount_type = "$"
    
    # Get base URL
    request_url = get_microservice_base_url(environment, "false") + "/cart-calculation-relay/v2/deals"

    dates_payload = return_first_and_last_date_year_payload()
    
    #Inputs for default payload of simple discount for cart calculation v2
    dict_values = {
        "accounts": accounts,
        "deals[0].dealId": deal_id,
        "deals[0].externalId": deal_id,
        "deals[0].conditions.simulationDateTime[0].startDate": dates_payload['startDate'],
        "deals[0].conditions.simulationDateTime[0].endDate": dates_payload['endDate'],
        "deals[0].conditions.lineItem.skus": [product_sku],
        "deals[0].conditions.lineItem.minimumQuantity": minimum_quantity,
        "deals[0].output.lineItemDiscount.skus": [product_sku],
        "deals[0].output.lineItemDiscount.type": discount_type,
        "deals[0].output.lineItemDiscount.discount": discount_value,
    }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "data/input_simple_discount_v2_payload.json")

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "false", "false")

    # Send request
    response = place_request("PUT", request_url, request_body, request_headers)

    if response.status_code == 202:
	    return "success"
    else:
        return response.status_code

# Input deals v2 stepped discount business rules to Cart Calculation microservice
def input_stepped_discount_to_cart_calculation_v2(deal_id, accounts, zone, environment, skus, discount_type, index_range, discount_range):
    product_sku = skus[0]['sku']
    
    if discount_type == "percentOff":
        discount_type = "%"
    else:
        discount_type = "$"
    
    # Get base URL
    request_url = get_microservice_base_url(environment, "false") + "/cart-calculation-relay/v2/deals"

    dates_payload = return_first_and_last_date_year_payload()

    #Inputs for default payload of stepped discount for cart calculation v2
    dict_values = {
        "accounts": accounts,
        "deals[0].dealId": deal_id,
        "deals[0].externalId": deal_id,
        "deals[0].conditions.simulationDateTime[0].startDate": dates_payload['startDate'],
        "deals[0].conditions.simulationDateTime[0].endDate": dates_payload['endDate'],
        "deals[0].conditions.scaledLineItem.skus": [product_sku],
        "deals[0].conditions.scaledLineItem.ranges[0].from": index_range[0],
        "deals[0].conditions.scaledLineItem.ranges[0].to": index_range[1],
        "deals[0].conditions.scaledLineItem.ranges[1].from": index_range[2],
        "deals[0].conditions.scaledLineItem.ranges[1].to": index_range[3],
        "deals[0].output.lineItemScaledDiscount.ranges[0].skus": [product_sku],
        "deals[0].output.lineItemScaledDiscount.ranges[0].type": discount_type,
        "deals[0].output.lineItemScaledDiscount.ranges[0].discount": discount_range[0],
        "deals[0].output.lineItemScaledDiscount.ranges[1].skus": [product_sku],
        "deals[0].output.lineItemScaledDiscount.ranges[1].type": discount_type,
        "deals[0].output.lineItemScaledDiscount.ranges[1].discount": discount_range[1],
    }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "data/input_stepped_discount_v2_payload.json")

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "false", "false")

    # Send request
    response = place_request("PUT", request_url, request_body, request_headers)

    if response.status_code == 202:
	    return "success"
    else:
        return response.status_code

# Input deals v2 stepped discount with maximum quantity business rules to Cart Calculation microservice
def input_stepped_discount_with_qtd_to_cart_calculation_v2(deal_id, accounts, zone, environment, skus, quantity, index_range, discount_type, discount_range):
    product_sku = skus[0]['sku']
    
    if discount_type == "percentOff":
        discount_type = "%"
    else:
        discount_type = "$"
    
    # Get base URL
    request_url = get_microservice_base_url(environment, "false") + "/cart-calculation-relay/v2/deals"

    dates_payload = return_first_and_last_date_year_payload()

    #Inputs for default payload of stepped discount with quantity for cart calculation v2
    dict_values = {
        "accounts": accounts,
        "deals[0].dealId": deal_id,
        "deals[0].externalId": deal_id,
        "deals[0].conditions.simulationDateTime[0].startDate": dates_payload['startDate'],
        "deals[0].conditions.simulationDateTime[0].endDate": dates_payload['endDate'],
        "deals[0].conditions.scaledLineItem.skus": [product_sku],
        "deals[0].conditions.scaledLineItem.ranges[0].from": index_range[0],
        "deals[0].conditions.scaledLineItem.ranges[0].to": index_range[1],
        "deals[0].output.lineItemScaledDiscount.ranges[0].skus": [product_sku],
        "deals[0].output.lineItemScaledDiscount.ranges[0].type": discount_type,
        "deals[0].output.lineItemScaledDiscount.ranges[0].discount": discount_range[0],
        "deals[0].output.lineItemScaledDiscount.ranges[0].maxQuantity": quantity,
    }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "data/input_stepped_discount_with_max_quantity_v2_payload.json")

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get header request
    request_headers = get_header_request(zone, "false", "false", "false", "false")

    # Send request
    response = place_request("PUT", request_url, request_body, request_headers)

    if response.status_code == 202:
        return "success"
    else:
        return response.status_code


def request_get_deals_promo_fusion_service(zone, environment, abi_id = ''):
    """Get deals data from the Promo Fusion Service
    Arguments:
        - abi_id: account_id
        - zone: e.g, DO,BR,CO
        - environment: e.g, UAT,SIT
    Return new json_object
    """
    # Get base URL
    request_url = get_microservice_base_url(environment) + '/promo-fusion-service/' + abi_id

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Send request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)

    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    else:
        print(text.Red + '\n- [Promo Fusion Service] Failure to retrieve deals. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        finishApplication()


def request_get_deals_promotion_service(abi_id, zone, environment):
    """Get deals data from the Promotion Service
    Arguments:
        - abi_id: account_id
        - zone: e.g, AR,CL
        - environment: e.g, UAT,SIT
    Return new json_object
    """
    # Get base URL
    request_url = get_microservice_base_url(environment) + '/promotion-service/?accountId=' + abi_id \
                  + '&includeDisabled=false'

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Send request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)

    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    else:
        print(text.Red + '\n- [Promo Fusion Service] Failure to retrieve deals. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        finishApplication()


def display_deals_information_promotion(abi_id, zone, environment):
    """Display deals information from the Promotion Service
    Arguments:
        - abi_id: account_id
        - zone: e.g, AR,CL
        - environment: e.g, UAT,SIT
    Print a table containing the available deals information
    """
    deals = request_get_deals_promotion_service(abi_id, zone, environment)

    promotions = deals['promotions']

    promotion_information = list()
    if len(promotions) == 0:
        print(text.Yellow + '\n- There is no promotion available for ' + abi_id)
    else:
        for i in range(len(promotions)):
            promotion_values = {
                'ID': promotions[i]['id'],
                'Type': promotions[i]['type'],
                'Title': promotions[i]['title'],
                'End Date': promotions[i]['endDate']
            }
            promotion_information.append(promotion_values)

        print(text.default_text_color + '\nPromotion Information')
        print(tabulate(promotion_information, headers='keys', tablefmt='grid'))


def display_deals_information_promo_fusion(abi_id, zone, environment):
    """Display deals information from the Promo Fusion Service
    Arguments:
        - abi_id: account_id
        - zone: e.g, BR,CO,DO
        - environment: e.g, UAT,SIT
    Print a table containing the available deals information
    """
    deals = request_get_deals_promo_fusion_service(zone, environment, abi_id)

    combos = deals['combos']
    promotions = deals['promotions']

    combo_information = list()
    if len(combos) == 0:
        print(text.Yellow + '\n- There is no combo available for ' + abi_id)
    else:
        for i in range(len(combos)):
            combo_values = {
                'ID': combos[i]['id'],
                'Type': combos[i]['type'],
                'Title': combos[i]['title'],
                'Original Price': combos[i]['originalPrice'],
                'Price': combos[i]['price'],
                'Stock Available': combos[i]['availableToday']
            }
            combo_information.append(combo_values)

        print(text.default_text_color + '\nCombo Information')
        print(tabulate(combo_information, headers='keys', tablefmt='grid'))

    promotion_information = list()
    if len(promotions) == 0:
        print(text.Yellow + '\n- There is no promotion available for ' + abi_id)
    else:
        for i in range(len(promotions)):
            promotion_values = {
                'SKU': promotions[i]['sku'],
                'ID': promotions[i]['discountId'],
                'Type': promotions[i]['type'],
                'Title': promotions[i]['title'],
                'Price': promotions[i]['price']
            }
            promotion_information.append(promotion_values)

        print(text.default_text_color + '\nPromotion Information')
        print(tabulate(promotion_information, headers='keys', tablefmt='grid'))
