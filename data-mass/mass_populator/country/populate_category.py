from category_magento import *
from products_magento import *
from mass_populator.log import *
import json


logger = logging.getLogger(__name__)


def associate_products_to_category_magento(country, environment, products):
    """Associate product to category
    Input Arguments:
        - Country (BR, DO, AR, CL, ZA, CO)
        - Environment (UAT, SIT)
        - List Products SKU
		- Category Name
        - Depth to populate categories
    """
    # get categories
    categories_web = get_categories_magento_web(country, environment)
    categories_mobile = get_categories_magento_mobile(country, environment)

    # associate by context
    associate(country, environment, categories_web, distinct_list(products, ['WEB']))
    associate(country, environment, categories_mobile, distinct_list(products, ['IOS', 'ANDROID']))


def associate(country, environment, categories, products):
    for category in categories:
        for sku in products:
            response_associate = associate_product_to_category(country, environment, sku, category)
            if response_associate == 'false':
                logger.error(log(Message.CATEGORY_PRODUCT_ASSOCIATE_ERROR,{"category": category, "sku": sku}))


def get_categories_magento_web(country, environment):
    """Get categories
    Input Arguments:
        - Country (BR, DO, AR, CL, ZA, CO)
        - Environment (UAT, SIT)
		- Depth to find categories
        - Category Name
    """
    category_name = 'Journey'
    nodes = request_get_categories(country, environment, {'level': 2})
    nodes_obj = json.loads(nodes.text)
    categories = []
    nodes_items = nodes_obj['items']
    
    if nodes_obj and nodes_items:
        for node in nodes_items:        
            parent_id = node['id']
            parent_name = node['name']

            if 'mobile' not in parent_name.lower():
                node_children = request_get_categories(country, environment,
                                                       {'parent_id': parent_id, 'name': category_name})
                node_children_obj = json.loads(node_children.text)
                nodes_items_children = node_children_obj['items']

                if node_children_obj and not nodes_items_children:
                    category_id = _create_category(country, environment, category_name, parent_id)
                else:
                    category_id = nodes_items_children[0]['id']
                categories.append(category_id)

    return categories


def get_categories_magento_mobile(country, environment):
    """Get categories
    Input Arguments:
        - Country (BR, DO, AR, CL, ZA, CO)
        - Environment (UAT, SIT)
		- Depth to find categories
        - Category Name
    """
    parent_category_name = 'Journey Category'
    sub_category_name = 'Journey'
    custom_attributes = {
        "brand_id": "",
        "web_brand_is_active": "0",
        "display_mode": "PRODUCTS",
        "disable_cross_category": "0",
        "custom_use_parent_settings": "0",
        "custom_apply_to_products": "0"
    }

    nodes = request_get_categories(country, environment, {'level': 2})
    nodes_obj = json.loads(nodes.text)
    categories = []
    nodes_items = nodes_obj['items']

    if nodes_obj and nodes_items:
        for node in nodes_items:
            parent_id = node['id']
            parent_name = node['name']

            if 'mobile' in parent_name.lower():
                node_parent_category = request_get_categories(country, environment,
                                                              {'parent_id': parent_id, 'name': parent_category_name})
                node_parent_category_obj = json.loads(node_parent_category.text)
                nodes_items_parent_category = node_parent_category_obj['items']

                if node_parent_category_obj and not nodes_items_parent_category:
                    custom_attributes["brand_id"] = "Journey" + str(parent_id)
                    parent_category_id = _create_category(country, environment, parent_category_name, parent_id,
                                                          custom_attributes)
                else:
                    parent_category_id = nodes_items_parent_category[0]['id']

                node_sub_category = request_get_categories(country, environment,
                                                           {'parent_id': parent_category_id, 'name': sub_category_name})
                node_sub_category_obj = json.loads(node_sub_category.text)
                nodes_items_sub_category = node_sub_category_obj['items']

                if node_sub_category_obj and not nodes_items_sub_category:
                    custom_attributes["brand_id"] = "Journey" + str(parent_category_id)
                    sub_category_id = _create_category(country, environment, sub_category_name, parent_category_id,
                                                       custom_attributes)
                else:
                    sub_category_id = nodes_items_sub_category[0]['id']

                categories.append(sub_category_id)

    return categories


def _create_category(country, environment, category_name, parent_id, custom_attributes={}):
    category_id = None
    category = create_category(country, environment, category_name, parent_id, custom_attributes)

    if category == 'false':
        logger.error(log(Message.CATEGORY_CREATE_ERROR,{"category": category_name}))
    else:
        category_id = category['id']

    return category_id


def distinct_list(arr, matchers):
    return [obj for obj in arr if any(xs in obj for xs in matchers)]
