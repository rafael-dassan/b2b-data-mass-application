from random import randint, uniform
from json import loads

import concurrent.futures

# Custom
from helpers.common import *


def check_products_account_exists_microservice(accountId, zone, environment):
    
    # Define headers
    request_headers = get_header_request(zone, 'true')

    # Define URL Middleware
    request_url = get_microservice_base_url(environment) + '/middleware-relay/products/offers?accountId=' + accountId

    # Send request
    response = place_request("GET", request_url, "", request_headers)
    json_data = loads(response.text)
    if response.status_code == 200 and len(json_data) > 0:
        return 'success'
    elif response.status_code == 200 and len(json_data) == 0:
        return 'false'
    else:
        return response.status_code


def check_products_account_exists_middleware(abi_id, zone, environment):
    # Define headers
    headers = get_header_request(zone, 'false', 'true')
    
    # Define URL Middleware
    url = get_middleware_base_url(zone, environment, "v4") + "/products/offers?accountId=" + abi_id
    
    # Send request
    response = place_request("GET", url, "", headers)
    json_data = loads(response.text)
    if response.status_code == 200 and json_data != '':
        return 'success'
    elif response.status_code == 200 and json_data == '':
        return 'false'
    else:
        return response.status_code


# Return array prices id's for products
def generate_random_price_ids(qtd):
    if qtd < 1:
        return []

    array_random_ids = set()
    prefix = "ANTARCTICA"
    while len(array_random_ids) < qtd:
        new_prefix = prefix + str(randint(10000, 99999))
        array_random_ids.add(new_prefix)

    return list(array_random_ids)


# Get body request for price product
def get_body_price_middleware_request(body_id, price_list_id):
    
    put_price_body = dumps({
        "endDate": "2021-12-31T00:00:00Z",
        "id": body_id,
        "price": round(uniform(1,2000), 2),
        "priceListId": price_list_id,
        "startDate": "2018-12-12T00:00:00Z"
    })

    return put_price_body

# Post request to get products from Middleware
def request_get_products_middleware(zone, environment):

    # Get header request
    headers = get_header_request(zone, "false", "true")
    
    # Get base URL
    request_url = get_middleware_base_url(zone, environment, "v4") + "/products"

    # Get body request
    request_body=""

    # Send request
    response = place_request("GET", request_url, request_body, headers)

    if response.status_code == 200:
        json_data = loads(response.text)
        return json_data
    else:
        print("- [Product] Something went wrong, please try again")


# Slices a list of products, returning the first X elements
def slice_array_products(quantity, products):
    return products[0: quantity]


# Does the necessary requests to add a product in a middleware-based zone
def product_post_requests_middleware(product_data, abi_id, zone, environment):
    index, product = product_data
    price_list_id = abi_id
    delivery_center_id = abi_id

    result = request_post_price_middleware(
        zone, environment, product['sku'], index, price_list_id)
    if result == 'false':
        return result
    result = request_post_price_inclusion_middleware(
        zone, environment, product['sku'], index, delivery_center_id)
    if result == 'false':
        return result

    # Workaround to prevent requests from CL to go to the Pricing Engine MS
    if zone != 'CL':
        result = request_post_price_microservice(
            abi_id, zone, environment, product['sku'], index)

    return 'true'


# Post requests product price and product inclusion in account
def request_post_products_account_middleware(abi_id, zone, environment, products_data):
    results = []

    print('\nAdding products. Please wait...')
    last = datetime.now()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(product_post_requests_middleware, product_data, abi_id, zone, environment) for
                   product_data in products_data]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    now = datetime.now()
    lapsed = (now - last).seconds
    print('{}\n- Products added: {} / failed: {}. Completed in {} seconds.'.format(text.LightGreen,
                                                                                   results.count('true'),
                                                                                   results.count('false'), lapsed))
    return 'success'


def format_seconds_to_mmss(seconds):
    minutes = seconds // 60
    seconds %= 60
    return '%02i:%02i' % (minutes, seconds)

