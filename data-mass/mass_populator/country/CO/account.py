from mass_populator.log import *
from mass_populator.country.populate_account import populate_poc

logger = logging.getLogger(__name__)


# Populate the accounts for BR
def populate_accounts(country, environment):
    populate_poc(country, environment, "9883300201", "CO_POC_001", ["CASH"], "41000", "50100", 100, True)
    populate_poc(country, environment, "9883300202", "CO_POC_002", ["CREDIT"], "42000", "50200", 100, True)
    populate_poc(country, environment, "9883300203", "CO_POC_003", ["CASH", "CREDIT"], "43000", "50300", 100, False)

    logger.info("Accounts populating finalized.")
