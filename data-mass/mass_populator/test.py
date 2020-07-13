from mass_populator.log import *
from mass_populator.country.populate_account import populate_poc
from mass_populator.country.populate_recomendation import populate_recommendation
from mass_populator.country.populate_user import populate_user
from mass_populator.country.delete_recommendation import delete_recommendation

logger = logging.getLogger(__name__)


def execute_test(country, environment):
    country = "DO"
    environment = "SIT"
    account = "9883300009"

    populate_poc(country, environment, account, "QA_POC_001", ["CASH", "CREDIT"], "45000", "45000", 100, True)
    logger.info("Account populating finalized.")
    
    populate_user(country, environment, "qa_abiautotest+1@gmail.com", "Password1", [account], "+5519992666529")
    logger.info("User populating finalized.")

    delete_recommendation(account, country, environment, 'CROSS_SELL_UP_SELL')
    delete_recommendation(account, country, environment, 'QUICK_ORDER')
    delete_recommendation(account, country, environment, 'FORGOTTEN_ITEMS')
    logger.info('Pre-condition: Removing recommendation finalized.')

    populate_recommendation(country, environment, account)
    logger.info("Beer Recommender populating finalized.")