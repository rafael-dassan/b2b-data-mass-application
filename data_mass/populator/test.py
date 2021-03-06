import logging

from data_mass.common import block_print, save_environment_to_env, save_environment_zone_to_env
from data_mass.populator.country.account import populate_poc
from data_mass.populator.country.category import (
    associate_products_to_category_magento
)
from data_mass.populator.country.combo import (
    populate_combo_discount,
    populate_combo_free_good,
    populate_combo_only_free_good
)
from data_mass.populator.country.deal import (
    populate_discount,
    populate_free_good,
    populate_stepped_discount,
    populate_stepped_discount_with_limit,
    populate_stepped_free_good
)
from data_mass.populator.country.invoice import populate_invoice
from data_mass.populator.country.order import populate_order
from data_mass.populator.country.product import (
    enable_product_magento,
    populate_product
)
from data_mass.populator.country.recommendation import populate_recommendation
from data_mass.populator.country.rewards import (
    enroll_poc,
    populate_challenge,
    populate_challenge_mark_complete,
    populate_challenge_purchase_multiple,
    populate_challenge_purchase_single,
    populate_challenge_take_photo
)
from data_mass.populator.country.user_iam import populate_user_iam_b2c
from data_mass.populator.helpers.database_helper import (
    delete_from_database_by_account,
    get_database_params
)
from data_mass.populator.log import logging
from data_mass.populator.preconditions import (
    delete_deal,
    delete_invoice,
    delete_recommendation
)
from data_mass.validations import REWARDS_COUNTRIES

logger = logging.getLogger(__name__)
COUNTRIES = ['AR', 'BR', 'CA', 'CO', 'EC', 'MX', 'PA', 'PE', 'PY', 'SV', 'ZA', 'TZ']

