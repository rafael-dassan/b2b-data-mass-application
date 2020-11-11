from mass_populator.log import logging
from mass_populator.csv_helper import search_data_by
from mass_populator.country.populate_rewards import disenroll_pocs

logger = logging.getLogger(__name__)


def execute_rewards(country, environment):
    disenroll_accounts(country, environment)
    return True


def disenroll_accounts(country, environment):
    logger.info("Disenroll_accounts for %s/%s", country, environment)
    disenroll_pocs(country, environment, search_data_by(country, 'rewards'))
    return True
