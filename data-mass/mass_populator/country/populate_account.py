from account import create_account_ms
from delivery_window import create_delivery_window_microservice
from credit import add_credit_to_account_microservice
from products import request_get_products_by_account_microservice
from products import request_get_products_microservice
from products import generate_random_price_ids
from products import slice_array_products
from products import request_post_products_account_microservice
from common import validate_state
from mass_populator.log import *

logger = logging.getLogger(__name__)


# Populate the POC
def populate_poc(country, environment, 
        account_id, 
        account_name, 
        payment_method, 
        credit, 
        balance, 
        amount_of_products,
        has_delivery_window, 
        products=None):
    
    populate_account(country, environment, account_id,account_name, payment_method)
    if has_delivery_window:
        populate_delivery_window(country, environment, account_id)
    populate_credit(country, environment, account_id, credit, balance)
    populate_product(account_id, country, environment, amount_of_products)
    if products:
        associate_products_to_account(country, environment, account_id, products)


# Populate an account
def populate_account(country, environment, account_id, account_name, payment_method):
    state = validate_state(country)
    if "success" != create_account_ms(account_id, account_name, payment_method, None, country, environment, state):
        logger.error(log(Message.ACCOUNT_ERROR, {"account_id": account_id}))


# Populate the delivery window for an account
def populate_delivery_window(country, environment, account_id):
    account_data = {
        "deliveryScheduleId": account_id,
        "accountId": account_id
    }
    if "success" != create_delivery_window_microservice(account_id, country, environment, account_data, "false"):
        logger.error(log(Message.DELIVERY_WINDOW_ERROR,
                         {"account_id": account_id}))


# Populate the credit for an account
def populate_credit(country, environment, account_id, credit, balance):
    if "success" != add_credit_to_account_microservice(account_id, country, environment, credit, balance):
        logger.error(log(Message.CREDIT_ERROR, {"account_id": account_id}))


# Populate the products for an account
def populate_product(account_id, country, environment, amount_of_products):
    account_data = {
        "deliveryCenterId": account_id,
        "accountId": account_id
    }
    if "success" != add_products_to_account(account_data, country, environment, amount_of_products):
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
    logger.debug("Products available to populate: {products} items".format(
        products=str(len(all_products))))

    amount_of_products = min(len(all_products), amount_of_products)
    logger.debug("Amount of products should be filled on account: {amount_of_products} items".format(
        amount_of_products=amount_of_products))

    # Get products by account
    products_by_account = request_get_products_by_account_microservice(
        account['accountId'], country, environment)
    logger.debug("Products found on account {account_id}: {products} items".format(account_id=account['accountId'],
                                                                                   products=str(len(products_by_account))))
    if not isinstance(products_by_account, list):
        return 'failed'

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
        return 'success'


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
    products_data = list(zip(generate_random_price_ids(products_length), [{'sku': products[i]} for i in range(products_length)]))

    if "success" != request_post_products_account_microservice(account['accountId'], country, environment, account['deliveryCenterId'], products_data):
        logger.error(log(Message.PRODUCT_ERROR, {"account_id": account_id}))