from mass_populator.log import *
from mass_populator.country.populate_recomendation import populate_recommendation
from mass_populator.country.delete_recommendation import delete_recommendation

logger = logging.getLogger(__name__)


def populate_recomendations(environment):
    country = "ZA"
    account_id_poc_1 = "9883300101"
    account_id_poc_2 = "9883300102"
    
    delete_recommendation(account_id_poc_1, country, environment, 'CROSS_SELL_UP_SELL')
    delete_recommendation(account_id_poc_2, country, environment, 'CROSS_SELL_UP_SELL')
    
    populate_recommendation(country, environment, account_id_poc_1)
    populate_recommendation(country, environment, account_id_poc_2)
    
    logger.info("Beer Recommender populating finalized.")