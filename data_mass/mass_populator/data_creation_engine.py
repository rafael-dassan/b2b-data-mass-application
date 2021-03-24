from ..mass_populator.country.account import populate_pocs
from ..mass_populator.country.combo import populate_combo_discount_base, populate_combo_free_good_base, populate_combo_only_free_good_base
from ..mass_populator.country.deal import populate_discount_base, populate_stepped_discount_base, \
    populate_stepped_discount_with_limit_base, populate_free_good_base, populate_stepped_free_good_base
from ..mass_populator.country.invoice import populate_invoices_base
from ..mass_populator.country.order import populate_orders_base
from ..mass_populator.country.user_iam import populate_users_iam_b2c
from ..mass_populator.country.recommendation import populate_recommendations as populate_recommendations_base
from ..mass_populator.country.category import associate_products_to_category_magento_base
from ..mass_populator.country.product import enable_products_magento as enable_products_magento_base
from ..mass_populator.helpers.csv_helper import search_data_by
from ..mass_populator.log import *


logger = logging.getLogger(__name__)


def populate_accounts(country, environment):
    logger.info("populate_accounts for %s/%s", country, environment)
    populate_pocs(country, environment, search_data_by(country, 'account'))


def populate_users_magento(country, environment):
    logger.info("populate_users_iam_b2c for %s/%s", country, environment)
    populate_users_iam_b2c(country, environment, search_data_by(country, 'user'))


def populate_recommendations(country, environment):
    logger.info("populate_recommendations for %s/%s", country, environment)
    populate_recommendations_base(country, environment, search_data_by(country, 'recommendation'))


def populate_deals(country, environment):
    logger.info("populate_deals for %s/%s", country, environment)
    populate_discount_base(country, environment, search_data_by(country, 'discount'))
    populate_stepped_discount_base(country, environment, search_data_by(country, 'stepped_discount'))
    populate_stepped_discount_with_limit_base(country, environment, search_data_by(country, 'discount_with_limit'))
    populate_free_good_base(country, environment, search_data_by(country, 'free_good'))
    populate_stepped_free_good_base(country, environment, search_data_by(country, 'stepped_free_good'))


def populate_combos(country, environment):
    logger.info("populate_combos for %s/%s", country, environment)
    populate_combo_discount_base(country, environment, search_data_by(country, 'combo_discount'))
    populate_combo_free_good_base(country, environment, search_data_by(country, 'combo_free_good'))
    populate_combo_only_free_good_base(country, environment, search_data_by(country, 'combo_only_free_good'))


def populate_orders(country, environment):
    logger.info("populate_orders for %s/%s", country, environment)
    populate_orders_base(country, environment, search_data_by(country, 'order'))


def populate_invoices(country, environment):
    logger.info("populate_invoices for %s/%s", country, environment)
    populate_invoices_base(country, environment, search_data_by(country, 'invoice'))


def categorize_and_enable_products_magento(country, environment):
    logger.info("categorize_and_enable_products_magento for %s/%s", country, environment)
    enable_products_magento(country, environment)
    associate_products_to_categories(country, environment)


def enable_products_magento(country, environment):
    logger.info("enable_products_magento %s/%s", country, environment)
    enable_products_magento_base(country, environment, search_data_by(country, 'category'))


def associate_products_to_categories(country, environment):
    logger.info("associate products to categories %s/%s", country, environment)
    associate_products_to_category_magento_base(country, environment, search_data_by(country, 'category'))
