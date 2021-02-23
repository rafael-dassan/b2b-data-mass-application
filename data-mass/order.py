# Standard library imports
import json
from json import loads
import os
from datetime import timedelta, datetime

# Third party imports
from tabulate import tabulate

# Local application imports
from common import update_value_to_json, convert_json_to_string, get_header_request, get_microservice_base_url, \
    place_request, set_to_dictionary, find_values, generate_erp_token
from classes.text import text


def configure_order_params(zone, environment, account_id, number_size, prefix):
    """
    Configure the fields prefix and order number size in the database sequence via Order Service
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        account_id: POC unique identifier
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
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)
    set_to_dictionary(request_headers, 'Authorization', generate_erp_token())

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


def request_order_creation(account_id, delivery_center_id, zone, environment, allow_order_cancel, order_items,
                           order_status):
    """
    Create an order through the Order Service
    Args:
        account_id: POC unique identifier
        delivery_center_id: POC's delivery center
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        order_status: e.g., PLACED, CANCELLED, etc
        order_items: list of SKUs
        allow_order_cancel: `Y` or `N`

    Returns: new json_data if success or error message in case of failure
    """
    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

    # Define url request 
    request_url = get_microservice_base_url(environment) + '/order-service'

    # Get body
    request_body = create_order_payload(account_id, delivery_center_id, allow_order_cancel, order_items, order_status)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    else:
        print(text.Red + '\n- [Order Service] Failure to create an order. Response Status: {response_status}. '
                         'Response message {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return 'false'


def create_order_payload(account_id, delivery_center_id, allow_order_cancel, order_items, order_status):
    """
    Create payload for order creation
    Args:
        account_id: POC unique identifier
        delivery_center_id: POC's delivery center
        order_items: list of SKUs
        allow_order_cancel: `Y` or `N`
        order_status: e.g., PLACED, CANCELLED, etc
    Returns: order payload
    """
    # Sets the format of the placement date of the order (current date and time)
    placement_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '+00:00'

    if order_status == 'DELIVERED':
        # Sets the format of the delivery date of the order (current date and time less one day)
        delivery_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    else:
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

    line_items = order_items.get('lineItems')
    item_list = list()
    for i in range(len(line_items)):
        item_values = {
            'price': line_items[i]['price'],
            'unitPrice': line_items[i]['unitPrice'],
            'unitPriceInclTax': line_items[i]['unitPriceInclTax'],
            'quantity': line_items[i]['quantity'],
            'discountAmount': line_items[i]['discountAmount'],
            'deposit': line_items[i]['deposit'],
            'subtotal': line_items[i]['subtotal'],
            'taxAmount': line_items[i]['taxAmount'],
            'total': line_items[i]['total'],
            'totalExclDeposit': line_items[i]['totalExclDeposit'],
            'sku': line_items[i]['sku'],
            'hasInventory': line_items[i]['hasInventory'],
            'freeGood': line_items[i]['freeGood'],
            'originalPrice': line_items[i]['originalPrice'],
        }
        item_list.append(item_values)

    dict_values = {
        'accountId': account_id,
        'deliveryCenter': delivery_center_id,
        'delivery.date': delivery_date,
        'deposit': order_items.get('deposit'),
        'discount': order_items.get('discountAmount'),
        'interestAmount': order_items.get('interestAmount'),
        'itemsQuantity': len(order_items.get('lineItems')),
        'total': order_items.get('total'),
        'subtotal': order_items.get('subtotal'),
        'tax': order_items.get('taxAmount'),
        'placementDate': placement_date,
        'status': order_status
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    set_to_dictionary(json_object, 'items', item_list)

    if order_status == 'PLACED':
        if allow_order_cancel == 'Y':
            set_to_dictionary(json_object, 'cancellableUntil', cancellable_date)
    elif order_status == 'CANCELLED':
        set_to_dictionary(json_object, 'cancellationReason', 'Order cancelled for testing purposes')

    return convert_json_to_string(json_object)


def get_order_prefix_params(zone):
    params = {
        'AR': {
            'order_number_size': 12,
            'prefix': 'UAT'
        },
        'BR': {
            'order_number_size': 8,
            'prefix': '31'
        },
        'CA': {
            'order_number_size': 7,
            'prefix': 'UAT'
        },
        'CO': {
            'order_number_size': 7,
            'prefix': 'UAT'
        },
        'DO': {
            'order_number_size': 7,
            'prefix': 'UAT'
        },
        'EC': {
            'order_number_size': 7,
            'prefix': 'UAT'
        },
        'MX': {
            'order_number_size': 7,
            'prefix': '5'
        },
        'PE': {
            'order_number_size': 7,
            'prefix': 'UAT'
        },
        'ZA': {
            'order_number_size': 7,
            'prefix': 'UAT'
        }
    }

    return params[zone]


def request_changed_order_creation(zone, environment, order_data):
    """
    Change/Update order information through the Order Relay Service
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
    request_body = get_changed_order_payload(order_data)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)
    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Order Relay Service] Failure to change an order. Response Status: {response_status}. '
                         'Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return 'false'


