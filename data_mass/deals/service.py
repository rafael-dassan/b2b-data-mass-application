from json import loads
from typing import Optional, Union

from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.common import (
    get_header_request,
    get_microservice_base_url,
    place_request
)
from data_mass.config import get_settings


def request_get_combos_promo_fusion_service(
        zone: str,
        environment: str,
        account_id: str):
    """
    Get combos data from the Promo Fusion Service

    Parameters
    ----------
    account_id : str
        POC unique identifier.
    zone : str
        e.g., AR, BR, CO, DO, MX, ZA.
    environment : str
        e.g., DEV, SIT, UAT.

    Returns
    -------
    dict
        A new json_object.
    """
    # Get base URL
    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/catalog-service/combos"

    # Define headers
    request_headers = get_header_request(
        zone=zone, use_jwt_auth=True, account_id=account_id
    )
    request_headers.update({'custID': account_id, 'regionID': zone})

    # Send request
    response = place_request('GET', request_url, '', request_headers)
    combos = loads(response.text)

    if response.status_code == 200 and len(combos) != 0:
        return combos
    print(
        f"{text.Red}\n- [Catalog Service] Failure to retrieve combos. "
        f"Response Status: {response.status_code}. "
        f" Response message: {response.text}"
    )
    return False


def request_get_deals_promo_fusion_service(
        zone: str,
        environment: str,
        account_id: str) -> Optional[dict]:
    """
    Get deals data from the Promo Fusion Service.

    Parameters
    ----------
    account_id : str
        POC unique identifier.
    zone : str
        e.g., AR, BR, CO, DO, MX, ZA.
    environment : str
        e.g., DEV, SIT, UAT.

    Returns
    -------
    Optional[dict]
        New json_object.
    """
    # Get base URL
    base_url = get_microservice_base_url(environment)
    request_url = f"{base_url}/deal-service/v1?accountId={account_id}"

    # Define headers
    request_headers = get_header_request(
        zone=zone.lower(),
        use_jwt_auth=True,
        account_id=account_id
    )

    # Get base URL
    if zone in ["CA", "US"]:
        settings = get_settings()
        base_url = get_microservice_base_url(environment, False)

        request_headers.update({
            "vendorId": settings.vendor_id,
            "vendorAccountId": account_id
        })

        request_url = f"{base_url}/deal-service/v2"

    # Send request
    response = place_request('GET', request_url, '', request_headers)
    json_data = loads(response.text)

    if response.status_code == 200 and json_data:
        return json_data

    print(
        f"{text.Red}\n- [Deal Service] Failure to retrieve deals. "
        f"Response Status: {response.status_code}. "
        f" Response message: {response.text}"
    )

    return None


def request_get_deals_promotion_service(
        account_id: str,
        zone: str,
        environment: str) -> Union[bool, str, dict]:
    """
    Get deals data from the Promotion Service.

    Parameters
    ----------
    account_id : str
        POC unique identifier.
    zone : str
        e.g., AR, BR, CO, DO, MX, ZA or US.
    environment : str
        e.g., DEV, SIT, UAT.

    Returns
    -------
    Optional[bool, str, dict]
        new json_object.
    """

    base_url = get_microservice_base_url(environment)
    request_url = (
        f"{base_url}/promotion-service/"
        f"?accountId={account_id}&includeDisabled=false"
    )

    request_headers = get_header_request(
        zone, True, False, False, False, account_id
    )

    response = place_request('GET', request_url, '', request_headers)
    json_data = loads(response.text)

    if response.status_code == 200:
        deals = json_data['promotions']
        if len(deals) != 0:
            return deals
        else:
            print(
                f"{text.Yellow}\n- [Promotion Service] "
                f"The account {account_id} does not have deals associated"
            )
            return 'not_found'
    elif response.status_code == 404:
        print(
            f"{text.Yellow}\n- [Promotion Service] The account {account_id} "
            "does not have deals associated"
        )
        return 'not_found'
    print(
        f"{text.Red}\n- [Promotion Service] Failure to retrieve deals. "
        f"Response Status: {response.status_code}. "
        f"Response message: {response.text}."
    )
    return False


def request_get_deals_pricing_service(
        account_id: str,
        zone: str,
        environment: str) -> Union[bool, str, dict]:
    """
    Retrieve deals from Pricing Conditions Service.

    Parameteres
    -----------
    account_id : str
        POC unique identifier.
    zone : str
        e.g., AR, BR, CO, DO, MX, ZA.
    environment : str
        e.g., SIT, UAT.

    Returns
    -------
        `dict` if the deals exists, else and `str` \
        and `bool` in case of failure.
    """
    # Get headers
    request_headers = get_header_request(
        zone, True, False, False, False, account_id
    )

    # Get base URL
    base_url = get_microservice_base_url(environment)
    request_url = (
        f"{base_url}'/cart-calculator/v2/"
        f"accounts/{account_id}/deals?projection=PLAIN"
    )

    # Send request
    response = place_request('GET', request_url, '', request_headers)

    json_data = loads(response.text)
    if response.status_code == 200:
        return json_data['deals']
    elif response.status_code == 404:
        print(
            f"{text.Yellow} \n- [Pricing Conditions Service] The account "
            f"{account_id} does not have deals associated."
        )
        return 'not_found'
    print(
        f"{text.Red}\n- [Pricing Conditions Service] Failure to retrieve "
        f"deals for account {account_id}. "
        f"Response Status: {response.status_code}. "
        f"Response message: {response.text}."
    )
    return False


