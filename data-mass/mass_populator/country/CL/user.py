from mass_populator.log import *
from mass_populator.country.populate_user import populate_user


logger = logging.getLogger(__name__)


def populate_users(environment):
    account_id_poc_1 = "2323434554"
    account_id_poc_2 = "1020303040"
    account_id_poc_3 = "3325534210"
    country = "CL"

    populate_user(country, environment, "abiautotest+2@mailinator.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "abiautotest+100@mailinator.com", "Pass()12", [account_id_poc_1, account_id_poc_3])
    populate_user(country, environment, "abiautotest+1@gmail.com", "Password1", [account_id_poc_2])
    populate_user(country, environment, "abiautotest+2@gmail.com", "Password1", [account_id_poc_2, account_id_poc_3])
    populate_user(country, environment, "abiautotest+100@gmail.com", "Pass()12", [account_id_poc_2, account_id_poc_3])

    logger.info("Users populating finalized.")
