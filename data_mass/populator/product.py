from data_mass.populator.log import *
from data_mass.populator.country.product import populate_products as populate_products_base
from data_mass.populator.helpers.csv_helper import search_data_by

logger = logging.getLogger(__name__)


def execute_product(country, environment):
    populate_products(country, environment)
    return True


def populate_products(country, environment):
    logger.info("populate_products for %s/%s", country, environment)
    populate_products_base(country, environment, search_data_by(country, 'product'))
