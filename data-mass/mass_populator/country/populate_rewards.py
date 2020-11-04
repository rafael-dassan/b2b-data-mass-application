from rewards import *


def unenroll_pocs(country, environment, dataframe_products):
    if dataframe_products is not None:
        dataframe_products.apply(exec_unenroll_poc, 
        args=(country, environment), axis=1)


def exec_unenroll_poc(row, country, environment):
    account_id = str(row['account_id_unenroll'])
    delete_enroll_poc_to_program(account_id, country, environment)
