from mass_populator.log import *
from mass_populator.country.populate_recomendation import populate_recommendation

logger = logging.getLogger(__name__)


def populate_recomendations(environment):
    country = "ZA"
    account_id_poc_1 = "9883300101"
    account_id_poc_3 = "9883300103"
    
    populate_recommendation(country, environment, account_id_poc_1)
    populate_recommendation(country, environment, account_id_poc_3)
    
    logger.info("Beer Recommender populating finalized.")