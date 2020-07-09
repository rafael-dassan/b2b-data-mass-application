from mass_populator.log import *
from mass_populator.country.populate_recomendation import populate_recommendation
from mass_populator.country.delete_recommendation import delete_sell_up_recommendation

logger = logging.getLogger(__name__)


def populate_recomendations(environment):
    country = "AR"
    account_id_poc_1 = "5444385012"
    account_id_poc_2 = "9932094352"

    delete_sell_up_recommendation(account_id_poc_1, country, environment)
    delete_sell_up_recommendation(account_id_poc_2, country, environment)

    populate_recommendation(country, environment, account_id_poc_1)
    populate_recommendation(country, environment, account_id_poc_2)
    
    logger.info("Beer Recommender populating finalized.")