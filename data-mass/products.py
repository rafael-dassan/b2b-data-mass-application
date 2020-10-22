# Standard library imports
import json
from json import dumps, loads
import os
import concurrent.futures
from random import randint, uniform
from datetime import datetime

# Third party imports
from tabulate import tabulate

# Local application imports
from common import get_microservice_base_url, get_header_request, place_request, update_value_to_json, \
    convert_json_to_string, print_product_quantity_menu, create_list
from validations import validate_yes_no_option
from classes.text import text


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


def request_post_price_microservice(abi_id, zone, environment, sku_product, product_price_id, price_values):
    """
    Define price for a specific product via Pricing Engine Relay Service
    Args:
        abi_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        sku_product: SKU unique identifier
        product_price_id: price record unique identifier
        price_values: price values dict, including tax, base price and deposit
    Returns: `success` in case of successful response or `false` in case of failure
    """

    # Zones that are using the Pricing Engine Relay Service v2
    cart_v2_zones = ['CO', 'MX', 'AR', 'ZA', 'EC', 'PE', 'DO']
    if zone in cart_v2_zones:
        # Get base URL
        request_url = get_microservice_base_url(environment, 'false') + '/cart-calculation-relay/v2/prices'
        # Get request body
        request_body = get_body_price_microservice_request_v2(abi_id, sku_product, product_price_id, price_values)
    else:
        # Get base URL
        request_url = get_microservice_base_url(environment, 'false') + '/cart-calculation-relay/prices'
        # Get request body
        request_body = get_body_price_microservice_request(abi_id, sku_product, product_price_id, price_values)

    # Get headers
    request_headers = get_header_request(zone)

    # Send request
    response = place_request('PUT', request_url, request_body, request_headers)
    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Pricing Engine Relay Service] Failure to define price for the SKU ' + sku_product
              + '. Response Status: ' + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def get_body_price_microservice_request(abi_id, sku_product, product_price_id, price_values):
    """
    Create body for posting new product price rules (API version 1) to the Pricing Engine Relay Service
    Args:
        abi_id: POC unique identifier
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
    file_path = os.path.join(abs_path, 'data/create_sku_price_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Update the price values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    return request_body


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
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(
        environment) + '/items/?includeDeleted=false&includeDisabled=false&pageSize=' + str(page_size)

    # Send request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200:
        return json_data['items']
    else:
        print(text.Red + '\n- [Item Service] Failure to retrieve products. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


# Make the necessary requests to add a product in a microservice-based zone
def product_post_requests_microservice(product_data, abi_id, zone, environment, delivery_center_id):
    index, product = product_data
    price_values = generate_price_values(zone, product)

    # Call product association via Product Assortment Relay Service
    product_inclusion_ms_result = request_post_price_inclusion_microservice(zone, environment, product['sku'],
                                                                            delivery_center_id)
    if product_inclusion_ms_result == 'false':
        return 'false'

    # Call price inclusion via Pricing Engine Relay Service
    price_inclusion_result = request_post_price_microservice(abi_id, zone, environment, product['sku'], index,
                                                             price_values)
    if price_inclusion_result == 'false':
        return 'false'

    return 'success'


# Post requests for product price creation and product inclusion
def request_post_products_account_microservice(abi_id, zone, environment, delivery_center_id, products_data):
    results = list()
    last = datetime.now()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(product_post_requests_microservice, product_data, abi_id, zone, environment,
                                   delivery_center_id) for product_data in products_data]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    now = datetime.now()
    lapsed = (now - last).seconds
    print(text.default_text_color + '{}\n- Products added: {} / failed: {}. Completed in {} seconds.'
          .format(text.Green, results.count('success'), results.count('false'), lapsed))

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
    request_headers = get_header_request(zone, 'false', 'false', 'true', sku_product)

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/product-assortment-relay/inclusion'

    # Get body request
    request_body = get_body_price_inclusion_microservice_request(delivery_center_id)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)
    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Product Assortment Relay Service] Failure to associate the SKU ' + sku_product
              + '. Response Status: ' + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


# Create body for product inclusion
def get_body_price_inclusion_microservice_request(delivery_center_id):
    body_price_inclusion = dumps({
        "deliveryCenters": [delivery_center_id]
    })

    return body_price_inclusion


def request_get_offers_microservice(abi_id, zone, environment):
    """
    Get available SKUs for a specific account via Catalog Service
    Projection: SMALL
    Args:
        abi_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
    Returns:
        json_data: new json object in case of success
        not_found: if there is no product association for an account
        false: if there is any error coming from the microservice
    """

    # Get headers
    headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(
        environment) + '/catalog-service/catalog?accountId=' + abi_id + '&projection=SMALL'

    # Send request
    response = place_request('GET', request_url, '', headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        return 'not_found'
    else:
        print(text.Red + '\n- [Catalog Service] Failure to get a list of available SKUs. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


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
    request_url = get_microservice_base_url(environment, 'false') + '/items/' + sku + '?includeDisabled=false'

    # Get headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Send request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data['sku']
    elif response.status_code == 404:
        print(text.Red + '\n- [Item Service] SKU ' + sku + ' not found for country ' + zone)
        return 'false'
    else:
        print(text.Red + '\n- [Item Service] Failure to retrieve the SKU ' + sku + '. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def request_get_products_by_account_microservice(abi_id, zone, environment):
    """
    Get available SKUs for a specific account via Catalog Service
    Projection: LIST
    Args:
        abi_id: POC unique identifier
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
    Returns:
        json_data: new json object in case of success
        not_found: if there is no product association for an account
        false: if there is any error coming from the microservice
    """

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Define base URL
    request_url = get_microservice_base_url(
        environment) + '/catalog-service/catalog?accountId=' + abi_id + '&projection=LIST'

    # Send request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data
    elif response.status_code == 200 and len(json_data) == 0:
        return 'not_found'
    else:
        print(text.Red + '\n- [Catalog Service] Failure to get a list of available SKUs. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


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
    headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment) + '/product-assortment/?accountId=accountId' + account_id \
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
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def create_item(zone, environment, item_data):
    """
    Create or update an item via Item Relay Service
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        item_data: all necessary and relevant SKU data
    Returns: item_data in case of success or `false` in case of failure
    """

    # Define headers
    request_headers = get_header_request(zone, 'false', 'true', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment, 'false') + '/item-relay/items'

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/create_item_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    # Update JSON values
    for key in item_data.keys():
        json_object = update_value_to_json(json_data, key, item_data[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    # Place request
    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
        update_item_response = set_item_enabled(zone, environment, item_data)
        get_item_response = check_item_enabled(item_data.get('sku'), zone, environment)
        if update_item_response != 'false' and get_item_response != 'false':
            return item_data
    else:
        print(text.Red + '\n- [Item Relay Service] Failure to create an item. Response Status: ' + str(
            response.status_code) + '. Response message ' + response.text)
        return 'false'


def get_item_input_data():
    """
    Get input data from the user
    Returns: a dictionary containing the customized item data
    """

    sku_identifier = input(text.default_text_color + 'SKU identifier: ')
    # Create random value for the SKU identifier if the entry is empty
    if len(sku_identifier) == 0:
        sku_identifier = 'DM' + str(randint(1, 100000))

    name = input(text.default_text_color + 'Item name: ')
    brand_name = input(text.default_text_color + 'Brand name (e.g., SKOL, PRESIDENTE LIGHT, CASTLE): ').upper()
    container_name = input(text.default_text_color + 'Container name (e.g., BOTTLE, PET, CAN): ').upper()

    # Validate container size input data
    while True:
        try:
            container_size = int(input(text.default_text_color + 'Container size: '))
            break
        except ValueError:
            print(text.Red + '\n- The container size must be an integer value\n')

    container_unit_measurement = input(
        text.default_text_color + 'Container unit of measurement (e.g., ML, OZ): ').upper()

    # Validate returnable input data
    is_returnable = input(text.default_text_color + 'Is it returnable? y/N: ').upper()
    while validate_yes_no_option(is_returnable) is False:
        print(text.Red + "\n- Invalid option\n")
        is_returnable = input(text.default_text_color + 'Is it returnable? y/N: ').upper()
    if is_returnable == 'Y':
        is_returnable = True
    else:
        is_returnable = False

    # Create random value for the sales ranking
    sales_ranking = randint(1, 100)

    # Create item dictionary
    item_data = {
        'sku': sku_identifier,
        'name': name,
        'brandName': brand_name,
        'subBrandName': brand_name,
        'package.id': sku_identifier,
        'container.name': container_name,
        'container.size': container_size,
        'container.returnable': is_returnable,
        'container.unitOfMeasurement': container_unit_measurement,
        'salesRanking': sales_ranking
    }

    return item_data


def set_item_enabled(zone, environment, item_data):
    """
    Update an item via Item Service
    Args:
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., DEV, SIT, UAT
        item_data: all necessary and relevant SKU data
    Returns: `success` when the item is updated successfully or `false` in case of failure
    """

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment, 'false') + '/items/' + item_data.get('sku')

    # Create file path
    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, 'data/update_item_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        'sku': item_data.get('sku'),
        'itemName': item_data.get('name'),
        'package.packageId': item_data.get('package.id'),
        'container.name': item_data.get('container.name'),
        'container.itemSize': item_data.get('container.size'),
        'container.unitOfMeasurement': item_data.get('container.unitOfMeasurement'),
        'description': item_data.get('name'),
        'salesRanking': item_data.get('salesRanking')
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
        print(text.Red + '\n- [Item Service] Failure to update an item. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


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
    headers = get_header_request(zone, 'true')

    # Get url base
    request_url = get_microservice_base_url(environment, 'false') + '/items/' + sku_id + '?includeDisabled=false'

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
