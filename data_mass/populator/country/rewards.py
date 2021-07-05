from data_mass.rewards.rewards import disenroll_poc_from_program, put_rewards
from data_mass.rewards.rewards_challenges import create_take_photo_challenge, \
    create_mark_complete_challenge, create_purchase_challenge
from data_mass.populator.log import *

logger = logging.getLogger(__name__)


def enroll_poc_base(country, environment, dataframe_rewards):
    if dataframe_rewards is not None:
        dataframe_rewards.apply(apply_enroll_poc, args=(country, environment), axis=1)


def apply_enroll_poc(row, country, environment):
    enroll_poc(country, environment, str(row['account_id_unenroll']))


def enroll_poc(country, environment, account_id):
    response = put_rewards(account_id, country, environment)

    if response.status_code == 201:
        logger.debug("The account {} has been successfully enrolled to a rewards program.".format(account_id))
    elif response.status_code == 409:
        logger.debug("The account {} is already enrolled to a rewards program.".format(account_id))
    elif response.status_code == 406:
        logger.error("The account {} is not eligible for a rewards program.".format(account_id))
    else:
        logger.error(log(Message.POC_ENROLLMENT_ERROR, {"account_id": account_id}))


def disenroll_pocs(country, environment, dataframe_products):
    if dataframe_products is not None:
        dataframe_products.apply(exec_disenroll_poc, args=(country, environment), axis=1)

    logger.debug("All the accounts are unenrolled!")


def exec_disenroll_poc(row, country, environment):
    account_id = str(row['account_id_unenroll'])

    disenroll_response = disenroll_poc_from_program(account_id, country, environment)
    if disenroll_response.status_code == 404:
        logger.debug("The account %s is already unenrolled. Skipping...", account_id)


def populate_challenge_base(country, environment, dataframe_rewards):
    if dataframe_rewards is not None:
        dataframe_rewards.apply(apply_populate_challenge, args=(country, environment), axis=1)


def apply_populate_challenge(row, country, environment):
    logger.debug("Adding challenges in %s/%s", country, environment)
    populate_challenge_take_photo(country, environment, row['take_photo_challenge_id'])
    populate_challenge_mark_complete(country, environment, row['mark_complete_challenge_id'])
    populate_challenge_purchase_single(country, environment, row['purchase_single_challenge_id'])
    populate_challenge_purchase_multiple(country, environment, row['purchase_multiple_challenge_id'])


def populate_challenge(country, environment):
    logger.debug("Adding challenges in %s/%s", country, environment)
    
    logger.debug("Adding TAKE_PHOTO challenges")
    # Create an Available TAKE_PHOTO challenge
    create_take_photo_challenge(country, environment)
    # Create an Expired TAKE_PHOTO challenge
    create_take_photo_challenge(country, environment, None, True)
    
    logger.debug("Adding MARK_COMPLETE challenges")
    # Create an Available MARK_COMPLETE challenge
    create_mark_complete_challenge(country, environment)
    # Create an Expired MARK_COMPLETE challenge
    create_mark_complete_challenge(country, environment, None, True)

    logger.debug("Adding PURCHASE challenges")
    # Create an Available PURCHASE challenge
    create_purchase_challenge(country, environment, False, None)
    # Create an Expired PURCHASE challenge
    create_purchase_challenge(country, environment, False, None, True)

    logger.debug("Adding PURCHASE_MULTIPLE challenges")
    # Create an Available PURCHASE_MULTIPLE challenge
    create_purchase_challenge(country, environment, True)
    # Create an Expired PURCHASE_MULTIPLE challenge
    create_purchase_challenge(country, environment, True, None, True)


def populate_challenge_take_photo(country, environment, challenge_id):
    logger.debug("Adding/Updating TAKE_PHOTO challenge")
    # Create an Available TAKE_PHOTO challenge
    create_take_photo_challenge(country, environment, challenge_id)


def populate_challenge_mark_complete(country, environment, challenge_id):
    logger.debug("Adding/Updating MARK_COMPLETE challenge")
    # Create an Available MARK_COMPLETE challenge
    create_mark_complete_challenge(country, environment, challenge_id)


def populate_challenge_purchase_single(country, environment, challenge_id):
    logger.debug("Adding/Updating PURCHASE challenge")
    # Create an Available PURCHASE challenge
    create_purchase_challenge(country, environment, False, challenge_id)


def populate_challenge_purchase_multiple(country, environment, challenge_id):
    logger.debug("Adding/Updating PURCHASE_MULTIPLE challenge")
    # Create an Available PURCHASE_MULTIPLE challenge
    create_purchase_challenge(country, environment, True, challenge_id)