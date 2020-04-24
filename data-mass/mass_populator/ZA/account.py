from account import create_account_ms
from account import create_account
from delivery_window import create_delivery_window_microservice
from delivery_window import create_delivery_window_middleware
from credit import add_credit_to_account, add_credit_to_account_microservice
from common import validate_state


def populate_accounts(country, environment):
    populate_poc1(country, environment)
    populate_poc2(country, environment)
    populate_poc3(country, environment)

    print("Accounts populating finalized.")


# Populate an account
def populate_account(country, environment, account_id, account_name):
    state = validate_state(country)
    if "success" != create_account_ms(account_id, account_name, ["CASH"], None, country, environment, state):
        print("Fail on populate account " + account_id + ".")

    if "success" != create_account(account_id, account_name, country, ["CASH"], environment, None, state):
        print("Fail on populate account " + account_id + " on Middleware.")


# Populate the delivery window for an account
def populate_delivery_window(country, environment, account_id):
    account_data = {
        "deliveryScheduleId": account_id,
        "accountId": account_id
    }
    if "success" != create_delivery_window_microservice(account_id, country, environment, account_data, "false"):
        print("Fail on populate delivery window for account " + account_id + ".")

    if "success" != create_delivery_window_middleware(account_id, country, environment):
        print("Fail on populate delivery window for account " + account_id + " on Middleware.")


# Include credit on ZA Account
def populate_credit(account_id, country, environment, credit, balance):
    if "success" != add_credit_to_account_microservice(account_id, country, environment, credit, balance):
        print("Fail on populate credit for account " + account_id + ".")

    if "success" != add_credit_to_account(account_id, country, environment, credit, balance):
        print("Fail on populate credit for account " + account_id + " on Middleware.")


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
    credit = "45000"
    balance = "45000"
    populate_account(country, environment, "9883300103", "ZA_POC_003")
    populate_credit("9883300103", country, environment, credit, balance)
