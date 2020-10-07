from mass_populator.log import *
from mass_populator.csv_helper import search_data_by
from mass_populator.country.populate_rewards import desenroll_pocs as desenroll_accounts_base

logger = logging.getLogger(__name__)

def execute_rewards(country, environment):
    desenroll_accounts(country, environment)
    return True

def desenroll_accounts(country, environment):
    logger.info("desenroll_accounts for %s/%s", country, environment)
    desenroll_accounts_base(country, environment, search_data_by(country,'rewards'))
    return True