def get_changed_order_payload(order_data):
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
    elif len(items) > 1:
        for i in range(len(items)):
            if items[i]['quantity'] > 1:
                item_qtd = 1
                item_subtotal = items[i]['price']
                item_total = items[i]['price']

                update_value_to_json(order_data[0], 'items['+str(i)+'].quantity', item_qtd)
                update_value_to_json(order_data[0], 'items['+str(i)+'].subtotal', item_subtotal)
                update_value_to_json(order_data[0], 'items['+str(i)+'].total', item_total)

    return convert_json_to_string(order_data)


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
                'Total': items[i]['total'],
                'Free Good': items[i]['freeGood']
            }
            if 'tax' in items:
                tax = items[i]['tax']
                set_to_dictionary(item_values, 'tax', tax)
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


def check_if_order_exists(account_id, zone, environment, order_id):
    """
    Check if an order exists via Order Service
    Args:
        account_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        order_id: order unique identifier

    Returns:
        empty: if an account does not have any order
        not_found: if the order_id does not exist
        false: if an error comes from back-end
    """
    # Get header request
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/order-service/v1?orderIds=' + order_id + '&accountId=' \
                  + account_id

    # Place request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        if order_id == '':
            print(text.Red + '\n- [Order Service] The account {account_id} does not have orders'
                  .format(account_id=account_id))
            return 'not_found'
        else:
            print(text.Red + '\n- [Order Service] The order {order_id} does not exist'.format(order_id=order_id))
            return 'not_found'
    else:
        print(text.Red + '\n- [Order Service] Failure to retrieve order information. Response Status: '
                         '{response_status}. Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return 'false'


def get_order_details(order_data):
    items = order_data['items']

    interest_amount = 0
    if 'interestAmount' in order_data:
        interest_amount = order_data['interestAmount']

    order_details = {
        'accountId': order_data['accountId'],
        'placementDate': order_data['placementDate'],
        'paymentMethod': order_data['paymentMethod'],
        'channel': order_data['channel'],
        'subtotal': order_data['subtotal'],
        'total': order_data['total'],
        'tax': order_data['tax'],
        'discount': order_data['discount'],
        'itemsQuantity': len(items),
        'interestAmount': interest_amount
    }

    return order_details


def get_order_items(order_data, zone):
    items = order_data['items']
    item_list = list()

    for i in range(len(items)):
        discount = 0
        if 'pricingReasonDetail' in items[i] and len(items[i]['pricingReasonDetail']) != 0:
            discount = items[i]['pricingReasonDetail'][0]['discountAmount']
            if discount is None:
                discount = 0

        if 'tax' in items[i]:
            if items[i]['tax'] is None:
                tax = 0
            else:
                tax = items[i]['tax']
        else:
            tax = 0

        if zone == "ZA":
            items_details = {
                'sku': items[i]['sku'],
                'price': items[i]['price'],
                'quantity': items[i]['quantity'],
                'subtotal': items[i]['subtotal'],
                'total': items[i]['total'],
                'freeGood': 0,
                'tax': tax,
                'discount': discount
            }
            item_list.append(items_details)
        else:
            items_details = {
                'sku': items[i]['sku'],
                'price': items[i]['price'],
                'quantity': items[i]['quantity'],
                'subtotal': items[i]['subtotal'],
                'total': items[i]['total'],
                'freeGood': items[i]['freeGood'],
                'tax': tax,
                'discount': discount
            }
            item_list.append(items_details)

    return item_list


def request_get_order_by_date_updated(zone, environment, account_id, order_prefix):
    """
        Check if an order exists via Order Service
        Args:
            account_id: POC unique identifier
            zone: e.g., AR, BR, CO, DO, MX, ZA
            environment: e.g., DEV, SIT, UAT
            order_prefix: order unique identifier
        Returns:
            json_data: order response data
            false: if an error comes from back-end
        """
    # Get header request
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

    updated_since = datetime.now().strftime('%Y-%m-%d') + 'T00:00:00.000Z'

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/order-service/v1?updatedSince={0}&accountId={1}&sort={2}'\
        .format(updated_since, account_id, 'DESC')

    # Place request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        for i in range(len(json_data)):
            if '{0}-{1}'.format(order_prefix, zone) in json_data[i]['orderNumber']:
                return json_data
    else:
        print(text.Red + '\n- [Order Service] Failure to retrieve order information. Response Status: '
                         '{response_status}. Response message: {response_message}'
                  .format(response_status=response.status_code, response_message=response.text))
        return 'false'
