from random import randint

from json import loads

from common import *


def check_if_order_exist(abi_id, zone, environment, order_id):

    # Get header request
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/order-service/v1?orderIds=' + order_id + '&accountId=' + abi_id

    # Place request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    else:
        return 'false'


def order_info(abi_id, zone, environment, order_id):
    order_response = check_if_order_exist(abi_id, zone, environment, order_id)

    if order_response == 'false':
        return 'error_ms'
    else:
        order_data = order_response[0]
        return order_data


def get_order_items(order_data):
    items = order_data['items']
    item_list = list()
    for i in range(len(items)):
        items_details = {
            'sku': items[i]['sku'],
            'price': items[i]['price'],
            'quantity': items[i]['quantity'],
            'subtotal': items[i]['subtotal'],
            'total': items[i]['total'],
            'freeGood': items[i]['freeGood'],
            'tax': items[i]['tax'],
            'discount': 0
        }
        item_list.append(items_details)
    return item_list


def get_order_details(order_data):
    order_details = {
        'accountId': order_data['accountId'],
        'placementDate': order_data['placementDate'],
        'paymentMethod': order_data['paymentMethod'],
        'channel': order_data['channel'],
        'subtotal': order_data['subtotal'],
        'total': order_data['total'],
        'tax': order_data['tax'],
        'discount': order_data['discount'],
        'itemsQuantity': order_data['itemsQuantity']
    }
    return order_details


def create_invoice_request(abi_id, zone, environment, order_id):
    order_data = order_info(abi_id, zone, environment, order_id)

    order_details = get_order_details(order_data)
    order_items = get_order_items(order_data)

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_invoice_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    invoice_id = 'DM-' + str(randint(1, 100000))

    dict_values = {
        'accountId': order_details.get('accountId'),
        'channel': order_details.get('channel'),
        'date': order_details.get('placementDate'),
        'interestAmount': order_details.get('total'),
        'itemsQuantity': order_details.get('itemsQuantity'),
        'orderDate': order_details.get('placementDate'),
        'orderId': order_id,
        'paymentTerm': order_details.get('paymentTerm'),
        'subtotal': order_details.get('subtotal'),
        'invoiceId': invoice_id,
        'tax': order_details.get('tax'),
        'total': order_details.get('total')
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    items = set_to_dictionary(json_object, 'items', order_items)

    # Send request
    if zone == 'ZA':
        request_url = get_middleware_base_url(zone, environment, 'v4') + '/invoices'
        request_headers = get_header_request(zone, 'false', 'true', 'false', 'false')
        request_body = convert_json_to_string(items)
    else:
        request_url = get_microservice_base_url(environment) + '/invoices-relay'
        request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')
        list_dict_values = create_list(items)
        request_body = convert_json_to_string(list_dict_values)

    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code != 202:
        print(text.Red + '\n- [Invoice] Something went wrong, please try again')
        finishApplication()
    else:
        print(text.Green + 'Invoice created: ' + invoice_id)
        return invoice_id

