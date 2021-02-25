from accounts import check_account_exists_microservice
from deals import create_stepped_discount_with_limit, create_discount, create_stepped_discount, create_free_good, \
    create_stepped_free_good
from mass_populator.log import *
from mass_populator.log import log, Message
from mass_populator.preconditions import logger
from products import request_get_offers_microservice

logger = logging.getLogger(__name__)


def populate_stepped_discount_with_limit_base(country, environment, dataframe_deals):
    if dataframe_deals is not None:
        dataframe_deals.apply(apply_populate_stepped_discount_with_limit, args=(country, environment), axis=1)


def apply_populate_stepped_discount_with_limit(row, country, environment):
    populate_stepped_discount_with_limit(country, environment, str(row['account_id']), row['deal_id'], row['sku'],
                                         row['discount_value'], row['max_quantity'])


def populate_stepped_discount_with_limit(country, environment, account_id, deal_id, sku, discount_value, max_quantity):
    # Default index range (from 1 to 9999 products)
    default_index_range = [1, 9999]

    if 'false' == check_account_exists_microservice(account_id, country, environment):
        logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
    else:
        if 'false' == create_stepped_discount_with_limit(account_id, sku, country, environment, default_index_range,
                                                     [discount_value], max_quantity, deal_id):
            logger.error(log(Message.CREATE_DEALS_ERROR, {'deal_id': deal_id, 'account_id': account_id}))


def populate_discount_base(country, environment, dataframe_deals):
    if dataframe_deals is not None:
        dataframe_deals.apply(apply_populate_discount, args=(country, environment), axis=1)


def apply_populate_discount(row, country, environment):
    populate_discount(country, environment, str(row['account_id']), row['deal_id'], row['sku'], row['discount_value'], row['min_quantity'])


def populate_discount(country, environment, account_id, deal_id, sku, discount_value, minimum_quantity):
    if 'false' == check_account_exists_microservice(account_id, country, environment):
        logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
    else:
        if 'false' == create_discount(account_id, sku, country, environment, discount_value, minimum_quantity, deal_id):
            logger.error(log(Message.CREATE_DEALS_ERROR, {'deal_id': deal_id, 'account_id': account_id}))


def populate_stepped_discount_base(country, environment, dataframe_deals):
    if dataframe_deals is not None:
        dataframe_deals.apply(apply_populate_stepped_discount, args=(country, environment), axis=1)


def apply_populate_stepped_discount(row, country, environment):
    populate_stepped_discount(country, environment, str(row['account_id']), row['deal_id'], row['sku'], row['ranges'])


def populate_stepped_discount(country, environment, account_id, deal_id, sku, ranges):
    if 'false' == check_account_exists_microservice(account_id, country, environment):
        logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
    else:
        range_list = list()
        for i in range(len(ranges)):
            range_values = ranges[i].split(',')
            dict_values = {
                'start': range_values[0],
                'end': range_values[1],
                'discount': range_values[2]
            }

            range_list.append(dict_values)

        if 'false' == create_stepped_discount(account_id, sku, country, environment, range_list, deal_id):
            logger.error(log(Message.CREATE_DEALS_ERROR, {'deal_id': deal_id, 'account_id': account_id}))


def populate_free_good_base(country, environment, dataframe_deals):
    if dataframe_deals is not None:
        dataframe_deals.apply(apply_populate_free_good, args=(country, environment), axis=1)


def apply_populate_free_good(row, country, environment):
    populate_free_good(country, environment, str(row['account_id']), row['deal_id'], row['sku'], row['proportion'],
                       row['quantity'], row['partial_free_good'], row['need_to_buy_product'])


def populate_free_good(country, environment, account_id, deal_id, sku, proportion, quantity, partial_free_good,
                       need_to_buy_product):
    if 'false' == check_account_exists_microservice(account_id, country, environment):
        logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
    else:
        product_offers = request_get_offers_microservice(account_id, country, environment)
        if product_offers == 'not_found':
            logger.error(log(Message.PRODUCT_NOT_FOUND_ERROR, {'account_id': account_id}))
        elif product_offers == 'false':
            logger.error(log(Message.RETRIEVE_PRODUCT_ERROR, {'account_id': account_id}))
        else:
            sku_list = list()
            for i in range(len(product_offers)):
                if product_offers[i]['sku'] == sku:
                    sku_list.append(product_offers[i])
            if len(sku_list) == 0:
                logger.info("Skipping populate_free_good step for account {0} since the SKU {1} is not associated"
                            .format(account_id, sku))
            else:
                if 'false' == create_free_good(account_id, sku_list, country, environment, proportion, quantity,
                                               partial_free_good, need_to_buy_product, deal_id):
                    logger.error(log(Message.CREATE_DEALS_ERROR, {'deal_id': deal_id, 'account_id': account_id}))


def populate_stepped_free_good_base(country, environment, dataframe_deals):
    if dataframe_deals is not None:
        dataframe_deals.apply(apply_populate_stepped_free_good, args=(country, environment), axis=1)


def apply_populate_stepped_free_good(row, country, environment):
    populate_stepped_free_good(country, environment, str(row['account_id']), row['deal_id'], row['sku'],
                               row['ranges'])


def populate_stepped_free_good(country, environment, account_id, deal_id, sku, ranges):
    if 'false' == check_account_exists_microservice(account_id, country, environment):
        logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
    else:
        range_list = list()
        for i in range(len(ranges)):
            range_values = ranges[i].split(',')
            dict_values = {
                'start': range_values[0],
                'end': range_values[1],
                'quantity': range_values[2],
                'proportion': range_values[3]
            }

            range_list.append(dict_values)

        if 'false' == create_stepped_free_good(account_id, sku, country, environment, range_list, deal_id):
            logger.error(log(Message.CREATE_DEALS_ERROR, {'deal_id': deal_id, 'account_id': account_id}))
