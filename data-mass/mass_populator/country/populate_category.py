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
    categories = get_categories_magento(country, environment)
    categories_mobile = [category['id'] for category in categories if 'mobile' in category['parent_name'].lower()]
    categories_web = [category['id'] for category in categories if 'mobile' not in category['parent_name'].lower()]

    # associate by context
    associate(country, environment, categories_web, distinct_list(products, ['WEB']))
    associate(country, environment, categories_mobile, distinct_list(products, ['IOS','ANDROID']))


def associate(country, environment, categories, products):
    for category in categories:
        for sku in products:
            response_associate = associate_product_to_category(country, environment, sku, category)
            if response_associate == 'false':
                logger.error(log(Message.CATEGORY_PRODUCT_ASSOCIATE_ERROR,{"category": category, "sku": sku}))


def get_categories_magento(country, environment, depth = 2, category_name = 'Journey'):
    """Get categories
    Input Arguments:
        - Country (BR, DO, AR, CL, ZA, CO)
        - Environment (UAT, SIT)
		- Depth to find categories
        - Category Name
    """
    nodes = request_get_categories(country, environment, {'level': depth})
    nodes_obj = json.loads(nodes.text)
    categories = []
    nodes_items = nodes_obj['items']
    
    if nodes_obj and nodes_items:
        for node in nodes_items:        
            parent_id = node['id']
            parent_name = node['name']
            node_children = request_get_categories(country, environment, {'parent_id': parent_id, 'name': category_name})
            node_children_obj = json.loads(node_children.text)
            nodes_items_children = node_children_obj['items']

            if node_children_obj and not nodes_items_children:
                category_id = _create_category(country, environment, category_name, parent_id)   
            else:
                category_id = nodes_items_children[0]['id']
            categories.append({ 'id': category_id, 'parent_name': parent_name })
            
        return categories


def _create_category(country, environment, category_name, parent_id):
    category_id = None
    category = create_category(country, environment, category_name, parent_id)

    if category == 'false':
        logger.error(log(Message.CATEGORY_CREATE_ERROR,{"category": category_name}))
    else:
        category_id = category['id']

    return category_id


def distinct_list(arr, matchers):
    return [obj for obj in arr if any(xs in obj for xs in matchers)]
