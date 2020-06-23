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

    order_data = check_if_order_exist(account_id, zone, environment, order_id)

    if order_data == 'false':
        return 'error_ms'
    else:
        order_info = order_data[0]
        return order_info

    print(order_info)
    print(order_info['status'])

    if order_info['status'] != 'CANCELLED' or order_info['status'] != 'DELIVERED' or order_info['status'] != 'PARTIAL_DELIVERED' or order_info['status'] != 'PENDIN_CANCELLATION':
        items = order_info['items']
        print(items)
        item_qtd = 10
        item_subtotal = items[0]['price'] * 10
        print(item_subtotal)
        item_total = items[0]['price'] * 10
        print(item_total)
        dif_item_total = items[0]['total'] - item_total
        dif_item_total = round(dif_item_total, 2)
        print(dif_item_total)
        dif_item_subtotal = items[0]['subtotal'] - item_subtotal
        dif_item_subtotal = round(dif_item_subtotal, 2)
        print(dif_item_subtotal)

        order_total = order_info['total'] - dif_item_total
        order_total = round(order_total, 2)
        print(order_total)
        order_subtotal = order_info['subtotal'] - dif_item_subtotal
        order_subtotal = round(order_subtotal, 2)
        print(order_subtotal)

        json_data = order_data
        json_object = update_value_to_json(order_info, 'items[0].quantity', item_qtd)
        json_object = update_value_to_json(order_info, 'items[0].subtotal', item_subtotal)
        json_object = update_value_to_json(order_info, 'items[0].total', item_total)
        json_object = update_value_to_json(order_info, 'subtotal', order_subtotal)
        json_object = update_value_to_json(order_info, 'total', order_total)

        # Create body
        request_body = convert_json_to_string(json_object)
        request_body = '[' + request_body + ']'
        print(request_body)

        # Define headers
        request_headers = get_header_request(zone, 'false', 'true', 'false', 'false')

        # Define url request
        request_url = get_microservice_base_url(environment) + '/account-relay/'

        # Send request
        response = place_request('POST', request_url, request_body, request_headers)

        if response.status_code == 202:
            print(text.Green + 'Order: ' + order_id + 'was change')
            return response
        else:
            return 'false'
    else:
        print(text.Red + '\n- [Order Change] The order status expected is ACTIVE but the value found was ' + order_info['status'])
