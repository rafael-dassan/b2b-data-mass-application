from mass_populator.log import *
from mass_populator.country.populate_account import populate_poc

logger = logging.getLogger(__name__)

def populate_accounts(country, environment):
    credit = "45000"
    balance = "45000"
    payment_method = ["CASH"]
    amount_of_products = 100
    products = ["0101WEB", "0102WEB", "0101ANDROID", "0102ANDROID", "0101IOS", "0102IOS"]

    populate_poc(country, environment, "5444385012", "AR_POC_001", payment_method, credit, balance, amount_of_products, True, products)
    populate_poc(country, environment, "9932094352", "AR_POC_002", payment_method, credit, balance, amount_of_products, True, products)
    populate_poc(country, environment, "1669325565", "AR_POC_003", payment_method, credit, balance, amount_of_products, False, products)

    logger.info("Accounts populating finalized.")