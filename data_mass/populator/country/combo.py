from data_mass.account.accounts import check_account_exists_microservice
from data_mass.combos import (
    input_combo_only_free_good,
    input_combo_type_discount,
    input_combo_type_free_good
)
from data_mass.populator.log import *

logger = logging.getLogger(__name__)


def populate_combo_discount_base(country, environment, dataframe_combos):
    if dataframe_combos is not None:
        dataframe_combos.apply(apply_populate_combo_discount, args=(country, environment), axis=1)


def apply_populate_combo_discount(row, country, environment):
    populate_combo_discount(country, environment, str(row['account_id']), row['combo_id'], row['sku'], row['discount_value'])


def populate_combo_discount(country, environment, account_id, combo_id, sku, discount_value):
    if country == "TZ":
        ...
    else:
        if False == check_account_exists_microservice(account_id, country, environment):
            logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
        else:
            if False == input_combo_type_discount(account_id, country, environment, sku, discount_value, combo_id):
                logger.error(log(Message.CREATE_COMBO_ERROR, {'account_id': account_id}))


def populate_combo_free_good_base(country, environment, dataframe_combos):
    if dataframe_combos is not None:
        dataframe_combos.apply(apply_populate_combo_free_good, args=(country, environment), axis=1)


def apply_populate_combo_free_good(row, country, environment):
    populate_combo_free_good(country, environment, str(row['account_id']), row['combo_id'], row['sku'])


def populate_combo_free_good(country, environment, account_id, combo_id, sku):
    if country == "TZ":
        ...
    else:
        if False == check_account_exists_microservice(account_id, country, environment):
            logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
        else:
            if False == input_combo_type_free_good(account_id, country, environment, sku, combo_id):
                logger.error(log(Message.CREATE_COMBO_ERROR, {'account_id': account_id}))


def populate_combo_only_free_good_base(country, environment, dataframe_combos):
    if dataframe_combos is not None:
        dataframe_combos.apply(apply_populate_combo_only_free_good, args=(country, environment), axis=1)


def apply_populate_combo_only_free_good(row, country, environment):
    populate_combo_only_free_good(country, environment, str(row['account_id']), row['combo_id'], row['sku'])


def populate_combo_only_free_good(country, environment, account_id, combo_id, sku):
    if country == "TZ":
        ...
    else:
        if False == check_account_exists_microservice(account_id, country, environment):
            logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
        else:
            if False == input_combo_only_free_good(account_id, country, environment, sku, combo_id):
                logger.error(log(Message.CREATE_COMBO_ERROR, {'account_id': account_id}))
