from ...accounts import check_account_exists_microservice
from ...invoices import create_invoice_request
from ...mass_populator.log import *
from ...mass_populator.log import log, Message
from ...mass_populator.preconditions import logger
from ...orders import request_get_order_by_date_updated, get_order_details, get_order_items

logger = logging.getLogger(__name__)


def populate_invoices_base(country, environment, dataframe_invoices):
    if dataframe_invoices is not None:
        dataframe_invoices.apply(apply_populate_invoice, args=(country, environment), axis=1)


def apply_populate_invoice(row, country, environment):
    populate_invoice(country, environment, str(row['account_id']), row['invoice_status'], row['order_prefix'],
                     row['invoice_prefix'])


def populate_invoice(country, environment, account_id, invoice_status, order_prefix, invoice_prefix):
    """
    Populate invoices
    Args:
        country: e.g., AR, BR, CO, etc
        environment: e.g., SIT, UAT
        account_id: POC unique identifier
        invoice_status: e.g., OPEN, CLOSED, etc
        order_prefix: order prefix that composes the order ID
        invoice_prefix: invoice prefix that composes the invoice ID
    """
    account = check_account_exists_microservice(account_id, country, environment)
    if account == 'false':
        logger.error(log(Message.RETRIEVE_ACCOUNT_ERROR, {'account_id': account_id}))

    response = request_get_order_by_date_updated(country, environment, account_id, order_prefix)
    if response == 'false':
        logger.error(log(Message.RETRIEVE_ORDER_ERROR, {'account_id': account_id}))
    else:
        order_data = response[0]
        order_details = get_order_details(order_data)
        order_items = get_order_items(order_data, country)
        order_id = order_data['orderNumber']
        invoice_id = '{0}-{1}'.format(invoice_prefix, country)

        if 'false' == create_invoice_request(country, environment, order_id, invoice_status, order_details,
                                             order_items, invoice_id):
            logger.error(log(Message.CREATE_INVOICE_ERROR, {'account_id': account_id}))
