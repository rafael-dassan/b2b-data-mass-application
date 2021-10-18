from data_mass.account.accounts import (
    create_account_ms,
    get_account_delivery_address
)
from data_mass.account.credit import add_credit_to_account_microservice
from data_mass.account.delivery_window import (
    create_delivery_window_microservice
)
from data_mass.populator.country.inventory import populate_default_inventory
from data_mass.populator.country.product import (
    check_product_associated_to_account
)
from data_mass.populator.log import *
from data_mass.product.relay import request_post_products_account_microservice
from data_mass.product.service import (
    request_get_products_by_account_microservice,
    request_get_products_microservice
)
from data_mass.product.utils import (
    generate_random_price_ids,
    slice_array_products
)

logger = logging.getLogger(__name__)


# Populate the POCS
def populate_pocs(country, environment, dataframe_accounts):
    if dataframe_accounts is not None:
        dataframe_accounts.apply(apply_populate_poc, args=(country, environment), axis=1)


def apply_populate_poc(row, country, environment):
    populate_poc(
        country,
        environment,
        row['account_id'],
        row['account_name'],
        row['payment_method'],
        row['credit'],
        row['balance'],
        row['amount_of_products'],
        row['has_delivery_window'],
        row['eligible_rewards'],
        row['products'])


# Populate the POC
def populate_poc(country, environment, account_id, account_name, payment_method, credit, balance, amount_of_products,
                 has_delivery_window, eligible_rewards, products=None, option='1'):
    
    populate_account(country, environment, account_id, account_name, payment_method, eligible_rewards)
    if has_delivery_window:
        populate_delivery_window(country, environment, account_id, option)
    populate_credit(country, environment, account_id, credit, balance)
    populate_product(account_id, country, environment, amount_of_products)
    if products:
        not_associated_products = check_product_associated_to_account(account_id, country, environment, products)
        if not_associated_products:
            products_length = len(not_associated_products)
            for i in range(len(not_associated_products)):
                if products_length <= 1:
                    associate_products_to_account(country, environment, account_id, not_associated_products)
                else:
                    associate_products_to_account(country, environment, account_id, [not_associated_products[i]])


# Populate an account
def populate_account(country, environment, account_id, account_name, payment_method, eligible_rewards):
    delivery_address = get_account_delivery_address(country)
    if not create_account_ms(
        account_id=account_id,
        name=account_name,
        payment_method=payment_method,
        minimum_order=None,
        zone=country,
        environment=environment,
        delivery_address=delivery_address,
        account_status='ACTIVE',
        enable_empties_loan=False,
        eligible_rewards=eligible_rewards
    ):
        logger.error(log(Message.ACCOUNT_ERROR, {"account_id": account_id}))


# Populate the delivery window for an account
def populate_delivery_window(country, environment, account_id, option):
    account_data = {
        "deliveryScheduleId": account_id,
        "accountId": account_id
    }
    if not create_delivery_window_microservice(country, environment, account_data, False, option):
        logger.error(log(Message.DELIVERY_WINDOW_ERROR,
                         {"account_id": account_id}))


# Populate the credit for an account
def populate_credit(country, environment, account_id, credit, balance):
    if not add_credit_to_account_microservice(account_id, country, environment, credit, balance):
        logger.error(log(Message.CREDIT_ERROR, {"account_id": account_id}))


# Populate the products for an account
def populate_product(account_id, country, environment, amount_of_products):
    account_data = {
        "deliveryCenterId": account_id,
        "accountId": account_id
    }
    if not add_products_to_account(account_data, country, environment, amount_of_products):
        logger.error(log(Message.PRODUCT_ERROR, {"account_id": account_id}))


# Populate the products for an account
def add_products_to_account(account, country, environment, amount_of_products):
    """Add products to account
    Arguments:
        - account: Object account
        - country: (e.g, BR,ZA,DO)
        - environment: (e.g, UAT,SIT)
        - amount_of_products: quantity
    Return new json_object
    """
    # Get all products
    all_products = request_get_products_microservice(
        country, environment, amount_of_products)
    if not all_products:
        all_products = []
    logger.debug("Products available to populate: {products} items".format(
        products=str(len(all_products))))

    amount_of_products = min(len(all_products), amount_of_products)
    logger.debug("Amount of products should be filled on account: {amount_of_products} items".format(
        amount_of_products=amount_of_products))

    # Get products by account
    products_by_account = request_get_products_by_account_microservice(
        account['accountId'], country, environment)
    if not products_by_account:
        logger.debug("Products not found on account {account_id}".format(account_id=account['accountId']))
        products_by_account = []
    logger.debug("Products found on account {account_id}: {products} items".format(account_id=account['accountId'],
                                                                                   products=str(len(products_by_account))))

    remaining_products = amount_of_products - len(products_by_account)
    logger.debug("Remaining products should be filled on account: {remaining_products} items".format(
        remaining_products=remaining_products))

    if remaining_products > 0:
        products_data = list(
            zip(generate_random_price_ids(remaining_products), slice_array_products(remaining_products, all_products)))
        logger.debug(
            "Total products to populate: {remaining_products} items".format(remaining_products=str(remaining_products)))

        # Insert products in account
        return request_post_products_account_microservice(account['accountId'], country, environment,
                                                          account['deliveryCenterId'], products_data)
    else:
        logger.debug(
            "Account already has the desired amount of products, not needed to populate!")
        return True


# Populate association products for an account
def associate_products_to_account(country, environment, account_id, products):
    """Associate products to account
    Arguments:
        - country: (e.g, BR,ZA,DO)
        - environment: (e.g, UAT,SIT)
        - account_id: account id
        - products: products to associate to account
    """
    account = {
        "deliveryCenterId": account_id,
        "accountId": account_id
    }

    products_length = len(products)
    products_data = list(zip(generate_random_price_ids(products_length), [{'sku': products[i]} for i in
                                                                          range(products_length)]))

    if not request_post_products_account_microservice(account['accountId'], country, environment,
                                                               account['deliveryCenterId'], products_data):
        logger.error(log(Message.PRODUCT_ERROR, {"account_id": account_id}))

    # Populate the default inventory for all countries
    populate_default_inventory(account_id, country, environment, account['deliveryCenterId'])
