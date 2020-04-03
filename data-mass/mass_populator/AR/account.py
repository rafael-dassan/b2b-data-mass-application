from account import create_account_ms


def populate_accounts(country, environment):

    if "success" != create_account_ms("386041", "NO RUTEAR B2B", ["CASH"], None, country, environment):
        print("Fail on populate account 386041.")

    if "success" != create_account_ms("0000000001", "ACCOUNT 01", ["CASH"], None, country, environment):
        print("Fail on populate account 0000000001.")

    print("Accounts populating finalized.")