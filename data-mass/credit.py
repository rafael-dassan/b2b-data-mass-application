from json import dumps
from common import *


# Include credit for account on microservice
def add_credit_to_account_microservice(accountId, zone, environment, credit, balance):
	# Define headers
	request_headers = get_header_request(zone, "false", "true")

	# Define URL Microservice
	request_url = get_microservice_base_url(environment) + 	"/account-relay/credits"

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
