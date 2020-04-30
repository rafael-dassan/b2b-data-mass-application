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