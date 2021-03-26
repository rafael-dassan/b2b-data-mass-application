# Standard library imports
import re
import logging

# Local application imports
from classes.text import text
from common import place_request, get_magento_base_url, get_magento_user_registration_access_token, \
    convert_json_to_string
from user_v3 import get_iam_b2c_params


def delete_user_v3(environment, country, user_name):
    iam_b2c_params = get_iam_b2c_params(environment, country)
    response_delete_magento = delete_user_magento(environment, country, user_name)
    response_delete_azure = delete_user_azure(user_name, iam_b2c_params)

    if response_delete_magento == "false" and response_delete_azure == "false":
        return "false"
    if response_delete_magento == "false" or response_delete_azure == "false":
        return "partial"
    return "success"


def delete_user_magento(environment, country, user_name):
    magento_url = get_magento_base_url(environment, country)
    magento_token = get_magento_user_registration_access_token(environment, country)

    user_id = get_user_id_magento(magento_url, magento_token, user_name)
    if user_id == "false":
        return "false"

    url = "{0}/rest/V1/customers/{1}?XDEBUG_SESSION_START=PHPSTORM".format(magento_url, user_id)
    headers = get_magento_header(magento_token)

    response = place_request("DELETE", url, None, headers)
    if response.status_code != 200:
        print("\n{0}- Fail [delete_user_magento]. Response status: {1}. Response message: {2}".format(text.Red, response.status_code,
                                                                                                      response.text))
        return "false"

    return response


def get_user_id_magento(magento_url, magento_token, user_name):
    payload = {
        "contacts": [{
            "type": get_user_name_type(user_name),
            "value": user_name
        }]
    }

    url = "{0}/rest/V1/accessmanagement/users/verify-contacts".format(magento_url)
    headers = get_magento_header(magento_token)

    response = place_request("POST", url, convert_json_to_string(payload), headers)
    logging.debug("Get user Magento :: Response................: {response}".format(response=response))

    if response.status_code != 200:
        print("\n{0}- Fail on get user Magento [get_user_id_magento]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                                                          response
                                                                                                                          .status_code,
                                                                                                                          response.text))
        return "false"

    response_text = response.text
    logging.debug("Get user Magento :: Response Text...........: {text}".format(text=response_text))

    magento_response = response.json()
    if len(magento_response) == 0 or not magento_response[0]["customer_id"]:
        print("\n{0}- User Magento not found [get_user_id_magento]: {1}".format(text.Red, user_name))
        return "false"

    return magento_response[0]["customer_id"]


def get_user_name_type(user_name):
    user_name_type = "EMAIL"

    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not email_regex.match(user_name):
        user_name_type = "CELLPHONE"

    return user_name_type


def get_magento_header(magento_token):
    headers = {
        "X-Access-Token": magento_token,
        "Content-Type": "application/json"
    }
    return headers


def delete_user_azure(user_name, iam_b2c_params):
    token = get_token_azure(iam_b2c_params)
    if token == "false":
        return "false"

    user_id = get_user_id_azure(user_name, iam_b2c_params, token)
    if user_id == "false":
        return "false"

    headers = {
        "Authorization": "Bearer {0}".format(token)
    }

    url = "https://graph.microsoft.com/v1.0/users/{0}".format(user_id)

    response = place_request("DELETE", url, None, headers)

    if response.status_code != 204:
        print("\n{0}- Fail on delete user Azure [delete_user_azure]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                                                         response
                                                                                                                         .status_code,
                                                                                                                         response.text))
        return "false"

    return response


def get_token_azure(iam_b2c_params):
    payload = {
        "client_id": iam_b2c_params["AZURE_CLIENT_ID"],
        "client_secret": iam_b2c_params["AZURE_CLIENT_SECRET"],
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials"
    }

    headers = {
        "Host": "login.microsoftonline.com",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    url = "https://login.microsoftonline.com/{0}/oauth2/v2.0/token".format(iam_b2c_params["B2B_PATH"])

    response = place_request("POST", url, payload, headers)
    logging.debug("Get token Azure :: Response................: {0}".format(response))

    if response.status_code != 200:
        print("\n{0}- Fail on get token Azure [get_token_azure]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                                                     response.status_code,
                                                                                                                     response.text))
        return "false"

    response_text = response.text
    logging.debug("Get token Azure :: Response Text...........: {0}".format(response_text))

    azure_response = response.json()
    token = azure_response["access_token"]

    return token


def get_user_id_azure(user_name, iam_b2c_params, token):
    headers = {
        "Authorization": "Bearer {0}".format(token)
    }

    url = "https://graph.microsoft.com/v1.0/users?$select=id,displayName&$filter=identities/any(c:c/issuerAssignedId eq '{0}' and " \
          "c/issuer eq '{1}')".format(user_name.replace("+", "%2B"), iam_b2c_params["B2B_PATH"])

    response = place_request("GET", url, None, headers)

    logging.debug("Get user Azure :: Response................: {response}".format(response=response))

    if response.status_code != 200:
        print("\n{0}- Fail on get user Azure [get_user_id_azure]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                                                      response.status_code,
                                                                                                                      response.text))
        return "false"

    response_text = response.text
    logging.debug("Get user Azure :: Response Text...........: {text}".format(text=response_text))

    azure_response = response.json()
    value_response = azure_response["value"]

    if len(value_response) == 0 or not value_response[0]["id"]:
        print("\n{0}- User Azure not found [get_user_id_azure]: {1}".format(text.Red, user_name))
        return "fail"

    return value_response[0]["id"]
