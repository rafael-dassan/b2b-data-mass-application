from mass_populator.log import *
from user_creation_magento import \
    create_user, user_already_exists_with_account, check_user, UserCheckDict, authenticate_user, \
    associate_user_to_account
from account import check_account_exists_microservice

logger = logging.getLogger(__name__)


def populate_users(environment):
    account_id_poc_1 = "9883300001"
    account_id_poc_2 = "9883300002"
    account_id_poc_3 = "9883300003"

    populate_user(environment, "abiautotest+2@mailinator.com", "Password1", [account_id_poc_1])
    populate_user(environment, "abiautotest+100@mailinator.com", "Pass()12", [account_id_poc_1, account_id_poc_3])
    populate_user(environment, "abiautotest+1@gmail.com", "Password1", [account_id_poc_2])
    populate_user(environment, "abiautotest+2@gmail.com", "Password1", [account_id_poc_2, account_id_poc_3])
    populate_user(environment, "abiautotest+100@gmail.com", "Pass()12", [account_id_poc_2, account_id_poc_3])

    logger.info("Users populating finalized.")


def populate_user(environment, username, password, account_ids):
    if "success" != create_user_do(environment, username, password, account_ids[0]):
        logger.error("Fail on populate user.")
    else:
        for account_id in account_ids[1:]:
            associate_user_do(environment, username, password, account_id)


def associate_user_do(environment, username, password, account_id):
    if not user_already_exists_with_account(environment, "DO", username, password, account_id):
        logger.debug(
            "Associating User: {user}/{password}/{account}".format(user=username, password=password, account=account_id))

        user = authenticate_user(environment, "DO", username, password)
        account_result = check_account_exists_microservice(account_id, "DO", environment)
        if "success" != associate_user_to_account(environment, "DO", user, account_result[0]):
            logger.error("Fail on associate account.")


def create_user_do(environment, username, password, account_id):
    result = check_user(environment, "DO", username, password, account_id)

    if result == UserCheckDict.USER_EXISTS_AND_HAS_ACCOUNT:
        log_user_already_exists_with_informed_account(username, password, account_id)
        return "success"
    else:
        if result == UserCheckDict.USER_EXISTS_BUT_WITHOUT_THE_ACCOUNT:
            log_user_already_exists_without_informed_account(username, password, account_id)
            return "fail"
        else:
            account_result = check_account_exists_microservice(account_id, "DO", environment)
            if "success" != create_user(environment, "DO", username, password, account_result[0]):
                log_user_and_or_passord_incorrect(username, password, account_id)
                return "fail"
            return "success"


def log_user_already_exists_with_informed_account(username, password, account_id):
    logger.debug("User {user}/{password} already exists with the informed account: {account}".format(
            user=username, password=password, account=account_id))


def log_user_already_exists_without_informed_account(username, password, account_id):
    logger.warning("User {user}/{password} already exists but doesn't have the informed account: {account}".format(
            user=username, password=password, account=account_id))


def log_user_and_or_passord_incorrect(username, password, account_id):
    logger.warning("User {user}/{password} already exists but was unable to check account information: {account}".format(
            user=username, password=password, account=account_id))

