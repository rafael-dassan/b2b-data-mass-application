import json

from data_mass.category.magento import *
from data_mass.populator.log import *

logger = logging.getLogger(__name__)


def associate_products_to_category_magento_base(country, environment, dataframe_products):
    if dataframe_products is not None:
        dataframe_products.apply(apply_associate_products_to_category_magento_base, args=(country, environment), axis=1)


def apply_associate_products_to_category_magento_base(row, country, environment):
    associate_products_to_category_magento(country, environment, row['name'], row['products'])


def associate_products_to_category_magento(country, environment, category, products):
    """Associate product to category
    Input Arguments:
        - Country (BR, DO, AR, ZA, CO)
        - Environment (UAT, SIT)
        - Category Name
        - List Products SKU
    """
    # get categories
    categories_web = get_categories_magento_web(country, environment, category)
    categories_mobile = get_categories_magento_mobile(country, environment, category)

    # associate by context
    associate(country, environment, categories_web, distinct_list(products, ['WEB']))
    associate(country, environment, categories_mobile, distinct_list(products, ['IOS', 'ANDROID']))


def associate(country, environment, categories, products):
    for category in categories:
        for sku in products:
            response_associate = associate_product_to_category(country, environment, sku, category)
            if not response_associate:
                logger.error(log(Message.CATEGORY_PRODUCT_ASSOCIATE_ERROR, {"category": category, "sku": sku}))


def get_categories_magento_web(country, environment, category_name):
    """Get categories
    Input Arguments:
        - Country (BR, DO, AR, ZA, CO)
        - Environment (UAT, SIT)
        - Category Name
    """
    categories = []
    nodes = request_get_categories(country, environment, {'level': 2})
    if nodes.status_code != 200:
        logger.error(log(Message.RETRIEVE_CATEGORY_ERROR, {"category": category_name}))
    else:
        nodes_obj = json.loads(nodes.text)
        nodes_items = nodes_obj['items']

        if nodes_obj and nodes_items:
            for node in nodes_items:
                parent_id = node['id']
                parent_name = node['name']

                if 'mobile' not in parent_name.lower() and 'promotions' not in parent_name.lower() and 'promotion' \
                        not in parent_name.lower() and 'promociones' not in parent_name.lower():
                    node_children = request_get_categories(country, environment, {'parent_id': parent_id, 'name': category_name})
                    if node_children.status_code != 200:
                        logger.error(log(Message.RETRIEVE_CATEGORY_ERROR, {"category": category_name}))
                    else:
                        node_children_obj = json.loads(node_children.text)
                        nodes_items_children = node_children_obj['items']

                        if node_children_obj and not nodes_items_children:
                            category_id = _create_category(country, environment, category_name, parent_id)
                        else:
                            category_id = nodes_items_children[0]['id']

                        if category_id is not None:
                            categories.append(category_id)
                        else:
                            logger.error(log(Message.SUBCATEGORY_CREATION_ERROR, {"subcategory_name": str(category_name),
                                                                                  "parent_id": str(parent_id)}))

    return categories


def get_categories_magento_mobile(country, environment, sub_category_name):
    """Get categories
    Input Arguments:
        - Country (BR, DO, AR, ZA, CO)
        - Environment (UAT, SIT)
        - Sub Category Name
    """
    parent_category_name = 'Journey Category'
    custom_attributes = {
        "brand_id": "",
        "web_brand_is_active": "0",
        "display_mode": "PRODUCTS",
        "automatic_sorting": "0",
        "custom_use_parent_settings": "0",
        "custom_apply_to_products": "0"
    }

    categories = []
    nodes = request_get_categories(country, environment, {'level': 2})
    if nodes.status_code != 200:
        logger.error(log(Message.RETRIEVE_CATEGORY_ERROR, {"category": sub_category_name}))
    else:
        nodes_obj = json.loads(nodes.text)
        nodes_items = nodes_obj['items']

        if nodes_obj and nodes_items:
            for node in nodes_items:
                parent_id = node['id']
                parent_name = node['name']

                if 'mobile' in parent_name.lower() and 'promotions' not in parent_name.lower() and 'promotion' \
                        not in parent_name.lower() and 'banners' not in parent_name.lower() and 'promociones' not in parent_name.lower():
                    node_parent_category = request_get_categories(country, environment, {'parent_id': parent_id,
                                                                                         'name': parent_category_name})
                    if node_parent_category.status_code != 200:
                        logger.error(log(Message.RETRIEVE_CATEGORY_ERROR, {"category": parent_category_name}))
                    else:
                        node_parent_category_obj = json.loads(node_parent_category.text)
                        nodes_items_parent_category = node_parent_category_obj['items']

                        if node_parent_category_obj and not nodes_items_parent_category:
                            custom_attributes["brand_id"] = sub_category_name + str(parent_id)
                            parent_category_id = _create_category(country, environment, parent_category_name, parent_id, custom_attributes)
                        else:
                            parent_category_id = nodes_items_parent_category[0]['id']

                        if parent_category_id is None:
                            logger.error(log(Message.SUBCATEGORY_CREATION_ERROR, {"subcategory_name": str(parent_category_name),
                                                                                  "parent_id": str(parent_id)}))

                        node_sub_category = request_get_categories(country, environment, {'parent_id': parent_category_id,
                                                                                          'name': sub_category_name})
                        node_sub_category_obj = json.loads(node_sub_category.text)
                        nodes_items_sub_category = node_sub_category_obj['items']

                        if node_sub_category_obj and not nodes_items_sub_category:
                            custom_attributes["brand_id"] = sub_category_name + str(parent_category_id)
                            sub_category_id = _create_category(country, environment, sub_category_name, parent_category_id,
                                                               custom_attributes)
                        else:
                            sub_category_id = nodes_items_sub_category[0]['id']

                        if sub_category_id is not None:
                            categories.append(sub_category_id)
                        else:
                            logger.error(log(Message.SUBCATEGORY_CREATION_ERROR, {"subcategory_name": str(sub_category_name),
                                                                                  "parent_id": str(parent_category_id)}))

    return categories


def _create_category(country, environment, category_name, parent_id, custom_attributes={}):
    category_id = None
    category = create_category(country, environment, category_name, parent_id, custom_attributes)

    if not category:
        logger.error(log(Message.CATEGORY_CREATE_ERROR, {"category": category_name}))
    else:
        category_id = category['id']

    return category_id


def distinct_list(arr, matchers):
    return [obj for obj in arr if any(xs in obj for xs in matchers)]
