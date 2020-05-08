from account import create_account_ms
from account import create_account
from account import check_account_exists_microservice
from delivery_window import create_delivery_window_microservice
from delivery_window import create_delivery_window_middleware
from credit import add_credit_to_account, add_credit_to_account_microservice
from products import request_get_products_by_account_microservice
from products import request_get_products_microservice
from products import generate_random_price_ids
from products import slice_array_products
from products import request_post_products_account_microservice
from common import validate_state
from mass_populator.log import *

logger = logging.getLogger(__name__)


def populate_accounts(country, environment):
    populate_poc1(country, environment)
    populate_poc2(country, environment)
    populate_poc3(country, environment)

    logger.info("Accounts populating finalized.")


# Populate an account
def populate_account(country, environment, account_id, account_name):
    state = validate_state(country)
    if "success" != create_account_ms(account_id, account_name, ["CASH"], None, country, environment, state):
        logger.info(log(Message.ACCOUNT_ERROR, {"account_id": account_id}))

    if "success" != create_account(account_id, account_name, country, ["CASH"], environment, None, state):
        logger.info(log(Message.ACCOUNT_ERROR_MIDDLEWARE, {"account_id": account_id}))


# Populate the delivery window for an account
def populate_delivery_window(country, environment, account_id):
    account_data = {
        "deliveryScheduleId": account_id,
        "accountId": account_id
    }
    if "success" != create_delivery_window_microservice(account_id, country, environment, account_data, "false"):
        logger.info(log(Message.DELIVERY_WINDOW_ERROR, {"account_id": account_id}))

    if "success" != create_delivery_window_middleware(account_id, country, environment):
        logger.info(log(Message.DELIVERY_WINDOW_ERROR_MIDDLEWARE, {"account_id": account_id}))


# Include credit on ZA Account
def populate_credit(account_id, country, environment, credit, balance):
    if "success" != add_credit_to_account_microservice(account_id, country, environment, credit, balance):
        logger.info(log(Message.CREDIT_ERROR, {"account_id": account_id}))

    if "success" != add_credit_to_account(account_id, country, environment, credit, balance):
        logger.info(log(Message.CREDIT_ERROR_MIDDLEWARE, {"account_id": account_id}))


# Populate the products for an account
def populate_product(account_id, country, environment, amount_of_products):
    account_data = {
        "deliveryCenterId": account_id,
        "accountId": account_id
    }
    if "success" != add_product_to_account(account_data, country, environment, amount_of_products):
        logger.info(log(Message.PRODUCT_ERROR, {"account_id": account_id}))


def add_product_to_account(account, country, environment, amount_of_products):
    """Associate products by account
    Arguments:
        - account: Object account
        - country: (e.g, BR,ZA,DO)
        - environment: (e.g, UAT,SIT)
        - amount_of_products: quantity
    Return new json_object
    """
    # Get all products
    all_products = request_get_products_microservice(country, environment)
    logger.debug("Products available to populate: {products} items".format(products=str(len(all_products))))
    
    amount_of_products = min(len(all_products), amount_of_products)
    logger.debug("Amount of products should be filled on account: {amount_of_products} items".format(amount_of_products=amount_of_products))

    # Get products by account
    products_by_account = request_get_products_by_account_microservice(account['accountId'], country, environment)
    logger.info("Products found on account {account_id}: {products} items".format(account_id=account['accountId'], products=str(len(products_by_account))))
    if not isinstance(products_by_account, list):
        return 'failed'
    
    remaining_products = amount_of_products - len(products_by_account)
    logger.debug("Remaining products should be filled on account: {remaining_products} items".format(remaining_products=remaining_products))
        
    if remaining_products > 0:
        products_data = list(zip(generate_random_price_ids(remaining_products), slice_array_products(remaining_products, all_products)))
        logger.debug("Total products to populate: {remaining_products} items".format(remaining_products=str(remaining_products)))
            
        # Insert products in account
        return request_post_products_account_microservice(account['accountId'], country, environment, account['deliveryCenterId'], products_data)
    else:
        logger.debug("Account already has the desired amount of products, not needed to populate!")
        return 'success'


# Populate the POC 1
def populate_poc1(country, environment):
    account_id = "9883300101"
    credit = "45000"
    balance = "45000"
    amount_of_products = 100
    populate_account(country, environment, account_id, "ZA_POC_001")
    populate_delivery_window(country, environment, account_id)
    populate_credit(account_id, country, environment, credit, balance)
    populate_product(account_id, country, environment, amount_of_products)


# Populate the POC 2
def populate_poc2(country, environment):
    account_id = "9883300102"
    credit = "45000"
    balance = "45000"
    amount_of_products = 100
    populate_account(country, environment, account_id, "ZA_POC_002")
    populate_delivery_window(country, environment, account_id)
    populate_credit(account_id, country, environment, credit, balance)
    populate_product(account_id, country, environment, amount_of_products)


# Populate the POC 3
def populate_poc3(country, environment):
    account_id = "9883300103"
    credit = "45000"
    balance = "45000"
    amount_of_products = 100
    populate_account(country, environment, account_id, "ZA_POC_003")
    populate_credit(account_id, country, environment, credit, balance)
    populate_product(account_id, country, environment, amount_of_products)
