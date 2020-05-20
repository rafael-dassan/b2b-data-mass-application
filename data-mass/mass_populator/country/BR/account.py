from mass_populator.log import *
from mass_populator.country.populate_account import populate_poc

logger = logging.getLogger(__name__)

# Populate the accounts for BR
def populate_accounts(country, environment):
    credit = "45000"
    balance = "45000"
    payment_method = ["CASH", "BANK_SLIP"]
    amount_of_products = 100
    
    populate_poc(country, environment, "99481543000135", "BR_POC_001", payment_method, credit, balance, amount_of_products, True)
    populate_poc(country, environment, "56338831000122", "BR_POC_002", payment_method, credit, balance, amount_of_products, True)
    populate_poc(country, environment, "42282891000166", "BR_POC_003", payment_method, credit, balance, amount_of_products, False)

    logger.info("Accounts populating finalized.")