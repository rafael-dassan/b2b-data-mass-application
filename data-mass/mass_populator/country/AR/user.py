from mass_populator.log import *
from mass_populator.country.populate_user import populate_user

logger = logging.getLogger(__name__)


def populate_users(environment):
    account_id_poc_1 = "5444385012"
    account_id_poc_2 = "9932094352"
    account_id_poc_3 = "1669325565"
    country = "AR"

    populate_user(country, environment, "qm.team.ar+222@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.ar+333@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.ar+10000@gmail.com", "Pass()12", [account_id_poc_1, account_id_poc_3])
    
    populate_user(country, environment, "qm.team.ar+1@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.ar+2@gmail.com", "Password1", [account_id_poc_2, account_id_poc_3])
    populate_user(country, environment, "qm.team.ar+3@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.ar+100@gmail.com", "Pass()12", [account_id_poc_2, account_id_poc_3])
    
    populate_user(country, environment, "qm.team.ar+11@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.ar+22@gmail.com", "Password1", [account_id_poc_2, account_id_poc_3])
    populate_user(country, environment, "qm.team.ar+33@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.ar+1000@gmail.com", "Pass()12", [account_id_poc_2, account_id_poc_3])

    logger.info("Users populating finalized.")

