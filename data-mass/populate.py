import sys

from mass_populator.log import *
from mass_populator.all import execute_all
from mass_populator.common import execute_common
from mass_populator.test import execute_test
from mass_populator.validation import *

logger = logging.getLogger(__name__)

def common(country, environment):
    logger.debug("COMMON method executed with Country/Environment: {a}/{b}".format(a=country, b=environment))
    execute_common(country, environment)

def all(country, environment):
    logger.debug("ALL method executed with Country/Environment: {a}/{b}".format(a=country, b=environment))
    execute_all(country, environment)

def test(country, environment):
    logger.debug("TEST method executed with Country/Environment: {a}/{b}".format(a=country, b=environment))
    execute_test(country, environment)

def execute(country, environment, execution_type):
    logger.info("Country: %s", country)
    logger.info("Environment: %s", environment)
    logger.info("Execution type: %s", execution_type)

    # to discover wich function to call
    switcher = {
            "all": all,
            "common": common,
            "test": test
        }

    # get the function to call
    func = switcher.get(execution_type)

    # call that function
    func(country, environment)

# Init
if __name__ == '__main__':
    try:
        if not valid_parameters(sys.argv):
            raise ValueError("Invalid parameters. Three parameters were expected: [ [ COUNTRY ] [ ENVIRONMENT ] [ all | common ] ]", sys.argv)

        country = sys.argv[1].upper()
        environment = sys.argv[2].upper()
        execution_type = sys.argv[3].lower()

        if not valid_country(country):
            raise ValueError("Country is not valid", country)

        if not valid_environment(environment):
            raise ValueError("Environment is not valid", environment)

        if not valid_execution_type(execution_type):
            raise ValueError("Execution Type is not valid", execution_type)

        execute(country, environment, execution_type)
    except Exception as err:
        logging.error("Exception: {}".format(err))
        sys.exit(1)
