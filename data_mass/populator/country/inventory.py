from data_mass.inventory.relay import request_inventory_creation
from data_mass.populator.log import *
from data_mass.product.service import request_get_account_product_assortment

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
    if True != request_inventory_creation(country, environment, account_id, delivery_center_id, products):
        logger.error(log(Message.INVENTORY_CREATE_ERROR, {"account_id": account_id}))
