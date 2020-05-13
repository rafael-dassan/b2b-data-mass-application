from mass_populator.log import *
from mass_populator.country.populate_account import populate_poc

logger = logging.getLogger(__name__)


def populate_accounts(country, environment):
    credit = "45000"
    balance = "45000"
    payment_method = ["CASH", "CREDIT"]
    amount_of_products = 100

    populate_poc(country, environment, "9883300001", "DO_POC_001", payment_method, credit, balance, amount_of_products, True)
    populate_poc(country, environment, "9883300002", "DO_POC_002", payment_method, credit, balance, amount_of_products, True)
    populate_poc(country, environment, "9883300003", "DO_POC_003", payment_method, credit, balance, amount_of_products, False)
    
    logger.info("Accounts populating finalized.")