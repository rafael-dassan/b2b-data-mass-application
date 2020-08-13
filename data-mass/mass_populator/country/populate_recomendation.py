import pandas as pd
from products import request_get_offers_microservice
from beer_recommender import request_quick_order, request_forgotten_items
from mass_populator.log import *
from mass_populator.country.delete_recommendation import delete_recommendation

logger = logging.getLogger(__name__)


def populate_recommendations(country, environment, dataframe_recommendations):
    if dataframe_recommendations is not None:
        dataframe_recommendations.apply(apply_populate_recommendation,
            args=(country, environment), axis=1)


def apply_populate_recommendation(row, country, environment):
    delete_recommendation(row['account_id'], country, environment, 'CROSS_SELL_UP_SELL')
    populate_recommendation(country, environment, row['account_id'])


def populate_recommendation(country, environment, account_id):
    """ Populate recommendation as quick order
    Arguments:
        - country: (e.g, BR,ZA,DO)
        - environment: (e.g, UAT,SIT)
        - account: account object
    Return new json_object
    """
    # Retrieve all SKUs of the specified Account and DeliveryCenter IDs
    product_offers = request_get_offers_microservice(
        account_id, country, environment)
    if not isinstance(product_offers, list) or not len(product_offers):
        logger.warning("Not found SKUs on account: {account_id}".format(
            account_id=account_id))
        return 'failed'

    enabled_skus = list()
    aux_index = 0
    while aux_index < len(product_offers):
        sku = product_offers[aux_index]['sku']
        enabled_skus.append(sku)
        aux_index = aux_index + 1

    logger.debug("Available_products to populate in recommendations: {available_products} items".format(
        available_products=len(enabled_skus)))

    min_amount = 20
    if len(enabled_skus) >= min_amount:
        # Request for Quick Order
        if "success" != request_quick_order(country, environment, account_id, enabled_skus):
            logger.error(log(Message.RECOMMENDER_QUICK_ORDER_ERROR, {
                         "account_id": account_id}))

        # Request for Forgotten Items
        if "success" != request_forgotten_items(country, environment, account_id, enabled_skus):
            logger.error(log(Message.RECOMMENDER_FORGOTTEN_ITEMS_ERROR, {
                         "account_id": account_id}))
    else:
        logger.warning("Not enough products to populate recommendations. Min amount is {}".format(str(min_amount)))