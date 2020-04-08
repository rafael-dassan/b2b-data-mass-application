from account import create_account_ms


def populate_accounts(country, environment):
    if "success" != create_account_ms("9883300001", "DO_POC_001", ["CASH", "CREDIT"], None, country, environment):
        print("Fail on populate account 9883300001.")

    if "success" != create_account_ms("9883300002", "DO_POC_002", ["CASH", "CREDIT"], None, country, environment):
        print("Fail on populate account 9883300002.")

    if "success" != create_account_ms("9883300003", "DO_POC_003", ["CASH", "CREDIT"], None, country, environment):
        print("Fail on populate account 9883300003.")

    print("Accounts populating finalized.")



