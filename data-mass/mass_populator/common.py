from mass_populator.log import *
from mass_populator.AR.account import populate_accounts as populate_accounts_ar
from mass_populator.BR.account import populate_accounts as populate_accounts_br
from mass_populator.CL.account import populate_accounts as populate_accounts_cl
from mass_populator.DO.account import populate_accounts as populate_accounts_do
from mass_populator.ZA.account import populate_accounts as populate_accounts_za
from mass_populator.BR.user import populate_users as populate_users_br
from mass_populator.DO.user import populate_users as populate_users_do
from mass_populator.AR.user import populate_users as populate_users_ar
from mass_populator.CL.user import populate_users as populate_users_cl
from mass_populator.ZA.user import populate_users as populate_users_za
from mass_populator.BR.recommendation import populate_recomendations as populate_recommendations_br
from mass_populator.DO.recommendation import populate_recomendations as populate_recommendations_do
from mass_populator.ZA.recommendation import populate_recomendations as populate_recommendations_za

logger = logging.getLogger(__name__)


def execute_common(country, environment):
    populate_accounts(country, environment)
    populate_users_magento(country, environment)
    populate_recommendations(country, environment)

    return True


def populate_accounts(country, environment):
    populate_accounts_switcher = {
        "AR": populate_accounts_ar,
        "BR": populate_accounts_br,
        "CL": populate_accounts_cl,
        "DO": populate_accounts_do,
        "ZA": populate_accounts_za
    }

    if environment == "SIT":
        translated_environment = "QA"
    else:
        translated_environment = environment

    function = populate_accounts_switcher.get(country)
    if function != "":
        function(country, translated_environment)


def populate_users_magento(country, environment):
    allowed_environments = ["UAT", "SIT"]

    if (environment not in allowed_environments):
        logger.info("Skipping populate users magento, because the environment is not supported!")
        return False

    populate_users_magento_switcher = {
        "BR": populate_users_br,
        "DO": populate_users_do,
        "AR": populate_users_ar,
        "CL": populate_users_cl,
        "ZA": populate_users_za
    }

    function = populate_users_magento_switcher.get(country)
    if function != "":
        logger.info("populate_users_magento for %s/%s", country, environment)
        function(environment)


def populate_recommendations(country, environment):
    allowed_environments = ["UAT", "SIT"]
    allowed_countries = ["BR", "DO", "ZA"]

    if (country not in allowed_countries):
        logger.info("Skipping populate recomendations, because the country is not supported!")
        return False

    populate_recommendations_switcher = {
        "BR": populate_recommendations_br,
        "DO": populate_recommendations_do,
        "ZA": populate_recommendations_za
    }

    if environment == "SIT":
        translated_environment = "QA"
    else:
        translated_environment = environment

    function = populate_recommendations_switcher.get(country)
    if function != "":
        logger.info("populate_recommendations for %s/%s", country, translated_environment)
        function(translated_environment)