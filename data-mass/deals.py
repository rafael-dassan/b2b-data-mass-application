from random import randint
from common import *
from tabulate import tabulate


def input_deal_to_account(abi_id, sku, deal_type, zone, environment):
    """
    Input deal to a specific POC. The deal is created by calling the Promotion Relay Service
    Args:
        abi_id: POC unique identifier
        sku: Product unique identifier that will have discount/free good associated with it
        deal_type: e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD, STEPPED_FREE_GOOD
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
    Returns: `deal_id` if success and error message in case of failure
    """

    # Deal unique identifier
    deal_id = 'DM-' + str(randint(1, 100000))

    # Assign an account group unique identifier
    account_group_id = create_account_group(abi_id, zone, environment)

    # Assign a SKU group unique identifier
    sku_group_id = create_sku_group(sku, zone, environment)

    # Assign a free good group unique identifier when needed
    free_good_group_id = list()
    if deal_type == 'FREE_GOOD' or deal_type == 'STEPPED_FREE_GOOD':
        free_good = create_free_good_group(sku, zone, environment)
        free_good_group_id.append(free_good)

    if zone != 'DO':
        # Get body
        request_body = get_deals_payload_v1(deal_id, deal_type, account_group_id, sku_group_id, free_good_group_id)

        # Get base URL
        request_url = get_microservice_base_url(environment) + '/promotion-relay/'
    else:
        # Get body
        request_body = get_deals_payload_v2(deal_id, deal_type)

        # Get base URL
        request_url = get_microservice_base_url(environment) + '/promotion-relay/v2'

    # Get headers
    request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202 or response.status_code == 200:
        return deal_id
    else:
        print(text.Red + '\n- [Promotion Relay Service] Failure create deal. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def get_deals_payload_v1(deal_id, deal_type, account_group_id, sku_group_id, free_good_group_id):
    """
    Create a payload to associate a promotion to a POC (Promotion Relay Service v1)
    Args:
        deal_id: deal unique identifier
        deal_type: e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD, STEPPED_FREE_GOOD
        account_group_id: account group unique identifier
        sku_group_id: sku group unique identifier
        free_good_group_id: free good group unique identifier
    Returns: new promotion payload
    """

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/create_promotion_payload_v1.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Create dictionary with deal's values
    dict_values = {
        'accountGroupIds': [account_group_id],
        'description': 'This is a description for a deal type ' + deal_type + ' / ' + deal_id,
        'freeGoodGroupIds': free_good_group_id,
        'id': deal_id,
        'skuGroupIds': [sku_group_id],
        'title': deal_type + ' / ' + deal_id,
        'type': deal_type
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    return request_body


def get_deals_payload_v2(deal_id, deal_type):
    """
    Create a payload to associate a promotion to a POC (Promotion Relay Service v2)
    Args:
        deal_id: deal unique identifier
        deal_type: e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD, STEPPED_FREE_GOOD
    Returns: new promotion payload
    """

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/create_promotion_payload_v2.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Create dictionary with deal's values
    dict_values = {
        'description': 'This is a description for a deal type ' + deal_type + ' / ' + deal_id,
        'id': deal_id,
        'promotionId': deal_id,
        'title': deal_type + ' / ' + deal_id,
        'type': deal_type
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    return request_body


def create_account_group(abi_id, zone, environment):
    """
    Create new account group, used to create a new deal via the Promotion Relay Service
    Args:
        abi_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
    Returns: `account_group_id` if success and error message in case of failure
    """

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_account_group_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Assign an account group unique identifier
    account_group_id = 'DM-' + str(randint(1, 100000))

    # Create dictionary with account group's values
    dict_values = {
        'accountGroupId': account_group_id,
        'accounts': [abi_id]
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    # Get header request
    request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/promotion-relay/account-group'

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return account_group_id
    else:
        print(text.Red + '\n- [Promotion Relay Service] Failure create account group. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def create_sku_group(sku, zone, environment):
    """
    Create new SKU group, used to create a new deal via the Promotion Relay Service
    Args:
        sku: Product unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
    Returns: `sku_group_id` if success and error message in case of failure
    """

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_sku_group_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Assign a SKU group unique identifier
    sku_group_id = 'DM-' + str(randint(1, 100000))

    # Create dictionary with SKU group's values
    dict_values = {
        'skuGroupId': sku_group_id,
        'skus': [sku]
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    # Get headers
    request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/promotion-relay/sku-group'

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return sku_group_id
    else:
        print(text.Red + '\n- [Promotion Relay Service] Failure create sku group. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def create_free_good_group(sku, zone, environment):
    """
    Create new free good group, used to create a new deal via the Promotion Relay Service
    Args:
        sku: Product unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
    Returns: `free_good_group_id` if success and error message in case of failure
    """

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_free_good_group_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Assign a free good group unique identifier
    free_good_group_id = 'DM-' + str(randint(1, 100000))

    # Create dictionary with free good group's values
    dict_values = {
        'freeGoodGroupId': free_good_group_id,
        'skus': [sku]
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    # Get headers
    request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/promotion-relay/free-good-group'

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return free_good_group_id
    else:
        print(text.Red + '\n- [Promotion Relay Service] Failure create free good group. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def input_discount_to_account(abi_id, sku, deal_type, zone, environment):
    """
    Input a deal type discount to a specific POC by calling the Promotion Relay Service and Pricing Engine Relay Service
    Args:
        abi_id: POC unique identifier
        sku: product unique identifier
        deal_type: e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD, STEPPED_FREE_GOOD
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g, DEV, SIT, UAT
    Returns: `promotion_response` if success
    """

    minimum_quantity = print_minimum_quantity_menu()
    discount_type = print_discount_type_menu()
    discount_value = print_discount_value_menu(discount_type)

    promotion_response = input_deal_to_account(abi_id, sku, deal_type, zone, environment)

    cart_response = input_discount_to_cart_calculation_v2(abi_id, promotion_response, zone, environment, sku,
                                                          discount_type, discount_value, minimum_quantity)

    if promotion_response != 'false' and cart_response == 'success':
        return promotion_response
    else:
        return 'false'


def input_stepped_discount_with_qtd_to_account(abi_id, sku, deal_type, zone, environment):
    """
    Input a deal type stepped discount with max quantity to a specific POC by calling the Promotion Relay Service and
    Pricing Engine Relay Service
    Args:
        abi_id: POC unique identifier
        sku: product unique identifier
        deal_type: e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD, STEPPED_FREE_GOOD
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g, DEV, SIT, UAT
    Returns: `promotion_response` if success
    """

    index_range = print_index_range_menu(2)
    discount_type = print_discount_type_menu()
    discount_range = print_discount_range_menu(1)
    quantity = input(text.default_text_color + 'Quantity: ')

    promotion_response = input_deal_to_account(abi_id, sku, deal_type, zone, environment)

    cart_response = input_stepped_discount_with_qtd_to_cart_calculation_v2(abi_id, promotion_response, zone,
                                                                           environment, sku, quantity, index_range,
                                                                           discount_type, discount_range)

    if promotion_response != 'false' and cart_response == 'success':
        return promotion_response
    else:
        return 'false'


def input_stepped_discount_to_account(abi_id, sku, deal_type, zone, environment):
    """
    Input a deal type stepped discount to a specific POC by calling the Promotion Relay Service and
    Pricing Engine Relay Service
    Args:
        abi_id: POC unique identifier
        sku: product unique identifier
        deal_type: e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD, STEPPED_FREE_GOOD
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g, DEV, SIT, UAT
    Returns: `promotion_response` if success
    """

    index_range = print_index_range_menu()
    discount_type = print_discount_type_menu()
    discount_range = print_discount_range_menu()

    promotion_response = input_deal_to_account(abi_id, sku, deal_type, zone, environment)

    cart_response = input_stepped_discount_to_cart_calculation_v2(abi_id, promotion_response, zone, environment,
                                                                  sku, discount_type, index_range, discount_range)

    if promotion_response != 'false' and cart_response == 'success':
        return promotion_response
    else:
        return 'false'


def input_free_good_to_account(abi_id, sku, sku_list, deal_type, zone, environment):
    """
    Input a deal type free good to a specific POC by calling the Promotion Relay Service and Pricing Engine Relay
    Service
    Args:
        abi_id: POC unique identifier
        sku: product unique identifier
        sku_list: SKU list to offer as free good
        deal_type: e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD, STEPPED_FREE_GOOD
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g, DEV, SIT, UAT
    Returns: `promotion_response` if success
    """

    if zone != 'BR':
        partial_free_good = 'N'
    else:
        partial_free_good = input(text.default_text_color + 'Would you like to register this free goods as an optional'
                                                            ' SKU rescue?: (y/n): ')
        while partial_free_good.upper() != 'Y' and partial_free_good.upper() != 'N':
            print(text.Red + '\n- Invalid option')
            partial_free_good = input(text.default_text_color + 'Would you like to register this free goods as an '
                                                                'optional SKU rescue? (y/n): ')

    # Validate if like optional free good associate in buy something
    need_buy_product = 'Y'
    if partial_free_good.upper() == 'Y':
        need_buy_product = input(text.default_text_color + 'Would you like to link the redemption of an optional free'
                                                           ' good to the purchase of a sku? (y/n): ')
        while need_buy_product.upper() != 'Y' and need_buy_product.upper() != 'N':
            print(text.Red + '\n- Invalid option')
            need_buy_product = input(text.default_text_color + 'Would you like to link the redemption of an optional '
                                                               'free good to the purchase of a sku? (y/n): ')

    if need_buy_product.upper() == 'Y':
        minimum_quantity = print_minimum_quantity_menu()
        quantity = print_quantity_menu()
    else:
        minimum_quantity = 1
        quantity = 1

    promotion_response = input_deal_to_account(abi_id, sku, deal_type, zone, environment)

    cart_response = input_free_good_to_cart_calculation_v2(abi_id, promotion_response, zone, environment, sku,
                                                           sku_list, minimum_quantity, quantity, partial_free_good,
                                                           need_buy_product)

    if promotion_response != 'false' and cart_response == 'success':
        return promotion_response
    else:
        return 'false'


def input_stepped_free_good_to_account(abi_id, sku, deal_type, zone, environment):
    """
    Input a deal type stepped free good to a specific POC by calling the Promotion Relay Service and Pricing Engine
    Relay Service
    Args:
        abi_id: POC unique identifier
        sku: product unique identifier
        deal_type: e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD, STEPPED_FREE_GOOD
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g, DEV, SIT, UAT
    Returns: `promotion_response` if success
    """

    index_range = print_index_range_menu()
    quantity_range = print_quantity_range_menu()

    promotion_response = input_deal_to_account(abi_id, sku, deal_type, zone, environment)

    cart_response = input_stepped_free_good_to_cart_calculation_v2(abi_id, promotion_response, zone, environment,
                                                                   sku, index_range, quantity_range)

    if promotion_response != 'false' and cart_response == 'success':
        return promotion_response
    else:
        return 'false'


def input_free_good_to_cart_calculation_v2(abi_id, deal_id, zone, environment, sku, sku_list, minimum_quantity,
                                           quantity, partial_free_good, need_buy_product):
    """
    Input deal type free good rules (API version 2) to the Pricing Engine Relay Service
    Args:
        deal_id: deal unique identifier
        abi_id: POC unique identifier
        sku: product unique identifier
        zone: e.g., BR, DO, CO
        environment: e.g., DEV, SIT, UAT
        sku_list: list of SKUs used as free goods
        minimum_quantity: SKU minimum's quantity for the free good to be applied
        quantity: quantity of SKUs to offer as free goods
        partial_free_good: partial SKU to be rescued
        need_buy_product: e.g., `Y` or `N`
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

    if need_buy_product.upper() == 'Y':
        path_file = 'data/create_free_good_payload_v2.json'
        # Create dictionary with deal's values
        dict_values = {
            'accounts': [abi_id],
            'deals[0].dealId': deal_id,
            'deals[0].externalId': deal_id,
            'deals[0].accumulationType': accumulation_type,
            'deals[0].conditions.simulationDateTime[0].startDate': dates_payload['startDate'],
            'deals[0].conditions.simulationDateTime[0].endDate': dates_payload['endDate'],
            'deals[0].conditions.lineItem.skus': [sku],
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
    else:
        path_file = 'data/create_free_good_no_buy_item_payload_v2.json'
        # Create dictionary with deal's values
        dict_values = {
            'accounts': [abi_id],
            'deals[0].dealId': deal_id,
            'deals[0].externalId': deal_id,
            'deals[0].accumulationType': accumulation_type,
            'deals[0].conditions.simulationDateTime[0].startDate': dates_payload['startDate'],
            'deals[0].conditions.simulationDateTime[0].endDate': dates_payload['endDate'],
            'deals[0].output.freeGoods.proportion': 1,
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
    file_path = os.path.join(path, path_file)

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
        print(text.Red + '\n- [Pricing Engine Relay Service] Failure to associate a deal. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def input_stepped_free_good_to_cart_calculation_v2(abi_id, deal_id, zone, environment, sku, index_range,
                                                   quantity_range):
    """
    Input deal type stepped free good rules (API version 2) to the Pricing Engine Relay Service
    Args:
        deal_id: deal unique identifier
        abi_id: POC unique identifier
        zone: e.g., BR, DO, CO
        environment: e.g., DEV, SIT, UAT
        sku: product unique identifier
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
        'accounts': [abi_id],
        'deals[0].dealId': deal_id,
        'deals[0].externalId': deal_id,
        'deals[0].accumulationType': accumulation_type,
        'deals[0].conditions.simulationDateTime[0].startDate': dates_payload['startDate'],
        'deals[0].conditions.simulationDateTime[0].endDate': dates_payload['endDate'],
        'deals[0].conditions.scaledLineItem.skus': [sku],
        'deals[0].conditions.scaledLineItem.ranges[0].from': index_range[0],
        'deals[0].conditions.scaledLineItem.ranges[0].to': index_range[1],
        'deals[0].conditions.scaledLineItem.ranges[1].from': index_range[2],
        'deals[0].conditions.scaledLineItem.ranges[1].to': index_range[3],
        'deals[0].output.scaledFreeGoods.ranges[0].freeGoods[0].skus[0].sku': sku,
        'deals[0].output.scaledFreeGoods.ranges[0].freeGoods[0].quantity': quantity_range[0],
        'deals[0].output.scaledFreeGoods.ranges[0].proportion': quantity_range[0],
        'deals[0].output.scaledFreeGoods.ranges[1].freeGoods[0].skus[0].sku': sku,
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
        print(text.Red + '\n- [Pricing Engine Relay Service] Failure to associate a deal. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def input_discount_to_cart_calculation_v2(abi_id, deal_id, zone, environment, deal_sku, discount_type, discount_value,
                                          minimum_quantity):
    """
    Input deal type discount rules (API version 2) to the Pricing Engine Relay Service
    Args:
        deal_id: deal unique identifier
        abi_id: POC unique identifier
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
        'accounts': [abi_id],
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
        print(text.Red + '\n- [Pricing Engine Relay Service] Failure to associate a deal. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def input_stepped_discount_to_cart_calculation_v2(abi_id, deal_id, zone, environment, deal_sku, discount_type,
                                                  index_range, discount_range):
    """
    Input deal type stepped discount rules (API version 2) to the Pricing Engine Relay Service
    Args:
        deal_id: deal unique identifier
        abi_id: POC unique identifier
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
        'accounts': [abi_id],
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
        print(text.Red + '\n- [Pricing Engine Relay Service] Failure to associate a deal. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def input_stepped_discount_with_qtd_to_cart_calculation_v2(abi_id, deal_id, zone, environment, sku, quantity,
                                                           index_range, discount_type, discount_range):
    """
    Input deal type stepped discount rules (API version 2) to the Pricing Engine Relay Service
    Args:
        deal_id: deal unique identifier
        abi_id: POC unique identifier
        zone: e.g., BR, DO, CO
        environment: e.g., DEV, SIT, UAT
        sku: product unique identifier
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
        'accounts': [abi_id],
        'deals[0].dealId': deal_id,
        'deals[0].externalId': deal_id,
        'deals[0].accumulationType': accumulation_type,
        'deals[0].conditions.simulationDateTime[0].startDate': dates_payload['startDate'],
        'deals[0].conditions.simulationDateTime[0].endDate': dates_payload['endDate'],
        'deals[0].conditions.scaledLineItem.skus': [sku],
        'deals[0].conditions.scaledLineItem.ranges[0].from': index_range[0],
        'deals[0].conditions.scaledLineItem.ranges[0].to': index_range[1],
        'deals[0].output.lineItemScaledDiscount.ranges[0].skus': [sku],
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
        print(text.Red + '\n- [Pricing Engine Relay Service] Failure to associate a deal. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def request_get_deals_promo_fusion_service(zone, environment, abi_id=''):
    """
    Get deals data from the Promo Fusion Service
    Args:
        abi_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
    Returns: new json_object
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
        return 'false'


def request_get_deals_promotion_service(abi_id, zone, environment):
    """
    Get deals data from the Promotion Service
    Args:
        abi_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
    Returns: new json_object
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
        print(text.Red + '\n- [Promotion Service] Failure to retrieve deals. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def display_deals_information_promotion(abi_id, deals):
    """
    Display deals information from the Promotion Service
    Args:
        abi_id: POC unique identifier
        deals: deals object
    Returns: a table containing the available deals information
    """

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


def display_deals_information_promo_fusion(abi_id, deals):
    """
    Display deals information from the Promo Fusion Service
    Args:
        abi_id: POC unique identifier
        deals: deals object
    Returns: a table containing the available deals information
    """

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