# Post request product price microservice
def request_post_price_microservice(abi_id, zone, environment, sku_product, product_price_id):
    # Get header request
    request_headers = get_header_request(zone)

    # Get url base
    request_url = get_microservice_base_url(environment) + "/cart-calculation-relay/prices"

    # Get request body
    request_body = get_body_price_microservice_request(abi_id, sku_product, product_price_id)

    # Place request
    response = place_request("PUT", request_url, request_body, request_headers)
    if response.status_code != 202:
        print('- [Product] Something went wrong in define product price SKU ' + str(sku_product) + ' on microservice price engine')
        return 'false'
    
    return 'true'

# Get body product price microservice request
def get_body_price_microservice_request(abi_id, sku_product, product_price_id):
    put_price_microservice_body = dumps({
        "accounts": [abi_id],
        "prices": [
            {
                "sku": sku_product,
                "taxes": [
                    {
                        "taxId": product_price_id,
                        "type": "$",
                        "value": str(randint(1, 20)),
                        "taxBaseInclusionIds": [
                        ]
                    }
                ],
                "basePrice": round(uniform(1, 2000), 2),
                "measureUnit": "CS",
                "minimumPrice": 0,
                "tax": round(uniform(1, 10), 2),
                "deposit": round(uniform(1, 5), 2),
                "quantityPerPallet": round(uniform(1, 2000), 2)
            }
        ]
    })

    return put_price_microservice_body

# Post request product price middleware
def request_post_price_middleware(zone, environment, sku_product, product_price_id, price_list_id):
    
    # Get header request
    request_headers = get_header_request(zone, 'false', 'true')

    # Get url base
    request_url = get_middleware_base_url(zone, environment, "v4") + "/products/" + str(sku_product) + "/prices"

    # Get request body
    request_body = get_body_price_middleware_request(product_price_id, price_list_id)

    # Place request
    response = place_request("POST", request_url, request_body, request_headers)
    if response.status_code != 202:
        print('- [Product] Something went wrong in define product price SKU ' + str(sku_product) + ' on middleware')
        return 'false'
    
    return 'true'

# Post request product inclusion middleware
def request_post_price_inclusion_middleware(zone, environment, sku_product, product_price_id, delivery_center_id):

    # Get header request
    request_headers = get_header_request(zone, 'false', 'true')

    # Get url base
    request_url = get_middleware_base_url(zone, environment, "v4") + "/products/" + str(sku_product) + "/inclusions"

    # Get body request
    request_body = get_body_price_inclusion_request(product_price_id, delivery_center_id)

    # Place request
    response = place_request("POST", request_url, request_body, request_headers)
    if response.status_code != 202:
        print('- [Product] Something went wrong in post product SKU ' + str(sku_product) + ' on account')
        return 'false'
    
    return 'true'

# Create body for product inclusion in account
def get_body_price_inclusion_request(product_price_id, delivery_center_id):
    body_price_inclusion = dumps({
        "deliveryCenterId": delivery_center_id,
        "id": product_price_id,
    })

    return body_price_inclusion


# Add products in middleware account
def add_products_to_account_middleware(abi_id, zone, environment):
    # Request get products middleware
    all_products_middleware = request_get_products_middleware(zone, environment)
    maximum = min(15, len(all_products_middleware))

    qtd = input("Number of products you want to add (Maximum: " + str(len(all_products_middleware)) + " - Default: " + str(maximum) + "): ")
    if qtd == "":
        qtd = maximum

    qtd = int(qtd)

    # Builds a list of products to be posted, along with their generated random IDs for price and inclusion in account
    products_data = list(zip(generate_random_price_ids(qtd), slice_array_products(qtd, all_products_middleware)))

    # Insert products in account
    result = request_post_products_account_middleware(abi_id, zone, environment, products_data)

    return result


