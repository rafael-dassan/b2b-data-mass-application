from account import create_account_ms


def populate_accounts(country, environment):
    if "success" != create_account_ms(
            "99481543000135", "BR_POC_001", ["CASH", "BANK_SLIP"], None, country, environment):
        print("Fail on populate account 99481543000135.")

    if "success" != create_account_ms(
            "56338831000122", "BR_POC_002", ["CASH", "BANK_SLIP"], None, country, environment):
        print("Fail on populate account 56338831000122.")

    if "success" != create_account_ms(
            "42282891000166", "BR_POC_003", ["CASH", "BANK_SLIP"], None, country, environment):
        print("Fail on populate account 42282891000166.")

    print("Accounts populating finalized.")
