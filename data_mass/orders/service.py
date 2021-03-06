from datetime import datetime
from json import loads

from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.common import (
    convert_json_to_string,
    find_values,
    get_header_request,
    get_microservice_base_url,
    place_request,
    set_to_dictionary,
    update_value_to_json
)


def get_changed_order_payload(order_data: list):
    """
    Create payload for order update.

    Parameters
    ----------
    order_data : list
        A list of dict. Order information.

    Returns
    -------
    dict
        Updated order payload.
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
    items = orders[0].get('items', [])
    item_information = []
    if not items:
        item_information.append({'Items': 'None'})
    else:
        for item in items:
            item_values = {
                'SKU': item.get('sku', ""),
                'Price': item.get('price', ""),
                'Quantity': item.get('quantity', ""),
                'Subtotal': item.get('subtotal', ""),
                'Total': item.get('total', ""),
                'Free Good': item.get('freeGood', "")
            }
            if 'tax' in items:
                tax = item.get('tax', "")
                set_to_dictionary(item_values, 'tax', tax)
            item_information.append(item_values)

    combos = orders[0].get('combos', [])
    combo_information = []
    if not combos:
        combo_information.append({'Combos': 'None'})
    else:
        for combo in combos:
            combo_values = {
                'Combo ID': combo.get('id', ''),
                'Type': combo.get('type', ''),
                'Quantity': combo.get('quantity', ''),
                'Title': combo.get('title', ''),
                'Description': combo.get('description', ''),
                'Original Price': combo.get('originalPrice', ''),
                'Price': combo.get('price', '')
            }
            combo_information.append(combo_values)

    order_information = []

    for order in orders:
        order_values = validate_order_parameters(order)
        order_information.append(order_values)

    print(text.default_text_color + '\nOrder Information By Account')
    print(tabulate(order_information, headers='keys', tablefmt='fancy_grid'))

    print(text.default_text_color + '\nOrder items')
    print(tabulate(item_information, headers='keys', tablefmt='fancy_grid'))

    print(text.default_text_color + '\nOrder combos')
    print(tabulate(combo_information, headers='keys', tablefmt='fancy_grid'))


def display_all_order_information(orders):
    """
    Display all order information by POC
    Args:
        orders: order data by account

    Returns: a table containing the available order information
    """
    order_information = list()

    for order in orders:
        order_values = validate_order_parameters(order)
        order_information.append(order_values)

    print(text.default_text_color + '\nAll Order Information By Account')
    print(tabulate(order_information, headers='keys', tablefmt='fancy_grid'))


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


def check_if_order_exists(account_id, zone, environment, order_id, order_status=None):
    """
    Check if an order exists via Order Service
    Args:
        account_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        order_id: order unique identifier
        order_status: order status, e.g., PLACED, DELIVERED

    Returns:
        empty: if an account does not have any order
        not_found: if the order_id does not exist
        false: if an error comes from back-end
    """
    # Get header request
    request_headers = get_header_request(
        zone, True, False, False, False, account_id
    )
    base_url = get_microservice_base_url(environment)

    if zone in ["CA", "US"]:
        request_url = (
            f"{base_url}/order-service/v2?orderIds={order_id}&"
            "orderBy=placementDate&sort=ASC&pageSize=2147483647"
        )
    elif order_status is not None:
        request_url = (
            f"{base_url}/order-service/v1?orderIds={order_id}&"
            f"orderStatus={order_status}&accountId={account_id}"
        )
    else:
        request_url = (
            f"{base_url}/order-service/v1?orderIds={order_id}&"
            f"accountId={account_id}"
        )

    # Place request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        if order_id == '':
            print(
                f"{text.Red}- [Order Service] The account "
                f"{account_id} does not have orders"
            )
            return 'not_found'
        else:
            print(
                f"{text.Red}- [Order Service] The order {order_id} "
                "does not exist."
            )
            return 'not_found'

    print(
        f"{text.Red}- [Order Service] Failure to retrieve order information.\n"
        f"Response Status: {response.status_code}.\n"
        f"Response message: {response.text}."
    )
    return False


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
        if 'pricingReasonDetail' in items[i] and items[i].get('pricingReasonDetail', []):
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
                'freeGood': items[i].get('freeGood', False),
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
    request_headers = get_header_request(zone, True, False, False, False, account_id)

    updated_since = datetime.now().strftime('%Y-%m-%d') + 'T00:00:00.000Z'

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/order-service/v1?updatedSince={}&accountId={}&sort={}'\
        .format(updated_since, account_id, 'DESC')

    # Place request
    response = place_request('GET', request_url, '', request_headers)
    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        if json_data[0]['orderNumber']:
            return json_data
    else:
        print(text.Red + '\n- [Order Service] Failure to retrieve order information. Response Status: '
                         '{response_status}. Response message: {response_message}'
                  .format(response_status=response.status_code, response_message=response.text))
        return False
