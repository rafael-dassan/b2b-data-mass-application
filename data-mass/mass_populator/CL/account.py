from account import create_account_ms
from delivery_window import create_delivery_window_microservice


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
    create_delivery_window_microservice(account_id, country, environment, account_data, "false")

# Populate account for CL environment
def populate_account_CL(country, environment, account_id, account_name):
    if "success" != create_account_ms(
            account_id, account_name, ["CASH"], None, country, environment):

        print("Populate account failed. " + account_id + ".")


# Populate the POC 1
def populate_poc1(country, environment):
    account_id = "2323434554"
    populate_account_CL(country, environment, account_id, "CL_POC_001")
    populate_delivery_window(country, environment, account_id)


# Populate the POC 2
def populate_poc2(country, environment):
    account_id = "1020303040"
    populate_account_CL(country, environment, account_id, "CL_POC_002")
    populate_delivery_window(country, environment, account_id)


# Populate the POC 3
def populate_poc3(country, environment):
    populate_account_CL(country, environment, "3325534210", "CL_POC_003")