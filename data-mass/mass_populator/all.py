from mass_populator.log import *
from mass_populator.common import execute_common

logger = logging.getLogger(__name__)


def execute_all(country, environment):
    return execute_common(country, environment)

