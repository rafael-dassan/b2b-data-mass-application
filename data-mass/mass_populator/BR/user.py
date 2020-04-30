from mass_populator.log import logging
from user_creation_magento import \
    create_user, user_already_exists_with_account, authenticate_user, associate_user_to_account
from account import check_account_exists_microservice


def populate_users(environment):
    account_id_poc_1 = "99481543000135"
    account_id_poc_2 = "56338831000122"
    account_id_poc_3 = "42282891000166"

    populate_user(environment, "abiautotest+2@mailinator.com", "Password1", [account_id_poc_1])
    populate_user(environment, "abiautotest+100@mailinator.com", "Pass()12", [account_id_poc_1, account_id_poc_3])
    populate_user(environment, "abiautotest+1@gmail.com", "Password1", [account_id_poc_2])
    populate_user(environment, "abiautotest+2@gmail.com", "Password1", [account_id_poc_2, account_id_poc_3])
    populate_user(environment, "abiautotest+100@gmail.com", "Pass()12", [account_id_poc_2, account_id_poc_3])

    print("Users populating finalized.")


def populate_user(environment, username, password, account_ids):
    create_user_br(environment, username, password, account_ids[0])
    for account_id in account_ids[1:]:
        associate_user_br(environment, username, password, account_id)


def create_user_br(environment, username, password, account_id):
    if not user_already_exists_with_account(environment, "BR", username, password, account_id):
        logging.debug(
            "Creating User: {user}/{password}/{account}".format(user=username, password=password, account=account_id))

        account_result = check_account_exists_microservice(account_id, "BR", environment)
        if "success" != create_user(environment, "BR", username, password, account_result[0]):
            logging.error("Fail on populate user.")
    else:
        logging.debug(
            "User already exists with the informed account: {user}/{password}/{account}".format(
                user=username, password=password, account=account_id))


def associate_user_br(environment, username, password, account_id):
    if not user_already_exists_with_account(environment, "BR", username, password, account_id):
        logging.debug(
            "Creating User: {user}/{password}/{account}".format(user=username, password=password, account=account_id))

        user = authenticate_user(environment, "BR", username, password)
        account_result = check_account_exists_microservice(account_id, "BR", environment)
        if "success" != associate_user_to_account(environment, "BR", user, account_result[0]):
            logging.error("Fail on associate account.")
    else:
        logging.debug(
            "User already exists with the informed account: {user}/{password}/{account}".format(
                user=username, password=password, account=account_id))
