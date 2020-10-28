from mass_populator.log import *
from mass_populator.csv_helper import search_data_by
from mass_populator.country.populate_rewards import unenroll_pocs as unenroll_accounts_base

logger = logging.getLogger(__name__)

def execute_rewards(country, environment):
    unenroll_accounts(country, environment)
    return True

def unenroll_accounts(country, environment):
    logger.info("unenroll_accounts for %s/%s", country, environment)
    unenroll_accounts_base(country, environment, search_data_by(country,'rewards'))
    return True