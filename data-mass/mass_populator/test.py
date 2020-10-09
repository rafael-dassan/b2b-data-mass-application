from common import block_print
from mass_populator.country.populate_category import associate_products_to_category_magento
from mass_populator.country.populate_product import enable_product_magento, populate_product
from mass_populator.country.populate_user_v3 import populate_user_iam_b2c
from mass_populator.log import *
from mass_populator.country.populate_account import populate_poc
from mass_populator.country.populate_recomendation import populate_recommendation
from mass_populator.country.populate_user import populate_user
from mass_populator.preconditions import delete_recommendation, delete_available_deals

logger = logging.getLogger(__name__)


def execute_test(country, environment):
    iam_b2c_countries = ['BR', 'CO', 'DO', 'EC', 'MX', 'PE']
    account_params = get_account_params(country)
    user_params = get_user_params(country)
    product_params = get_product_params()
    category_params = get_category_params()

    # Overwrite standard output (stdout) - disable `print`
    block_print()

    # Run pre-conditions
    logger.info("Running pre-conditions for %s/%s", country, environment)
    delete_recommendation(account_params.get('id'), country, environment, 'QUICK_ORDER')
    delete_recommendation(account_params.get('id'), country, environment, 'FORGOTTEN_ITEMS')
    delete_recommendation(account_params.get('id'), country, environment, 'CROSS_SELL_UP_SELL')
    delete_available_deals(account_params.get('id'), country, environment)

    # Start creating data mass
    logger.info("populate_products for %s/%s", country, environment)
    populate_product(country, environment, product_params.get('sku'),
                     product_params.get('name'), product_params.get('brand_name'), product_params.get('sub_brand_name'),
                     product_params.get('package_id'), product_params.get('container_name'),
                     product_params.get('container_size'), product_params.get('container_returnable'),
                     product_params.get('container_unit_measurement'), product_params.get('sales_ranking'))

    logger.info("populate_accounts for %s/%s", country, environment)
    populate_poc(country, environment, account_params.get('id'), account_params.get('name'),
                 account_params.get('payment_method'), account_params.get('credit'), account_params.get('balance'),
                 account_params.get('amount_of_products'), account_params.get('has_delivery_window'),
                 [product_params.get('sku')])

    if country in iam_b2c_countries:
        logger.info("populate_users_iam_b2c for %s/%s", country, environment)
        populate_user_iam_b2c(country, environment, user_params.get('email'), user_params.get('password'),
                              [account_params.get('id')])
    else:
        logger.info("populate_users_magento for %s/%s", country, environment)
        populate_user(country, environment, user_params.get('email'), user_params.get('password'),
                      [account_params.get('id')], None)

    logger.info("populate_recommendations for %s/%s", country, environment)
    populate_recommendation(country, environment, account_params.get('id'))

    logger.info("enable_products_magento %s/%s", country, environment)
    enable_product_magento(country, environment, category_params.get('sku'))

    logger.info("associate products to categories %s/%s", country, environment)
    associate_products_to_category_magento(country, environment, category_params.get('name'),
                                           category_params.get('sku'))


def get_email_param(country):
    switcher = {
        'AR': 'test-populator-ar@mailinator.com',
        'BR': 'test-populator-br@mailinator.com',
        'CL': 'test-populator-cl@mailinator.com',
        'CO': 'test-populator-co@mailinator.com',
        'DO': 'test-populator-do@mailinator.com',
        'EC': 'test-populator-ec@mailinator.com',
        'MX': 'test-populator-mx@mailinator.com',
        'PE': 'test-populator-pe@mailinator.com',
        'ZA': 'test-populator-za@mailinator.com'
    }

    return switcher.get(country, False)


def get_account_params(country):
    params = {
        'id': '17629091762452',
        'name': 'TEST_POC_001_{country}'.format(country=country),
        'payment_method': ['CASH'],
        'credit': '30000',
        'balance': '30000',
        'amount_of_products': 100,
        'has_delivery_window': True
    }

    return params


def get_user_params(country):
    params = {
        'email': get_email_param(country),
        'password': 'Password1'
    }

    return params


def get_product_params():
    params = {
        'sku': '0101TEST',
        'name': 'TEST MASS POPULATOR',
        'brand_name': 'Test',
        'sub_brand_name': 'Test',
        'package_id': '0101TEST',
        'container_name': 'Bottle',
        'container_size': 1000,
        'container_returnable': False,
        'container_unit_measurement': 'ML',
        'sales_ranking': 1,
    }

    return params


def get_category_params():
    params = {
        'name': 'Journey',
        'sku': '0101WEB'
    }

    return params
