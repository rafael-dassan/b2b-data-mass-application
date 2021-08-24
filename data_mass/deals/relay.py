import json
from random import randint
from typing import Optional, Union

import pkg_resources

from data_mass.classes.text import text
from data_mass.common import (
    convert_json_to_string,
    create_list,
    get_header_request,
    get_microservice_base_url,
    place_request,
    return_first_and_last_date_year_payload,
    update_value_to_json
)

def request_create_stepped_discount_multivendor(
        vendor_account_id: str,
        zone: str,
        environment: str,
        discount_value: int,
        minimum_quantity: float,
        ranges: dict,
        deal_id: str = None,
        vendor_item_id: list = None,
        quantity: int = 10,
        ) -> str:
    """
    Create deal for multivendor.

    Parameters
    ----------
    vendor_account_id : str
    zone : str
    environment : str
    vendor_item_id : str
    deal_id : str

    Returns
    -------
    str
        The deal ID.
    """
    request_headers = get_header_request(zone=zone)
    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/promotion-relay/v3/promotions"

    if deal_id is None:
        vendor_promotion_id = f"DM-{str(randint(1, 100000))}"
    else:
        vendor_promotion_id = deal_id

    body = {
        "vendorPromotionId": vendor_promotion_id,
        "title": f"Discount Promotion: {vendor_promotion_id}",
        "description": "Stepped Discount Promotion, Created by Data Mass",
        "type": "STEPPED_DISCOUNT",
        "startDate": "2020-01-01T00:00:00.000Z",
        "endDate": "2050-03-31T23:59:59.999Z",
        "image": None,
        "budget": 10,
        "quantityLimit": quantity
    }

    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=json.dumps([body]),
        request_headers=request_headers
    )

    if response.status_code in [200, 202]:
        request_url = f"{base_url}/deal-relay/v2"

        deal_body = {
            "vendorAccountIds": [vendor_account_id],
            "deals": [{
                "vendorDealId": vendor_promotion_id,
                "vendorPromotionId": vendor_promotion_id,
                "conditions": {
                    "multipleLineItem":  {
                        "items":[{
                            "vendorItemIds": [vendor_item_id],
                            "minimumQuantity": int(minimum_quantity)
                        }]
                    }
                },
                "output": {
                    "lineItemScaledDiscount": {
                        "vendorItemIds": [vendor_item_id],
                        "ranges": ranges
                    },
                    
                }
            }
          ]
        }


        response = place_request(
            request_method="PUT",
            request_url=request_url,
            request_body=json.dumps(deal_body),
            request_headers=request_headers
        )

        if response.status_code in [200, 202]:
            return vendor_promotion_id

    return False


def request_create_discount_multivendor(
        vendor_account_id: str,
        zone: str,
        environment: str,
        discount_value: int,
        minimum_quantity: float,
        deal_id: str = None,
        vendor_item_id: list = None,
        quantity: int = 10) -> str:
    """
    Create deal for multivendor.

    Parameters
    ----------
    vendor_account_id : str
    zone : str
    environment : str
    vendor_item_id : str
    deal_id : str

    Returns
    -------
    str
        The deal ID.
    """
    request_headers = get_header_request(zone=zone)
    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/promotion-relay/v3/promotions"

    if deal_id is None:
        vendor_promotion_id = f"DM-{str(randint(1, 100000))}"
    else:
        vendor_promotion_id = deal_id

    body = {
        "vendorPromotionId": vendor_promotion_id,
        "title": f"Discount Promotion: {vendor_promotion_id}",
        "description": "Stepped Discount Promotion, Created by Data Mass",
        "type": "STEPPED_DISCOUNT",
        "startDate": "2020-01-01T00:00:00.000Z",
        "endDate": "2050-03-31T23:59:59.999Z",
        "image": None,
        "budget": 10,
        "quantityLimit": quantity
    }

    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=json.dumps([body]),
        request_headers=request_headers
    )

    if response.status_code in [200, 202]:
        request_url = f"{base_url}/deal-relay/v2"
        line_items_discounts = []

        line_items_discounts.append({
            "vendorItemId": vendor_item_id,
            "value": discount_value,
            "maxQuantity": quantity
        })

        deal_body = {
            "vendorAccountIds": [vendor_account_id],
            "deals": [{
                "vendorDealId": vendor_promotion_id,
                "vendorPromotionId": vendor_promotion_id,
                "conditions": {
                    "lineItem": {
                        "vendorItemIds": [vendor_item_id]
                    }
                },
                "output": {
                    "lineItemDiscount": {
                        "vendorItemIds": [vendor_item_id]
                    }
                }
            }]
        }

        response = place_request(
            request_method="PUT",
            request_url=request_url,
            request_body=json.dumps(deal_body),
            request_headers=request_headers
        )

        if response.status_code in [200, 202]:
            return vendor_promotion_id

    return False


