from products import request_get_offers_microservice
from products import check_item_enabled
from beer_recommender import request_quick_order, request_forgotten_items, request_sell_up
from mass_populator.log import *

logger = logging.getLogger(__name__)


def populate_recommendation(country, environment, account_id):
    """ Populate recommendation as quick order
    Arguments:
        - country: (e.g, BR,ZA,DO)
        - environment: (e.g, UAT,SIT)
        - account: account object
    Return new json_object
    """
    # Retrieve all SKUs of the specified Account and DeliveryCenter IDs
    product_offers = request_get_offers_microservice(account_id, country, environment, account_id, True)
    if not isinstance(product_offers, list) or not len(product_offers):
        logger.debug("Not found SKUs on account: {account_id}".format(account_id=account_id))
        return 'failed'

    enabled_skus = list()
    index = 0
    while index < len(product_offers):
        if country == "ZA":
            sku = product_offers[index]
        else:
            sku = product_offers[index]['sku']

        # Check if the SKU is enabled on Items MS
        if check_item_enabled(sku, country, environment) != False:
            enabled_skus.append(sku)
        index = index + 1

    logger.debug("Available_products to populate in recommendations: {available_products} items".format(
        available_products=len(enabled_skus)))
    
    if len(enabled_skus) >= 25:
        # Request for Quick Order
        if "success" != request_quick_order(country, environment, account_id, enabled_skus):
            logger.debug(log(Message.RECOMMENDER_QUICK_ORDER_ERROR, {"account_id": account_id}))

        # Request for Forgotten Items
        if "success" != request_forgotten_items(country, environment, account_id, enabled_skus):
            logger.debug(log(Message.RECOMMENDER_FORGOTTEN_ITEMS_ERROR, {"account_id": account_id}))

        # Request for Sell Up
        if "success" != request_sell_up(country, environment, account_id, enabled_skus):
            logger.debug(log(Message.RECOMMENDER_SELL_UP_ERROR, {"account_id": account_id}))