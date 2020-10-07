def desenroll_pocs(country, environment, dataframe_products):
    if dataframe_products is not None:
        dataframe_products.apply(exec_denseroll_account, 
        args=(country, environment), axis=1)


def exec_denseroll_account(row, country, environment):
    print(row['account_id_unroll'])