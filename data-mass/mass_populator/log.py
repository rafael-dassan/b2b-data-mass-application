from enum import Enum
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')


def log(message, kwargs):
    if isinstance(message, Enum):
        message = message.value

    return message.format(**kwargs)


class Message(Enum):
    ACCOUNT_ERROR = "Fail on populate account {account_id}."
    ACCOUNT_ERROR_MIDDLEWARE = "Fail on populate account {account_id} on Middleware."
    CREDIT_ERROR = "Fail on populate credit for account {account_id}."
    CREDIT_ERROR_MIDDLEWARE = "Fail on populate credit for account {account_id} on Middleware."
    DELIVERY_WINDOW_ERROR = "Fail on populate delivery window for account {account_id}."
    DELIVERY_WINDOW_ERROR_MIDDLEWARE = "Fail on populate delivery window for account {account_id} on Middleware."
    PRODUCT_ERROR = "Fail on populate product for account {account_id}."
    RECOMMENDER_QUICK_ORDER_ERROR = "Fail on populate recommender quick order for account {account_id}."
    RECOMMENDER_FORGOTTEN_ITEMS_ERROR = "Fail on populate recommender forgotten items for account {account_id}."
    RECOMMENDER_SELL_UP_ERROR = "Fail on populate recommender sell up for account {account_id}."
    RETRIEVE_RECOMMENDER_ERROR = "Fail on retrieve {use_case_type} recommendation for account {account_id}."
    DELETE_RECOMMENDER_ERROR = "Fail on delete {use_case_type} recommendation for account {account_id}."
    PRODUCT_CREATE_ERROR = "Fail on create product for sku: {sku}"
    PRODUCT_ENABLE_ERROR = "Fail on enable product for sku: {sku}"
    CATEGORY_PRODUCT_ASSOCIATE_ERROR = "Fail on associate category {category} to product {sku}."
    CATEGORY_CREATE_ERROR = "Fail on create category {category}."
    INVENTORY_CREATE_ERROR = "Fail on creating inventory for account {account_id}."
    SUBCATEGORY_CREATION_ERROR = "It was not possible to create the subcategory {subcategory_name}" \
                                 " within the parent category of id {parent_id}."
    CREATE_USER_IAM_ERROR = "Fail on populate user IAM B2C {email} with account {account_id}."
    RETRIEVE_ACCOUNT_ERROR = "Failure to retrieve the account {account_id}."
    RETRIEVE_PROMOTION_ERROR = "Failure to retrieve promotions for account {account_id}."
    DELETE_PROMOTION_ERROR = "Fail on delete deals for account {account_id}."
    RETRIEVE_PRODUCT_ERROR = "Failure to retrieve products for account {account_id}."
    CREATE_DEALS_ERROR = "Fail on populate deal {deal_id} with account {account_id}."
    CONFIGURE_ORDER_PREFIX_ERROR = "Fail on configure order prefix and number size for account {account_id}."
    CREATE_ORDER_ERROR = "Fail on create an order for account {account_id}."
    ORDER_SIMULATION_ERROR = "Fail on simulate the order for account {account_id}."
