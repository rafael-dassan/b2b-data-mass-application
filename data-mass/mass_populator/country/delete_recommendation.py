from beer_recommender import get_recommendation_by_account, delete_recommendation_by_id
from mass_populator.log import *


logger = logging.getLogger(__name__)


# Delete recommendation from account
def delete_recommendation(abi_id, zone, environment, use_case):
    up_sell_data = get_recommendation_by_account(abi_id, zone, environment, use_case)

    if up_sell_data == 'not_found':
        logger.info('Recommendation type {use_case_type} not found for account {account_id}. Skipping...'
                    .format(use_case_type=use_case, account_id=abi_id))
    elif up_sell_data == 'false':
        logger.error(log(Message.RETRIEVE_RECOMMENDER_ERROR, {'use_case_type': use_case, 'account_id': abi_id}))
    else:
        if 'success' != delete_recommendation_by_id(environment, up_sell_data):
            logger.error(log(Message.DELETE_RECOMMENDER_ERROR, {'use_case_type': use_case, 'account_id': abi_id}))