def execute_test(country, environment):
    save_environment_to_env(environment)
    save_environment_zone_to_env(country)
    account_params = get_account_params(country)
    user_params = get_user_params(country)
    product_params = get_product_params()
    category_params = get_category_params()
    discount_params = get_deals_params(country, 'DISCOUNT')
    stepped_discount_params = get_deals_params(country, 'STEPPED_DISCOUNT')
    stepped_discount_limit_params = get_deals_params(country, 'STEPPED_DISCOUNT_LIMIT')
    free_good_params = get_deals_params(country, 'FREE_GOOD')
    stepped_free_good_params = get_deals_params(country, 'STEPPED_FREE_GOOD')
    order_params = get_order_params(country)
    invoice_params = get_invoice_params(country)
    algo_selling_params = get_algo_selling_params(country)
    order_database_params = get_database_params(country, environment, 'order-service-ms')
    combo_discount_params = get_combo_params(country, 'DISCOUNT')
    combo_free_good_params = get_combo_params(country, 'FREE_GOOD')
    rewards_params = get_rewards_params(country)

    # Overwrite standard output (stdout) - disable `print`
    block_print()

    # Run preconditions
    execute_preconditions(country, environment, account_params, order_database_params, invoice_params)

    # Start creating data mass
    logger.info("populate_products for %s/%s", country, environment)
    populate_product(country, environment, product_params.get('sku'), product_params.get('name'), product_params.get('brand_name'),
                     product_params.get('sub_brand_name'), product_params.get('package_id'), product_params.get('container_name'),
                     product_params.get('container_size'), product_params.get('container_returnable'),
                     product_params.get('container_unit_measurement'), product_params.get('sales_ranking'),
                     product_params.get('is_narcotic'), product_params.get('is_alcoholic'))
    
    logger.info("populate_accounts for %s/%s", country, environment)
    populate_poc(country, environment, account_params.get('id'), account_params.get('name'), account_params.get('payment_method'),
                 account_params.get('credit'), account_params.get('balance'), account_params.get('amount_of_products'),
                 account_params.get('has_delivery_window'), account_params.get('eligible_rewards'), [product_params.get('sku')])

    # if country.lower() == "sv":
    #     ...
    # else:
    #     logger.info("populate_users_iam_b2c for %s/%s", country, environment)
    #     populate_user_iam_b2c(country, environment, user_params.get('email'), user_params.get('password'), [account_params.get('id')])

    logger.info("populate_recommendations for %s/%s", country, environment)
    populate_recommendation(country, environment, algo_selling_params.get('account_id'), algo_selling_params.get('products'))

    logger.info("populate_deals for %s/%s", country, environment)
    populate_discount(country, environment, discount_params.get('account_id'), discount_params.get('deal_id'), discount_params.get('sku'),
                      discount_params.get('discount_value'), discount_params.get('min_quantity'), discount_params.get('priority'))

    populate_stepped_discount(country, environment, stepped_discount_params.get('account_id'), stepped_discount_params.get('deal_id'),
                              stepped_discount_params.get('sku'), stepped_discount_params.get('ranges'),
                              stepped_discount_params.get('priority'))

    populate_stepped_discount_with_limit(country, environment, stepped_discount_limit_params.get('account_id'),
                                         stepped_discount_limit_params.get('deal_id'), stepped_discount_limit_params.get('sku'),
                                         stepped_discount_limit_params.get('discount_value'),
                                         stepped_discount_limit_params.get('max_quantity'))

    populate_free_good(country, environment, free_good_params.get('account_id'), free_good_params.get('deal_id'),
                       free_good_params.get('sku'), free_good_params.get('proportion'), free_good_params.get('quantity'),
                       free_good_params.get('partial_free_good'), free_good_params.get('need_to_buy_product'))

    populate_stepped_free_good(country, environment, stepped_free_good_params.get('account_id'), stepped_free_good_params.get('deal_id'),
                               stepped_free_good_params.get('sku'), stepped_free_good_params.get('ranges'))

    logger.info("populate_combos for %s/%s", country, environment)
    populate_combo_discount(country, environment, combo_discount_params.get('account_id'), combo_discount_params.get('combo_id'),
                            combo_discount_params.get('sku'), combo_discount_params.get('discount_value'))

    populate_combo_free_good(country, environment, combo_free_good_params.get('account_id'), combo_free_good_params.get('combo_id'),
                             combo_free_good_params.get('sku'))

    populate_combo_only_free_good(country, environment, combo_free_good_params.get('account_id'), 'DMA-{0}-TEST-COFG'.format(country),
                                  combo_free_good_params.get('sku'))

    logger.info("populate_orders for %s/%s", country, environment)
    populate_order(country, environment, order_params.get('account_id'), order_params.get('allow_order_cancel'), order_params.get('items'),
                   order_params.get('quantity'), order_params.get('order_status'), order_params.get('prefix'))

    logger.info("populate_invoices for %s/%s", country, environment)
    populate_invoice(country, environment, invoice_params.get('account_id'), invoice_params.get('invoice_status'),
                     invoice_params.get('order_prefix'), invoice_params.get('invoice_prefix'))

    if country in REWARDS_COUNTRIES:
        logger.info("enroll_poc_rewards for %s/%s", country, environment)
        enroll_poc(country, environment, rewards_params.get('account_id'))

        logger.info("populate_rewards_challenges for %s/%s", country, environment)
        populate_challenge_take_photo(country, environment, rewards_params.get('take_photo_challenge_id'))
        populate_challenge_mark_complete(country, environment, rewards_params.get('mark_complete_challenge_id'))
        populate_challenge_purchase_single(country, environment, rewards_params.get('purchase_single_challenge_id'))
        populate_challenge_purchase_multiple(country, environment, rewards_params.get('purchase_multiple_challenge_id'))

    logger.info("enable_products_magento %s/%s", country, environment)
    enable_product_magento(country, environment, category_params.get('sku'))

    logger.info("associate products to categories %s/%s", country, environment)
    associate_products_to_category_magento(country, environment, category_params.get('name'), category_params.get('sku'))


def execute_preconditions(country, environment, account_params, order_database_params, invoice_params):
    # Run pre-conditions
    logger.info("Running pre-conditions for %s/%s", country, environment)
    logger.info("delete_recommendations for account %s", account_params.get('id'))
    delete_recommendation(account_params.get('id'), country, environment, ['QUICK_ORDER'])
    delete_recommendation(account_params.get('id'), country, environment, ['FORGOTTEN_ITEMS'])
    delete_recommendation(account_params.get('id'), country, environment, ['CROSS_SELL_UP_SELL'])

    logger.info("delete_orders for account %s", account_params.get('id'))
    delete_from_database_by_account(order_database_params.get('client'), order_database_params.get('db_name'),
                                order_database_params.get('collection_name'), order_database_params.get('prefix'))

    logger.info("delete_deals for account %s", account_params.get('id'))
    delete_deal(account_params.get('id'), country, environment)

    # logger.info("delete_invoices for account %s", invoice_params.get('account_id'))
    # delete_invoice(invoice_params.get('account_id'), country, environment)


def get_email_param(country):
    """
    Create and return an email for populator test with country param.

    Args:
        country (str): the country to be used in email

    Returns:
        str: email for populator test.
        bool: country not valid.
    """
    if country in COUNTRIES:
        return f"test-populator-{country.lower()}@mailinator.com"
    return False