def display_deals_information_promotion(deals):
    """
    Display deals information from the Promotion Service
    Args:
        deals: deals object
    Returns: a table containing the available deals information
    """
    promotion_information = list()

    for i in range(len(deals)):
        promotion_values = {
            'ID': deals[i]['id'],
            'Type': deals[i]['type'],
            'Title': deals[i]['title'],
            'End Date': deals[i]['endDate']
        }
        promotion_information.append(promotion_values)

    print(text.default_text_color + '\nPromotion Information')
    print(tabulate(
        promotion_information,
        headers='keys',
        tablefmt='fancy_grid'
    ))


def display_deals_information_multivendor(
        vendor_account_id: str,
        deals: list):
    """
    Display, using tabulate, deals and combos.

    Parameters
    ----------
    vendor_account_id : str
    deals : list
    """
    response = []

    if deals:
        for deal in deals:
            output = list(deal.get("output", {}))
            deal_type = output[0] if output else None
            items = []

            if deal_type == "freeGoods":
                output = deal.get("output", {})
                deal_items, = output.get(deal_type, {}).get("items", [])

                for item in deal_items.get("vendorItems", {}):
                    items.append(item.get("vendorItemId"))
            elif deal_type == "multipleLineItemDiscount":
                output = deal.get("output", {})
                deal_items = output.get(deal_type, {}).get("items", [])

                for item in deal_items:
                    items.append(item.get("vendorItemId"))
            else:
                output = deal.get("output", {})
                items = output.get(deal_type, {}).get("vendorItemIds")

            response.append({
                "Id": deal.get("vendorDealId"),
                "Type": deal_type,
                "Items": ", ".join(items) if isinstance(items, list) else items
            })

        print(tabulate(response, headers='keys', tablefmt='fancy_grid'))
    else:
        print(
            f"{text.Yellow}\n"
            "- There is no promotion available "
            f"for the account {vendor_account_id}"
        )


def display_deals_information_promo_fusion(
        account_id: str,
        deals: dict,
        combos: dict):
    """
    Display deals information from the Promo Fusion Service.

    Parameters
    ----------
    account_id : str
        POC unique identifier.
    deals : dict
        Deals object.
    combos : dict
        Combos object.
    """
    combo_information = []

    if not combos.get("combos"):
        print(
            f"{text.Yellow}\n- There is no combo available for the "
            f"account {account_id}"
        )
    else:
        for combo in combos.get('combos'):
            combo_values = {
                'ID': combo.get('id'),
                'Type': combo.get('type'),
                'Title': combo.get('title'),
                'Original Price': combo.get('originalPrice'),
                'Price': combo.get('price'),
                'Stock Available': combo.get('availableToday')
            }
            combo_information.append(combo_values)

        print(text.default_text_color + '\nCombo Information')
        print(tabulate(
            combo_information,
            headers='keys',
            tablefmt='fancy_grid'
        ))

    if not deals.get("deals"):
        print(
            f"{text.Yellow}\n- There is no deal available "
            f"for the account {account_id}"
        )
    else:
        deal_info = []
        for deal in deals.get('deals'):
            name = list(deal.get('output'))[0]
            if name == 'freeGoods':
                id_ = deal['dealId']
                temp_skus = deal['output'][name]['items'][0]['skus'][:]
                skus = []
                for temp_sku in temp_skus:
                    skus.append(temp_sku['sku'])
                    skus = list(set(skus))
                deal_info.append({
                    'id': id_,
                    'type': name,
                    'skus': skus
                })
            elif name == 'lineItemDiscount':
                id_ = deal['dealId']
                temp_skus = deal['output'][name]
                skus = []
                for temp_sku in temp_skus['skus']:
                    skus.append(temp_sku)
                    skus = list(set(skus))
                deal_info.append({
                    'id': id_,
                    'type': name,
                    'skus': skus
                })
            elif name == 'multipleLineItemDiscount':
                id_ = deal['dealId']
                temp_skus = deal['output'][name]['items'][:]
                skus = []
                for temp_sku in temp_skus:
                    skus.append(temp_sku['sku'])
                    skus = list(set(skus))
                deal_info.append({
                    'id': id_,
                    'type': name,
                    'skus': skus
                })
            elif name == 'lineItemScaledDiscount':
                id_ = deal['dealId']
                temp_skus = deal['output'][name][:]
                skus = []
                for temp_sku in temp_skus:
                    skus.append(temp_sku['skus'][0])
                    skus = list(set(skus))
                deal_info.append({
                    'id': id_,
                    'type': name,
                    'skus': skus
                })
            elif name == 'scaledFreeGoods':
                id_ = deal['dealId']
                temp_skus = deal['output'][name]["0"]["items"][0]['skus'][:]
                skus = []
                for temp_sku in temp_skus:
                    skus.append(temp_sku['sku'])
                deal_info.append({
                    'id': id_,
                    'type': name,
                    'skus': skus
                })
        print(text.default_text_color + '\nDeal Information')
        print(tabulate(deal_info, headers='keys', tablefmt='fancy_grid'))
