from datetime import timedelta
from products import *
from common import *
import json


def configure_order_params(zone, environment, number_size, prefix):
    """
    Configure the fields prefix and order number size in the database sequence via Order Service
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        number_size: order number size
        prefix: order prefix
    Returns: `success` or error message in case of failure
    """

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/configure_order_prefix_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'orderNumberSize': number_size,
        'prefix': prefix
    }

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Define url request 
    request_url = get_microservice_base_url(environment) + '/order-service/configure'

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)
    
    if response.status_code == 204:
        return 'success'
    else:
        print(text.Red + '\n- [Order Service] Failure to configure order prefix and number size. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def create_order_account(account_id, zone, environment, order_status, sku_list, allow_order_cancel, more_sku):
    """
    Create an order via the Order Service
    Args:
        account_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        order_status: e.g., PLACED, CANCELLED, etc
        sku_list: list of SKUs
        allow_order_cancel: `Y` or `N`
    Returns: new json_data if success or error message in case of failure
    """

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Define url request 
    request_url = get_microservice_base_url(environment) + '/order-service'

    # Get body
    if more_sku == 'N':
        request_body = create_order_payload(account_id, sku_list, allow_order_cancel, order_status)
    else:
        request_body = create_order_with_sku_payload(account_id, sku_list, allow_order_cancel, zone, environment)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    else:
        print(text.Red + '\n- [Order Service] Failure to create an order. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def create_order_payload(abi_id, sku_list, allow_order_cancel, order_status):
    """
    Create payload for order creation
    Args:
        abi_id: POC unique identifier
        sku_list: list of SKUs
        allow_order_cancel: `Y` or `N`
        order_status: e.g., PLACED, CANCELLED, etc
    Returns: order payload
    """

    # Sets the format of the placement date of the order (current date and time)
    placement_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '+00:00'

    # Sets the format of the delivery date of the order (current date and time more one day)
    delivery_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    # Sets the format of the cancellable date of the order (current date and time more ten days)
    cancellable_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%dT%H:%M:%S') + '+00:00'

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/create_order_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'accountId': str(abi_id),
        'delivery.date': delivery_date,
        'items[0].sku': sku_list[0],
        'items[1].sku': sku_list[1],
        'placementDate': placement_date
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    if order_status == 'ACTIVE':
        if allow_order_cancel == 'Y':   
            json_object = set_to_dictionary(json_object, 'status', 'PLACED')
            json_object = set_to_dictionary(json_object, 'cancellableUntil', cancellable_date)
        else:
            json_object = set_to_dictionary(json_object, 'status', 'PLACED')
    elif order_status == 'CANCELLED':
        json_object = set_to_dictionary(json_object, 'status', 'CANCELLED')
        json_object = set_to_dictionary(json_object, 'cancellationReason', 'ORDER CANCELLED FOR TESTING PURPOSES')
    elif order_status == 'DELIVERED':
        # Sets the format of the delivery date of the order (current date and time more one day)
        delivery_date_old = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        dict_values = {
            'delivery.date': delivery_date_old
        }

        for key in dict_values.keys():
            json_object = update_value_to_json(json_data, key, dict_values[key])

        json_object = set_to_dictionary(json_object, 'status', 'DELIVERED')

    # Create body
    request_body = convert_json_to_string(json_object)

    return request_body


def create_order_with_sku_payload(abi_id, sku_list, allow_order_cancel, zone, environment):
    """
    Create payload for order creation
    Args:
        abi_id: POC unique identifier
        sku_list: list of SKUs
        allow_order_cancel: `Y` or `N`
    Returns: order payload
    """

    # Sets the format of the placement date of the order (current date and time)
    placement_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '+00:00'

    # Sets the format of the delivery date of the order (current date and time more one day)
    delivery_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    # Sets the format of the cancellable date of the order (current date and time more ten days)
    cancellable_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%dT%H:%M:%S') + '+00:00'

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/create_order_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    item_list = list()
    for i in range(len(sku_list)):
        item = check_item_enabled(sku_list[i]['sku'], zone, environment)
        if item != 'false':
            quantity = int(sku_list[i]['quantity'])
            price = round(uniform(1, 2000), 2)
            total = round(price * quantity, 2)
            dict_values = {
                    'price': price,
                    'unitPrice': price,
                    'unitPriceInclTax': price,
                    'quantity': sku_list[i]['quantity'],
                    'discountAmount': round(uniform(1, 20), 2),
                    'deposit': round(uniform(1, 20), 2),
                    'subtotal': total,
                    'taxAmount': round(uniform(1, 20), 2),
                    'total': total,
                    'totalExclDeposit': round(uniform(1, 20), 2),
                    'tax': round(uniform(1, 2000), 2),
                    'sku': sku_list[i]['sku'],
                    'hasInventory': 'true',
                    'freeGood': 'false',
                    'originalPrice': price
                }
            item_list.append(dict_values)

    order_info = {
        'accountId': str(abi_id),
        'delivery.date': delivery_date,
        'placementDate': placement_date
    }
    for key in order_info.keys():
        json_object = update_value_to_json(json_data, key, order_info[key])

    if allow_order_cancel == 'Y':
        json_object = set_to_dictionary(json_object, 'status', 'PLACED')
        json_object = set_to_dictionary(json_object, 'cancellableUntil', cancellable_date)
    json_object = set_to_dictionary(json_object, 'accountId', str(abi_id))
    json_object = set_to_dictionary(json_object, 'delivery.date', delivery_date)
    json_object = set_to_dictionary(json_object, 'placementDate', placement_date)

    items = set_to_dictionary(json_object, 'items', item_list)

    # Create body
    request_body = convert_json_to_string(json_object)
    return request_body


def change_order(zone, environment, order_data):
    """
    Change/Update order information via the Order Relay Service
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        order_data: order information
    Returns `success` or error message in case of failure
    """

    # Define headers
    request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

    # Define url request
    request_url = get_microservice_base_url(environment) + '/order-relay/'

    # Get body
    request_body = create_changed_order_payload(order_data)
    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Order Relay Service] Failure to change an order. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def create_changed_order_payload(order_data):
    """
    Create payload for order update
    Args:
        order_data: order information
    Returns: updated order payload
    """

    items = order_data[0]['items']

    if len(items) == 1:
        if items[0]['quantity'] > 1:
            item_subtotal = items[0]['price']
            item_total = items[0]['price']
            dif_item_total = round(items[0]['total'] - item_total, 2)
            dif_item_subtotal = round(items[0]['subtotal'] - item_subtotal, 2)

            order_total = round(order_data[0]['total'] - dif_item_total, 2)
            order_subtotal = round(order_data[0]['subtotal'] - dif_item_subtotal, 2)

            update_value_to_json(order_data[0], 'items[0].quantity', 1)
            update_value_to_json(order_data[0], 'items[0].subtotal', item_subtotal)
            update_value_to_json(order_data[0], 'items[0].total', item_total)
            update_value_to_json(order_data[0], 'subtotal', order_subtotal)
            update_value_to_json(order_data[0], 'total', order_total)

            # Create body
            request_body = convert_json_to_string(order_data)

    elif len(items) > 1:
        for i in range(len(items)):
            if items[i]['quantity'] > 1:
                item_qtd = 1
                item_subtotal = items[i]['price']
                item_total = items[i]['price']

                update_value_to_json(order_data[0], 'items['+str(i)+'].quantity', item_qtd)
                update_value_to_json(order_data[0], 'items['+str(i)+'].subtotal', item_subtotal)
                update_value_to_json(order_data[0], 'items['+str(i)+'].total', item_total)

        # Create body
        request_body = convert_json_to_string(order_data)

    return request_body


def display_specific_order_information(orders):
    """
    Display order information
    Args:
        orders: order data by account and order ID
    Returns: a table containing the available order information
    """

    items = orders[0]['items']
    item_information = list()
    if len(items) == 0:
        item_values = {
            'Items': 'None'
        }
        item_information.append(item_values)
    else:
        for i in range(len(items)):
            item_values = {
                'SKU': items[i]['sku'],
                'Price': items[i]['price'],
                'Quantity': items[i]['quantity'],
                'Subtotal': items[i]['subtotal'],
                'Tax': items[i]['tax'],
                'Total': items[i]['total'],
                'Free Good': items[i]['freeGood']
            }
            item_information.append(item_values)

    combos = orders[0]['combos']
    combo_information = list()
    if len(combos) == 0:
        combo_values = {
            'Combos': 'None'
        }
        combo_information.append(combo_values)
    else:
        for i in range(len(combos)):
            combo_values = {
                'Combo ID': combos[i]['id'],
                'Type': combos[i]['type'],
                'Quantity': combos[i]['quantity'],
                'Title': combos[i]['title'],
                'Description': combos[i]['description'],
                'Original Price': combos[i]['originalPrice'],
                'Price': combos[i]['price']
            }
            combo_information.append(combo_values)

    order_information = list()

    for i in range(len(orders)):
        order_values = validate_order_parameters(orders[i])
        order_information.append(order_values)

    print(text.default_text_color + '\nOrder Information By Account')
    print(tabulate(order_information, headers='keys', tablefmt='grid'))

    print(text.default_text_color + '\nOrder items')
    print(tabulate(item_information, headers='keys', tablefmt='grid'))

    print(text.default_text_color + '\nOrder combos')
    print(tabulate(combo_information, headers='keys', tablefmt='grid'))


def display_all_order_information(orders):
    """
    Display all order information by POC
    Args:
        orders: order data by account
    Returns: a table containing the available order information
    """

    order_information = list()

    for i in range(len(orders)):
        order_values = validate_order_parameters(orders[i])
        order_information.append(order_values)

    print(text.default_text_color + '\nAll Order Information By Account')
    print(tabulate(order_information, headers='keys', tablefmt='grid'))


def validate_order_parameters(order):
    """
    Validate order parameters
    Args:
        order: order information
    Returns: validated order values
    """

    if 'subtotal' not in order:
        subtotal = 'null'
    else:
        subtotal = order['subtotal']

    if 'tax' not in order:
        tax = 'null'
    else:
        tax = order['tax']

    if 'total' not in order:
        total = 'null'
    else:
        total = order['total']

    json_str = convert_json_to_string(order)
    payment_method = find_values('paymentMethod', json_str)
    delivery_date = find_values('date', json_str)
    placement_date = find_values('placementDate', json_str).split('T')[0]
    discount = find_values('discount', json_str)

    order_values = {
        'Order ID': order['orderNumber'],
        'Status': order['status'],
        'Placement Date': placement_date,
        'Delivery Date': delivery_date,
        'Payment Method': payment_method,
        'Subtotal': subtotal,
        'Tax': tax,
        'Discount': discount,
        'Total': total
    }

    return order_values


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


def check_if_order_exists(abi_id, zone, environment, order_id):
    """
    Check if an order exists via Order Service
    Args:
        abi_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        order_id: order unique identifier
    Returns:
        empty: if an account does not have any order
        not_found: if the order_id does not exist
        false: if an error comes from back-end
    """

    # Get header request
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/order-service/v1?orderIds=' + order_id + '&accountId=' \
                  + abi_id

    # Place request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        if order_id == '':
            return 'empty'
        else:
            return 'not_found'
    else:
        print(text.Red + '\n- [Order Service] Failure to retrieve order information. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'
