from account import create_account_ms


def populate_accounts(country, environment):
    if "success" != create_account_ms("100006", "NO RUTEAR B2B", ["CASH"], None, country, environment):
        print("Fail on populate account 100006.")

    if "success" != create_account_ms("0301999999", "CL_ASSOC_01", ["CASH"], None, country, environment):
        print("Fail on populate account 0301999999.")

    print("Accounts populating finalized.")