from mass_populator.log import *
from mass_populator.country.AR.account import populate_accounts as populate_accounts_ar
from mass_populator.country.BR.account import populate_accounts as populate_accounts_br
from mass_populator.country.CL.account import populate_accounts as populate_accounts_cl
from mass_populator.country.DO.account import populate_accounts as populate_accounts_do
from mass_populator.country.ZA.account import populate_accounts as populate_accounts_za
from mass_populator.country.CO.account import populate_accounts as populate_accounts_co
from mass_populator.country.BR.user import populate_users as populate_users_br
from mass_populator.country.DO.user import populate_users as populate_users_do
from mass_populator.country.AR.user import populate_users as populate_users_ar
from mass_populator.country.CL.user import populate_users as populate_users_cl
from mass_populator.country.ZA.user import populate_users as populate_users_za
from mass_populator.country.CO.user import populate_users as populate_users_co
from mass_populator.country.AR.recommendation import populate_recomendations as populate_recommendations_ar
from mass_populator.country.BR.recommendation import populate_recomendations as populate_recommendations_br
from mass_populator.country.DO.recommendation import populate_recomendations as populate_recommendations_do
from mass_populator.country.ZA.recommendation import populate_recomendations as populate_recommendations_za
from mass_populator.country.CO.recommendation import populate_recomendations as populate_recommendations_co
from mass_populator.country.AR.category import associate_product_to_category as associate_product_to_category_ar
from mass_populator.country.AR.product import enable_products_magento as enable_product_magento_ar
from mass_populator.country.BR.category import associate_product_to_category as associate_product_to_category_br
from mass_populator.country.BR.product import enable_products_magento as enable_product_magento_br
from mass_populator.country.CO.category import associate_product_to_category as associate_product_to_category_co
from mass_populator.country.CO.product import enable_products_magento as enable_product_magento_co
from mass_populator.country.DO.category import associate_product_to_category as associate_product_to_category_do
from mass_populator.country.DO.product import enable_products_magento as enable_product_magento_do
from mass_populator.country.ZA.category import associate_product_to_category as associate_product_to_category_za
from mass_populator.country.ZA.product import enable_products_magento as enable_product_magento_za


logger = logging.getLogger(__name__)


def execute_common(country, environment):
    populate_accounts(country, environment)
    populate_users_magento(country, environment)
    populate_recommendations(country, environment)

    enable_products_magento(country, environment)
    associate_products_to_categories(country, environment)

    return True


def populate_accounts(country, environment):
    populate_accounts_switcher = {
        "AR": populate_accounts_ar,
        "BR": populate_accounts_br,
        "CL": populate_accounts_cl,
        "DO": populate_accounts_do,
        "ZA": populate_accounts_za,
        "CO": populate_accounts_co
    }

    function = populate_accounts_switcher.get(country)
    if function != "":
        logger.info("populate_accounts for %s/%s", country, environment)
        function(country, environment)


def populate_users_magento(country, environment):
    allowed_environments = ["UAT", "SIT"]

    if (environment not in allowed_environments):
        logger.info(
            "Skipping populate users magento, because the environment is not supported!")
        return False

    populate_users_magento_switcher = {
        "BR": populate_users_br,
        "DO": populate_users_do,
        "AR": populate_users_ar,
        "CL": populate_users_cl,
        "ZA": populate_users_za,
        "CO": populate_users_co
    }

    function = populate_users_magento_switcher.get(country)
    if function != "":
        logger.info("populate_users_magento for %s/%s", country, environment)
        function(environment)


def populate_recommendations(country, environment):
    allowed_countries = ["AR","BR", "DO", "ZA", "CO"]

    if (country not in allowed_countries):
        logger.info(
            "Skipping populate recomendations, because the country is not supported!")
        return False

    populate_recommendations_switcher = {
        "AR": populate_recommendations_ar,
        "BR": populate_recommendations_br,
        "DO": populate_recommendations_do,
        "ZA": populate_recommendations_za,
        "CO": populate_recommendations_co
    }

    function = populate_recommendations_switcher.get(country)
    if function != "":
        logger.info("populate_recommendations for %s/%s", country, environment)
        function(environment)


def enable_products_magento(country, environment):
    allowed_countries = ["AR","BR", "DO", "ZA", "CO"]

    if (country not in allowed_countries):
        logger.info(
            "Skipping products activation in Magento, because the country is not supported!")
        return False
    
    enable_product_magento_switcher = {
        "BR": enable_product_magento_br,
        "DO": enable_product_magento_do,
        "AR": enable_product_magento_ar,
        "ZA": enable_product_magento_za,
        "CO": enable_product_magento_co
    }

    function = enable_product_magento_switcher.get(country)
    if function != "":
        logger.info("enable products magento %s/%s", country, environment)
        function(country, environment)


def associate_products_to_categories(country, environment):
    allowed_countries = ["AR","BR", "DO", "ZA", "CO"]

    if (country not in allowed_countries):
        logger.info(
            "Skipping products association to categories, because the country is not supported!")
        return False
    
    associate_products_to_categories_switcher = {
        "BR": associate_product_to_category_br,
        "DO": associate_product_to_category_do,
        "AR": associate_product_to_category_ar,
        "ZA": associate_product_to_category_za,
        "CO": associate_product_to_category_co
    }

    function = associate_products_to_categories_switcher.get(country)
    if function != "":
        logger.info("associate products to categories %s/%s", country, environment)
        function(country, environment)