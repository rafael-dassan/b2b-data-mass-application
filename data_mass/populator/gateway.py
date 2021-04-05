from data_mass.common import block_print
from data_mass.populator.data_creation_engine import populate_accounts, \
    populate_users_magento, categorize_and_enable_products_magento
from data_mass.populator.helpers.csv_helper import search_data_by
from data_mass.populator.preconditions import run_preconditions


def execute_gateway(country, environment):
    block_print()
    run_preconditions(search_data_by(country, 'account'), country, environment)
    populate_accounts(country, environment)
    populate_users_magento(country, environment)
    categorize_and_enable_products_magento(country, environment)
    return True
