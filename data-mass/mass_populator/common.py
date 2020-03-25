from mass_populator.log import log

def log_local(key, message):
    log("  common-file :: " + key, message)

def execute_common(country, environment):
    log_local("Country", country)
    log_local("Environment", environment)

    return False