from account import create_account_ms
from account import create_account
from delivery_window import create_delivery_window_microservice
from delivery_window import create_delivery_window_middleware
from credit import add_credit_to_account, add_credit_to_account_microservice
from common import validate_state
from mass_populator.log import *

logger = logging.getLogger(__name__)


def populate_accounts(country, environment):
    populate_poc1(country, environment)
    populate_poc2(country, environment)
    populate_poc3(country, environment)

    logger.info("Accounts populating finalized.")


# Populate an account
def populate_account(country, environment, account_id, account_name):
    state = validate_state(country)
    if "success" != create_account_ms(account_id, account_name, ["CASH"], None, country, environment, state):
        logger.info(log(Message.ACCOUNT_ERROR, {"account_id": account_id}))

    if "success" != create_account(account_id, account_name, country, ["CASH"], environment, None, state):
        logger.info(log(Message.ACCOUNT_ERROR_MIDDLEWARE, {"account_id": account_id}))


# Populate the delivery window for an account
def populate_delivery_window(country, environment, account_id):
    account_data = {
        "deliveryScheduleId": account_id,
        "accountId": account_id
    }
    if "success" != create_delivery_window_microservice(account_id, country, environment, account_data, "false"):
        logger.info(log(Message.DELIVERY_WINDOW_ERROR, {"account_id": account_id}))

    if "success" != create_delivery_window_middleware(account_id, country, environment):
        logger.info(log(Message.DELIVERY_WINDOW_ERROR_MIDDLEWARE, {"account_id": account_id}))


# Include credit on ZA Account
def populate_credit(account_id, country, environment, credit, balance):
    if "success" != add_credit_to_account_microservice(account_id, country, environment, credit, balance):
        logger.info(log(Message.CREDIT_ERROR, {"account_id": account_id}))

    if "success" != add_credit_to_account(account_id, country, environment, credit, balance):
        logger.info(log(Message.CREDIT_ERROR_MIDDLEWARE, {"account_id": account_id}))


# Populate the POC 1
def populate_poc1(country, environment):
    account_id = "9883300101"
    credit = "45000"
    balance = "45000"
    populate_account(country, environment, account_id, "ZA_POC_001")
    populate_delivery_window(country, environment, account_id)
    populate_credit(account_id, country, environment, credit, balance)


# Populate the POC 2
def populate_poc2(country, environment):
    account_id = "9883300102"
    credit = "45000"
    balance = "45000"
    populate_account(country, environment, account_id, "ZA_POC_002")
    populate_delivery_window(country, environment, account_id)
    populate_credit(account_id, country, environment, credit, balance)


# Populate the POC 3
def populate_poc3(country, environment):
    account_id = "9883300103"
    credit = "45000"
    balance = "45000"
    populate_account(country, environment, account_id, "ZA_POC_003")
    populate_credit(account_id, country, environment, credit, balance)