def get_account_params(country):
    return {
        'id': '17629091762452',
        'name': f'TEST_POC_001_{country}',
        'payment_method': ['CASH'],
        'credit': '30000',
        'balance': '30000',
        'amount_of_products': 100,
        'has_delivery_window': True,
        'eligible_rewards': True
    }


def get_user_params(country):
    return {
        'email': get_email_param(country),
        'password': 'Password1'
    }


def get_product_params():
    return {
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
        'is_narcotic': False,
        'is_alcoholic': True
    }

def get_product_params_us():
    return {
        'sku': '102102',
        'name': 'TEST MASS POPULATOR',
        'brand_name': 'Test',
        'sub_brand_name': 'Test',
        'package_id': '0101TEST',
        'vendorItemId': '102102-C',
        'container_name': 'Bottle',
        'container_size': 1000,
        'container_returnable': False,
        'container_unit_measurement': 'ML',
        'sales_ranking': 1,
        'is_narcotic': False,
        'is_alcoholic': True
    }

def get_category_params():
    return {
        'name': 'Journey',
        'sku': '0101WEB'
    }


def get_deals_params(country, deal_type):
    params = {
        'DISCOUNT': {
            'account_id': get_account_params(country).get('id'),
            'deal_id': 'DMA-{country}-TEST-0102'.format(country=country),
            'sku': get_product_params().get('sku'),
            'discount_value': 15,
            'min_quantity': 1,
            'priority': 1
        },
        'STEPPED_DISCOUNT': {
            'account_id': get_account_params(country).get('id'),
            'deal_id': 'DMA-{country}-TEST-0103'.format(country=country),
            'sku': get_product_params().get('sku'),
            'ranges': ['1,10,10', '11,9999,15'],
            'priority': 1
        },
        'STEPPED_DISCOUNT_LIMIT': {
            'account_id': get_account_params(country).get('id'),
            'deal_id': 'DMA-{country}-TEST-0101'.format(country=country),
            'sku': get_product_params().get('sku'),
            'discount_value': 10,
            'max_quantity': 10
        },
        'FREE_GOOD': {
            'account_id': get_account_params(country).get('id'),
            'deal_id': 'DMA-{country}-TEST-0104'.format(country=country),
            'sku': get_product_params().get('sku'),
            'proportion': 10,
            'quantity': 1,
            'partial_free_good': 'N',
            'need_to_buy_product': 'Y'
        },
        'STEPPED_FREE_GOOD': {
            'account_id': get_account_params(country).get('id'),
            'deal_id': 'DMA-{country}-TEST-0105'.format(country=country),
            'sku': get_product_params().get('sku'),
            'ranges': ['1,10,1,2', '11,9999,2,2']
        }
    }
    return params[deal_type]


def get_order_params(country):
    return {
        'account_id': get_account_params(country).get('id'),
        'allow_order_cancel': 'Y',
        'items': get_product_params().get('sku'),
        'quantity': 5,
        'order_status': 'PLACED',
        'prefix': 'DMA-TEST-{0}-'.format(country)
    }


def get_invoice_params(country):
    return {
        'account_id': get_account_params(country).get('id'),
        'invoice_status': 'CLOSED',
        'order_prefix': 'DMA-TEST',
        'invoice_prefix': 'DMA-TEST'
    }


def get_algo_selling_params(country):
    return {
        'account_id': get_account_params(country).get('id'),
        'products': ['0101TEST']
    }


def get_combo_params(country, combo_type):
    params = {
        'DISCOUNT': {
            'account_id': get_account_params(country).get('id'),
            'combo_id': 'DMA-{0}-TEST-CD'.format(country),
            'sku': get_product_params().get('sku'),
            'discount_value': 10
        },
        'FREE_GOOD': {
            'account_id': get_account_params(country).get('id'),
            'combo_id': 'DMA-{0}-TEST-CFG'.format(country),
            'sku': get_product_params().get('sku')
        }
    }
    return params[combo_type]


def get_rewards_params(country):
    return {
        'account_id': get_account_params(country).get('id'),
        'take_photo_challenge_id': 'DMA-{0}-01-TEST'.format(country),
        'mark_complete_challenge_id': 'DMA-{0}-02-TEST'.format(country),
        'purchase_single_challenge_id': 'DMA-{0}-03-TEST'.format(country),
        'purchase_multiple_challenge_id': 'DMA-{0}-04-TEST'.format(country),
    }
