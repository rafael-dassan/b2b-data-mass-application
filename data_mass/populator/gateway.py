from data_mass.common import block_print, save_environment_to_env, save_environment_zone_to_env
from data_mass.populator.data_creation_engine import (
    categorize_and_enable_products_magento,
    populate_accounts,
)
from data_mass.populator.helpers.csv_helper import search_data_by
from data_mass.populator.preconditions import run_preconditions


def execute_gateway(country, environment):
    save_environment_to_env(environment)
    save_environment_zone_to_env(country)
    block_print()
    run_preconditions(search_data_by(country, 'account'), country, environment)
    populate_accounts(country, environment)
    # if country.lower() == 'sv':
    #     ...
    # else:
    #     populate_users_magento(country, environment)
    categorize_and_enable_products_magento(country, environment)
    return True
