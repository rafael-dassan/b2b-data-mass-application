from mass_populator.log import *
from mass_populator.country.populate_user import populate_user

logger = logging.getLogger(__name__)


def populate_users(environment):
    account_id_poc_1 = "9883300101"
    account_id_poc_2 = "9883300102"
    account_id_poc_3 = "9883300103"
    country = "ZA"

    populate_user(country, environment, "qm.team.za+222@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.za+333@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.za+10000@gmail.com", "Pass()12", [account_id_poc_1, account_id_poc_3])
    
    populate_user(country, environment, "qm.team.za+1@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.za+2@gmail.com", "Password1", [account_id_poc_2, account_id_poc_3])
    populate_user(country, environment, "qm.team.za+3@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.za+100@gmail.com", "Pass()12", [account_id_poc_2, account_id_poc_3])
    
    populate_user(country, environment, "qm.team.za+11@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.za+22@gmail.com", "Password1", [account_id_poc_2, account_id_poc_3])
    populate_user(country, environment, "qm.team.za+33@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.za+1000@gmail.com", "Pass()12", [account_id_poc_2, account_id_poc_3])

    logger.info("Users populating finalized.")