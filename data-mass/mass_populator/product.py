from mass_populator.log import *
from mass_populator.country.AR.product import populate_products as populate_products_ar
from mass_populator.country.BR.product import populate_products as populate_products_br
from mass_populator.country.CL.product import populate_products as populate_products_cl
from mass_populator.country.DO.product import populate_products as populate_products_do
from mass_populator.country.ZA.product import populate_products as populate_products_za
from mass_populator.country.CO.product import populate_products as populate_products_co

logger = logging.getLogger(__name__)


def execute_product(country, environment):
    populate_products(country, environment)
    return True


def populate_products(country, environment):
    populate_products_switcher = {
        "AR": populate_products_ar,
        "BR": populate_products_br,
        "CL": populate_products_cl,
        "DO": populate_products_do,
        "ZA": populate_products_za,
        "CO": populate_products_co
    }

    function = populate_products_switcher.get(country)
    if function != "":
        logger.info("populate_products for %s/%s", country, environment)
        function(country, environment)