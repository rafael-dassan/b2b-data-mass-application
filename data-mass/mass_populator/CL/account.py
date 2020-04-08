from account import create_account_ms


def populate_accounts(country, environment):
    if "success" != create_account_ms("2323434554", "CL_POC_001", ["CASH"], None, country, environment):
        print("Fail on populate account 2323434554.")

    if "success" != create_account_ms("1020303040", "CL_POC_002", ["CASH"], None, country, environment):
        print("Fail on populate account 1020303040.")

    if "success" != create_account_ms("3325534210", "CL_POC_003", ["CASH"], None, country, environment):
        print("Fail on populate account 3325534210.")

    print("Accounts populating finalized.")