from mass_populator.data_creation_engine import populate_deals, populate_orders, populate_invoices, populate_recommendations, \
    populate_combos
from mass_populator.gateway import execute_gateway


def execute_regression(country, environment):
    execute_gateway(country, environment)
    populate_recommendations(country, environment)
    populate_deals(country, environment)
    populate_combos(country, environment)
    populate_orders(country, environment)
    populate_invoices(country, environment)
    return True
