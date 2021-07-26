# Standard library imports
import json
from itertools import repeat
from multiprocessing import Pool

import pkg_resources

from data_mass.classes.text import text
# Local application imports
from data_mass.common import (
    convert_json_to_string,
    get_header_request,
    get_microservice_base_url,
    place_request,
    return_first_and_last_date_year_payload,
    update_value_to_json
)
from data_mass.product.service import (
    check_item_enabled,
    get_sku_name,
    request_get_account_product_assortment,
    request_get_products_microservice
)


# Show all available SKUs of the account in the screen
def display_available_products(account_id, zone, environment, delivery_center_id):
    # Retrieve all SKUs for the specified Account and DeliveryCenter IDs
    product_offers = request_get_account_product_assortment(account_id, zone, environment, delivery_center_id)
    # Retrieve all SKUs for the specified Zone
    products = request_get_products_microservice(zone, environment)
    if products:
        products_list = list()
        for sku in products:
            products_list.append(sku['sku'])

        valid_products = list(set(product_offers).intersection(products_list))

        if isinstance(product_offers, list):
            # Check if the SKU is enabled
            enabled_skus = list()
            if len(product_offers):
                with Pool(20) as pool:
                    enabled_skus = pool.starmap(check_item_enabled,
                                                zip(valid_products, repeat(zone), repeat(environment)))

            # Get SKU name
            if len(enabled_skus) > 0:
                print(text.default_text_color + '\n Wait. We are bringing the available products: ')
                quantity_enabled_skus = len(enabled_skus)
                with Pool(20) as pool:
                    sku_name = pool.starmap(get_sku_name, zip(repeat(zone), repeat(environment), enabled_skus))

                    aux_index = 0

                    while aux_index < quantity_enabled_skus:
                        if not enabled_skus[aux_index]:
                            aux_index = aux_index + 1
                        else:
                            print(
                                text.default_text_color + '\n SKU: ' + text.Blue + enabled_skus[aux_index] + '  ||  ' +
                                sku_name[aux_index].upper())
                            aux_index = aux_index + 1

                    sku_id = input(text.default_text_color + '\n Type here the SKU from the list above you want to add '
                                                             'SKU Limit: ')

                    while not validate_sku(sku_id.strip(), enabled_skus):
                        print(text.Red + '\n- Invalid SKU. Please check the list above and try again.')
                        sku_id = input(
                            text.default_text_color + '\n Type here the SKU from the list above you want to add '
                                                      'SKU Limit: ')

                    sku_quantity = input(text.default_text_color + '\n Type here the quantity you want to add to it: ')

                    while not sku_quantity.isdigit():
                        print(text.Red + '\n- Invalid option.')
                        sku_quantity = input(
                            text.default_text_color + '\n Type here the quantity you want to add to it: ')

                    update_sku_limit = update_sku_limit_enforcement_microservice(
                        zone,
                        environment,
                        account_id,
                        sku_id, sku_quantity
                    )

                if update_sku_limit:
                    return True
                else:
                    return False
            else:
                return 'error_len'
        else:
            return product_offers
    else:
        return False


def update_sku_limit_enforcement_microservice(
        zone: str,
        environment: str,
        account_id: str,
        sku_id: str = None,
        sku_quantity: int = 0) -> bool:
    """
    Update SKU limit.

    Parameters
    ----------
    zone : str
    environment : str
    account_id : str
    sku_id : str, optional
        By default `None`.
    sku_quantity : int, optional
        By default `0`.

    Returns
    -------
    bool
        Whenever a update occours.
    """

    # Define url request
    request_url = get_microservice_base_url(environment) + '/enforcement-relay-service/'

    # Get start and end dates
    dates_payload = return_first_and_last_date_year_payload()

    # Create dictionary with sku limits values
    dict_values = {
        'accounts': [account_id],
        'enforcements[0].entityId': sku_id,
        'enforcements[0].startDate': dates_payload['startDate'] + 'T00:00:00.000Z',
        'enforcements[0].endDate': dates_payload['endDate'] + 'T00:00:00.000Z',
        'enforcements[0].limits[0].value': int(sku_quantity)
    }

    # Define headers
    request_headers = get_header_request(zone, False, False, False, False)

    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/update_sku_limit_payload.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return True
    else:
        print(text.Red + '\n- [Enforcement Relay Service] Failure to add SKU Limit. Response Status: '
                         '{response_status}. Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return False


# Validate SKU
def validate_sku(sku_id, enabled_skus):
    aux_index = 0

    while aux_index < len(enabled_skus):
        if enabled_skus[aux_index] == sku_id:
            return True
        aux_index = aux_index + 1
