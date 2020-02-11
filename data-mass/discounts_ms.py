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
        print(' -- Skus Need Purchase -- ')
        print(skusPurchase)
        print(' -- Skus quantity need purchase -- ')
        print(minimumQuantityPurchase)
        print(' -- Payment method applied -- ')
        print(paymentMethod)
        print(' -- Skus can be select -- ')
        print(skusFreeGoods)
        return 'success'
    else:
        return response.status_code

# Input stepped discount for an account
def inputSteppedDiscount(accounts, zone, environment, skuDiscount):
    request_url = get_microservice_base_url(environment) + '/cart-calculation-relay/deals'

    request_body = dumps({
        "accounts": accounts,
        "deals": [
            {
                "dealId": "ANTARCTICA-" + str(uuid1()) + '-SteppedD',
                "dealRules": {
                    "dealSKUScaledRule": {
                        "skus": skuDiscount,
                        "ranges": [
                            {
                                "rangeIndex": 0,
                                "from": 10,
                                "to": 20
                            },
                            {
                                "rangeIndex": 1,
                                "from": 21,
                                "to": 30
                            }
                        ]
                    }
                },
                "dealOutput": {
                    "dealOutputSKUScaledDiscount": [
                        {
                            "rangeIndex": 0,
                            "skus": skuDiscount,
                            "percentOff": 10.0
                        },
                        {
                            "rangeIndex": 1,
                            "skus": skuDiscount,
                            "percentOff": 20.0
                        }
                    ]
                },
                "externalId": "ANTARCTICA-" + str(uuid1()) + '-SteppedD'
            }
        ]
    })

    request_headers = get_header_request(zone, 'false', 'false')

    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 202:
        print('Skus you need to purchase: ' + str(skuDiscount))
        print('Description: Buy from 10 to 20 and get 10% off. Buy from 21 to 30 and get 20%')
        return 'success'
    else:
        return response.status_code

# Input stepped discount for an account
def inputSteppedFreeGood(accounts, zone, environment, skuFreeGood):
    request_url = get_microservice_base_url(environment) + '/cart-calculation-relay/deals'

    request_body = dumps({
        "accounts": accounts,
        "deals": [
            {
                "dealId": "ANTARCTICA-" + str(uuid1()) + '-SteppedFG',
                "dealRules": {
                    "dealSKUScaledRule": {
                        "skus": skuFreeGood,
                        "ranges": [
                            {
                                "rangeIndex": 0,
                                "from": 10,
                                "to": 20
                            },
                            {
                                "rangeIndex": 1,
                                "from": 21,
                                "to": 30
                            }
                        ]
                    }
                },
                "dealOutput": {
                    "dealOutputScaledFreeGoods": [
                        {
                            "rangeIndex": 0,
                            "skus": skuFreeGood,
                            "quantity": 1,
                            "measureUnit": "UNIT"
                        },
                        {
                            "rangeIndex": 1,
                            "skus": skuFreeGood,
                            "quantity": 2,
                            "measureUnit": "UNIT"
                        }
                    ]
                },
                "externalId": "ANTARCTICA-" + str(uuid1()) + '-SteppedFG'
            }
        ]
    })

    request_headers = get_header_request(zone, 'false', 'false')

    response = place_request('PUT', request_url, request_body, request_headers)
    if response.status_code == 202:
        print('Skus you need to purchase: ' + str(skuFreeGood))
        print('Descprition: Buy from 10 to 20 and get 1 item. Buy from 21 to 30 and get 2')
        return 'success'
    else:
        return response.status_code