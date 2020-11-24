from rewards import *
from mass_populator.log import logging

logger = logging.getLogger(__name__)


def disenroll_pocs(country, environment, dataframe_products):
    if dataframe_products is not None:
        dataframe_products.apply(exec_disenroll_poc, 
        args=(country, environment), axis=1)

    logger.info("All the accounts are unenrolled!")


def exec_disenroll_poc(row, country, environment):
    account_id = str(row['account_id_unenroll'])

    rewards_status = get_rewards_status(account_id, country, environment)
    if rewards_status == 200:
        delete_enroll_poc_to_program(account_id, country, environment)
    else:
        logger.info("The account %s is already unenrolled. Skipping...", account_id)

