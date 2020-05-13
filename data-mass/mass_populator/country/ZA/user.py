from mass_populator.log import *
from mass_populator.country.populate_user import populate_user

logger = logging.getLogger(__name__)


def populate_users(environment):
    account_id_poc_1 = "9883300101"
    account_id_poc_2 = "9883300102"
    account_id_poc_3 = "9883300103"
    country = "ZA"

    populate_user(country, environment, "abiautotest+2@mailinator.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "abiautotest+100@mailinator.com", "Pass()12", [account_id_poc_1, account_id_poc_3])
    populate_user(country, environment, "abiautotest+1@gmail.com", "Password1", [account_id_poc_2])
    populate_user(country, environment, "abiautotest+2@gmail.com", "Password1", [account_id_poc_2, account_id_poc_3])
    populate_user(country, environment, "abiautotest+100@gmail.com", "Pass()12", [account_id_poc_2, account_id_poc_3])

    logger.info("Users populating finalized.")