import pandas as pd
import os
import sys
from mass_populator.log import *


logger = logging.getLogger(__name__)
    

def converter_string_to_list(columns_converter=[]):
    return dict.fromkeys(columns_converter, lambda str: str.split(";"))


def converters_by_entity(entity):
    entities_converters_switcher = {
        'account': ['payment_method', 'products'],
        'category': ['products'],
        'user': ['account_ids'],
        'stepped_discount': ['index_range', 'discount_range']
    }
    converter = entities_converters_switcher.get(entity)
    return converter if converter is not None else {}


def converter_dtype_to_string_by_entity(entity):
    entities_converters_switcher = {
        'account': ['account_id'],
        'recommendation': ['account_id'],
        'rewards': ['account_id_unenroll','account_id_enrolled']
    }
    converter = entities_converters_switcher.get(entity)
    return dict.fromkeys(converter, 'str') if converter is not None else {}


def search_file_path(country, entity, is_default_file=True):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    base_file = "../country/data"

    default_file = "{base_file}/{entity}.csv".format(
        base_file=base_file, entity=entity)
    if not is_default_file:
        default_file = "{base_file}/{country}/{entity}.csv".format(
            base_file=base_file, country=country, entity=entity)
    
    return '{}/{}'.format(absolute_path, default_file)


def search_file_content(country, entity, file_path, is_default_file):
    try:
        return pd.read_csv(file_path,
        converters=converter_string_to_list(converters_by_entity(entity)),
        dtype=converter_dtype_to_string_by_entity(entity))
    except FileNotFoundError:
        if is_default_file:
            logger.error("file not found for: {}, entity: {}, path: {}".format(
                country, entity, file_path))
        return None
    except Exception as e:
        logger.error("Unexpected error: {}".format(e))
        sys.exit(1)


def search_data(country, entity, is_default_file=False):
    file_path = search_file_path(country, entity, is_default_file)
    return search_file_content(country, entity, file_path, is_default_file)


def search_data_by(country, entity):
    logger.debug("search_data_by country: {}, entity: {}".format(country, entity))
    
    country = country.lower()
    data = search_data(country, entity)
    if data is None:
        logger.debug("using standard data for country: {}, entity: {}".format(country, entity))
        data = search_data(country, entity, True)
    return data
