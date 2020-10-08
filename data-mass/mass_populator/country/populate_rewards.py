from rewards import *

def desenroll_pocs(country, environment, dataframe_products):
    if dataframe_products is not None:
        dataframe_products.apply(exec_denseroll_poc, 
        args=(country, environment), axis=1)

def exec_denseroll_poc(row, country, environment):
    account_id = str(row['account_id_unroll'])
    delete_enroll_poc_to_program(account_id, country, environment)