from mass_populator.log import *
from mass_populator.country.populate_recomendation import populate_recommendation

logger = logging.getLogger(__name__)


def populate_recomendations(environment):
    country = "BR"
    account_id_poc_1 = "99481543000135"
    account_id_poc_2 = "56338831000122"

    populate_recommendation(country, environment, account_id_poc_1)
    populate_recommendation(country, environment, account_id_poc_2)
    
    logger.info("Beer Recommender populating finalized.")