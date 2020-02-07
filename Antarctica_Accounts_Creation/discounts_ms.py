import sys
from json import dumps
from uuid import uuid1

# Custom
from helper import *

# Input discount rule by payment method
def inputDiscountByPaymentMethod(accounts, zone, environment, paymentMethod, typeDiscount, valueDiscount):

    request_url = get_microservice_base_url(environment) + '/cart-calculation-relay/deals'
    if typeDiscount == 1:
        strTypeDiscount = "percentOff"
    else:
        strTypeDiscount = "amountOff"

    request_body = dumps({
        "accounts": accounts,
        "deals": [
            {
                "dealId": "ANTARCTICA-" + str(uuid1()) + '-paymentMethod',
                "dealRules": {
                    "dealPaymentMethodRule": {
                        "paymentMethod": paymentMethod
                    }
                },
                "dealOutput": {
                    "dealOutputTotalDiscount": {
                        strTypeDiscount: valueDiscount
                    }
                },
                "externalId": "ANTARCTICA-" + str(uuid1()) + '-paymentMethod'
            }
        ]
    })

    request_headers = get_header_request(zone, 'false', 'false')

    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
	    return 'success'
    else:
        return response.status_code

# Input discount rule by deliveryDate
def inputDiscountByDeliveryDate(accounts, zone, environment, listDates, typeDiscount, valueDiscount):

    request_url = get_microservice_base_url(environment) + '/cart-calculation-relay/deals'
    if typeDiscount == 1:
        strTypeDiscount = "percentOff"
    else:
        strTypeDiscount = "amountOff"

    request_body = dumps({
        "accounts": accounts,
        "deals": [
            {
                "dealId": "ANTARCTICA-" + str(uuid1()) + '-deliveryDate',
                "dealRules": {
                    "dealDeliveryDateRules": [
                        {
                            "startDate": listDates['startDate'],
                            "endDate": listDates['endDate']
                        }
                    ]
                },
                "dealOutput": {
                    "dealOutputTotalDiscount": {
                        strTypeDiscount: valueDiscount
                    }
                },
                "externalId": "ANTARCTICA-" + str(uuid1()) + '-deliveryDate',
            }
        ]
    })

    request_headers = get_header_request(zone, 'false', 'false')

    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
	    return 'success'
    else:
        return response.status_code

# Input discount rule by sku
def inputDiscountBySku(accounts, zone, environment, listOffers, typeDiscount, valueDiscount):

    request_url = get_microservice_base_url(environment) + '/cart-calculation-relay/deals'
    if typeDiscount == 1:
        strTypeDiscount = "percentOff"
    else:
        strTypeDiscount = "amountOff"

    request_body = dumps({
        "accounts": accounts,
        "deals": [
            {
                "dealId": "ANTARCTICA-" + str(uuid1()) + '-bySku',
                "dealRules": {
                    "dealSKURule": {
                        "skus": listOffers,
                        "minimumQuantity": 1
                    }
                },
                "dealOutput": {
                    "dealOutputSKUDiscount": {
                        "skus": listOffers,
                        strTypeDiscount: valueDiscount,
                        "maxQuantity": 1000
                    }
                },
                "externalId": "ANTARCTICA-" + str(uuid1()) + '-bySku',
            }
        ]
    })

    request_headers = get_header_request(zone, 'false', 'false')

    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
	    return 'success'
    else:
        return response.status_code


def inputFreeGoodsSelection(accounts, zone, environment, minimumQuantityPurchase, quantitySkusEarn, quantityMultiplierSku, skusPurchase, skusFreeGoods, paymentMethod):
    request_url = get_microservice_base_url(environment) + '/cart-calculation-relay/deals'

    request_body = dumps({
        "accounts": accounts,
        "deals": [
            {
                "dealId": "ANTARCTICA-" + str(uuid1()) + '-bySku',
                "dealRules": {
                    "dealSKURule": {
                        "skus": skusPurchase,
                        "minimumQuantity": minimumQuantityPurchase
                    },
                    "dealPaymentMethodRule": {
                        "paymentMethod": paymentMethod
                    }
                },
                "dealOutput": {
                    "dealOutputFreeGoods": {
                        "skus": skusFreeGoods,
                        "quantity": quantitySkusEarn,
                        "quantityDivisor": quantityMultiplierSku
                    }
                },
                "externalId": "ANTARCTICA-" + str(uuid1()) + '-bySku',
            }
        ]
    })

    request_headers = get_header_request(zone, 'false', 'false')

    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
	    return 'success'
    else:
        return response.status_code
