from mass_populator.country.populate_product import *

logger = logging.getLogger(__name__)


def populate_products(country, environment):
    populate_product(country, environment, '0101WEB', 'QMWEB01', 'Journey', 'Journey', '0101WEB', 'Botella', '1000', False, 'ML', 1)
    populate_product(country, environment, '0101ANDROID', 'QMANDROID01', 'Journey', 'Journey', '0101ANDROID', 'Botella', '1000', False, 'ML', 1)
    populate_product(country, environment, '0101IOS', 'QMIOS01', 'Journey', 'Journey', '0101IOS', 'Botella', '1000', False, 'ML', 1)
    populate_product(country, environment, '0102WEB', 'QMWEB02', 'Journey', 'Journey', '0102WEB', 'Botella', '1000', False, 'ML', 2)
    populate_product(country, environment, '0102ANDROID', 'QMANDROID02', 'Journey', 'Journey', '0102ANDROID', 'Botella', '1000', False, 'ML', 2)
    populate_product(country, environment, '0102IOS', 'QMIOS02', 'Journey', 'Journey', '0102IOS', 'Botella', '1000', False, 'ML', 2)

    logger.info('Products populating finalized.')


def enable_products_magento(country, environment):
    enable_product_magento(country, environment, '0101WEB')
    enable_product_magento(country, environment, '0101ANDROID')
    enable_product_magento(country, environment, '0101IOS')
    enable_product_magento(country, environment, '0102WEB')
    enable_product_magento(country, environment, '0102ANDROID')
    enable_product_magento(country, environment, '0102IOS')
