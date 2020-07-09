from beer_recommender import get_recommendation_by_account, delete_recommendation_by_id
from mass_populator.log import *


logger = logging.getLogger(__name__)


def delete_sell_up_recommendation(abi_id, zone, environment, use_case='CROSS_SELL_UP_SELL'):
    up_sell_data = get_recommendation_by_account(abi_id, zone, environment, use_case)

    if up_sell_data == 'not_found':
        logger.info('Skipping the removal of sell up recommendation because there is none for the account %s', abi_id)
    elif up_sell_data == 'false':
        logger.error(log(Message.RETRIEVE_RECOMMENDER_SELL_UP_ERROR, {'account_id': abi_id}))
    else:
        if 'success' != delete_recommendation_by_id(environment, up_sell_data):
            logger.error(log(Message.DELETE_RECOMMENDER_SELL_UP_ERROR, {'account_id': abi_id}))
