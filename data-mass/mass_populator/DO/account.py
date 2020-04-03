from account import create_account_ms


def populate_accounts(country, environment):
    if "success" != create_account_ms("0101000002", "DR_WEB_MULTI", ["CASH", "CREDIT"], None, country, environment):
        print("Fail on populate account 0101000002.")

    if "success" != create_account_ms("0101999999", "DR_ASSOC_01", ["CASH", "CREDIT"], None, country, environment):
        print("Fail on populate account 0101999999.")

    print("Accounts populating finalized.")



