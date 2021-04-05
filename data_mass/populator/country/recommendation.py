from data_mass.accounts import check_account_exists_microservice
from data_mass.populator.preconditions import logger
from data_mass.product.products import request_get_offers_microservice
from data_mass.algo_selling import request_quick_order, request_forgotten_items
from data_mass.populator.log import *

logger = logging.getLogger(__name__)


def populate_recommendations(country, environment, dataframe_recommendations):
    if dataframe_recommendations is not None:
        dataframe_recommendations.apply(apply_populate_recommendation, args=(country, environment), axis=1)


def apply_populate_recommendation(row, country, environment):
    populate_recommendation(country, environment, row['account_id'], row['products'])


def populate_recommendation(country, environment, account_id, products):
    """ Populate recommendation as quick order
    Arguments:
        - country: (e.g, BR,ZA,DO)
        - environment: (e.g, UAT,SIT)
        - account: account object
        - products: specific products registered as recommended ones
    Return new json_object
    """
    if False == check_account_exists_microservice(account_id, country, environment):
        logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
    else:
        # Retrieve all SKUs of the specified Account and DeliveryCenter IDs
        product_offers = request_get_offers_microservice(account_id, country, environment)
        if product_offers == 'not_found':
            logger.error(log(Message.PRODUCT_NOT_FOUND_ERROR, {'account_id': account_id}))
        elif not product_offers:
            logger.error(log(Message.RETRIEVE_PRODUCT_ERROR, {'account_id': account_id}))
        else:
            sku_list = list()
            for i in range(len(product_offers)):
                for j in range(len(products)):
                    if product_offers[i]['sku'] == products[j]:
                        sku_list.append(product_offers[i]['sku'])
            if len(sku_list) == 0:
                logger.info("Skipping populate_recommendation step for account {0} since the products are not associated"
                            .format(account_id))
            else:
                # Request for Quick Order
                if "success" != request_quick_order(country, environment, account_id, sku_list):
                    logger.error(log(Message.RECOMMENDER_QUICK_ORDER_ERROR, {"account_id": account_id}))

                # Request for Forgotten Items
                if "success" != request_forgotten_items(country, environment, account_id, sku_list):
                    logger.error(log(Message.RECOMMENDER_FORGOTTEN_ITEMS_ERROR, {"account_id": account_id}))
