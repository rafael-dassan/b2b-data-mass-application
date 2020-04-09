from account import create_account_ms
from delivery_window import create_delivery_window_microservice


def populate_accounts(country, environment):
    populate_poc1(country, environment)
    populate_poc2(country, environment)
    populate_poc3(country, environment)

    print("Accounts populating finalized.")


# Populate an account
def populate_account(country, environment, account_id, account_name):
    if "success" != create_account_ms(account_id, account_name, ["CASH", "CREDIT"], None, country, environment):
        print("Fail on populate account " + account_id + ".")


# Populate the delivery window for an account
def populate_delivery_window(country, environment, account_id):
    account_data = {
        "deliveryScheduleId": account_id,
        "accountId": account_id
    }
    if "success" != create_delivery_window_microservice(account_id, country, environment, account_data, "false"):
        print("Fail on populate delivery window for account " + account_id + ".")


# Populate the POC 1
def populate_poc1(country, environment):
    account_id = "9883300001"
    populate_account(country, environment, account_id, "DO_POC_001")
    populate_delivery_window(country, environment, account_id)


# Populate the POC 2
def populate_poc2(country, environment):
    account_id = "9883300002"
    populate_account(country, environment, account_id, "DO_POC_002")
    populate_delivery_window(country, environment, account_id)


# Populate the POC 3
def populate_poc3(country, environment):
    populate_account(country, environment, "9883300003", "DO_POC_003")


