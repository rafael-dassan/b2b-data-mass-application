from accounts import check_account_exists_microservice
from combos import input_combo_type_discount
from mass_populator.log import *

logger = logging.getLogger(__name__)


def populate_combo_discount_base(country, environment, dataframe_combos):
    if dataframe_combos is not None:
        dataframe_combos.apply(apply_populate_combo_discount, args=(country, environment), axis=1)


def apply_populate_combo_discount(row, country, environment):
    populate_combo_discount(country, environment, str(row['account_id']), row['combo_id'], row['sku'], row['discount_value'])


def populate_combo_discount(country, environment, account_id, combo_id, sku, discount_value):
    if 'false' == check_account_exists_microservice(account_id, country, environment):
        logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
    else:
        if 'false' == input_combo_type_discount(account_id, country, environment, sku, discount_value, combo_id):
            logger.error(log(Message.CREATE_COMBO_ERROR, {'account_id': account_id}))
