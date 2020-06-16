from mass_populator.log import *
from mass_populator.country.populate_user import populate_user

logger = logging.getLogger(__name__)


def populate_users(environment):
    account_id_poc_1 = "99481543000135"
    account_id_poc_2 = "56338831000122"
    account_id_poc_3 = "42282891000166"
    country = "BR"

    populate_user(country, environment, "qm.team.br+222@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.br+333@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.br+10000@gmail.com", "Pass()12", [account_id_poc_1, account_id_poc_3])
    
    populate_user(country, environment, "qm.team.br+1@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.br+2@gmail.com", "Password1", [account_id_poc_2, account_id_poc_3])
    populate_user(country, environment, "qm.team.br+3@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.br+100@gmail.com", "Pass()12", [account_id_poc_2, account_id_poc_3])
    
    populate_user(country, environment, "qm.team.br+11@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.br+22@gmail.com", "Password1", [account_id_poc_2, account_id_poc_3])
    populate_user(country, environment, "qm.team.br+33@gmail.com", "Password1", [account_id_poc_1])
    populate_user(country, environment, "qm.team.br+1000@gmail.com", "Pass()12", [account_id_poc_2, account_id_poc_3])

    logger.info("Users populating finalized.")