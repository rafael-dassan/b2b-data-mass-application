from random import randint, uniform
from json import loads, dumps
import concurrent.futures
from common import *
from tabulate import tabulate


# Return an array of price IDs for price inclusion
def generate_random_price_ids(qtd):
    if qtd < 1:
        return []

    array_random_ids = set()
    prefix = 'DM'
    while len(array_random_ids) < qtd:
        new_prefix = prefix + str(randint(10000, 99999))
        array_random_ids.add(new_prefix)

    return list(array_random_ids)


# Get body request for product's price
def get_body_price_middleware_request(body_id, price_list_id, price_values):
    price = price_values.get('basePrice') + price_values.get('tax') + price_values.get('deposit')

    dict_values = {
        'id': body_id,
        'price': round(price, 2),
        'priceListId': price_list_id
    }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/price_inclusion_middleware.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    put_price_body = convert_json_to_string(json_object)

    return put_price_body


# Slices a list of products, returning the first X elements
def slice_array_products(quantity, products):
    return products[0: quantity]


# Does the necessary requests to add a product in a middleware-based zone
def product_post_requests_middleware(product_data, abi_id, zone, environment):
    index, product = product_data
    price_list_id = abi_id
    delivery_center_id = abi_id

    price_values = generate_price_values_v1()

    # Request to create price on microservice
    post_price_ms_result = request_post_price_microservice(abi_id, zone, environment, product['sku'], index,
                                                           price_values)

    # Request to create price on middleware
    post_price_middleware_result = request_post_price_middleware(zone, environment, product['sku'], index,
                                                                 price_list_id, price_values)

    # Request to include a product into a specific delivery center
    product_inclusion_result = product_inclusion_middleware(zone, environment, product['sku'], index,
                                                            delivery_center_id)

    if post_price_ms_result == 'false' or post_price_middleware_result == 'false' or product_inclusion_result == 'false':
        return 'false'

    return 'true'


def format_seconds_to_mmss(seconds):
    minutes = seconds // 60
    seconds %= 60
    return '%02i:%02i' % (minutes, seconds)


# Post request product price microservice
def request_post_price_microservice(abi_id, zone, environment, sku_product, product_price_id, price_values):
    # Get header request
    request_headers = get_header_request(zone)

    if zone == 'CO' or zone == 'MX' or zone == 'AR' or zone == 'ZA':
        # Get base URL
        request_url = get_microservice_base_url(environment, 'false') + '/cart-calculation-relay/v2/prices'

        # Get request body
        request_body = get_body_price_microservice_request_v2(abi_id, sku_product, product_price_id)
    else:
        # Get url base
        request_url = get_microservice_base_url(environment) + '/cart-calculation-relay/prices'

        # Get request body
        request_body = get_body_price_microservice_request(abi_id, sku_product, product_price_id, price_values)

    # Place request
    response = place_request('PUT', request_url, request_body, request_headers)
    if response.status_code != 202:
        print(text.Red + '\n- [Product] Something went wrong in define product price SKU '
              + str(sku_product) + ' on microservice price engine')
        return 'false'

    return 'true'


# Get body product price microservice request
def get_body_price_microservice_request(abi_id, sku_product, product_price_id, price_values):
    put_price_microservice_body = dumps({
        "accounts": [abi_id],
        "prices": [
            {
                "sku": sku_product,
                "taxes": [
                    {
                        "taxId": product_price_id,
                        "type": "$",
                        "value": str(price_values.get('tax')),
                        "taxBaseInclusionIds": [
                        ]
                    }
                ],
                "basePrice": price_values.get('basePrice'),
                "measureUnit": "CS",
                "minimumPrice": 0,
                "tax": price_values.get('tax'),
                "deposit": price_values.get('deposit'),
                "quantityPerPallet": round(uniform(1, 2000), 2)
            }
        ]
    })

    return put_price_microservice_body


