from account import create_account_ms
from delivery_window import create_delivery_window_microservice
from credit import add_credit_to_account_microservice
from common import validate_state


def populate_accounts(country, environment):
    populate_poc1(country, environment)
    populate_poc2(country, environment)
    populate_poc3(country, environment)

    print("Accounts populating finalized.")


# Populate an account
def populate_account(country, environment, account_id, account_name):
    state = validate_state(country)
    if "success" != create_account_ms(account_id, account_name, ["CASH", "CREDIT"], None, country, environment, state):
        print("Fail on populate account " + account_id + ".")


# Populate the delivery window for an account
def populate_delivery_window(country, environment, account_id):
    account_data = {
        "deliveryScheduleId": account_id,
        "accountId": account_id
    }
    if "success" != create_delivery_window_microservice(account_id, country, environment, account_data, "false"):
        print("Fail on populate delivery window for account " + account_id + ".")


# Populate the credit for an account
def populate_credit(country, environment, account_id, credit, balance):
    if "success" != add_credit_to_account_microservice(account_id, country, environment, credit, balance):
        print("Fail on populate credit for account " + account_id + ".")


# Populate the POC 1
def populate_poc1(country, environment):
    account_id = "9883300001"
    populate_account(country, environment, account_id, "DO_POC_001")
    populate_delivery_window(country, environment, account_id)
    populate_credit(country, environment, account_id, "45000", "45000")


# Populate the POC 2
def populate_poc2(country, environment):
    account_id = "9883300002"
    populate_account(country, environment, account_id, "DO_POC_002")
    populate_delivery_window(country, environment, account_id)
    populate_credit(country, environment, account_id, "45000", "45000")


# Populate the POC 3
def populate_poc3(country, environment):
    account_id = "9883300003"
    populate_account(country, environment, account_id, "DO_POC_003")
    populate_credit(country, environment, account_id, "45000", "45000")
