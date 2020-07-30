from json import dumps
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


def input_discount_to_account(abi_id, accounts, deal_sku, deal_type, zone, environment):
    free_good_sku = []
    minimum_quantity = print_minimum_quantity_menu()
    discount_type = print_discount_type_menu()
    discount_value = print_discount_value_menu(discount_type)

    promotion_response = input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone, environment)

    cart_response = input_discount_to_cart_calculation_v2(promotion_response, accounts, zone, environment, deal_sku,
                                                          discount_type, discount_value, minimum_quantity)

    if promotion_response == 'false' or cart_response != 'success':
        print(text.Red + '\n- [Deals] Something went wrong, please try again')
    else:
        print(text.Green + '\n- Deal successfully registered')
        print(text.default_text_color + '\n- Deal ID: ' + promotion_response)
        if zone == 'ZA':
            print(text.Yellow + '- Please, run the cron jobs `webjump_discount_import` and `webjump_discount_update_'
                                'online_customers` to import your deal, so it can be used in the front-end '
                                'applications')


def input_stepped_discount_with_qtd_to_account(abi_id, accounts, deal_sku, deal_type, zone, environment):
    free_good_sku = []
    index_range = print_index_range_menu(2)
    discount_type = print_discount_type_menu()
    discount_range = print_discount_range_menu(1)
    quantity = input(text.default_text_color + 'Quantity: ')

    promotion_response = input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone, environment)

    cart_response = input_stepped_discount_with_qtd_to_cart_calculation_v2(promotion_response, accounts, zone,
                                                                           environment, deal_sku, quantity, index_range,
                                                                           discount_type, discount_range)

    if promotion_response == 'false' or cart_response != 'success':
        print(text.Red + '\n- [Deals] Something went wrong, please try again')
    else:
        print(text.Green + '\n- Deal successfully registered')
        print(text.default_text_color + '\n- Deal ID: ' + promotion_response)
        if zone == 'ZA':
            print(text.Yellow + '- Please, run the cron jobs `webjump_discount_import` and `webjump_discount_update_'
                                'online_customers` to import your deal, so it can be used in the front-end '
                                'applications')


def input_stepped_discount_to_account(abi_id, accounts, deal_sku, deal_type, zone, environment):
    free_good_sku = []
    index_range = print_index_range_menu()
    discount_type = print_discount_type_menu()
    discount_range = print_discount_range_menu()

    promotion_response = input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone, environment)

    cart_response = input_stepped_discount_to_cart_calculation_v2(promotion_response, accounts, zone, environment,
                                                                  deal_sku, discount_type, index_range, discount_range)

    if promotion_response == 'false' or cart_response != 'success':
        print(text.Red + '\n- [Deals] Something went wrong, please try again')
    else:
        print(text.Green + '\n- Deal successfully registered')
        print(text.default_text_color + '\n- Deal ID: ' + promotion_response)
        if zone == 'ZA':
            print(text.Yellow + '- Please, run the cron jobs `webjump_discount_import` and `webjump_discount_update_'
                                'online_customers` to import your deal, so it can be used in the front-end '
                                'applications')


def input_free_good_to_account(abi_id, accounts, deal_sku, sku_list, deal_type, zone, environment):
    if zone != 'BR':
        partial_free_good = 'N'
    else:
        partial_free_good = input(text.default_text_color + 'Would you like to register this free goods as an optional SKU rescue?: (y/n): ')
        while partial_free_good.upper() != 'Y' and partial_free_good.upper() != 'N':
            print(text.Red + '\n- Invalid option')
            partial_free_good = input(text.default_text_color + 'Would you like to register this free goods as an optional SKU rescue? (y/n): ')

    free_good_sku = deal_sku
    minimum_quantity = print_minimum_quantity_menu()
    quantity = print_quantity_menu()

    promotion_response = input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone, environment)

    cart_response = input_free_good_to_cart_calculation_v2(promotion_response, accounts, zone, environment, deal_sku, sku_list, minimum_quantity, quantity, partial_free_good)

    if promotion_response == 'false' or cart_response != 'success':
        print(text.Red + '\n- [Deals] Something went wrong, please try again')
    else:
        print(text.Green + '\n- Deal successfully registered')
        print(text.default_text_color + '\n- Deal ID: ' + promotion_response)


