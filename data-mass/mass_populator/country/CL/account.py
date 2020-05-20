from mass_populator.log import *
from mass_populator.country.populate_account import populate_poc

logger = logging.getLogger(__name__)


def populate_accounts(country, environment):
    credit = "45000"
    balance = "45000"
    payment_method = ["CASH"]
    amount_of_products = 100

    populate_poc(country, environment, "2323434554", "CL_POC_001", payment_method, credit, balance, amount_of_products, True)
    populate_poc(country, environment, "1020303040", "CL_POC_002", payment_method, credit, balance, amount_of_products, True)
    populate_poc(country, environment, "3325534210", "CL_POC_003", payment_method, credit, balance, amount_of_products, False)

    logger.info("Accounts populating finalized.")