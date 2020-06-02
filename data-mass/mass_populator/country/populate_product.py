from products import create_item
from mass_populator.log import *

logger = logging.getLogger(__name__)


def populate_product(country, environment,
        sku,
        name,
        brand_name,
        sub_brand_name,
        package_id,
        container_name,
        container_size,
        container_returnable,
        container_unitOfMeasurement,
        sales_ranking):
    """ Populate products
    Arguments:
        - country: (e.g, BR,ZA,DO)
        - environment: (e.g, UAT,SIT)
        -  sku': sku 
        -  name': name
        -  brand_name': brand_name 
        -  sub_brand_name': sub_brand_name
        -  package_id': package_id
        -  container_name': container_name
        -  container_size': container_size
        -  container_returnable': container_returnable
        -  container_unitOfMeasurement': container_unitOfMeasurement
        -  sales_ranking': sales_ranking
    """
    item_data = {
        'sku': sku, 
        'name': name,
        'brandName': brand_name, 
        'subBrandName': sub_brand_name,
        'package.id': package_id,
        'container.name': container_name,
        'container.size': container_size,
        'container.returnable': container_returnable,
        'container.unitOfMeasurement': container_unitOfMeasurement,
        'salesRanking': sales_ranking
    }
    response = create_item(country, environment, item_data)
    if response is None:
        logger.error(log(Message.PRODUCT_CREATE_ERROR,{"sku": sku}))