def create_mix_match(
        vendor_account_id: str,
        zone: str,
        environment: str,
        vendor_item_ids: list,
        max_quantity: int,
        quantity: int = 10) -> Optional[str]:
    """
    Create Mix & Match deal for multivendor POC.

    Parameters
    ----------
    vendor_account_id : str
        POC unique identifier.
    zone : str
        One of AR, BR, CO, DO, MX, ZA and US.
    environment : str
        One o DEV, SIT and UAT.
    vendor_item_ids : str
        List of products uniques identifiers.
    max_quantity : int
        Maximum quantity for each SKU to be applied.
    quantity : int
        The promotion quantity limit. By default `10`.

    Returns
    -------
    str
        Whenever a request was successfully completed, returns the deal id.
    """
    request_headers = get_header_request(zone=zone)
    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/promotion-relay/v3/promotions"

    vendor_promotion_id = f"DM-{str(randint(1, 100000))}"

    body = {
        "vendorPromotionId": vendor_promotion_id,
        "title": f"Mix & Match: {vendor_promotion_id}",
        "description": "Mix & Match Promotion, Created by Data Mass",
        "type": "FLEXIBLE_DISCOUNT",
        "startDate": "2020-01-01T00:00:00.000Z",
        "endDate": "2050-03-31T23:59:59.999Z",
        "image": None,
        "budget": 10,
        "quantityLimit": quantity
    }

    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=json.dumps([body]),
        request_headers=request_headers
    )

    if response.status_code in [200, 202]:
        request_url = f"{base_url}/deal-relay/v2"
        items_id = []

        for item in vendor_item_ids:
            item_id = item.get("sourceData", {}).get("vendorItemId")
            items_id.append(item_id)

        deal_body = {
            "vendorAccountIds": [vendor_account_id],
            "deals": [{
                "vendorDealId": vendor_promotion_id,
                "vendorPromotionId": vendor_promotion_id,
                "conditions": {
                    "lineItem": {
                        "vendorItemIds": items_id
                    }
                },
                "output": {
                    "lineItemDiscount": {
                        "vendorItemIds": items_id
                    }
                }
            }]
        }

        response = place_request(
            request_method="PUT",
            request_url=request_url,
            request_body=json.dumps(deal_body),
            request_headers=request_headers
        )

        if response.status_code in [200, 202]:
            return vendor_promotion_id

    return False


