from account import create_account_ms
from account import create_account


def populate_accounts(country, environment):
    if "success" != create_account_ms("0201000002", "ZA_WEB_MULTI", ["CASH"], None, country, environment):
        print("Fail on populate account 0201000002 on Microservice.")

    if "success" != create_account_ms("0201999999", "ZA_ASSOC_01", ["CASH"], None, country, environment):
        print("Fail on populate account 0201999999 on Microservice.")

    if "success" != create_account("0201000002", "ZA_WEB_MULTI", country, ["CASH"], environment, None):
        print("Fail on populate account 0201000002 on Middleware.")

    if "success" != create_account("0201999999", "ZA_ASSOC_01", country, ["CASH"], environment, None):
        print("Fail on populate account 0201999999 on Middleware.")

    print("Accounts populating finalized.")



