import pandas as pd
from products import create_item, request_get_offers_microservice
from products_magento import enable_product
from mass_populator.log import *

logger = logging.getLogger(__name__)


def populate_products(country, environment, dataframe_products):
    if dataframe_products is not None:
        dataframe_products.apply(apply_populate_product, 
        args=(country, environment), axis=1)


def apply_populate_product(row, country, environment):
    populate_product(country, environment,
        row['sku'],
        row['name'],
        row['brand_name'],
        row['sub_brand_name'],
        row['package_id'],
        row['container_name'],
        row['container_size'],
        row['container_returnable'],
        row['container_unitOfMeasurement'],
        row['sales_ranking'])


def populate_product(country, environment,
        sku,
        name,
        brand_name,
        sub_brand_name,
        package_id,
        container_name,
        container_size,
        container_returnable,
        container_unitOfMeasurement,
        sales_ranking):
    """ Populate products
    Arguments:
        - country: (e.g, BR,ZA,DO)
        - environment: (e.g, UAT,SIT)
        -  sku': sku 
        -  name': name
        -  brand_name': brand_name 
        -  sub_brand_name': sub_brand_name
        -  package_id': package_id
        -  container_name': container_name
        -  container_size': container_size
        -  container_returnable': container_returnable
        -  container_unitOfMeasurement': container_unitOfMeasurement
        -  sales_ranking': sales_ranking
    """
    item_data = {
        'sku': sku, 
        'name': name,
        'brandName': brand_name, 
        'subBrandName': sub_brand_name,
        'package.id': package_id,
        'container.name': container_name,
        'container.size': container_size,
        'container.returnable': container_returnable,
        'container.unitOfMeasurement': container_unitOfMeasurement,
        'salesRanking': sales_ranking
    }
    response = create_item(country, environment, item_data)
    if response is None:
        logger.error(log(Message.PRODUCT_CREATE_ERROR,{"sku": sku}))


def enable_products_magento(country, environment, dataframe_products):
    if dataframe_products is not None:
        dataframe_products.apply(apply_enable_products_magento, 
        args=(country, environment), axis=1)


def apply_enable_products_magento(row, country, environment):
    for product in row['products']:
        enable_product_magento(country, environment, product)


def enable_product_magento(country, environment, product_sku):
    """Enable product magento
    Arguments:
        - country: (e.g, BR,ZA,DO)
        - environment: (e.g, UAT,SIT)
        - product: product to enable
    """
    response = enable_product(country, environment, product_sku)
    if response == 'false':
        logger.error(log(Message.PRODUCT_ENABLE_ERROR,{"sku": product_sku}))


def check_product_associated_to_account(account_id, country, environment, products):
    """
    Check if SKU is associated with a specific POC
    Args:
        account_id: POC unique identifier
        country: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., SIT, UAT
        products: product array
    Returns: array of SKUs not associated to a specific POC
    """
    product_offers = request_get_offers_microservice(account_id, country, environment)
    if product_offers == 'not_found':
        logger.info("[Catalog Service] Products not found for account "
                    "{account_id}. Skipping...".format(account_id=account_id))
    elif product_offers == 'false':
        logger.error(log(Message.RETRIEVE_PRODUCT_ERROR, {'account_id': account_id}))
    else:
        available_skus = list()
        not_associated_skus = list()
        for i in range(len(product_offers)):
            available_skus.append(product_offers[i]['sku'])

        for i in range(len(products)):
            if products[i] in available_skus:
                logger.info("[Catalog Service] Product {product} is already associated to the account {account_id}."
                            " Skipping...".format(product=products[i], account_id=account_id))
            else:
                not_associated_skus.append(products[i])
                logger.info("[Catalog Service] Product {product} is not associated to the account {account_id} and"
                            " needs to be added.".format(product=products[i], account_id=account_id))
                return not_associated_skus
