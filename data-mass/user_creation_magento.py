from json import loads
from common import *


# Try authenticate user
def authenticate_user(environment, country, user_name, password):
    url = get_magento_base_url(environment, country) + "/rest/V1/facade/authentication"

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "userName": user_name,
        "password": password
    }

    response = place_request("POST", url, convert_json_to_string(body), headers)
    json_data = loads(response.text)

    if response.status_code == 200 and json_data != "":
        print("Authentication successful")
        return json_data
    else:
        print("- Authentication failed: '" + response.text + "'.")
        return "fail"


# Returns the accountId if the user authenticate successfully
def get_user_accounts(environment, country, user_name, password):
    json_data = authenticate_user(environment, country, user_name, password)

    account_id_list = []

    if json_data != "fail":
        accounts = json_data.get("user").get("accounts")
        for account in accounts:
            account_id_list.append(account.get("custID"))

    return account_id_list


def create_user(environment, country, email, password, account):
    url = get_magento_base_url(environment, country) + "/rest/V1/accessmanagement/users"

    access_token = get_magento_access_token(environment, country)

    headers = {
        "Content-Type": "application/json",
        "x-access-token": access_token
    }

    response = create_user_request(url, account, headers, email, password)

    if response.status_code == 200:
        return "success"
    else:
        print("- Fail on create user: '" + response.text + "'.")
        return response.status_code


def create_user_request(url, account, headers, email, password):
    name = email.split("@")[0]
    data = {
        "firstName": name,
        "lastName": name,
        "password": password,
        "phoneVerified": 'false',
        "email": email,
        "phone": "",
        "emailVerified": 'true',
        "account": account
    }

    return place_request("POST", url, convert_json_to_string(data), headers)


def user_already_exists_with_account(environment, country, username, password, account_id):
    account_id_list = get_user_accounts(environment, country, username, password)

    if len(account_id_list) > 0:
        if account_id in account_id_list:
            return True

    return False


def associate_user_to_account(environment, country, user, account):
    response = associate_user_to_account_request(environment, country, user, account)
    if response.status_code == 200:
        return "success"
    else:
        print("- Fail on associate user to account: '" + response.text + "'.")
        return response.status_code


def associate_user_to_account_request(environment, country, user, account):
    region_id = get_region_id(country)

    headers = {
        "Content-Type": "application/json",
        "X-Access-Token": user['token'],
        "custID": user['user']['accounts'][0]["custID"],
        "regionID": region_id
    }

    data = {
        "inviterEmail": "",
        "inviteeEmail": "",
        "invoiceDate": "",
        "customerSoldToNumber": "",
        "customerID": account['accountId'],
        "taxID": account["taxId"],
        "invoiceID": "",
        "postalCode": "",
        "zipCode": "",
        "regionID": region_id
    }

    base_url = get_magento_base_url(environment, country)

    return place_request("POST", base_url + "/rest/V1/facade/accounts/connect", convert_json_to_string(data), headers)
