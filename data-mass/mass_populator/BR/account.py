from account import create_account_ms
from delivery_window import create_delivery_window_microservice
from credit import add_credit_to_account_microservice
from common import validate_state
from mass_populator.log import *

logger = logging.getLogger(__name__)


# Populate the accounts for BR
def populate_accounts(country, environment):
    populate_poc1(country, environment)
    populate_poc2(country, environment)
    populate_poc3(country, environment)

    logger.info("Accounts populating finalized.")


# Populate an account
def populate_account(country, environment, account_id, account_name):
    state = validate_state(country)
    if "success" != create_account_ms(account_id, account_name, ["CASH", "BANK_SLIP"], None, country, environment, state):
        logger.info(log(Message.ACCOUNT_ERROR, {"account_id": account_id}))


# Populate the delivery window for an account
def populate_delivery_window(country, environment, account_id):
    account_data = {
        "deliveryScheduleId": account_id,
        "accountId": account_id
    }
    if "success" != create_delivery_window_microservice(account_id, country, environment, account_data, "false"):
        logger.info(log(Message.DELIVERY_WINDOW_ERROR, {"account_id": account_id}))


# Populate the credit for an account
def populate_credit(country, environment, account_id, credit, balance):
    if "success" != add_credit_to_account_microservice(account_id, country, environment, credit, balance):
        print("Fail on populate credit for account " + account_id + ".")


# Populate the POC 1
def populate_poc1(country, environment):
    account_id = "99481543000135"
    populate_account(country, environment, account_id, "BR_POC_001")
    populate_delivery_window(country, environment, account_id)
    populate_credit(country, environment, account_id, "45000", "45000")


# Populate the POC 2
def populate_poc2(country, environment):
    account_id = "56338831000122"
    populate_account(country, environment, account_id, "BR_POC_002")
    populate_delivery_window(country, environment, account_id)
    populate_credit(country, environment, account_id, "45000", "45000")


# Populate the POC 3
def populate_poc3(country, environment):
    account_id = "42282891000166"
    populate_account(country, environment, account_id, "BR_POC_003")
    populate_credit(country, environment, account_id, "45000", "45000")
