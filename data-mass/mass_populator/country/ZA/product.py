from mass_populator.log import *
from mass_populator.country.populate_product import *

logger = logging.getLogger(__name__)

def populate_products(country, environment):
    populate_product(country, environment, '0101WEB', 'QMJourney01', 'Journey', 'Journey', '0101WEB', 'Bottle', '1000', True, 'ML', 1)
    populate_product(country, environment, '0101ANDROID', 'QMJourney01', 'Journey', 'Journey', '0101ANDROID', 'Bottle', '1000', True, 'ML', 1)
    populate_product(country, environment, '0101IOS', 'QMJourney01', 'Journey', 'Journey', '0101IOS', 'Bottle', '1000', True, 'ML', 1)
    populate_product(country, environment, '0102WEB', 'QMJourney02', 'Journey', 'Journey', '0102WEB', 'Bottle', '1000', True, 'ML', 2)
    populate_product(country, environment, '0102ANDROID', 'QMJourney02', 'Journey', 'Journey', '0102ANDROID', 'Bottle', '1000', True, 'ML', 2)
    populate_product(country, environment, '0102IOS', 'QMJourney02', 'Journey', 'Journey', '0102IOS', 'Bottle', '1000', True, 'ML', 2)

    logger.info('Products populating finalized.')