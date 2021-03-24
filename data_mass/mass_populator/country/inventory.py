from ...product_inventory import request_inventory_creation
from ...products import request_get_account_product_assortment
from ...mass_populator.log import *

logger = logging.getLogger(__name__)


def populate_default_inventory(account_id, country, environment, delivery_center_id):
    """
    Populate the default inventory (99999) for all products associated to an account_id
    Args:
        account_id: POC unique identifier
        country: e.g., AR, CO, DO, ZA
        environment: SIT, UAT
        delivery_center_id: POC's delivery center unique identifier
    """
    # Get assortment from the specific POC
    products = request_get_account_product_assortment(account_id, country, environment, delivery_center_id)

    # Request the creation of the default inventory
    if "true" != request_inventory_creation(country, environment, account_id, delivery_center_id, products):
        logger.error(log(Message.INVENTORY_CREATE_ERROR, {"account_id": account_id}))