def input_stepped_free_good_to_account(abi_id, accounts, deal_sku, deal_type, zone, environment):
    free_good_sku = deal_sku
    index_range = print_index_range_menu()
    quantity_range = print_quantity_range_menu()

    promotion_response = input_deal_to_account(abi_id, deal_sku, free_good_sku, deal_type, zone, environment)

    cart_response = input_stepped_free_good_to_cart_calculation_v2(promotion_response, accounts, zone, environment,
                                                                   deal_sku, index_range, quantity_range)

    if promotion_response == 'false' or cart_response != 'success':
        print(text.Red + '\n- [Deals] Something went wrong, please try again')
    else:
        print(text.Green + '\n- Deal successfully registered')
        print(text.default_text_color + '\n- Deal ID: ' + promotion_response)


def input_free_good_to_cart_calculation_v2(deal_id, accounts, zone, environment, deal_sku, sku_list, minimum_quantity, quantity, partial_free_good):
    """
    Input deal type free good rules (API version 2) to the Pricing Engine Relay Service
    Args:
        deal_id: deal unique identifier
        accounts: account list
        zone: e.g., BR, DO, CO
        environment: e.g., DEV, SIT, UAT
        sku_list: list of SKUs used as free goods
        minimum_quantity: SKU minimum's quantity for the free good to be applied
        quantity: quantity of SKUs to offer as free goods

    Returns: Success if the request went ok and the status code if there's a problem
    """
    # Define if free good promotion is partial sku rescue
    if partial_free_good.upper() == 'Y':
        boolean_partial_free_good = 'True'
    else:
        boolean_partial_free_good = 'False'

    # Change the accumulationType to UNIQUE only for AR
    if zone == 'AR':
        accumulation_type = 'UNIQUE'
    else:
        accumulation_type = None
    
    # Get base URL
    request_url = get_microservice_base_url(environment, 'false') + '/cart-calculation-relay/v2/deals'

    # Get deal's start and end dates
    dates_payload = return_first_and_last_date_year_payload()

    # Create dictionary with deal's values
    dict_values = {
        'accounts': accounts,
        'deals[0].dealId': deal_id,
        'deals[0].externalId': deal_id,
        'deals[0].accumulationType': accumulation_type,
        'deals[0].conditions.simulationDateTime[0].startDate': dates_payload['startDate'],
        'deals[0].conditions.simulationDateTime[0].endDate': dates_payload['endDate'],
        'deals[0].conditions.lineItem.skus': [deal_sku],
        'deals[0].conditions.lineItem.minimumQuantity': minimum_quantity,
        'deals[0].output.freeGoods.proportion': minimum_quantity,
        'deals[0].output.freeGoods.partial': boolean_partial_free_good,
        'deals[0].output.freeGoods.freeGoods[0].skus[0].sku': sku_list[0]['sku'],
        'deals[0].output.freeGoods.freeGoods[0].skus[0].price': sku_list[0]['price'],
        'deals[0].output.freeGoods.freeGoods[0].quantity': quantity,
        'deals[0].output.freeGoods.freeGoods[1].skus[0].sku': sku_list[1]['sku'],
        'deals[0].output.freeGoods.freeGoods[1].skus[0].price': sku_list[1]['price'],
        'deals[0].output.freeGoods.freeGoods[1].skus[1].sku': sku_list[2]['sku'],
        'deals[0].output.freeGoods.freeGoods[1].skus[1].price': sku_list[2]['price'],
        'deals[0].output.freeGoods.freeGoods[1].quantity': quantity
    }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_free_good_payload_v2.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get headers
    request_headers = get_header_request(zone, 'false', 'false', 'false', 'false')

    # Send request
    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'success'
    else:
        return response.status_code


