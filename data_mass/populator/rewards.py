from data_mass.common import block_print
from data_mass.populator.log import logging
from data_mass.populator.helpers.csv_helper import search_data_by
from data_mass.populator.country.rewards import disenroll_pocs, populate_challenge

logger = logging.getLogger(__name__)


def execute_rewards(country, environment):
    block_print()
    disenroll_accounts(country, environment)
    add_challenges_to_accounts(country, environment)
    return True


def disenroll_accounts(country, environment):
    logger.info("Disenroll_accounts for %s/%s", country, environment)
    disenroll_pocs(country, environment, search_data_by(country, 'rewards'))
    return True


def add_challenges_to_accounts(country, environment):
    logger.info("Starting to add challenges...")
    populate_challenge(country, environment)
    return True