def get_deals_payload_v2(deal_id: str, deal_type: str):
    """
    Create a payload to associate a promotion to a\
    POC (Promotion Relay Service v2).

    Parameters
    ----------
    deal_id : str
        Deal unique identifier.
    deal_type : str
        e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD, \
        STEPPED_FREE_GOOD.

    Returns
    -------
    dict
        New promotion payload.
    """
    # Create file path
    content = pkg_resources.resource_string(
        "data_mass",
        "data/create_promotion_payload_v2.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    # Create dictionary with deal's values
    dict_values = {
        'description': (
            f"This is a description for a deal type {deal_type} / {deal_id}"
        ),
        'id': deal_id,
        'promotionId': deal_id,
        'title': f"{deal_type} / {deal_id}",
        'type': deal_type
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    return request_body


def request_create_deal_v2(
        deal_type: str,
        zone: str,
        environment: str,
        deal_id: str = None):
    """
    Input deal to a specific POC. The deal is created by calling the \
    Promotion Relay Service V2.

    Parameters
    ----------
    deal_id : str
        deal unique identifier.
    deal_type: e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD, \
        STEPPED_FREE_GOOD.
    zone : str
        e.g., AR, BR, CO, DO, MX
    environment : str
        e.g., DEV, SIT, UAT.

    Returns
    -------
        The `deal_id` if success and error message in case of failure.
    """
    if deal_id is None:
        # Deal unique identifier
        deal_id = f"DM-{str(randint(1, 100000))}"

    request_body = get_deals_payload_v2(deal_id, deal_type)

    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/promotion-relay/v2"

    request_headers = get_header_request(zone, False, False, True, False)

    response = place_request(
        'POST', request_url, request_body, request_headers
    )

    if response.status_code in [200, 202]:
        return deal_id

    print(
        f"{text.Red}"
        "\n- [Promotion Relay Service] Failure create deal."
        f"Response Status: {response.status_code}. "
        f"Response message: {response.text}."
    )

    return False


def create_discount(
        account_id: str,
        sku: str,
        zone: str,
        environment: str,
        discount_value: int,
        minimum_quantity: int,
        deal_id: str = None,
        discount_type: str = 'percentOff',
        deal_type: str = 'DISCOUNT') -> Union[dict, bool]:
    """
    Input a deal type discount to a specific POC by \
    calling the. Promotion Relay Service and \
    Pricing Engine Relay Service.

    Parameters
    ----------
    account_id : str
        POC unique identifier
    sku : str
        product unique identifier
    zone : str
        e.g., AR, BR, CO, DO, MX, ZA or US.
    environment : str
        e.g, DEV, SIT, UAT.
    discount_value : str
        Value of discount to be applied.
    minimum_quantity : str
        Minimum quantity for the discount to be applied.
    discount_type : str
        Default by `percentOff`.
    deal_type : str
        e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD, \
        STEPPED_FREE_GOOD.
    deal_id : str
        Deal unique identifier.

    Returns
    -------
    Union[dict, bool]
        `dict` if success, else `bool`.
    """
    promotion_response = request_create_deal_v2(
        deal_type=deal_type,
        zone=zone,
        environment=environment,
        deal_id=deal_id
    )

    cart_response = request_create_discount_cart_calculation(
        account_id=account_id,
        deal_id=promotion_response,
        zone=zone,
        environment=environment,
        deal_sku=sku,
        discount_type=discount_type,
        discount_value=discount_value,
        minimum_quantity=minimum_quantity
    )

    if promotion_response and cart_response:
        return promotion_response

    return False


def create_stepped_discount_with_limit(
        account_id: str,
        sku: str,
        zone: str,
        environment: str,
        index_range: int,
        discount_range: int,
        max_quantity: int,
        deal_id: str = None,
        discount_type: str = "percentOff",
        deal_type: str = "STEPPED_DISCOUNT") -> Optional[bool]:
    """
    Input a deal type stepped discount with max quantity to a specific \
    POC by calling the Promotion Relay Service and \
    Pricing Engine Relay Service.

    Parameters
    ----------
    account_id : str
        POC unique identifier.
    sku : str
        product unique identifier.
    zone : str
        e.g., AR, BR, CO, DO, MX, ZA or US.
    environment : str
        e.g, DEV, SIT, UAT.
    index_range : int
        range of quantity for the discount to be \
        applied (e.g., from 1 to 50).
    discount_range : int
        range of discount values to be applied \
        (e.g., 10% for the range 0 e 20% for the range 1).
    max_quantity : str
        deal limit.
    discount_type : str
        By default `percentOff`.
    deal_type : str
        e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD, \
        STEPPED_FREE_GOOD.
    deal_id : str
        Deal unique identifier.

    Returns
    -------
    Optional[bool]
        Whenever an error has occurred it returns `False`.
    """
    promotion_response = request_create_deal_v2(
        deal_type=deal_type,
        zone=zone,
        environment=environment,
        deal_id=deal_id
    )

    cart_response = create_stepped_discount_with_limit_cart_calculation(
        account_id=account_id,
        deal_id=promotion_response,
        zone=zone,
        environment=environment,
        sku=sku,
        quantity=max_quantity,
        index_range=index_range,
        discount_type=discount_type,
        discount_range=discount_range
    )

    if promotion_response and cart_response:
        return promotion_response

    return False


def create_stepped_discount(
        account_id: str,
        sku: str,
        zone: str,
        environment: str,
        ranges: int,
        deal_id: str = None,
        discount_type: str = "percentOff",
        deal_type: str = "STEPPED_DISCOUNT"):
    """
    Input a deal type stepped discount to a specific POC by calling the \
    Promotion Relay Service and Pricing Engine Relay Service.

    Parameters
    ----------
    account_id : str
        POC unique identifier.
    deal_id : str
        Deal unique identifier.
    sku : str
        Product unique identifier.
    zone: e.g., AR, BR, CO, DO, MX, ZA
    environment: e.g, DEV, SIT, UAT
    ranges: range of SKU quantities and discount values to be applied
    discount_type: percentOff
    deal_type: e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD,
        STEPPED_FREE_GOOD
    Returns: `promotion_response` if success
    """
    promotion_response = request_create_deal_v2(
        deal_type=deal_type,
        zone=zone,
        environment=environment,
        deal_id=deal_id
    )

    cart_response = request_create_stepped_discount_cart_calculation(
        account_id=account_id,
        deal_id=promotion_response,
        zone=zone,
        environment=environment,
        deal_sku=sku,
        discount_type=discount_type,
        ranges=ranges
    )

    if promotion_response and cart_response:
        return promotion_response

    return False


def create_free_good(
    account_id,
    sku_list,
    zone,
    environment,
    proportion,
    quantity,
    partial_free_good,
    need_to_buy_product,
    deal_id=None,
    deal_type='FREE_GOOD'
):
    """
    Input a deal type free good to a specific POC by calling the Promotion
    Relay Service and Pricing Engine Relay Service.
    Args:
        account_id: POC unique identifier
        deal_id: deal unique identifier
        sku_list: SKU list to offer as free good
        deal_type: e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD,
            STEPPED_FREE_GOOD
        zone: e.g., AR, BR, CO, DO, MX, ZA
        environment: e.g, DEV, SIT, UAT
        proportion: proportion for the free good to be applied
        quantity: quantity of SKUs to offer as free goods
        partial_free_good: partial SKU to be rescued
        need_to_buy_product: e.g., `Y` or `N`
    Returns: `promotion_response` if success
    """
    promotion_response = request_create_deal_v2(
        deal_type=deal_type,
        zone=zone,
        environment=environment,
        deal_id=deal_id
    )

    cart_response = request_create_free_good_cart_calculation(
        account_id=account_id,
        deal_id=promotion_response,
        zone=zone,
        environment=environment,
        sku_list=sku_list,
        proportion=proportion,
        quantity=quantity,
        partial_free_good=partial_free_good,
        need_buy_product=need_to_buy_product
    )

    if promotion_response and cart_response:
        return promotion_response

    return False


def create_stepped_free_good(
        account_id: str,
        sku: str,
        zone: str,
        environment: str,
        ranges: int,
        deal_id: str = None,
        deal_type: str = "STEPPED_FREE_GOOD"):
    """
    Input a deal type stepped free good to a specific POC by calling \
    the Promotion Relay Service and Pricing Engine. Relay Service.

    Parameters
    ----------
    account_id : str
        POC unique identifier.
    deal_id : str
        Deal unique identifier.
    sku : str
        Product unique identifier
    deal_type : str
        e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD, STEPPED_FREE_GOOD.
    zone : str
        e.g., AR, BR, CO, DO, MX, ZA or US.
    environment : str
        e.g, DEV, SIT, UAT.
    ranges : int
        Range of SKU quantities and free good values to be applied.

    Returns
    -------
        `promotion_response` if success.
    """
    promotion_response = request_create_deal_v2(
        deal_type=deal_type,
        zone=zone,
        environment=environment,
        deal_id=deal_id
    )

    cart_response = request_create_stepped_free_good_cart_calculation(
        account_id=account_id,
        deal_id=promotion_response,
        zone=zone,
        environment=environment,
        sku=sku,
        ranges=ranges
    )

    if promotion_response and cart_response:
        return promotion_response

    return False


def create_free_good_multivendor(
        vendor_account_id: str,
        zone: str,
        environment: str,
        vendor_item_ids: list,
        quantity: int = 10) -> Optional[str]:
    """
    Create free good multivendor.

    Parameters
    ----------
    vendor_account_id : str
    zone : str
    environment : str
    vendor_item_ids : list
    quantity : int, optional
        By default 10.

    Returns
    -------
    Optional[str]
        The response body.
    """
    request_headers = get_header_request(zone=zone)
    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/promotion-relay/v3/promotions"

    vendor_promotion_id = f"DM-{str(randint(1, 100000))}"

    body = {
        "vendorPromotionId": vendor_promotion_id,
        "title": f"Free Goods: {vendor_promotion_id}",
        "description": "Free Goods Promotion, Created by Data Mass",
        "type": "FREE_GOOD",
        "startDate": "2020-01-01T00:00:00.000Z",
        "endDate": "2050-03-31T23:59:59.999Z",
        "image": None,
        "budget": 10,
        "quantityLimit": quantity
    }

    response = place_request(
        request_method="POST",
        request_url=request_url,
        request_body=json.dumps([body]),
        request_headers=request_headers
    )

    if response.status_code in [200, 202]:
        request_url = f"{base_url}/deal-relay/v2"
        items_id = []

        for item in vendor_item_ids:
            item_id = item.get("sourceData", {}).get("vendorItemId")
            items_id.append(item_id)

        deal_body = {
            "vendorAccountIds": [vendor_account_id],
            "deals": [{
                "vendorDealId": vendor_promotion_id,
                "vendorPromotionId": vendor_promotion_id,
                "conditions": {
                    "lineItem": {
                        "vendorItemIds": items_id
                    }
                },
                "output": {
                    "lineItemDiscount": {
                        "vendorItemIds": items_id
                    }
                },
            }]
        }

        response = place_request(
            request_method="PUT",
            request_url=request_url,
            request_body=json.dumps(deal_body),
            request_headers=request_headers
        )

        if response.status_code in [200, 202]:
            return vendor_promotion_id

    return False


# Create Interactive Combos v1 List
def create_interactive_combos(
    account_id,
    sku,
    zone,
    environment,
    index_range,
    deal_type='FLEXIBLE_DISCOUNT'
):
    """
    Input a deal type interactive combos to a specific POC by calling the
    Promotion Relay Service and Pricing Engine
    Relay Service
    Args:
        account_id: POC unique identifier
        sku: product unique identifier
        zone: e.g., BR, CO, AR
        environment: e.g, DEV, SIT, UAT
        index_range: SKU quantity range for the discount to be applied
        deal_type: e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD, 
            STEPPED_FREE_GOOD, FLEXIBLE_DISCOUNT
    Returns: `promotion_response` if success
    """
    promotion_response = request_create_deal_v2(
        deal_type=deal_type,
        zone=zone,
        environment=environment
    )

    cart_response = request_create_interactive_combos_cart_calculation(
        account_id=account_id,
        deal_id=promotion_response,
        zone=zone,
        environment=environment,
        sku=sku,
        index_range=index_range
    )

    if promotion_response and cart_response:
        return promotion_response

    return False


def create_interactive_combos_v2(
    account_id,
    sku,
    zone,
    environment,
    index_range,
    deal_type='FLEXIBLE_DISCOUNT'
):
    """
    Create Interactive Combos v2 List.
    Input a deal type interactive combos to a specific POC by calling the
    Promotion Relay Service and Pricing Engine
    Relay Service
    Args:
        account_id: POC unique identifier
        sku: product unique identifier
        zone: e.g., BR, CO, AR
        environment: e.g, DEV, SIT, UAT
        index_range: range for the free good rule to be applied
        deal_type: e.g., DISCOUNT, STEPPED_DISCOUNT, FREE_GOOD,
            STEPPED_FREE_GOOD, FLEXIBLE_DISCOUNT
    Returns: `promotion_response` if success
    """
    promotion_response = request_create_deal_v2(
        deal_type=deal_type,
        zone=zone,
        environment=environment
    )

    cart_response = request_create_interactive_combos_cart_calculation_v2(
        account_id=account_id,
        deal_id=promotion_response,
        zone=zone,
        environment=environment,
        sku=sku,
        index_range=index_range
    )

    if promotion_response and cart_response:
        return promotion_response

    return False


def request_create_free_good_cart_calculation(
    account_id,
    deal_id,
    zone,
    environment,
    sku_list,
    proportion,
    quantity,
    partial_free_good,
    need_buy_product
):
    """
    Input deal type free good rules (API version 2) to the 
        Pricing Engine Relay Service
    Args:
        deal_id: deal unique identifier
        account_id: POC unique identifier
        sku_list: list of SKUs
        zone: e.g., BR, DO, CO
        environment: e.g., DEV, SIT, UAT
        sku_list: list of SKUs used as free goods
        proportion: proportion for the free good to be applied
        quantity: quantity of SKUs to offer as free goods
        partial_free_good: partial SKU to be rescued
        need_buy_product: e.g., `Y` or `N`
    Returns: Success if the request went ok and the 
        status code if there's a problem
    """

    # Define if free good promotion is partial sku rescue
    if partial_free_good.upper() == 'Y':
        boolean_partial_free_good = True
    else:
        boolean_partial_free_good = False

    # Change the accumulationType to UNIQUE only for AR
    if zone in ['AR', 'UY']:
        accumulation_type = 'UNIQUE'
    else:
        accumulation_type = None
        
    base_url = get_microservice_base_url(environment, False)
    
    # Get base URL
    if zone == "US":
        request_url = f"{base_url}/deal-relay/v2"
    else:
        request_url = f"{base_url}/deal-relay/v1"

    # Get deal's start and end dates
    dates_payload = return_first_and_last_date_year_payload()

    if need_buy_product.upper() == 'Y':
        path_file = 'data/create_free_good_payload_v2.json'
        # Create dictionary with deal's values
        dict_values = {
            'accounts': [account_id],
            'deals[0].dealId': deal_id,
            'deals[0].promotionId': deal_id,
            'deals[0].externalId': deal_id,
            'deals[0].accumulationType': accumulation_type,
            'deals[0].conditions.simulationDateTime.startDateTime': dates_payload['startDate'],
            'deals[0].conditions.simulationDateTime.endDateTime': dates_payload['endDate'],
            'deals[0].conditions.lineItem.skus': [sku_list[0]['sku']],
            'deals[0].output.freeGoods.proportion': proportion,
            'deals[0].output.freeGoods.partial': boolean_partial_free_good,
            'deals[0].output.freeGoods.freeGoods[0].skus[0].sku': sku_list[0]['sku'],
            'deals[0].output.freeGoods.freeGoods[0].skus[0].price': sku_list[0]['price'],
            'deals[0].output.freeGoods.freeGoods[0].quantity': quantity
        }
    else:
        path_file = 'data/create_free_good_no_buy_item_payload_v2.json'
        # Create dictionary with deal's values
        dict_values = {
            'accounts': [account_id],
            'deals[0].dealId': deal_id,
            'deals[0].promotionId': deal_id,
            'deals[0].externalId': deal_id,
            'deals[0].accumulationType': accumulation_type,
            'deals[0].quantityLimit': quantity,
            'deals[0].conditions.simulationDateTime.startDateTime': dates_payload['startDate'],
            'deals[0].conditions.simulationDateTime.endDateTime': dates_payload['endDate'],
            'deals[0].output.freeGoods.partial': boolean_partial_free_good,
            'deals[0].output.freeGoods.freeGoods[0].skus[0].sku': sku_list[0]['sku'],
            'deals[0].output.freeGoods.freeGoods[0].skus[0].price': sku_list[0]['price'],
            'deals[0].output.freeGoods.freeGoods[0].quantity': quantity
        }

    content = pkg_resources.resource_string("data_mass", path_file)
    json_data = json.loads(content.decode("utf-8"))

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get headers
    request_headers = get_header_request(zone, False, False, False, False)

    # Send request
    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
        return True
    else:
        print(text.Red + '\n- [Pricing Engine Relay Service] Failure to associate a deal. Response Status: '
                         '{response_status}. Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return False


def request_create_stepped_free_good_cart_calculation(account_id, deal_id, zone, environment, sku, ranges):
    """
    Input deal type stepped free good rules (API version 2) to the Pricing Engine Relay Service
    Args:
        deal_id: deal unique identifier
        account_id: POC unique identifier
        zone: e.g., BR, DO, CO
        environment: e.g., DEV, SIT, UAT
        sku: product unique identifier
        ranges: range of SKU quantities and free good values to be applied
    Returns: Success if the request went ok and the status code if there's a problem
    """

    # Change the accumulationType to UNIQUE only for AR
    if zone in ['AR', 'UY']:
        accumulation_type = 'UNIQUE'
    else:
        accumulation_type = None

    base_url = get_microservice_base_url(environment, False)

    # Get base URL
    if zone == "US":
        request_url = f"{base_url}/deal-relay/v2"
    else:
        request_url = f"{base_url}/deal-relay/v1"

    # Get deal's start and end dates
    dates_payload = return_first_and_last_date_year_payload()

    # Create dictionary with deal's values
    dict_values = {
        'accounts': [account_id],
        'deals[0].dealId': deal_id,
        'deals[0].promotionId': deal_id,
        'deals[0].externalId': deal_id,
        'deals[0].accumulationType': accumulation_type,
        'deals[0].conditions.simulationDateTime.startDateTime': dates_payload['startDate'],
        'deals[0].conditions.simulationDateTime.endDateTime': dates_payload['endDate'],
        'deals[0].conditions.scaledLineItem.skus': [sku],
        'deals[0].conditions.scaledLineItem.ranges[0].from': ranges[0]['start'],
        'deals[0].conditions.scaledLineItem.ranges[0].to': ranges[0]['end'],
        'deals[0].conditions.scaledLineItem.ranges[1].from': ranges[1]['start'],
        'deals[0].conditions.scaledLineItem.ranges[1].to': ranges[1]['end'],
        'deals[0].output.scaledFreeGoods.ranges[0].freeGoods[0].skus[0].sku': sku,
        'deals[0].output.scaledFreeGoods.ranges[0].freeGoods[0].quantity': ranges[0]['quantity'],
        'deals[0].output.scaledFreeGoods.ranges[0].proportion': ranges[0]['proportion'],
        'deals[0].output.scaledFreeGoods.ranges[1].freeGoods[0].skus[0].sku': sku,
        'deals[0].output.scaledFreeGoods.ranges[1].freeGoods[0].quantity': ranges[1]['quantity'],
        'deals[0].output.scaledFreeGoods.ranges[1].proportion': ranges[1]['proportion']
    }

    content = pkg_resources.resource_string(
        "data_mass",
        "data/create_stepped_free_good_payload_v2.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get headers
    request_headers = get_header_request(zone, False, False, False, False)

    # Send request
    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
        return True
    else:
        print(text.Red + '\n- [Pricing Engine Relay Service] Failure to associate a deal. Response Status: '
                         '{response_status}. Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return False


def request_create_discount_cart_calculation(account_id, deal_id, zone, environment, deal_sku, discount_type,
                                             discount_value, minimum_quantity):
    """
    Input deal type discount rules (API version 2) to the Pricing Engine Relay Service
    Args:
        deal_id: deal unique identifier
        account_id: POC unique identifier
        zone: e.g., BR, DO, CO
        environment: e.g., DEV, SIT, UAT
        deal_sku: SKU that will have discount applied
        discount_type: type of discount being applied (percent or amount)
        discount_value: value of discount being applied
        minimum_quantity: SKU minimum's quantity for the discount to be applied
    Returns: Success if the request went ok and the status code if there's a problem
    """
    # Get the correct discount type
    if discount_type == 'percentOff':
        discount_type = '%'

    # Change the accumulationType to UNIQUE only for AR
    if zone in ['AR', 'UY']:
        accumulation_type = 'UNIQUE'
    else:
        accumulation_type = None
        
    base_url = get_microservice_base_url(environment, False)

    # Get base URL
    if zone == "US":
        request_url = f"{base_url}/deal-relay/v2"
    else:
        request_url = f"{base_url}/deal-relay/v1"

    # Get deal's start and end dates
    dates_payload = return_first_and_last_date_year_payload()

    # Create dictionary with deal's values
    dict_values = {
        'accounts': [account_id],
        'deals[0].dealId': deal_id,
        'deals[0].promotionId': deal_id,
        'deals[0].externalId': deal_id,
        'deals[0].accumulationType': accumulation_type,
        'deals[0].conditions.simulationDateTime.startDateTime': dates_payload['startDate'],
        'deals[0].conditions.simulationDateTime.endDateTime': dates_payload['endDate'],
        'deals[0].conditions.lineItem.skus': [deal_sku],
        'deals[0].conditions.lineItem.minimumQuantity': minimum_quantity,
        'deals[0].output.lineItemDiscount.skus': [deal_sku],
        'deals[0].output.lineItemDiscount.type': discount_type,
        'deals[0].output.lineItemDiscount.discount': discount_value
    }
    
    content = pkg_resources.resource_string(
        "data_mass",
        "data/create_discount_payload_v2.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get headers
    request_headers = get_header_request(zone, False, False, False, False)

    # Send request
    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 202:
        return True

    print(
        f"{text.Red} \n"
        "- [Pricing Engine Relay Service] Failure to associate a deal."
        f"Response Status: {response.status_code}"
        f"Response message: {response.text}"
    )

    return False


def request_create_stepped_discount_cart_calculation(
    account_id, deal_id, zone, environment, deal_sku, discount_type, ranges
) -> bool:
    """
    Input deal type stepped discount rules (API version 2) to 
        the Pricing Engine Relay Service
    Args:
        deal_id: deal unique identifier
        account_id: POC unique identifier
        zone: e.g., BR, DO, CO
        environment: e.g., DEV, SIT, UAT
        deal_sku: SKU that will have discount applied
        discount_type: type of discount being applied (percent or amount)
        ranges: range of SKU quantities and discount values to be applied
    Returns: Success if the request went ok and the status code
        if there's a problem
    """

    # Get the correct discount type
    if discount_type == 'percentOff':
        discount_type = '%'

    # Change the accumulationType to UNIQUE only for AR
    if zone in ['AR', 'UY']:
        accumulation_type = 'UNIQUE'
    else:
        accumulation_type = None

    base_url = get_microservice_base_url(environment, False)

    # Get base URL
    if zone in ["US", "CA"]:
        request_url = f"{base_url}/deal-relay/v2"
    else:
        request_url = f"{base_url}/deal-relay/v1"

    # Get deal's start and end dates
    dates_payload = return_first_and_last_date_year_payload()

    # Create dictionary with deal's values
    dict_values = {
        'accounts': [account_id],
        'deals[0].dealId': deal_id,
        'deals[0].promotionId': deal_id,
        'deals[0].accumulationType': accumulation_type,
        'deals[0].conditions.simulationDateTime.startDateTime': dates_payload['startDate'],
        'deals[0].conditions.simulationDateTime.endDateTime': dates_payload['endDate'],
        'deals[0].conditions.scaledLineItem.skus': [deal_sku],
        'deals[0].conditions.scaledLineItem.ranges[0].from': ranges[0]['start'],
        'deals[0].conditions.scaledLineItem.ranges[0].to': ranges[0]['end'],
        'deals[0].conditions.scaledLineItem.ranges[1].from': ranges[1]['start'],
        'deals[0].conditions.scaledLineItem.ranges[1].to': ranges[1]['end'],
        'deals[0].output.lineItemScaledDiscount.ranges[0].skus': [deal_sku],
        'deals[0].output.lineItemScaledDiscount.ranges[0].type': discount_type,
        'deals[0].output.lineItemScaledDiscount.ranges[0].discount': ranges[0]['discount'],
        'deals[0].output.lineItemScaledDiscount.ranges[1].skus': [deal_sku],
        'deals[0].output.lineItemScaledDiscount.ranges[1].type': discount_type,
        'deals[0].output.lineItemScaledDiscount.ranges[1].discount': ranges[1]['discount']
    }

    content = pkg_resources.resource_string(
        "data_mass",
        "data/create_stepped_discount_payload_v2.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get headers
    request_headers = get_header_request(zone, False, False, False, False)

    # Send request
    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 202:
        return True

    print(
        f"{text.Red}\n-[Pricing Engine Relay Service] Failure to associate "
        f"a deal. Response Status: '{response.status_code}'. "
        f"Response message: '{response.text}'"
    )

    return False


def create_stepped_discount_with_limit_cart_calculation(
        account_id: str,
        deal_id: str,
        zone: str,
        environment: str,
        sku: str,
        quantity: int,
        index_range: str,
        discount_type: str,
        discount_range: str) -> bool:
    """
    Input deal type stepped discount rules (API version 2) to the Pricing \
    Engine Relay Service.

    Parametes
    ---------
    deal_id : str
        Deal unique identifier.
    account_id : str
        POC unique identifier.
    zone : str
        e.g., BR, AR, CO.
    environment : str
        e.g., DEV, SIT, UAT.
    sku : str
        Product unique identifier.
    quantity : int
        Quantity limit for the deal to be applied.
    discount_type : str
        Type of discount being applied (percent or amount).
    index_range : int
        Range of SKU quantities that the discount \
        is valid to be applied.
    discount_range : int
        Different discount values to be applied according \
        to the index_range parameter.

    Returns
    -------
    bool
        Whenever the creation is done successfully or not.
    """
    # Get the correct discount type
    if discount_type == 'percentOff':
        discount_type = '%'

    # Change the accumulationType to UNIQUE only for AR
    if zone in ['AR', 'UY']:
        accumulation_type = 'UNIQUE'
    else:
        accumulation_type = None

    base_url = get_microservice_base_url(environment, False)

    # Get base URL
    if zone == "US":
        request_url = f"{base_url}/deal-relay/v2"
    else:
        request_url = f"{base_url}/deal-relay/v1"

    # Get deal's start and end dates
    dates_payload = return_first_and_last_date_year_payload()

    # Create dictionary with deal's values
    dict_values = {
        'accounts': [account_id],
        'deals[0].dealId': deal_id,
        'deals[0].promotionId': deal_id,
        'deals[0].externalId': deal_id,
        'deals[0].accumulationType': accumulation_type,
        'deals[0].conditions.simulationDateTime.startDateTime': dates_payload['startDate'],
        'deals[0].conditions.simulationDateTime.endDateTime': dates_payload['endDate'],
        'deals[0].conditions.scaledLineItem.skus': [sku],
        'deals[0].conditions.scaledLineItem.ranges[0].from': index_range[0],
        'deals[0].conditions.scaledLineItem.ranges[0].to': index_range[1],
        'deals[0].output.lineItemScaledDiscount.ranges[0].skus': [sku],
        'deals[0].output.lineItemScaledDiscount.ranges[0].type': discount_type,
        'deals[0].output.lineItemScaledDiscount.ranges[0].discount': discount_range[0],
        'deals[0].output.lineItemScaledDiscount.ranges[0].maxQuantity': quantity
    }

    content = pkg_resources.resource_string(
        "data_mass",
        "data/create_stepped_discount_max_qtd_payload_v2.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get headers
    request_headers = get_header_request(zone, False, False, False, False)

    # Send request
    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 202:
        return True

    print(text.Red + '\n- [Pricing Engine Relay Service] Failure to associate a deal. Response Status: '
                        '{response_status}. Response message: {response_message}'
            .format(response_status=response.status_code, response_message=response.text))
    return False


def request_create_interactive_combos_cart_calculation(
        account_id: str,
        deal_id: str,
        zone: str,
        environment: str,
        sku: str,
        index_range: int) -> bool:
    """
    Input deal type stepped discount rules (API version 2) to the \
    Pricing Engine Relay Service.

    Parameters
    ----------
    deal_id : str
        Deal unique identifier.
    account_id : str
        POC unique identifier.
    zone : str
        e.g., BR, DO, CO.
    environment : str
        e.g., DEV, SIT, UAT.
    sku : str
        Product unique identifier.
    maxquantity : int
        Maximum quantity for each SKU to be applied.
    minquantity : int
        Minimum quantity for each SKU to be applied.

    Returns
    -------
    bool
        Whenever the creation is done successfully or not.
    """
    base_url = get_microservice_base_url(environment, False)

    # Get base URL
    if zone == "US":
        request_url = f"{base_url}/deal-relay/v2"
    else:
        request_url = f"{base_url}/deal-relay/v1"

    # Create dictionary with deal's values
    dict_values = {
        'accounts': [account_id],
        'deals[0].dealId': deal_id,
        'deals[0].promotionId': deal_id,
        'deals[0].externalId': deal_id,
        'deals[0].conditions.multipleLineItem.items[0].skus': [sku[0]['sku']],
        'deals[0].conditions.multipleLineItem.items[1].skus': [sku[1]['sku']],
        'deals[0].conditions.multipleLineItem.items[2].skus': [sku[2]['sku']],
        'deals[0].conditions.multipleLineItem.items[0].minimumQuantity': int(index_range['minimum'][0]),
        'deals[0].conditions.multipleLineItem.items[1].minimumQuantity': int(index_range['minimum'][1]),
        'deals[0].conditions.multipleLineItem.items[2].minimumQuantity': int(index_range['minimum'][2]),
        'deals[0].output.multipleLineItemDiscount.items[0].sku': sku[0]['sku'],
        'deals[0].output.multipleLineItemDiscount.items[1].sku': sku[1]['sku'],
        'deals[0].output.multipleLineItemDiscount.items[2].sku': sku[2]['sku'],
        'deals[0].output.multipleLineItemDiscount.items[0].value': sku[0]['price'],
        'deals[0].output.multipleLineItemDiscount.items[1].value': sku[1]['price'],
        'deals[0].output.multipleLineItemDiscount.items[2].value': sku[2]['price'],
        'deals[0].output.multipleLineItemDiscount.items[0].maxQuantity': int(index_range['maximum'][0]),
        'deals[0].output.multipleLineItemDiscount.items[1].maxQuantity': int(index_range['maximum'][1]),
        'deals[0].output.multipleLineItemDiscount.items[2].maxQuantity': int(index_range['maximum'][2])
    }

    content = pkg_resources.resource_string(
        "data_mass",
        "data/create_interactive_combos_payload_v1.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get headers
    request_headers = get_header_request(zone, False, False, False, False)

    # Send request
    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
        return True

    print(text.Red + '\n- [Pricing Engine Relay Service] Failure to associate a deal. Response Status: '
                        '{response_status}. Response message: {response_message}'
            .format(response_status=response.status_code, response_message=response.text))
    return False


def request_create_interactive_combos_cart_calculation_v2(
        account_id: str,
        deal_id: str,
        zone: str,
        environment: str,
        sku: str,
        index_range: int) -> bool:
    """
    Input deal type stepped discount rules (API version 2) to \
    the Pricing Engine Relay Service.

    Parameters
    ----------
    deal_id : str
        Deal unique identifier.
    account_id : str
        POC unique identifier.
    zone : str
        e.g., BR, AR, CO.
    environment : str
        e.g., DEV, SIT, UAT.
    sku : str
        Product unique identifier.
    index_range : int
        Quantity ranges for each SKU to be applied.

    Returns
    -------
    bool
        Whenever the creation is done successfully or not.
    """
    # Get base URL
    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/deal-relay/v1"

    # Create dictionary with deal's values
    dict_values = {

        'accounts': [account_id],
        'deals[0].dealId': deal_id,
        'deals[0].promotionId': deal_id,
        'deals[0].externalId': deal_id,
        'deals[0].conditions.multipleLineItem.items[0].skus': [sku[0]['sku'], sku[1]['sku']],
        'deals[0].conditions.multipleLineItem.items[1].skus': [sku[2]['sku']],
        'deals[0].conditions.multipleLineItem.items[0].minimumQuantity': int(index_range['minimum'][0]),
        'deals[0].conditions.multipleLineItem.items[1].minimumQuantity': int(index_range['minimum'][1]),
        'deals[0].output.multipleLineItemDiscount.items[0].sku': sku[0]['sku'],
        'deals[0].output.multipleLineItemDiscount.items[1].sku': sku[1]['sku'],
        'deals[0].output.multipleLineItemDiscount.items[2].sku': sku[2]['sku'],
        'deals[0].output.multipleLineItemDiscount.items[0].value': sku[0]['price'],
        'deals[0].output.multipleLineItemDiscount.items[1].value': sku[1]['price'],
        'deals[0].output.multipleLineItemDiscount.items[2].value': sku[2]['price'],
        'deals[0].output.multipleLineItemDiscount.items[0].maxQuantity': int(index_range['maximum'][0]),
        'deals[0].output.multipleLineItemDiscount.items[1].maxQuantity': int(index_range['maximum'][1]),
        'deals[0].output.multipleLineItemDiscount.items[2].maxQuantity': int(index_range['maximum'][2])
    }

    content = pkg_resources.resource_string(
        "data_mass",
        "data/create_interactive_combos_payload_v2.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get headers
    request_headers = get_header_request(zone, False, False, False, False)

    # Send request
    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 202:
        return True

    print(
        f"{text.Red}\n- [Pricing Engine Relay Service] "
        "Failure to associate a deal. "
        f"Response Status: {response.status_code}. "
        f"Response message: {response.text}"
    )

    return False


def request_delete_deal_by_id(
        account_id: str,
        zone: str,
        environment: str,
        data: dict):
    """
    Delete deal by ID via Promotion Relay Service v2.

    Parameters
    ----------
    account_id : str
        POC unique identifier.
    zone : str
        e.g., AR, BR, CO, DO, MX, ZA or US.
    environment : str
        e.g., SIT, UAT.
    data : dict
        Deals response payload.
    """
    # Create file path
    content = pkg_resources.resource_string(
        "data_mass",
        "data/delete_deal_payload.json"
    )

    json_data = json.loads(content.decode("utf-8"))

    # Get headers
    request_headers = get_header_request(zone, False, False, True, False)

    deal_ids = []
    for deal in range(len(data)):
        deal_id = data[deal]['promotionId']
        deal_ids.append(deal_id)

    dict_values = {
        'accounts': [account_id],
        'promotions': deal_ids
    }

    # Update the deal's values in runtime
    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    # Create body
    request_body = convert_json_to_string(json_object)

    # Get base URL
    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/promotion-relay/v2"

    # Send request
    response = place_request(
        request_method="DELETE",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code != 202:
        print(
            f"{text.Red}\n- [Promotion Relay Service] Failure to delete "
            f"the deal {deal_id}. "
            f"Response Status: {response.status_code}. "
            f"Response message: {response.text}"
        )

        return False


def request_delete_deals_pricing_service(
        account_id: str,
        zone: str,
        environment: str,
        data: dict) -> Optional[bool]:
    """
    Delete deal by ID form Pricing Conditions Service database.

    Parameters
    ----------
    account_id : str
        POC unique identifier.
    zone : str
        e.g., AR, BR, CO, DO, MX, ZA or US.
    environment : str
        e.g., SIT, UAT.
    data : dict
        Deals response payload.

    Returns
    -------
    Optional[bool]
        Whenever an error has occurred it returns `False`.
    """
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        use_root_auth=False,
        use_inclusion_auth=False,
        sku_product=False,
        account_id=account_id
    )

    for i in range(len(data)):
        deal_id = data[i]['dealId']

        base_url = get_microservice_base_url(environment)
        request_url = (
            f"{base_url}/cart-calculator/v1/account/"
            f"{account_id}/deals/{deal_id}"
        )

        response = place_request(
            request_method="DELETE",
            request_url=request_url,
            request_body="",
            request_headers=request_headers
        )

        if response.status_code not in [200, 202]:
            print(
                f"{text.Red}"
                "\n- [Pricing Conditions Service] Failure to delete the deal "
                f"{deal_id}. "
                f"Response Status: {response.status_code}. "
                f"Response message: {response.text}"
            )

            return False
