import logging
import sys

from data_mass.populator.gateway import execute_gateway
from data_mass.populator.log import *
from data_mass.populator.regression import execute_regression
from data_mass.populator.test import execute_test
from data_mass.populator.product import execute_product
from data_mass.populator.rewards import execute_rewards
from data_mass.populator.validation import *

logger = logging.getLogger(__name__)


def gateway(country, environment):
    logger.debug("GATEWAY method executed with Country/Environment: {a}/{b}".format(a=country, b=environment))
    execute_gateway(country, environment)


def regression(country, environment):
    logger.debug("REGRESSION method executed with Country/Environment: {a}/{b}".format(a=country, b=environment))
    execute_regression(country, environment)


def test(country, environment):
    logger.debug("TEST method executed with Country/Environment: {a}/{b}".format(a=country, b=environment))
    execute_test(country, environment)


def product(country, environment):
    logger.debug("PRODUCT method executed with Country/Environment: {a}/{b}".format(a=country, b=environment))
    execute_product(country, environment)


def rewards(country, environment):
    logger.debug("REWARDS method executed with Country/Environment: {a}/{b}".format(a=country, b=environment))
    execute_rewards(country, environment)


def execute(country, environment, execution_type):
    logger.info("Country: %s", country)
    logger.info("Environment: %s", environment)
    logger.info("Execution type: %s", execution_type)

    # to discover which function to call
    switcher = {
            "gateway": gateway,
            "regression": regression,
            "test": test,
            "product": product,
            "rewards": rewards
        }

    # get the function to call
    func = switcher.get(execution_type)

    # call that function
    func(country, environment)


# Init
if __name__ == '__main__':
    try:
        if not valid_parameters(sys.argv):
            raise ValueError("Invalid parameters. Three parameters were expected: [ [ COUNTRY ] [ ENVIRONMENT ] "
                             "[ gateway | regression | test | product | rewards ] ]", sys.argv)

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
