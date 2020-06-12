from mass_populator.log import *
from mass_populator.country.populate_user import populate_user


logger = logging.getLogger(__name__)


def populate_users(environment):
    account_id_poc_1 = "9883300201"
    account_id_poc_2 = "9883300202"
    account_id_poc_3 = "9883300203"
    country = "CO"

    populate_user(country, environment, "qm.team.co+222@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.co+333@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.co+10000@gmail.com", "Pass()12", [account_id_poc_1, account_id_poc_3])
    
    populate_user(country, environment, "qm.team.co+1@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.co+2@gmail.com", "Password1", [account_id_poc_2, account_id_poc_3])
    populate_user(country, environment, "qm.team.co+3@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.co+100@gmail.com", "Pass()12", [account_id_poc_2, account_id_poc_3])
    
    populate_user(country, environment, "qm.team.co+11@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.co+22@gmail.com", "Password1", [account_id_poc_2, account_id_poc_3])
    populate_user(country, environment, "qm.team.co+33@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.co+1000@gmail.com", "Pass()12", [account_id_poc_2, account_id_poc_3]) 

    logger.info("Users populating finalized.")