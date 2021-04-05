import json
from json import dumps, loads
import os
import concurrent.futures

from random import randint, uniform
from datetime import datetime
from tabulate import tabulate
from data_mass.common import get_microservice_base_url, get_header_request, \
    place_request, update_value_to_json, convert_json_to_string, create_list, \
    finish_application
from data_mass.menus.product_menu import print_product_quantity_menu, \
    print_is_returnable_menu, print_is_narcotic_menu, print_is_alcoholic_menu
from data_mass.classes.text import text


def generate_random_price_ids(qtd):
    if qtd < 1:
        return []

    array_random_ids = set()
    while len(array_random_ids) < qtd:
        new_prefix = 'DM' + str(randint(10000, 99999))
        array_random_ids.add(new_prefix)

    return list(array_random_ids)


# Slices a list of products, returning the first X elements
def slice_array_products(quantity, products):
    return products[0: quantity]


def format_seconds_to_min_sec(seconds):
    minutes = seconds // 60
    seconds %= 60
    return '%02i:%02i' % (minutes, seconds)


def request_post_price_microservice(account_id, zone, environment, sku_product, product_price_id, price_values):
    """
    Define price for a specific product via Pricing Engine Relay Service
    Args:
        account_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        sku_product: SKU unique identifier
        product_price_id: price record unique identifier
        price_values: price values dict, including tax, base price and deposit
    Returns: `success` in case of successful response or `false` in case of failure
    """

    # Get base URL
    request_url = get_microservice_base_url(environment, False) + '/cart-calculation-relay/v2/prices'

    # Get request body
    request_body = get_body_price_microservice_request_v2(account_id, sku_product, product_price_id, price_values)

    # Get headers
    request_headers = get_header_request(zone)

    # Send request
    response = place_request('PUT', request_url, request_body, request_headers)
    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Pricing Engine Relay Service] Failure to define price for the SKU {sku}. Response '
                         'status: {response_status}. Response message: {response_message}'
              .format(sku=sku_product, response_status=response.status_code, response_message=response.text))
        return False


def generate_price_values(zone, product):
    """
    Generate random price values for a specific product
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        product: product information, such as name, brand name, returnable, etc.
    Returns: new price values dict
    """

    # Generate random base price
    base_price = round(uniform(50, 2000), 2)
    deposit = None

    # Check if the SKU is returnable for ZA and DO (the ones that have deposit value enabled in order summary)
    if zone == 'ZA' or zone == 'DO':
        if 'container' in product and product['container']['returnable'] is True:
            deposit = ((2 / 100) * base_price)

    # Create dictionary with price values
    price_values = {
        'basePrice': base_price,
        'tax': randint(1, 5),
        'deposit': deposit,
        'quantityPerPallet': round(uniform(1, 2000), 2)
    }

    return price_values


# Add products in microservice account
def add_products_to_account_microservice(abi_id, zone, environment, delivery_center_id, all_products_zone):
    # Get desired product quantity to be associated
    product_qty = print_product_quantity_menu(all_products_zone)

    # Builds a list of products to be posted, along with their generated random IDs for price and inclusion
    products_data = list(zip(generate_random_price_ids(product_qty), slice_array_products(product_qty,
                                                                                          all_products_zone)))

    # Associate products to an account
    result = request_post_products_account_microservice(abi_id, zone, environment, delivery_center_id, products_data)

    return result


def request_get_products_microservice(zone, environment, page_size=100000):
    """
    Get all available products for a specific zone via Item Service
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        page_size: page size for searching products in the microservice
    Returns: array of items in case of success or `false` in case of failure
    """

    # Get headers
    request_headers = get_header_request(zone, True, False, False, False)

    # Get base URL
    request_url = get_microservice_base_url(
        environment) + '/items/?includeDeleted=false&includeDisabled=false&pageSize=' + str(page_size)

    # Send request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200:
        return json_data['items']
    else:
        print(text.Red + '\n- [Item Service] Failure to retrieve products. Response Status: {response_status}. '
                         'Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return False


# Make the necessary requests to add a product in a microservice-based zone
def product_post_requests_microservice(product_data, account_id, zone, environment, delivery_center_id):
    index, product = product_data
    price_values = generate_price_values(zone, product)

    # Call product association via Product Assortment Relay Service
    product_inclusion_ms_result = request_post_price_inclusion_microservice(zone, environment, product['sku'],
                                                                            delivery_center_id)
    if not product_inclusion_ms_result:
        return False

    # Call price inclusion via Pricing Engine Relay Service
    price_inclusion_result = request_post_price_microservice(account_id, zone, environment, product['sku'], index,
                                                             price_values)
    if not price_inclusion_result:
        return False

    return 'success'


# Post requests for product price creation and product inclusion
def request_post_products_account_microservice(account_id, zone, environment, delivery_center_id, products_data):
    results = list()
    last = datetime.now()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(product_post_requests_microservice, product_data, account_id, zone, environment,
                                   delivery_center_id) for product_data in products_data]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    now = datetime.now()
    lapsed = (now - last).seconds
    print(text.default_text_color + '{}\n- Products added: {} / failed: {}. Completed in {} seconds.'
          .format(text.Green, results.count('success'), results.count(False), lapsed))

    return 'success'


