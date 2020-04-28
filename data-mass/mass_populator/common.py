from mass_populator.log import log
from mass_populator.AR.account import populate_accounts as populate_accounts_ar
from mass_populator.BR.account import populate_accounts as populate_accounts_br
from mass_populator.CL.account import populate_accounts as populate_accounts_cl
from mass_populator.DO.account import populate_accounts as populate_accounts_do
from mass_populator.ZA.account import populate_accounts as populate_accounts_za
from mass_populator.BR.user import populate_users as populate_users_br
from mass_populator.DO.user import populate_users as populate_users_do


def log_local(key, message):
    log("  common-file :: " + key, message)


def execute_common(country, environment):
    log_local("Country", country)
    log_local("Environment", environment)

    populate_accounts(country, environment)
    populate_users_v2(country, environment)

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


def populate_users_v2(country, environment):
    allowed_countries = ["BR", "DO"]
    allowed_environments = ["UAT", "SIT"]

    if (country not in allowed_countries) or (environment not in allowed_environments):
        print("Skipping populate users v2, because the country or environment are not supported!")
        return False

    populate_users_v2_switcher = {
        "BR": populate_users_br,
        "DO": populate_users_do
    }

    function = populate_users_v2_switcher.get(country)
    if function != "":
        print("populate_users_v2 for ", country, environment)
        function(environment)

