from beer_recommender import get_recommendation_by_account, delete_recommendation_by_id
from deals import request_get_deals_promotion_service, request_delete_deal_by_id, request_get_deals_pricing_service, \
    request_delete_deals_pricing_service
from invoice import get_invoices, delete_invoice_by_id
from mass_populator.helpers.database_helper import delete_from_database, get_database_params
from mass_populator.log import *

logger = logging.getLogger(__name__)


def run_preconditions(dataframe_account, country, environment):
    logger.info("Running pre-conditions for %s/%s", country, environment)

    logger.info("delete_orders for %s/%s", country, environment)
    order_database_params = get_database_params(country, environment, 'order-service-ms')
    delete_from_database(order_database_params.get('client'), order_database_params.get('db_name'),
                         order_database_params.get('collection_name'), order_database_params.get('prefix'))

    if dataframe_account is not None:
        dataframe_account.apply(apply_run_preconditions, args=(country, environment), axis=1)


def apply_run_preconditions(row, country, environment):
    account_id = row['account_id']

    logger.info("delete_recommendations for account %s", account_id)
    delete_recommendation(account_id, country, environment, 'CROSS_SELL_UP_SELL')

    logger.info("delete_deals for account %s", account_id)
    delete_deal(account_id, country, environment)

    logger.info("delete_invoices for account %s", account_id)
    delete_invoice(account_id, country, environment)


def delete_deal(account_id, country, environment):
    """
    Delete available deals from Cart-Calculation MS and Promotion MS databases
    Args:
        account_id: POC unique identifier
        country: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., SIT, UAT
    """
    # Check for available deals in Cart-Calculation MS database
    customer_deals = request_get_deals_pricing_service(account_id, country, environment)
    if customer_deals == 'false':
        logger.error(log(Message.RETRIEVE_PROMOTION_ERROR, {'account_id': account_id}))
    elif customer_deals == 'not_found':
        logger.debug("[Pricing Conditions Service] The account {account_id} does not have deals associated. Skipping..."
                    .format(account_id=account_id))
    else:
        # Delete deals from Cart-Calculation MS database
        if 'false' == request_delete_deals_pricing_service(account_id, country, environment, customer_deals):
            logger.error(log(Message.DELETE_PROMOTION_ERROR, {'account_id': account_id}))

    # Check for available deals in Promotion MS database
    promotions = request_get_deals_promotion_service(account_id, country, environment)
    if promotions == 'false':
        logger.error(log(Message.RETRIEVE_PROMOTION_ERROR, {'account_id': account_id}))
    elif promotions == 'not_found':
        logger.debug("[Promotion Service] The account {account_id} does not have deals associated. Skipping..."
                    .format(account_id=account_id))
    else:
        # Delete deals from Promotion MS database
        if 'false' == request_delete_deal_by_id(account_id, country, environment, promotions):
            logger.error(log(Message.DELETE_PROMOTION_ERROR, {'account_id': account_id}))


def delete_recommendation(account_id, country, environment, use_case):
    """
    Delete recommendation
    Args:
        account_id: POC unique identifier
        country: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., SIT, UAT
        use_case: e.g., QUICK_ORDER, CROSS_SELL_UP_SELL, FORGOTTEN_ITEMS
    """
    up_sell_data = get_recommendation_by_account(account_id, country, environment, use_case)
    if up_sell_data == 'not_found':
        logger.debug("[Global Recommendation Service] Recommendation type {use_case_type} not found for account "
                     "{account_id}. Skipping...".format(use_case_type=use_case, account_id=account_id))
    elif up_sell_data == 'false':
        logger.error(log(Message.RETRIEVE_RECOMMENDER_ERROR, {'use_case_type': use_case, 'account_id': account_id}))
    else:
        if 'success' != delete_recommendation_by_id(environment, up_sell_data):
            logger.error(log(Message.DELETE_RECOMMENDER_ERROR, {'use_case_type': use_case, 'account_id': account_id}))


def delete_invoice(account_id, country, environment):
    """
    Delete invoice
    Args:
        account_id: POC unique identifier
        country: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g., SIT, UAT
    """
    invoices_by_account = get_invoices(country, account_id, environment)
    if invoices_by_account == 'false':
        logger.error(log(Message.RETRIEVE_INVOICE_ERROR, {'account_id': account_id}))
    else:
        invoice_ids = list()
        for i in invoices_by_account['data']:
            invoice_id = i['invoiceId']
            invoice_ids.append(invoice_id)

        for i in range(len(invoice_ids)):
            if 'false' == delete_invoice_by_id(country, environment, invoice_ids[i]):
                logger.error(log(Message.DELETE_INVOICE_ERROR, {'account_id': account_id}))