def input_stepped_free_good_to_cart_calculation_v2(deal_id, accounts, zone, environment, deal_sku, index_range,
                                                   quantity_range):
    """
    Input deal type stepped free good rules (API version 2) to the Pricing Engine Relay Service
    Args:
        deal_id: deal unique identifier
        accounts: account list
        zone: e.g., BR, DO, CO
        environment: e.g., DEV, SIT, UAT
        deal_sku: SKU that will have free good applied
        index_range: range of SKU quantities that the free good is valid to be applied
        quantity_range: different free good values to be applied according to the index_range parameter

    Returns: Success if the request went ok and the status code if there's a problem
    """

    # Change the accumulationType to UNIQUE only for AR
    if zone == 'AR':
        accumulation_type = 'UNIQUE'
    else:
        accumulation_type = None

    # Get base URL
    request_url = get_microservice_base_url(environment, 'false') + '/cart-calculation-relay/v2/deals'

    # Get deal's start and end dates
    dates_payload = return_first_and_last_date_year_payload()

    # Create dictionary with deal's values
    dict_values = {
        'accounts': accounts,
        'deals[0].dealId': deal_id,
        'deals[0].externalId': deal_id,
        'deals[0].accumulationType': accumulation_type,
        'deals[0].conditions.simulationDateTime[0].startDate': dates_payload['startDate'],
        'deals[0].conditions.simulationDateTime[0].endDate': dates_payload['endDate'],
        'deals[0].conditions.scaledLineItem.skus': [deal_sku],
        'deals[0].conditions.scaledLineItem.ranges[0].from': index_range[0],
        'deals[0].conditions.scaledLineItem.ranges[0].to': index_range[1],
        'deals[0].conditions.scaledLineItem.ranges[1].from': index_range[2],
        'deals[0].conditions.scaledLineItem.ranges[1].to': index_range[3],
        'deals[0].output.scaledFreeGoods.ranges[0].freeGoods[0].skus[0].sku': deal_sku,
        'deals[0].output.scaledFreeGoods.ranges[0].freeGoods[0].quantity': quantity_range[0],
        'deals[0].output.scaledFreeGoods.ranges[0].proportion': quantity_range[0],
        'deals[0].output.scaledFreeGoods.ranges[1].freeGoods[0].skus[0].sku': deal_sku,
        'deals[0].output.scaledFreeGoods.ranges[1].freeGoods[0].quantity': quantity_range[1],
        'deals[0].output.scaledFreeGoods.ranges[1].proportion': quantity_range[1]
    }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "data/create_stepped_free_good_payload_v2.json")

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get headers
    request_headers = get_header_request(zone, 'false', 'false', 'false', 'false')

    # Send request
    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'success'
    else:
        return response.status_code


def input_discount_to_cart_calculation_v2(deal_id, accounts, zone, environment, deal_sku, discount_type, discount_value,
                                          minimum_quantity):
    """
    Input deal type discount rules (API version 2) to the Pricing Engine Relay Service
    Args:
        deal_id: deal unique identifier
        accounts: account list
        zone: e.g., BR, DO, CO
        environment: e.g., DEV, SIT, UAT
        deal_sku: SKU that will have discount applied
        discount_type: type of discount being applied (percent or amount)
        discount_value: value of discount being applied
        minimum_quantity: SKU minimum's quantity for the discount to be applied

    Returns: Success if the request went ok and the status code if there's a problem
    """

    # Get the correct discount type
    if discount_type == 'percentOff':
        discount_type = '%'
    else:
        discount_type = '$'

    # Change the accumulationType to UNIQUE only for AR
    if zone == 'AR':
        accumulation_type = 'UNIQUE'
    else:
        accumulation_type = None

    # Get base URL
    request_url = get_microservice_base_url(environment, 'false') + '/cart-calculation-relay/v2/deals'

    # Get deal's start and end dates
    dates_payload = return_first_and_last_date_year_payload()

    # Create dictionary with deal's values
    dict_values = {
        'accounts': accounts,
        'deals[0].dealId': deal_id,
        'deals[0].externalId': deal_id,
        'deals[0].accumulationType': accumulation_type,
        'deals[0].conditions.simulationDateTime[0].startDate': dates_payload['startDate'],
        'deals[0].conditions.simulationDateTime[0].endDate': dates_payload['endDate'],
        'deals[0].conditions.lineItem.skus': [deal_sku],
        'deals[0].conditions.lineItem.minimumQuantity': minimum_quantity,
        'deals[0].output.lineItemDiscount.skus': [deal_sku],
        'deals[0].output.lineItemDiscount.type': discount_type,
        'deals[0].output.lineItemDiscount.discount': discount_value
    }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_discount_payload_v2.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get headers
    request_headers = get_header_request(zone, 'false', 'false', 'false', 'false')

    # Send request
    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'success'
    else:
        return response.status_code


