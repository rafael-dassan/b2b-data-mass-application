from random import randint
from common import *


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
        'discount': order_data['discount']
    }
    return order_details


def create_invoice_request(zone, environment, order_id, status, order_data):
    order_details = get_order_details(order_data)
    order_items = get_order_items(order_data)
    size_items = len(order_items)

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_invoice_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    invoice_id = 'DM-' + str(randint(1, 100000))
    order_placement_date = order_details.get('placementDate')
    if zone == 'DO':
        placement_date = order_placement_date.split('T')[0] + 'T00:00:00Z'
    else:
        placement_date = order_placement_date.split('+')[0] + 'Z'

    dict_values = {
        'accountId': order_details.get('accountId'),
        'channel': order_details.get('channel'),
        'date': placement_date,
        'interestAmount': order_details.get('total'),
        'orderDate': placement_date,
        'orderId': order_id,
        'paymentTerm': order_details.get('paymentTerm'),
        'subtotal': order_details.get('subtotal'),
        'invoiceId': invoice_id,
        'status': status,
        'tax': order_details.get('tax'),
        'total': order_details.get('total'),
        'poNumber': order_id
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    if 'itemsQuantity' not in order_data:
        set_to_dictionary(json_data, 'itemsQuantity', size_items)
    else:
        set_to_dictionary(json_data, 'itemsQuantity', order_data['itemsQuantity'])

    items = set_to_dictionary(json_object, 'items', order_items)

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/invoices-relay'

    # Get headers
    request_headers = get_header_request(zone, 'false', 'false', 'true', 'false')

    # Create body
    list_dict_values = create_list(items)
    request_body = convert_json_to_string(list_dict_values)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return invoice_id
    else:
        print(text.Red + '\n- [Invoice Relay Service] Failure to create an invoice. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'