# Add products in microservice account
def add_products_to_account_microservice(abi_id, zone, environment, delivery_center_id):
    # Request get products microservice
    all_products_microservice = request_get_products_microservice(zone, environment)
    maximum = min(15, len(all_products_microservice))

    qtd = input("Number of products you want to add (Maximum: " + str(len(all_products_microservice)) + " - Default " + str(maximum) + "):")
    if qtd == "":
        qtd = maximum

    qtd = int(qtd)

    # Builds a list of products to be posted, along with their generated random IDs for price and inclusion in account
    products_data = list(zip(generate_random_price_ids(qtd), slice_array_products(qtd, all_products_microservice)))

    # Insert products in account
    result = request_post_products_account_microservice(abi_id, zone, environment, delivery_center_id, products_data)

    return result

# Post requests get products from microservice
def request_get_products_microservice(zone, environment):

    # Get header request
    request_headers = get_header_request(zone, 'true')

    # Get url base
    request_url = get_microservice_base_url(environment) + "/items"

    # Get body request
    request_body = ""

    # Place request
    response = place_request("GET", request_url, request_body, request_headers)
    if response.status_code == 200:
        json_data = loads(response.text)
        return json_data['items']
    else:
        print('- [Product] Something went wrong in search products on microservice')


# Does the necessary requests to add a product in a microservice-based zone
def product_post_requests_microservice(product_data, abi_id, zone, environment, delivery_center_id):
    index, product = product_data

    result = request_post_price_inclusion_microservice(zone, environment, product['sku'], index, delivery_center_id)
    if result == 'false':
        return result

    # Post price product in Price Engine Microservice
    # Workaround to prevent requests from CL to go to the Pricing Engine MS
    if zone != 'CL':
        result = request_post_price_microservice(abi_id, zone, environment, product['sku'], index)
    if result == 'false':
        return result

    return 'true'


# Post requests product price and product inclusion in account
def request_post_products_account_microservice(abi_id, zone, environment, delivery_center_id, products_data):
    results = []
    print('\nAdding products. Please wait...')
    last = datetime.now()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(product_post_requests_microservice, product_data, abi_id, zone, environment,
                                   delivery_center_id) for product_data in products_data]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    now = datetime.now()
    lapsed = (now - last).seconds
    print('{}\n- Products added: {} / failed: {}. Completed in {} seconds.'.format(text.LightGreen,
                                                                                   results.count('true'),
                                                                                   results.count('false'), lapsed))
    return 'success'


# Post request product inclusion microservice
def request_post_price_inclusion_microservice(zone, environment, sku_product, product_price_id, delivery_center_id):

    # Get header request
    request_headers = get_header_request(zone, 'false', 'false', 'true', sku_product)

    # Get url base
    #request_url = get_microservice_base_url(environment) + "/middleware-relay/products/" + str(sku_product) + "/inclusions"
    request_url = get_microservice_base_url(environment) + "/product-assortment-relay/inclusion"

    # Get body request
    request_body = get_body_price_inclusion_microservice_request(delivery_center_id)

    # Place request
    response = place_request("POST", request_url, request_body, request_headers)

    if response.status_code != 202:
        print('- [Product] Something went wrong in post product SKU ' + str(sku_product) + ' on account product-assortment-relay')
        return 'false'

    return 'true'

# Create body for product inclusion in account
def get_body_price_inclusion_microservice_request(delivery_center_id):
    body_price_inclusion = dumps({
        "deliveryCenters": [delivery_center_id]
    })

    return body_price_inclusion

# Get offers account in microservice
def request_get_offers_microservice(accountId, zone, environment, deliveryCenterId):
    # Get header request
    headers = get_header_request(zone, 'true')

    # Get url base
    request_url = get_microservice_base_url(environment) + "/product-assortment/?accountId=accountId" + accountId + '&deliveryCenterId=' + deliveryCenterId

    # Get body request
    request_body = ""

    # Place request
    response = place_request("GET", request_url, request_body, headers)
    
    if response.status_code == 200 and response.text != "":
        json_data = loads(response.text)
        return json_data['skus']
    else:
        print('- [Products] Something went wrong when searching for products')
