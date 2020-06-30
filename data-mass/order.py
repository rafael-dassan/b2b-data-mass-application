from datetime import timedelta
from products import *
from common import *
import json


# Configure prefix and order number size
def configure_order_params(zone, environment, position):
    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Define url request 
    request_url = get_microservice_base_url(environment) + '/order-service/configure'

    if position == 1:
        dict_values = {
            'orderNumberSize': 5,
            'prefix': 'DM-ORDER-'
        }
    elif position == 2:
        dict_values = {
            'orderNumberSize': 9,
            'prefix': '00'
        }

    # Create body
    request_body = convert_json_to_string(dict_values)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)
    
    if response.status_code == 204:
        return 'true'
    else:
        return 'false'


# Create order in microservice
def create_order_account(account_id, zone, environment, delivery_center_id, order_option):
    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Define url request 
    request_url = get_microservice_base_url(environment) + '/order-service'

    # Retrieve all SKUs of the specified Account and DeliveryCenter IDs
    product_offers = request_get_offers_microservice(account_id, zone, environment, delivery_center_id, True)

    enabled_skus = list()
    aux_index = 0

    enabled_counter = 0
    
    while (aux_index < len(product_offers)) and (enabled_counter < 2):
        if zone == 'ZA' or zone == 'AR':
            sku_offer = product_offers[aux_index]
        else:
            sku_offer = product_offers[aux_index]['sku']
        
        # Check if the SKU is enabled on Items MS
        sku_enable = check_item_enabled(sku_offer, zone, environment)

        if sku_enable:
            enabled_skus.append(sku_offer)
            enabled_counter += 1
            aux_index += 1
        else:
            aux_index += 1

    # Check if the account has at least 2 enabled SKUs added to it
    if enabled_counter >= 2:

        # Check if the request is for an active order or for a cancelled one
        if order_option == 'ACTIVE':
            allow_order_cancel = input(text.default_text_color + '\nDo you want to make this order cancellable? y/N: ')
            allow_order_cancel = allow_order_cancel.upper()

            while allow_order_cancel != 'Y' and allow_order_cancel != 'N':
                print(text.Red + '\n[Order] Invalid option.')
                allow_order_cancel = input(text.default_text_color + '\nDo you want to make this order cancellable? y/N: ')
                allow_order_cancel = allow_order_cancel.upper()
        else:
            allow_order_cancel = 'N'

        print(text.default_text_color + '\nCreating Order...')

        # Get body request for Order
        request_body_order = set_file_request_order(request_url, request_headers, account_id, zone, delivery_center_id, enabled_skus,
                                                    allow_order_cancel, order_option)

        # Extracts the order number created from the request's response
        order_id_created = request_body_order.text
        order_id_created = order_id_created[16:30]

        if request_body_order.status_code == 200:
            print(text.Green + '\n- [Order Creation] The Order ' + order_id_created + ' has been created successfully')
            return 'true'
        else:
            return 'false'
    else:
        return 'error_len'


