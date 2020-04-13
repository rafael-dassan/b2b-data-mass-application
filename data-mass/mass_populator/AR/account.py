from account import create_account_ms
from delivery_window import create_delivery_window_microservice
from credit import add_credit_to_account_microservice


def populate_accounts(country, environment):
    populate_poc1(country, environment)
    populate_poc2(country, environment)
    populate_poc3(country, environment)

    print("Accounts populating finalized.")


# Populate the delivery window for an account
def populate_delivery_window(country, environment, account_id):
    account_data = {
        "deliveryScheduleId": account_id,
        "accountId": account_id
    }
    if "success" != create_delivery_window_microservice(account_id, country, environment, account_data, "false"):
        print("Fail on populate delivery window for account " + account_id + ".")


# Populate account for AR environment
def populate_account(country, environment, account_id, account_name):
    if "success" != create_account_ms(account_id, account_name, ["CASH"], None, country, environment):
        print("Fail on populate account " + account_id + ".")


# Include credit on AR account
def populate_credit(account_id, country, environment, credit, balance):
    if "success" != add_credit_to_account_microservice(account_id, country, environment, credit, balance):
        print("Fail on populate credit for account " + account_id + ".")


# Populate the POC 1
def populate_poc1(country, environment):
    credit = "45000"
    balance = "45000"
    account_id = "5444385012"
    populate_account(country, environment, account_id, "AR_POC_001")
    populate_delivery_window(country, environment, account_id)
    populate_credit(account_id, country, environment, credit, balance)


# Populate the POC 2
def populate_poc2(country, environment):
    account_id = "9932094352"
    credit = "45000"
    balance = "45000"
    populate_account(country, environment, account_id, "AR_POC_002")
    populate_delivery_window(country, environment, account_id)
    populate_credit(account_id, country, environment, credit, balance)


# Populate the POC 3
def populate_poc3(country, environment):
    credit = "45000"
    balance = "45000"
    populate_account(country, environment, "1669325565", "AR_POC_003")
    populate_credit("1669325565", country, environment, credit, balance)
