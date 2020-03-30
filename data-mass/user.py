from json import loads
from common import *


# Try authenticate user
# Returns the accountId if the user authenticate successfully
# Returns 'false' otherwise
def authenticate_user(environment, country, user_name, password):
    url = get_magento_base_url(environment, country) + "/rest/V1/facade/authentication"

    # Define headers
    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "userName": user_name,
        "password": password
    }

    # Send request
    response = place_request("POST", url, convert_json_to_string(body), headers)
    json_data = loads(response.text)

    account_id_list = []

    if response.status_code == 200 and json_data != "":
        accounts = json_data.get("user").get("accounts")

        for account in accounts:
            account_id_list.append(account.get("custID"))

    return account_id_list


def create_user(environment, country, email, password, account):
    url = get_magento_base_url(environment, country) + "/rest/V1/accessmanagement/users"

    access_token = get_magento_access_token(environment, country)

    # Define headers
    headers = {
        "Content-Type": "application/json",
        "x-access-token": access_token
    }

    # Send request
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

    # Send request
    return place_request("POST", url, convert_json_to_string(data), headers)
