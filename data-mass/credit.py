import sys
from json import dumps

#Custom
from helpers.common import *

# Include credit in middleware account
def add_credit_to_account(accountId, zone, env):
	# Define headers
	header = get_header_request(zone, 'false', 'true')

	# Define URL Middleware
	url = get_middleware_base_url(zone, env, "v5") + "/accounts/" + accountId + "/credit"

	credit = input("Desire credit (Default 5000):")
	balance = input("Desire balance (Default 15000):")

	if credit == "":
		credit = "5000"

	if balance == "":
		balance = "15000"

	credit = int(credit)
	balance = int(balance)

	# Body request
	request_body = dumps({
        "balance": balance,
        "creditAvailable": credit,
        "overdue": 0,
        "paymentTerms": "CASH",
        "total": (credit + balance)
    })

	# Send request
	response = place_request("POST", url, request_body, header)

	if response.status_code == 202:
		return 'success'
	else:
		return response.status_code


def add_credit_to_account_microservice(accountId, zone, environment):
	credit = input("Desire credit (Default 5000):")
	balance = input("Desire balance (Default 15000):")
	paymentMethod = printPaymentMethodMenu(zone)

	if credit == "":
		credit = "5000"

	if balance == "":
		balance = "15000"
	
	if paymentMethod == '':
		paymentMethod = 'CASH'

	credit = int(credit)
	balance = int(balance)

	request_headers = get_header_request(zone, 'false', 'true')
	request_url = get_microservice_base_url(environment) + 	'/account-relay/credits'
	request_body = dumps({
		"accountId": accountId,
		"available": credit,
		"balance": balance,
		"consumption": 0,
		"overdue": 0,
		"paymentTerms": paymentMethod.upper(),
		"total": (credit + balance)
    })

	response = place_request('POST', request_url, request_body, request_headers)
	if response.status_code == 202:
		return 'success'
	else:
		return response.status_code

def printPaymentMethodMenu(zone):
	if zone.upper() == 'BR':
		paymentMethod = input("Define the type of credit payment method to be entered (1- CASH, 2- BANK_SLIP):")
		switcher = {
			'1': 'CASH',
			'2': 'BANK_SLIP'
		}

		paymentMethod = switcher.get(paymentMethod, "")
	elif zone.upper() == 'DR':
		paymentMethod = input("Define the type of credit payment method to be entered (1- CASH, 2- CREDIT):")
		switcher = {
			'1': 'CASH',
			'2': 'CREDIT'
		}

		paymentMethod = switcher.get(paymentMethod, "")
	else:
		paymentMethod = 'CASH'
	
	return paymentMethod