def request_post_price_inclusion_microservice(zone, environment, sku_product, delivery_center_id):
    """
    Create product association to an account via Product Assortment Relay Service
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        sku_product: SKU unique identifier
        delivery_center_id: POC's unique delivery center
    Returns: `success` in case of successful response or `false` in case of failure
    """

    # Get headers
    request_headers = get_header_request(zone, False, False, True, sku_product)

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/product-assortment-relay/inclusion'

    # Get body request
    request_body = get_body_price_inclusion_microservice_request(delivery_center_id)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)
    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Product Assortment Relay Service] Failure to associate the SKU {sku}. Response status: '
                         '{response_status}. Response message: {response_message}'
              .format(sku=sku_product, response_status=response.status_code, response_message=response.text))
        return False


# Create body for product inclusion
def get_body_price_inclusion_microservice_request(delivery_center_id):
    body_price_inclusion = dumps({
        "deliveryCenters": [delivery_center_id]
    })

    return body_price_inclusion


def request_get_offers_microservice(account_id, zone, environment):
    """
    Get available SKUs for a specific account via Catalog Service
    Projection: SMALL
    Args:
        account_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
    Returns:
        json_data: new json object in case of success
        not_found: if there is no product association for an account
        false: if there is any error coming from the microservice
    """

    # Get headers
    headers = get_header_request(zone, True, False, False, False, account_id)

    # Get base URL
    request_url = get_microservice_base_url(
        environment) + '/catalog-service/catalog?accountId=' + account_id + '&projection=SMALL'

    # Send request
    response = place_request('GET', request_url, '', headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        return 'not_found'
    else:
        print(text.Red + '\n- [Catalog Service] Failure to get a list of available SKUs. Response Status: '
                         '{response_status}. Response message: {response_message}'
              .format(response_status=response.status_code,response_message=response.text))
        return False


def check_item_enabled(sku, zone, environment):
    """
    Check if a SKU is enabled via Item Service
    Args:
        sku: product unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
    Returns:
        json_data: new json object in case of success
        not_found: if the product is disabled
        False: if there is any error coming from the microservice
    """

    # Get base URL
    request_url = get_microservice_base_url(environment, False) + '/items/' + sku + '?includeDisabled=false'

    # Get headers
    request_headers = get_header_request(zone, True, False, False, False)

    # Send request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data['sku']
    elif response.status_code == 404:
        print(text.Red + '\n- [Item Service] SKU {sku} not found for country {country}'.format(sku=sku, country=zone))
        return False
    else:
        print(text.Red + '\n- [Item Service] Failure to update an item. Response Status: {response_status}. Response '
                         'message: {response_message}'.format(response_status=response.status_code,
                                                              response_message=response.text))
        return False


def request_get_products_by_account_microservice(account_id, zone, environment):
    """
    Get available SKUs for a specific account via Catalog Service
    Projection: LIST
    Args:
        account_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
    Returns:
        json_data: new json object in case of success
        not_found: if there is no product association for an account
        false: if there is any error coming from the microservice
    """

    # Define headers
    request_headers = get_header_request(zone, True, False, False, False, account_id)

    # Define base URL
    request_url = get_microservice_base_url(
        environment) + '/catalog-service/catalog?accountId=' + account_id + '&projection=LIST'

    # Send request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        return 'not_found'
    else:
        print(text.Red + '\n- [Catalog Service] Failure to get a list of available SKUs. Response Status: '
                         '{response_status}. Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return False


def get_body_price_microservice_request_v2(abi_id, sku_product, product_price_id, price_values):
    """
    Create body for posting new product price rules (API version 2) to the Pricing Engine Relay Service
    Args:
        abi_id: account_id
        sku_product: SKU unique identifier
        product_price_id: price record unique identifier
        price_values: price values dict, including tax, base price and deposit
    Returns: new price body
    """

    # Create dictionary with price values
    dict_values = {
        'accounts': [abi_id],
        'prices[0].sku': sku_product,
        'prices[0].basePrice': price_values.get('basePrice'),
        'prices[0].deposit': price_values.get('deposit'),
        'prices[0].quantityPerPallet': price_values.get('quantityPerPallet'),
        'prices[0].taxes[0].taxId': product_price_id,
        'prices[0].taxes[0].value': str(price_values.get('tax'))
    }

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/create_sku_price_payload_v2.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Update the price values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    put_price_microservice_body = convert_json_to_string(json_object)

    return put_price_microservice_body


def request_get_account_product_assortment(account_id, zone, environment, delivery_center_id):
    """
    Get product association for a specific account via Product Assortment Service
    Args:
        account_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        delivery_center_id: POC's delivery center unique identifier
    Returns: array of SKUs in case of success and `false` in case of failure
    """

    # Get headers
    headers = get_header_request(zone, True, False, False, False, account_id)

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/product-assortment/?accountId=' + account_id \
                  + '&deliveryCenterId=' + delivery_center_id

    # Place request
    response = place_request('GET', request_url, '', headers)

    json_data = loads(response.text)
    skus = json_data['skus']
    if response.status_code == 200 and len(json_data) != 0:
        return skus
    elif response.status_code == 200 and len(skus) == 0:
        return 'not_found'
    else:
        print(text.Red + '\n- [Product Assortment Service] Failure to get product association. Response Status: '
                         '{response_status}. Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return False


def create_product(zone, environment, product_data):
    """
    Create or update an product via Item Relay Service
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        product_data: all necessary and relevant SKU data
    Returns: product_data in case of success or `false` in case of failure
    """

    # Define headers
    request_headers = get_header_request(zone, False, True, False)

    # Get base URL
    request_url = '{0}/item-relay/items'.format(get_microservice_base_url(environment, False))

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/create_item_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Update JSON values
    for key in product_data.keys():
        json_object = update_value_to_json(json_data, key, product_data[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    # Place request
    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
        update_item_response = set_item_enabled(zone, environment, product_data)
        get_item_response = check_item_enabled(product_data.get('sku'), zone, environment)
        if update_item_response and get_item_response:
            return product_data
    else:
        print('\n{0}- [Item Relay Service] Failure to update an item. Response Status: {1}. Response message: {2}'
              .format(text.Red, response.status_code, response.text))
        return False


def get_item_input_data():
    """
    Get input data from the user
    Returns: a dictionary containing the customized product data
    """
    sku_identifier = input('{0}SKU identifier: '.format(text.default_text_color))
    # Create random value for the SKU identifier if the entry is empty
    if len(sku_identifier) == 0:
        sku_identifier = 'DM-{0}'.format(str(randint(1, 100000)))

    name = input('{0}Item name: '.format(text.default_text_color))
    brand_name = input('{0}Brand name (e.g., SKOL, PRESIDENTE): '.format(text.default_text_color)).upper()
    container_name = input('{0}Container name (e.g., BOTTLE, PET, CAN): '.format(text.default_text_color)).upper()

    # Validate container size input data
    while True:
        try:
            container_size = int(input('{0}Container size: '.format(text.default_text_color)))
            break
        except ValueError:
            print('\n{0}- The container size must be an integer value\n'.format(text.Red))

    container_unit_measurement = input('{0}Container unit of measurement (e.g., ML, OZ): '.format(text.default_text_color)).upper()
    is_returnable = print_is_returnable_menu()
    is_narcotic = print_is_narcotic_menu()
    is_alcoholic = print_is_alcoholic_menu()

    # Create item dictionary
    item_data = {
        'sku': sku_identifier,
        'name': name,
        'brandName': brand_name,
        'subBrandName': brand_name,
        'package.id': str(randint(1, 1000)),
        'container.name': container_name,
        'container.size': container_size,
        'container.returnable': is_returnable,
        'container.unitOfMeasurement': container_unit_measurement,
        'salesRanking': randint(1, 100),
        'isNarcotic': is_narcotic,
        'isAlcoholic': is_alcoholic
    }

    return item_data


def set_item_enabled(zone, environment, product_data):
    """
    Update an item via Item Service
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        product_data: all necessary and relevant SKU data
    Returns: `success` when the item is updated successfully or `false` in case of failure
    """
    # Define headers
    request_headers = get_header_request(zone, True, False, False)

    # Get base URL
    request_url = '{0}/items/{1}'.format(get_microservice_base_url(environment, False), product_data.get('sku'))

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/update_item_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'itemName': product_data.get('name'),
        'package.packageId': product_data.get('package.id'),
        'container.name': product_data.get('container.name'),
        'container.itemSize': product_data.get('container.size'),
        'container.unitOfMeasurement': product_data.get('container.unitOfMeasurement'),
        'description': product_data.get('name'),
        'salesRanking': product_data.get('salesRanking')
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Place request
    response = place_request('PUT', request_url, request_body, request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return 'success'
    else:
        print(text.Red + '\n- [Item Service] Failure to update an item. Response Status: {response_status}. '
                         'Response message: {response_message}'.format(response_status=response.status_code,
                                                                       response_message=response.text))
        return False


def display_product_information(product_offers):
    """
    Display item information
    Args:
        product_offers: product data by account
    Returns: a table containing the available item information
    """

    product_information = list()
    for i in range(len(product_offers)):
        product_values = {
            'SKU': product_offers[i]['sku'],
            'Name': product_offers[i]['itemName'],
            'Price': product_offers[i]['price'],
            'Returnable': product_offers[i]['container']['returnable'],
            'Stock Available': product_offers[i]['stockAvailable']
        }
        product_information.append(product_values)

    print(text.default_text_color + '\nProduct Information By Account')
    print(tabulate(product_information, headers='keys', tablefmt='grid'))


# Get SKU name
def get_sku_name(zone, environment, sku_id):
    # Get header request
    headers = get_header_request(zone, True)

    # Get url base
    request_url = get_microservice_base_url(environment, False) + '/items/' + sku_id + '?includeDisabled=false'

    # Place request
    response = place_request('GET', request_url, '', headers)
    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        sku_name = json_data['itemName']
    else:
        sku_name = ''

    return sku_name


def display_items_information_zone(items):
    list_items = list()
    if len(items) != 0:
        for i in range(len(items)):
            dict_values = {
                'SKU': items[i]['sku'],
                'Name': items[i]['itemName'],
                'Description': items[i]['description'],
                'Brand Name': items[i]['brandName'],
                'Returnable': items[i]['container']['returnable']
            }
            list_items.append(dict_values)
    else:
        dict_values = {
            'Products': 'None'
        }
        list_items.append(dict_values)

    print(text.default_text_color + '\nProduct Information By Zone')
    print(tabulate(list_items, headers='keys', tablefmt='grid'))


def get_sku_price(account_id, combo_item, zone, environment):
    # Get base URL
    request_url = get_microservice_base_url(environment) + '/cart-calculator/prices?accountID=' + account_id

    # Get header request
    request_headers = get_header_request(zone, True, False, False, False, account_id)

    # Send request
    response = place_request('GET', request_url, '', request_headers)

    json_data = json.loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        for my_dict in json_data:
            if my_dict['sku'] == combo_item:
                return my_dict['price']
    else:
        print(text.Red + '\n- [Pricing Engine Service] Failure to get price. Response '
                         'status: {response_status}. Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        finish_application()


def request_empties_discounts_creation(account_id, zone, environment, empty_sku, discount_value):
    # Define headers
    request_headers = get_header_request(zone)

    # Get base URL
    request_url = get_microservice_base_url(environment, False) + '/cart-calculation-relay/v2/prices'

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/create_empties_discounts_payload.json')

    dict_values = {
        'accounts': [account_id],
        'prices[0].sku': empty_sku,
        'prices[0].basePrice': discount_value,
        'prices[0].minimumPrice': discount_value
    }

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Update JSON values
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Place request
    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Pricing Engine Relay Service] Failure to define price for the empty SKU {sku}. Response '
                         'status: {response_status}. Response message: {response_message}'
              .format(sku=empty_sku, response_status=response.status_code, response_message=response.text))
        return False
