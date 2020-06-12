from mass_populator.log import *
from mass_populator.country.populate_user import populate_user


logger = logging.getLogger(__name__)


def populate_users(environment):
    account_id_poc_1 = "9883300001"
    account_id_poc_2 = "9883300002"
    account_id_poc_3 = "9883300003"
    country = "DO"

    populate_user(country, environment, "qm.team.do+222@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.do+333@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.do+10000@gmail.com", "Pass()12", [account_id_poc_1, account_id_poc_3])
    
    populate_user(country, environment, "qm.team.do+1@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.do+2@gmail.com", "Password1", [account_id_poc_2, account_id_poc_3])
    populate_user(country, environment, "qm.team.do+3@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.do+100@gmail.com", "Pass()12", [account_id_poc_2, account_id_poc_3])
    
    populate_user(country, environment, "qm.team.do+11@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.do+22@gmail.com", "Password1", [account_id_poc_2, account_id_poc_3])
    populate_user(country, environment, "qm.team.do+33@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.do+1000@gmail.com", "Pass()12", [account_id_poc_2, account_id_poc_3])
    
    logger.info("Users populating finalized.")