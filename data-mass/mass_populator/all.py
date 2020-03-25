from mass_populator.log import log

from mass_populator.common import execute_common

def log_local(key, message):
    log("  all-file :: " + key, message)

def execute_all(country, environment):
    log_local("Country", country)
    log_local("Environment", environment)
    
    return execute_common(country, environment)