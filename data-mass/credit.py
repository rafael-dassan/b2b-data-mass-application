import sys
from json import dumps

#Custom
from helpers.common import *

# Include credit for account on middleware
def add_credit_to_account(accountId, zone, env):
	# Define headers
	header = get_header_request(zone, "false", "true")

	# Define URL Middleware
	url = get_middleware_base_url(zone, env, "v5") + "/accounts/" + accountId + "/credit"

	credit = input("Desire credit (Default 5000): ")
	balance = input("Desire balance (Default 15000): ")

	if credit == "":
		credit = "5000"

	if balance == "":
		balance = "15000"

	credit = int(credit)
	balance = int(balance)

	# Body request
	request_body = dumps({
        "balance": balance,
        "available": credit,
        "overdue": 0,
        "paymentTerms": None,
        "total": (credit + balance)
    })

	# Send request
	response = place_request("POST", url, request_body, header)

	if response.status_code == 202:
		return "success"
	else:
		return response.status_code

# Include credit for account on microservice
def add_credit_to_account_microservice(accountId, zone, environment):
	# Define headers
	request_headers = get_header_request(zone, "false", "true")

	# Define URL Microservice
	request_url = get_microservice_base_url(environment) + 	"/account-relay/credits"

	credit = input("Desire credit (Default 5000): ")
	balance = input("Desire balance (Default 15000): ")

	if credit == "":
		credit = "5000"

	if balance == "":
		balance = "15000"

	credit = int(credit)
	balance = int(balance)
	
	# Body request
	request_body = dumps({
		"accountId": accountId,
		"available": credit,
		"balance": balance,
		"consumption": 0,
		"overdue": 0,
		"paymentTerms": None,
		"total": (credit + balance)
    })

	# Send request
	response = place_request("POST", request_url, request_body, request_headers)

	if response.status_code == 202:
		return "success"
	else:
		return response.status_code