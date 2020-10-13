from common import block_print
from mass_populator.csv_helper import search_data_by
from mass_populator.log import *
from mass_populator.country.populate_account import populate_pocs
from mass_populator.country.populate_user import populate_users
from mass_populator.country.populate_recomendation import populate_recommendations as populate_recommendations_base
from mass_populator.country.populate_category import associate_products_to_category_magento_base
from mass_populator.country.populate_product import enable_products_magento as enable_products_magento_base
from mass_populator.country.populate_user_v3 import populate_users_iam_b2c
from mass_populator.preconditions import run_preconditions

logger = logging.getLogger(__name__)


def execute_common(country, environment):
    block_print()
    run_preconditions(search_data_by(country, 'account'), country, environment)
    populate_accounts(country, environment)
    populate_users_magento(country, environment)
    populate_recommendations(country, environment)
    categorize_and_enable_products_magento(country, environment)
    return True


def populate_accounts(country, environment):
    logger.info("populate_accounts for %s/%s", country, environment)
    populate_pocs(country, environment, search_data_by(country, 'account'))


def populate_users_magento(country, environment):    
    logger.info("populate_users_magento for %s/%s", country, environment)

    # Colombia, Mexico, Brazil, Ecuador, Peru and Dominican Republic use the registration v3 (IAM B2C)
    # The other countries are still using registration v2
    iam_allowed_countries = ['CO', 'MX', 'BR', 'EC', 'PE', 'DO']
    if country in iam_allowed_countries:
        populate_users_iam_b2c(country, environment, search_data_by(country, 'user'))
    else:
        populate_users(country, environment, search_data_by(country, 'user'))


def populate_recommendations(country, environment):
    logger.info("populate_recommendations for %s/%s", country, environment)
    
    not_allowed_countries = ["CL"]
    if country in not_allowed_countries:
        logger.info(
            "Skipping populate recommendations, because the country is not supported!")
        return False
    
    populate_recommendations_base(country, environment, search_data_by(country, 'recommendation'))


def categorize_and_enable_products_magento(country, environment):
    logger.info("categorize_and_enable_products_magento for %s/%s", country, environment)
    enable_products_magento(country, environment)
    associate_products_to_categories(country, environment)


def enable_products_magento(country, environment):
    logger.info("enable_products_magento %s/%s", country, environment)
    
    not_allowed_countries = ["CL"]
    if (country in not_allowed_countries):
        logger.info(
            "Skipping products activation in Magento, because the country is not supported!")
        return False
    
    enable_products_magento_base(country, environment, search_data_by(country, 'category'))


def associate_products_to_categories(country, environment):
    logger.info("associate products to categories %s/%s", country, environment)

    not_allowed_countries = ["CL"]
    if (country in not_allowed_countries):
        logger.info(
            "Skipping products association to categories, because the country is not supported!")
        return False
    
    associate_products_to_category_magento_base(country, environment, search_data_by(country, 'category'))