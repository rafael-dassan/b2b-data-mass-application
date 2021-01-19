from account import check_account_exists_microservice
from deals import create_stepped_discount_with_limit, create_discount, create_stepped_discount
from mass_populator.log import *

logger = logging.getLogger(__name__)


def populate_stepped_discount_with_limit_base(country, environment, dataframe_deals):
    if dataframe_deals is not None:
        dataframe_deals.apply(apply_populate_stepped_discount_with_limit, args=(country, environment), axis=1)


def apply_populate_stepped_discount_with_limit(row, country, environment):
    populate_stepped_discount_with_limit(country, environment, str(row['account_id']), row['deal_id'], row['sku'],
                                         row['discount_value'], row['max_quantity'], row['operation'])


def populate_stepped_discount_with_limit(country, environment, account_id, deal_id, sku, discount_value, max_quantity,
                                         operation):
    # Default index range (from 1 to 9999 products)
    default_index_range = [1, 9999]

    if 'false' == check_account_exists_microservice(account_id, country, environment):
        logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
    else:
        if 'false' == create_stepped_discount_with_limit(account_id, sku, country, environment, default_index_range,
                                                     [discount_value], max_quantity, operation, deal_id):
            logger.error(log(Message.CREATE_DEALS_ERROR, {'deal_id': deal_id, 'account_id': account_id}))


def populate_discount_base(country, environment, dataframe_deals):
    if dataframe_deals is not None:
        dataframe_deals.apply(apply_populate_discount, args=(country, environment), axis=1)


def apply_populate_discount(row, country, environment):
    populate_discount(country, environment, str(row['account_id']), row['deal_id'], row['sku'], row['discount_value'],
                      row['min_quantity'], row['operation'])


def populate_discount(country, environment, account_id, deal_id, sku, discount_value, minimum_quantity, operation):
    if 'false' == check_account_exists_microservice(account_id, country, environment):
        logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
    else:
        if 'false' == create_discount(account_id, sku, country, environment, discount_value, minimum_quantity,
                                      operation, deal_id):
            logger.error(log(Message.CREATE_DEALS_ERROR, {'deal_id': deal_id, 'account_id': account_id}))


def populate_stepped_discount_base(country, environment, dataframe_deals):
    if dataframe_deals is not None:
        dataframe_deals.apply(apply_populate_stepped_discount, args=(country, environment), axis=1)


def apply_populate_stepped_discount(row, country, environment):
    populate_stepped_discount(country, environment, str(row['account_id']), row['deal_id'], row['sku'],
                              row['index_range'], row['discount_range'], row['operation'])


def populate_stepped_discount(country, environment, account_id, deal_id, sku, index_range, discount_range, operation):
    if 'false' == check_account_exists_microservice(account_id, country, environment):
        logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
    else:
        if 'false' == create_stepped_discount(account_id, sku, country, environment, index_range, discount_range,
                                              operation, deal_id):
            logger.error(log(Message.CREATE_DEALS_ERROR, {'deal_id': deal_id, 'account_id': account_id}))