# Define JSON to submmit Order creation
def set_file_request_order(url, headers, abi_id, zone, delivery_center_id, enabled_skus, allow_order_cancel, order_option):

    # Sets the format of the placement date of the order (current date and time)
    placement_date = datetime.now()
    placement_date = placement_date.strftime('%Y-%m-%dT%H:%M:%S')
    placement_date = placement_date + '+00:00'

    # Sets the format of the delivery date of the order (current date and time more one day)
    delivery_date = datetime.now() + timedelta(days=1)
    delivery_date = delivery_date.strftime('%Y-%m-%d')

    # Sets the format of the cancellable date of the order (current date and time more ten days)
    cancellable_date = datetime.now() + timedelta(days=10)
    cancellable_date = cancellable_date.strftime('%Y-%m-%dT%H:%M:%S')
    cancellable_date = cancellable_date + '+00:00'

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_order_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values  = {
        'accountId': str(abi_id),
        'delivery.date': delivery_date,
        'items[0].sku': enabled_skus[0],
        'items[1].sku': enabled_skus[1],
        'placementDate': placement_date
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    if order_option == 'ACTIVE':
        if allow_order_cancel == 'Y':   
            json_object = set_to_dictionary(json_object, 'status', 'PLACED')
            json_object = set_to_dictionary(json_object, 'cancellableUntil', cancellable_date)
        else:
            json_object = set_to_dictionary(json_object, 'status', 'PLACED')
    elif order_option == 'CANCELLED':
        json_object = set_to_dictionary(json_object, 'status', 'CANCELLED')
        json_object = set_to_dictionary(json_object, 'cancellationReason', 'ORDER CANCELLED FOR TESTING PURPOSES')

    # Create body
    request_body = convert_json_to_string(json_object)

    # Send request
    response = place_request('POST', url, request_body, headers)

    return response


def change_order(account_id, zone, environment, order_option, order_id):
    order_data = check_if_order_exists(account_id, zone, environment, order_id)

    if order_data == 'false':
        return 'error_ms'
    else:
        order_info = order_data[0]

    status = order_info['status']

    if status == 'DENIED' or status == 'CANCELLED' or status == 'DELIVERED' or status == 'PARTIAL_DELIVERY' \
            or status == 'PENDING_CANCELLATION':
        print(text.Red + '\n- [Order Service] Its not possible change this order because the order status is ' +
              order_info['status'])
    else:
        items = order_info['items']
        item_qtd = 10
        item_subtotal = round(items[0]['price'] * 10, 2)
        item_total = round(items[0]['price'] * 10, 2)
        dif_item_total = round(items[0]['total'] - item_total, 2)
        dif_item_subtotal = round(items[0]['subtotal'] - item_subtotal, 2)

        order_total = round(order_info['total'] - dif_item_total, 2)
        order_subtotal = round(order_info['subtotal'] - dif_item_subtotal, 2)

        json_data = order_data
        json_object = update_value_to_json(order_info, 'items[0].quantity', item_qtd)
        json_object = update_value_to_json(order_info, 'items[0].subtotal', item_subtotal)
        json_object = update_value_to_json(order_info, 'items[0].total', item_total)
        json_object = update_value_to_json(order_info, 'subtotal', order_subtotal)
        json_object = update_value_to_json(order_info, 'total', order_total)

        # Create body
        request_body = convert_json_to_string(json_object)
        request_body = '[' + request_body + ']'

        # Define headers
        request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

        # Define url request
        request_url = get_microservice_base_url(environment) + '/order-relay/'

        # Send request
        response = place_request('POST', request_url, request_body, request_headers)

        if response.status_code == 202:
            print(text.Green + 'Order: ' + order_id + ' was change')
            return response
        else:
            return 'false'


def display_specific_order_information(orders):
    """Display order information
    Arguments:
        - orders: order data by account and order ID
    Print a table containing the available order information
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
    order_values = {
        'Order ID': orders[0]['orderNumber'],
        'Status': orders[0]['status'],
        'Placement Date': orders[0]['placementDate'],
        'Delivery Date': orders[0]['delivery']['date'],
        'Payment Method': orders[0]['paymentMethod'],
        'Subtotal': orders[0]['subtotal'],
        'Tax': orders[0]['tax'],
        'Discount': orders[0]['discount'],
        'Total': orders[0]['total']
    }
    order_information.append(order_values)

    print(text.default_text_color + '\nOrder Information By Account')
    print(tabulate(order_information, headers='keys', tablefmt='grid'))

    print(text.default_text_color + '\nOrder items')
    print(tabulate(item_information, headers='keys', tablefmt='grid'))

    print(text.default_text_color + '\nOrder combos')
    print(tabulate(combo_information, headers='keys', tablefmt='grid'))


def display_all_order_information(orders):
    """Display all order information by POC
    Arguments:
        - orders: order data by account
    Print a table containing the available order information
    """
    order_information = list()

    for i in range(len(orders)):
        order_values = {
            'Order ID': orders[i]['orderNumber'],
            'Status': orders[i]['status'],
            'Placement Date': orders[i]['placementDate'],
            'Delivery Date': orders[i]['delivery']['date'],
            'Payment Method': orders[i]['paymentMethod'],
            'Subtotal': orders[i]['subtotal'],
            'Tax': orders[i]['tax'],
            'Discount': orders[i]['discount'],
            'Total': orders[i]['total']
        }
        order_information.append(order_values)

    print(text.default_text_color + '\nAll Order Information By Account')
    print(tabulate(order_information, headers='keys', tablefmt='grid'))