def input_stepped_discount_to_cart_calculation_v2(deal_id, accounts, zone, environment, deal_sku, discount_type,
                                                  index_range, discount_range):
    """
    Input deal type stepped discount rules (API version 2) to the Pricing Engine Relay Service
    Args:
        deal_id: deal unique identifier
        accounts: account list
        zone: e.g., BR, DO, CO
        environment: e.g., DEV, SIT, UAT
        deal_sku: SKU that will have discount applied
        discount_type: type of discount being applied (percent or amount)
        index_range: range of SKU quantities that the discount is valid to be applied
        discount_range: different discount values to be applied according to the index_range parameter

    Returns: Success if the request went ok and the status code if there's a problem
    """

    # Get the correct discount type
    if discount_type == 'percentOff':
        discount_type = '%'
    else:
        discount_type = '$'

    # Change the accumulationType to UNIQUE only for AR
    if zone == 'AR':
        accumulation_type = 'UNIQUE'
    else:
        accumulation_type = None
    
    # Get base URL
    request_url = get_microservice_base_url(environment, 'false') + '/cart-calculation-relay/v2/deals'

    # Get deal's start and end dates
    dates_payload = return_first_and_last_date_year_payload()

    # Create dictionary with deal's values
    dict_values = {
        'accounts': accounts,
        'deals[0].dealId': deal_id,
        'deals[0].externalId': deal_id,
        'deals[0].accumulationType': accumulation_type,
        'deals[0].conditions.simulationDateTime[0].startDate': dates_payload['startDate'],
        'deals[0].conditions.simulationDateTime[0].endDate': dates_payload['endDate'],
        'deals[0].conditions.scaledLineItem.skus': [deal_sku],
        'deals[0].conditions.scaledLineItem.ranges[0].from': index_range[0],
        'deals[0].conditions.scaledLineItem.ranges[0].to': index_range[1],
        'deals[0].conditions.scaledLineItem.ranges[1].from': index_range[2],
        'deals[0].conditions.scaledLineItem.ranges[1].to': index_range[3],
        'deals[0].output.lineItemScaledDiscount.ranges[0].skus': [deal_sku],
        'deals[0].output.lineItemScaledDiscount.ranges[0].type': discount_type,
        'deals[0].output.lineItemScaledDiscount.ranges[0].discount': discount_range[0],
        'deals[0].output.lineItemScaledDiscount.ranges[1].skus': [deal_sku],
        'deals[0].output.lineItemScaledDiscount.ranges[1].type': discount_type,
        'deals[0].output.lineItemScaledDiscount.ranges[1].discount': discount_range[1]
    }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_stepped_discount_payload_v2.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get headers
    request_headers = get_header_request(zone, 'false', 'false', 'false', 'false')

    # Send request
    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'success'
    else:
        return response.status_code


def input_stepped_discount_with_qtd_to_cart_calculation_v2(deal_id, accounts, zone, environment, deal_sku, quantity,
                                                           index_range, discount_type, discount_range):
    """
    Input deal type stepped discount rules (API version 2) to the Pricing Engine Relay Service
    Args:
        deal_id: deal unique identifier
        accounts: account list
        zone: e.g., BR, DO, CO
        environment: e.g., DEV, SIT, UAT
        deal_sku: SKU that will have discount applied
        quantity: quantity limit for the deal to be applied
        discount_type: type of discount being applied (percent or amount)
        index_range: range of SKU quantities that the discount is valid to be applied
        discount_range: different discount values to be applied according to the index_range parameter

    Returns: Success if the request went ok and the status code if there's a problem
    """

    # Get the correct discount type
    if discount_type == 'percentOff':
        discount_type = '%'
    else:
        discount_type = '$'

    # Change the accumulationType to UNIQUE only for AR
    if zone == 'AR':
        accumulation_type = 'UNIQUE'
    else:
        accumulation_type = None
    
    # Get base URL
    request_url = get_microservice_base_url(environment, 'false') + '/cart-calculation-relay/v2/deals'

    # Get deal's start and end dates
    dates_payload = return_first_and_last_date_year_payload()

    # Create dictionary with deal's values
    dict_values = {
        'accounts': accounts,
        'deals[0].dealId': deal_id,
        'deals[0].externalId': deal_id,
        'deals[0].accumulationType': accumulation_type,
        'deals[0].conditions.simulationDateTime[0].startDate': dates_payload['startDate'],
        'deals[0].conditions.simulationDateTime[0].endDate': dates_payload['endDate'],
        'deals[0].conditions.scaledLineItem.skus': [deal_sku],
        'deals[0].conditions.scaledLineItem.ranges[0].from': index_range[0],
        'deals[0].conditions.scaledLineItem.ranges[0].to': index_range[1],
        'deals[0].output.lineItemScaledDiscount.ranges[0].skus': [deal_sku],
        'deals[0].output.lineItemScaledDiscount.ranges[0].type': discount_type,
        'deals[0].output.lineItemScaledDiscount.ranges[0].discount': discount_range[0],
        'deals[0].output.lineItemScaledDiscount.ranges[0].maxQuantity': quantity
    }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_stepped_discount_max_qtd_payload_v2.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get headers
    request_headers = get_header_request(zone, 'false', 'false', 'false', 'false')

    # Send request
    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'success'
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
