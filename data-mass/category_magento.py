import sys
from json import dumps, loads
from common import *


def get_categories(country, environment, parent_id):
	"""Get Categories
    Input Arguments:
        - Country (BR, DO, AR, CL, ZA, CO)
        - Environment (UAT, SIT)
        - Parent ID
    Return list of categories
    """
	response = request_get_categories(country, environment, parent_id)
	if response.status_code == 200:
		arr = loads(response.text)
		return arr['items']


def associate_product_to_category(country, environment, product_sku, category_id):
	"""Associate product to category
    Input Arguments:
        - Country (BR, DO, AR, CL, ZA, CO)
        - Environment (UAT, SIT)
        - Product SKU
		- Category ID
	Return str (success: association has been succeeded)
    """
	response = request_associate_product_to_category(country, environment, product_sku, category_id)
	if response.status_code == 200 and response.text == 'true':
		return 'success'
	else:
		return 'false'


def create_category(country, environment, category_name, parent_id):
	"""Create Category
    Input Arguments:
        - Country (BR, DO, AR, CL, ZA, CO)
        - Environment (UAT, SIT)
        - Category name
		- Parent ID
    Return category object
    """
	response = request_create_category(country, environment, category_name, parent_id)
	if response.status_code == 200:
		return loads(response.text)
	else:
		return 'false'


def request_associate_product_to_category(country, environment, product_sku, category_id):
    # Get header request
	url = "{url_base}/rest/V1/categories/{product_sku}/products".format(
		url_base=get_magento_base_url(environment, country), product_sku=product_sku)
    
	# Get base URL
	access_token = get_magento_datamass_access_token(environment, country)
	
	# Get header request
	headers = {
        "Content-Type": "application/json",
        "x-access-token": access_token
    }

	data = {
        "productLink": {
			"sku": product_sku,
			"position": 0,
			"category_id": category_id,
			"extension_attributes": {}
    	}
	}

	# Send request
	return place_request("POST", url, convert_json_to_string(data), headers)


def request_get_categories(country, environment, parent_id = 0):
	# Get header request
	url = get_magento_base_url(environment, country) + "/rest/V1/categories/list?searchCriteria[filterGroups][0][filters][0][field]=parent_id&searchCriteria[filterGroups][0][filters][0][value]=" + str(parent_id) 
    
	# Get base URL
	access_token = get_magento_datamass_access_token(environment, country)
	
	# Get header request
	headers = {
        "Content-Type": "application/json",
        "x-access-token": access_token
    }

	# Send request
	return place_request("GET", url, '', headers)


def request_create_category(country, environment, category_name, parent_id = 0):
	# Get header request
	url = "{url_base}/rest/V1/categories".format(url_base=get_magento_base_url(environment, country))
    
	# Get base URL
	access_token = get_magento_datamass_access_token(environment, country)

	# Get header request
	headers = {
        "Content-Type": "application/json",
        "x-access-token": access_token
    }

	data = {
        "category": {
			"parent_id": parent_id,
			"name": category_name,
			"is_active": True,
			"position": 0,
			"level": 0,
			"children": "",
			"available_sort_by": [],
			"include_in_menu": True,
			"extension_attributes": {},
			"custom_attributes": []
    	}
	}

	# Send request
	return place_request("POST", url, convert_json_to_string(data), headers)