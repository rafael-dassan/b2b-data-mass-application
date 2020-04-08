from account import create_account_ms


def populate_accounts(country, environment):

    if "success" != create_account_ms("5444385012", "AR_POC_001", ["CASH"], None, country, environment):
        print("Fail on populate account 5444385012.")

    if "success" != create_account_ms("9932094352", "AR_POC_002", ["CASH"], None, country, environment):
        print("Fail on populate account 9932094352.")

    if "success" != create_account_ms("1669325565", "AR_POC_003", ["CASH"], None, country, environment):
        print("Fail on populate account 1669325565.")

    print("Accounts populating finalized.")