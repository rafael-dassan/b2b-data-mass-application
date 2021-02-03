from products import request_get_offers_microservice
from algo_selling import request_quick_order, request_forgotten_items
from mass_populator.log import *

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
    # Retrieve all SKUs of the specified Account and DeliveryCenter IDs
    product_offers = request_get_offers_microservice(
        account_id, country, environment)
    if not isinstance(product_offers, list) or not len(product_offers):
        logger.warning("Not found SKUs on account: {account_id}".format(account_id=account_id))
        return 'failed'

    # Request for Quick Order
    if "success" != request_quick_order(country, environment, account_id, products):
        logger.error(log(Message.RECOMMENDER_QUICK_ORDER_ERROR, {"account_id": account_id}))

    # Request for Forgotten Items
    if "success" != request_forgotten_items(country, environment, account_id, products):
        logger.error(log(Message.RECOMMENDER_FORGOTTEN_ITEMS_ERROR, {"account_id": account_id}))
