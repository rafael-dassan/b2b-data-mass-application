from data_mass.populator.log import logging
from data_mass.rewards.rewards import disenroll_poc_from_program
from data_mass.rewards.challenges import create_take_photo_challenge, \
    create_mark_complete_challenge, create_purchase_challenge

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


def populate_challenges(country, environment):
    exec_populate_challenges(country, environment)
    logger.info("All needed challenges were created.")


def exec_populate_challenges(country, environment):
    logger.info("Adding challenges in %s/%s", country, environment)
    
    logger.info("Adding TAKE_PHOTO challenges")
    # Create an Available TAKE_PHOTO challenge
    create_take_photo_challenge(country, environment)
    # Create an Expired TAKE_PHOTO challenge
    create_take_photo_challenge(country, environment, True)
    
    logger.info("Adding MARK_COMPLETE challenges")
    # Create an Available MARK_COMPLETE challenge
    create_mark_complete_challenge(country, environment)
    # Create an Expired MARK_COMPLETE challenge
    create_mark_complete_challenge(country, environment, True)

    logger.info("Adding PURCHASE challenges")
    # Create an Available PURCHASE challenge
    create_purchase_challenge(country, environment, False)
    # Create an Expired PURCHASE challenge
    create_purchase_challenge(country, environment, False, True)

    logger.info("Adding PURCHASE_MULTIPLE challenges")
    # Create an Available PURCHASE_MULTIPLE challenge
    create_purchase_challenge(country, environment, True)
    # Create an Expired PURCHASE_MULTIPLE challenge
    create_purchase_challenge(country, environment, True, True)