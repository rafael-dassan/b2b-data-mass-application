from mass_populator.log import logging
from rewards.rewards import disenroll_poc_from_program
from rewards.rewards_challenges import input_challenge_to_zone

logger = logging.getLogger(__name__)


def disenroll_pocs(country, environment, dataframe_products):
    if dataframe_products is not None:
        dataframe_products.apply(exec_disenroll_poc, 
        args=(country, environment), axis=1)

    logger.info("All the accounts are unenrolled!")


def exec_disenroll_poc(row, country, environment):
    account_id = str(row['account_id_unenroll'])

    disenroll_response = disenroll_poc_from_program(account_id, country, environment)
    if disenroll_response.status_code == 404:
        logger.info("The account %s is already unenrolled. Skipping...", account_id)


def populate_challenges(country, environment, dataframe_products):
    if dataframe_products is not None:
        dataframe_products.apply(exec_populate_challenges,
        args=(country, environment), axis=1)

    logger.info("All needed challenges was created.")


def exec_populate_challenges(row, country, environment):
    account_id = str(row['account_id_enrolled'])
    if account_id != 'nan':
        logger.info("Adding challenges for account %s in %s/%s", account_id, country, environment)
        input_challenge_to_zone(account_id, country, environment)