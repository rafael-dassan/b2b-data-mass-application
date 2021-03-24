from accounts import check_account_exists_microservice
from mass_populator.country.product import check_product_associated_to_account
from mass_populator.log import *
from orders import configure_order_params, request_order_creation, get_order_prefix_params
from products import request_get_offers_microservice
from simulation import request_order_simulation

logger = logging.getLogger(__name__)


def populate_orders_base(country, environment, dataframe_orders):
    if dataframe_orders is not None:
        dataframe_orders.apply(apply_populate_order, args=(country, environment), axis=1)


def apply_populate_order(row, country, environment):
    populate_order(country, environment, str(row['account_id']), row['allow_order_cancel'], row['items'],
                   row['quantity'], row['order_status'], row['prefix'])


def populate_order(country, environment, account_id, allow_order_cancel, items, quantity, order_status, prefix):
    """
    Populate orders
    Args:
        country: e.g., AR, BR, CO, etc
        environment: e.g., SIT, UAT
        account_id: POC unique identifier
        allow_order_cancel: e.g., `Y` or `N`
        items: order items
        quantity: items quantity
        order_status: e.g., PLACED, DELIVERED, etc
        prefix: order prefix
    """
    account = check_account_exists_microservice(account_id, country, environment)
    if account == 'false':
        logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))
    else:
        delivery_center_id = account[0]['deliveryCenterId']

        not_associated_products = check_product_associated_to_account(account_id, country, environment, [items])
        if not_associated_products is not False:
            product_offers = request_get_offers_microservice(account_id, country, environment)
            if product_offers != 'false':
                data = {'sku': items, 'itemQuantity': quantity}

                # Call function to configure prefix and order number size in the database sequence
                if 'false' == configure_order_params(country, environment, account_id, 8,
                                                     '{0}-{1}-'.format(prefix, country)):
                    logger.error(log(Message.CONFIGURE_ORDER_PREFIX_ERROR, {'account_id': account_id}))
                else:
                    order_items = request_order_simulation(country, environment, account_id, delivery_center_id, [data],
                                                           None, None, 'CASH', 0)
                    if order_items == 'false':
                        logger.error(log(Message.ORDER_SIMULATION_ERROR, {'account_id': account_id}))
                    else:
                        if 'false' == request_order_creation(account_id, delivery_center_id, country, environment,
                                                             allow_order_cancel, order_items, order_status):
                            logger.error(log(Message.CREATE_ORDER_ERROR, {'account_id': account_id}))
                        else:
                            # Call function to re-configure prefix and order number size according to the zone's format
                            order_prefix_params = get_order_prefix_params(country)
                            if 'false' == configure_order_params(country, environment, account_id,
                                                                 order_prefix_params.get('order_number_size'),
                                                                 order_prefix_params.get('prefix')):
                                logger.error(log(Message.CONFIGURE_ORDER_PREFIX_ERROR, {'account_id': account_id}))
