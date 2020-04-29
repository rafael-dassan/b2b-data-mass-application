from user_creation_magento import create_user, user_already_exists_with_account
from account import check_account_exists_microservice
from mass_populator.log import logging


def populate_users(environment):
    populate_users_for_POC_1(environment)
    populate_users_for_POC_2(environment)

    print("Users populating finalized.")


def populate_users_for_POC_1(environment):
    account_id = "9883300001"
    create_user_do(environment, "abiautotest+2@mailinator.com", "Password1", account_id)
    create_user_do(environment, "abiautotest+100@mailinator.com", "Pass()12", account_id)


def populate_users_for_POC_2(environment):
    account_id = "9883300002"
    create_user_do(environment, "abiautotest+1@gmail.com", "Password1", account_id)
    create_user_do(environment, "abiautotest+2@gmail.com", "Password1", account_id)
    create_user_do(environment, "abiautotest+100@gmail.com", "Pass()12", account_id)


def create_user_do(environment, username, password, account_id):
    if not user_already_exists_with_account(environment, "DO", username, password, account_id):
        logging.debug(
            "Creating User: {user}/{password}/{account}".format(user=username, password=password, account=account_id))

        account_result = check_account_exists_microservice(account_id, "DO", environment)
        if "success" != create_user(environment, "DO", username, password, account_result[0]):
            logging.debug("Fail on populate user.")
    else:
        logging.debug(
            "User already exists with the informed account: {user}/{password}/{account}".format(
                user=username, password=password, account=account_id))