# Generate random price values
def generate_price_values_v1():
    price_values = {
        'basePrice': round(uniform(1, 2000), 2),
        'tax': randint(1, 20),
        'deposit': round(uniform(1, 5), 2)
    }

    return price_values


# Post request product price middleware
def request_post_price_middleware(zone, environment, sku_product, product_price_id, price_list_id, price_values):
    # Get header request
    request_headers = get_header_request(zone, 'false', 'true')

    # Get url base
    request_url = get_middleware_base_url(zone, environment, 'v4') + '/products/' + str(sku_product) + '/prices'

    # Get request body
    request_body = get_body_price_middleware_request(product_price_id, price_list_id, price_values)

    # Place request
    response = place_request('POST', request_url, request_body, request_headers)
    if response.status_code != 202:
        print(text.Red + '\n- [Price Inclusion] Failure to define a product price. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'

    return 'true'


# Post request product inclusion middleware
def product_inclusion_middleware(zone, environment, sku_product, inclusion_id, delivery_center_id):
    # Define headers
    request_headers = get_header_request(zone, 'false', 'true')

    # Get base URL
    request_url = get_middleware_base_url(zone, environment, 'v4') + '/products/' + str(sku_product) + '/inclusions'

    dict_values = {
        'deliveryCenterId': delivery_center_id,
        'id': inclusion_id
    }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/product_inclusion_middleware.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code != 202:
        print(text.Red + '\n- [Product Inclusion] Product inclusion has failed. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'

    return 'true'


# Add products in microservice account
def add_products_to_account_microservice(abi_id, zone, environment, delivery_center_id):
    # Request get products microservice
    all_products_microservice = request_get_products_microservice(zone, environment)

    while True:
        try:
            qtd = int(input(text.default_text_color + 'Number of products you want to add (Maximum: '
                            + str(len(all_products_microservice)) + '): '))
            while qtd <= 0:
                print(text.Red + '\n- The product quantity must be more than 0\n')
                qtd = int(input(text.default_text_color + 'Number of products you want to add (Maximum: '
                                + str(len(all_products_microservice)) + '): '))
            break
        except ValueError:
            print(text.Red + '\n- The product quantity must be Numeric\n')

    # Builds a list of products to be posted, along with their generated random IDs for price and inclusion in account
    products_data = list(zip(generate_random_price_ids(qtd), slice_array_products(qtd, all_products_microservice)))

    # Insert products in account
    result = request_post_products_account_microservice(abi_id, zone, environment, delivery_center_id, products_data)

    return result


# Post requests get products from microservice
def request_get_products_microservice(zone, environment, page_size=100000):
    # Get header request
    request_headers = get_header_request(zone, "true", "false", "false", "false")

    # Get url base
    request_url = get_microservice_base_url(
        environment) + "/items/?includeDeleted=false&includeDisabled=false&pageSize=" + str(page_size)

    # Get body request
    request_body = ""

    # Place request
    response = place_request("GET", request_url, request_body, request_headers)
    if response.status_code == 200:
        json_data = loads(response.text)
        return json_data['items']
    else:
        print(text.Red + '\n- [Product] Something went wrong in search products on microservice')
        finishApplication()


# Does the necessary requests to add a product in a microservice-based zone
def product_post_requests_microservice(product_data, abi_id, zone, environment, delivery_center_id):
    index, product = product_data
    price_values = generate_price_values_v1()

    product_inclusion_ms_result = request_post_price_inclusion_microservice(zone, environment, product['sku'], index,
                                                                            delivery_center_id)
    if product_inclusion_ms_result == 'false':
        return 'false'

    if zone == 'ZA' or zone == 'AR':
        product_inclusion_mdw_result = product_post_requests_middleware(product_data, abi_id, zone, environment)
        if product_inclusion_mdw_result == 'false':
            return 'false'
    else:
        price_inclusion_result = request_post_price_microservice(abi_id, zone, environment, product['sku'], index,
                                                                 price_values)
        if price_inclusion_result == 'false':
            return 'false'

    return 'true'


# Post requests product price and product inclusion in account
def request_post_products_account_microservice(abi_id, zone, environment, delivery_center_id, products_data):
    results = []
    print(text.default_text_color + '\nAdding products. Please wait...')
    last = datetime.now()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(product_post_requests_microservice, product_data, abi_id, zone, environment,
                                   delivery_center_id) for product_data in products_data]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    now = datetime.now()
    lapsed = (now - last).seconds
    print(text.default_text_color + '{}\n- Products added: {} / failed: {}. Completed in {} seconds.'
          .format(text.Green, results.count('true'), results.count('false'), lapsed))

    return 'success'


# Post request product inclusion microservice
def request_post_price_inclusion_microservice(zone, environment, sku_product, product_price_id, delivery_center_id):
    # Get header request
    request_headers = get_header_request(zone, 'false', 'false', 'true', sku_product)

    # Get url base
    request_url = get_microservice_base_url(environment) + "/product-assortment-relay/inclusion"

    # Get body request
    request_body = get_body_price_inclusion_microservice_request(delivery_center_id)

    # Place request
    response = place_request("POST", request_url, request_body, request_headers)

    if response.status_code != 202:
        print(text.Red + '\n- [Product] Something went wrong in post product SKU '
              + str(sku_product) + ' on account product-assortment-relay')
        return 'false'

    return 'true'


# Create body for product inclusion in account
def get_body_price_inclusion_microservice_request(delivery_center_id):
    body_price_inclusion = dumps({
        "deliveryCenters": [delivery_center_id]
    })

    return body_price_inclusion


# Get offers account in microservice
def request_get_offers_microservice(abi_id, zone, environment, delivery_center_id, return_product_data = False):
    if zone == 'ZA' or zone == 'AR':
        product_offers = request_get_offers_middleware(abi_id, zone, environment, True)
        return product_offers

    # Define headers
    headers = get_header_request(zone, 'true')

    # Get base URL
    request_url = get_microservice_base_url(
        environment) + '/catalog-service/catalog?accountId=' + abi_id + '&projection=SMALL'

    # Place request
    response = place_request('GET', request_url, '', headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        if return_product_data:
            return json_data
        else:
            return True
    elif response.status_code == 200 and len(json_data) == 0:
        return json_data
    else:
        print(text.Red + '\n- [Product Offers] Failure to get product offers. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)


# Get offers by account on middleware
def request_get_offers_middleware(abi_id, zone, environment, return_product_data=False):
    # Get base URL
    request_url = get_middleware_base_url(zone, environment, 'v4') + '/products/offers?accountId=' + abi_id

    # Define headers
    headers = get_header_request(zone, 'false', 'true', 'false', 'false')

    # Place request
    response = place_request('GET', request_url, '', headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        if return_product_data:
            sku_list = list()
            for dict in json_data:
                sku = dict['sku']
                sku_list.append(sku)
            return sku_list
        else:
            return True
    elif response.status_code == 200 and len(json_data) == 0:
        return json_data
    else:
        print(text.Red + '\n- [Product Offers Middleware] Failure to get product offers. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)


def check_item_enabled(sku, zone, environment, return_item_data=False):
    # Get base URL
    request_url = get_microservice_base_url(environment, 'false') + '/items/' + sku + '?includeDisabled=false'

    # Get header request
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Send request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        if return_item_data:
            return json_data['sku']
        else:
            return True
    elif response.status_code == 404:
        return False
    else:
        print(text.Red + '\n- [Items] Something went wrong when searching for items')
        finishApplication()


def request_get_response_products_by_account_microservice(abi_id, zone, environment):
    """Get response products by query parameters
    Arguments:
        - abi_id: account_id
        - zone: (e.g, BR,ZA,DO)
        - environment: (e.g, UAT,SIT)
    Return new json_object
    """
    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Define URL Middleware
    request_url = get_microservice_base_url(
        environment) + '/catalog-service/catalog?accountId=' + abi_id + '&projection=LIST'

    # Send request
    return place_request('GET', request_url, '', request_headers)


def request_get_products_by_account_microservice(abi_id, zone, environment):
    """Get products by query parameters
    Arguments:
        - abi_id: account_id
        - zone: (e.g, BR,ZA,DO)
        - environment: (e.g, UAT,SIT)
    Return new json_object
    """
    response = request_get_response_products_by_account_microservice(abi_id, zone, environment)
    if response.status_code == 200:
        return loads(response.text)
    else:
        return 'false'


# Get body product price microservice request v2
def get_body_price_microservice_request_v2(abi_id, sku_product, product_price_id):
    base_price = round(uniform(1, 2000), 2)
    promotion_price = base_price - ((10 / 100) * base_price)
    minimum_price = 0
    deposit = ((2 / 100) * base_price)
    charge_amount = ((4 / 100) * base_price)
    charge_base = ((2 / 100) * base_price)

    if minimum_price < 0.0:
        minimum_price = 0.0

    if promotion_price < 0.0:
        promotion_price = 0.0

    # Inputs for default payload of price microservice
    dict_values = {
        "accounts": [abi_id],
        "prices[0].sku": sku_product,
        "prices[0].basePrice": base_price,
        "prices[0].deposit": deposit,
        "prices[0].quantityPerPallet": round(uniform(1, 2000), 2),
        "prices[0].taxes[0].taxId": product_price_id,
        "prices[0].taxes[0].type": "$",
        "prices[0].taxes[0].value": str(randint(1, 5)),
        "prices[0].charges[0].chargeId": product_price_id + "LOGISTIC_COST",
        "prices[0].charges[0].type": "$",
        "prices[0].charges[0].value": charge_amount,
        "prices[0].charges[0].base": charge_base,
        "prices[0].charges[0].tax": None
    }

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "data/put_price_sku_microservice_v2_payload.json")

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    put_price_microservice_body = convert_json_to_string(json_object)

    return put_price_microservice_body


# Get offers account in microservice
def request_get_account_product_assortment(account_id, zone, environment, delivery_center_id):
    # Get header request
    headers = get_header_request(zone, 'true')

    # Get url base
    request_url = get_microservice_base_url(
        environment) + '/product-assortment/?accountId=accountId' + account_id + '&deliveryCenterId=' + delivery_center_id

    # Place request
    response = place_request('GET', request_url, '', headers)

    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) != 0:
        return json_data['skus']
    else:
        print(text.Red + '\n- [Products] Something went wrong when searching for products')


def create_item(zone, environment, item_data):
    """Create or update an item
    Arguments:
        - zone: (e.g, BR,ZA,DO)
        - environment: (e.g, QA,UAT)
        - item_data: all necessary and relevant SKU data
    """
    # Define headers
    request_headers = get_header_request(zone, 'false', 'true', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment, 'false') + '/item-relay/items'

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_item_payload.json')

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
        get_item_response = check_item_enabled(item_data.get('sku'), zone, environment, False)
        if update_item_response == True and get_item_response == True:
            return item_data
    else:
        print(text.Red + '\n- [Item Service] Failure to create an item. Response Status: ' + str(
            response.status_code) + '. Response message ' + response.text)


def get_item_input_data():
    """Get input data from the user
    Return a dictionary containing the customized item data
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
    while validate_yes_no_option(is_returnable) == "false":
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
    """Update an item via API
    Arguments:
        - zone: (e.g, BR,ZA,DO)
        - environment: (e.g, UAT,SIT)
        - item_data: all necessary and relevant SKU data
    Return True when the item is updated successfully
    """
    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false')

    # Get base URL
    request_url = get_microservice_base_url(environment, 'false') + '/items/' + item_data.get('sku')

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/update_item_payload.json')

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
        return True
    else:
        print(text.Red + '\n- [Item Service] Failure to update an item. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)


def display_product_information(product_offers):
    """Display item information
    Arguments:
        - product_offers: product data by account
    Print a table containing the available item information
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
    sku_name = json_data['itemName']

    return sku_name
