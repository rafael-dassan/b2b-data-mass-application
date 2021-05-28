from datetime import datetime, timedelta

from data_mass.accounts import check_account_exists_microservice
from data_mass.orders import request_order_creation
from data_mass.populator.country.product import (
    check_product_associated_to_account
    )
from data_mass.populator.log import *
from data_mass.product.products import request_get_offers_microservice
from data_mass.simulation import request_order_simulation

logger = logging.getLogger(__name__)


def populate_orders_base(country, environment, dataframe_orders):
    if dataframe_orders is not None:
        dataframe_orders.apply(apply_populate_order, args=(country, environment), axis=1)


def apply_populate_order(row, country, environment):
    populate_order(country, environment, str(row['account_id']), row['allow_order_cancel'], row['items'],
                   row['quantity'], row['order_status'], row['prefix'])


def populate_order(country, environment, account_id, allow_order_cancel, items, quantity, order_status, prefix):
    """
    Create an order through the Order Service
    
    Parameters
    ----------
    country : str
        e.g., AR, BR, DO, etc
    environment : str
        e.g., DEV, SIT, UAT
    account_id : int
        POC unique identifier
    allow_order_cancel : str
        `Y` or `N`
    items : list
        order items
    order_status : str 
        e.g., PLACED, CANCELLED, etc
    order_items : list
        list of SKUs
    prefix : list
        order prefix
    """
    account = check_account_exists_microservice(account_id, country, environment)
    if not account:
        logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
    else:
        delivery_center_id = account[0]['deliveryCenterId']

        not_associated_products = check_product_associated_to_account(account_id, country, environment, [items])
        if not_associated_products:
            product_offers = request_get_offers_microservice(account_id, country, environment)
            if product_offers:
                data = {'sku': items, 'itemQuantity': quantity}

                tomorrow = datetime.today() + timedelta(1)
                delivery_date = str(datetime.date(tomorrow))

                order_items = request_order_simulation(country, environment, account_id, delivery_center_id, [data],
                                                        None, None, 'CASH', 0, delivery_date)
                if not order_items:
                    logger.error(log(Message.ORDER_SIMULATION_ERROR, {'account_id': account_id}))
                else:
                    if False == request_order_creation(account_id, delivery_center_id, country, environment,
                                                            allow_order_cancel, order_items, order_status, delivery_date):
                        logger.error(log(Message.CREATE_ORDER_ERROR, {'account_id': account_id}))
