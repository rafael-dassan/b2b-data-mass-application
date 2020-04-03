from mass_populator.log import log
from mass_populator.AR.account import populate_accounts as populate_accounts_ar
from mass_populator.BR.account import populate_accounts as populate_accounts_br
from mass_populator.CL.account import populate_accounts as populate_accounts_cl
from mass_populator.DO.account import populate_accounts as populate_accounts_do
from mass_populator.ZA.account import populate_accounts as populate_accounts_za


def log_local(key, message):
    log("  common-file :: " + key, message)


def execute_common(country, environment):
    log_local("Country", country)
    log_local("Environment", environment)

    populate_accounts_switcher = {
        "AR": populate_accounts_ar,
        "BR": populate_accounts_br,
        "CL": populate_accounts_cl,
        "DO": populate_accounts_do,
        "ZA": populate_accounts_za
    }

    function = populate_accounts_switcher.get(country)
    if function != "":
        function(country, environment)

    return True

