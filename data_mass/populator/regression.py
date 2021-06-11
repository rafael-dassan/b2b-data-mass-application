from data_mass.populator.data_creation_engine import (
    populate_challenges,
    populate_combos,
    populate_deals,
    populate_deals_us,
    populate_invoices,
    populate_orders,
    populate_recommendations
)
from data_mass.populator.gateway import execute_gateway


def execute_regression(country, environment):
    execute_gateway(country, environment)
    populate_recommendations(country, environment)
    populate_deals(country, environment)
    populate_combos(country, environment)
    populate_orders(country, environment)
    populate_invoices(country, environment)
    populate_challenges(country, environment)
    return True


def execute_regression_us(country, environment):
    execute_gateway(country, environment)
    populate_recommendations(country, environment)
    populate_deals_us(country, environment)
    populate_combos(country, environment)
    populate_orders(country, environment)
    populate_invoices(country, environment)
    populate_challenges(country, environment)
    return True
