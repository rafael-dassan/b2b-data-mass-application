import sys
from json import dumps, loads
from common import *


def enable_product(country, environment, product_sku):
    """Enable product
    Input Arguments:
        - Country (BR, DO, AR, CL, ZA, CO)
        - Environment (UAT, SIT)
        - Product SKU
        - Category ID
    Return str (success: product enabled has been succeeded)
    """
    response = request_enable_product(country, environment, product_sku)
    if response.status_code == 200:
        return 'success'
    else:
        return 'false'


def request_enable_product(country, environment, product_sku):
    # Get header request
    url = "{url_base}/rest/V1/products/{product_sku}".format(
        url_base=get_magento_base_url(environment, country), product_sku=product_sku)
    
    # Get base URL
    access_token = get_magento_datamass_access_token(environment, country)
	
	# Get header request
    headers = {
        "Content-Type": "application/json",
        "x-access-token": access_token
        }
    
    data = {
        "product": {
			"sku": product_sku,
			"status": 1
    	}
	}

    # Send request
    return place_request("PUT", url, convert_json_to_string(data), headers)