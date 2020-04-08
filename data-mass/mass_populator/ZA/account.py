from account import create_account_ms
from account import create_account


def populate_accounts(country, environment):
    if "success" != create_account_ms("9883300101", "ZA_POC_001", ["CASH"], None, country, environment):
        print("Fail on populate account 9883300101 on Microservice.")

    if "success" != create_account_ms("9883300102", "ZA_POC_002", ["CASH"], None, country, environment):
        print("Fail on populate account 9883300102 on Microservice.")

    if "success" != create_account_ms("9883300103", "ZA_POC_003", ["CASH"], None, country, environment):
        print("Fail on populate account 9883300103 on Microservice.")

    if "success" != create_account("9883300101", "ZA_POC_001", country, ["CASH"], environment, None):
        print("Fail on populate account 9883300101 on Middleware.")

    if "success" != create_account("9883300102", "ZA_POC_002", country, ["CASH"], environment, None):
        print("Fail on populate account 9883300102 on Middleware.")

    if "success" != create_account("9883300103", "ZA_POC_003", country, ["CASH"], environment, None):
        print("Fail on populate account 9883300103 on Middleware.")

    print("Accounts populating finalized.")



