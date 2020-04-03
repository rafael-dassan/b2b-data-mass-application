from account import create_account_ms


def populate_accounts(country, environment):
    if "success" != create_account_ms("0501000002", "BR_WEB_MULTI", ["CASH", "BANK_SLIP"], None, country, environment):
        print("Fail on populate account 0501000002.")

    if "success" != create_account_ms("0501999999", "BR_ASSOC_01", ["CASH", "BANK_SLIP"], None, country, environment):
        print("Fail on populate account 0501999999.")

    print("Accounts populating finalized.")



