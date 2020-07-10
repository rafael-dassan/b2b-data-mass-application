from mass_populator.log import *
from mass_populator.country.populate_category import associate_products_to_category_magento

logger = logging.getLogger(__name__)


def associate_product_to_category(country, environment):
    products = ['0101WEB', '0102WEB', '0101ANDROID', '0102ANDROID', '0101IOS', '0102IOS']
    associate_products_to_category_magento(country, environment, products)
    
    logger.info('Associate categories to products finalized.')