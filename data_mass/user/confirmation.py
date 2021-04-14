import logging
import re
import urllib

from data_mass.classes.text import text
from data_mass.tools.requests import place_request
from data_mass.user.utils import (
    get_cookies,
    get_cookies_header,
    merge_cookies,
)


def confirm_logon_request(params, self_asserted_response):
    url = params["BASE_SIGNIN_URL"] + "/api/" + self_asserted_response["API"] + "/confirmed"

    headers = {
        "csrf_token": self_asserted_response["CSRF"],
        "tx": self_asserted_response["TRANS_ID"],
        "p": params["B2B_SIGNIN_POLICY"],
        "Cookie": get_cookies_header(self_asserted_response["COOKIES"])
    }

    response = place_request("GET", url, None, headers)
    logging.debug("Logon :: confirmed() :: Response................: {response}".format(response=response))
    if response.status_code != 200:
        print("\n{0}- Fail [logon_confirm_request]. Response status: {1}. Response message: {2}".format(text.Red, response.status_code,
                                                                                                          response.text))
        return False

    response_text = response.text
    logging.debug("Logon :: confirmed() :: Response Text...........: {text}".format(text=response_text))

    if "id_token" in response_text:
        id_token = re.search(' id=\'id_token\' value=\'([^\']+)', response_text).group(1)
        logging.debug("Logon :: confirmed() :: Response Text...........: {text}".format(text=response_text))
        logging.debug("Logon :: confirmed() :: ID Token................: {value}".format(value=id_token))
        return id_token
    return False


def confirm_request(base_url, csrf, api, trans_id, b2b_signup_policy, cookies, csrf_response_required):
    headers = {"Cookie": get_cookies_header(cookies)}

    url = '{0}/api/{1}/confirmed?csrf_token={2}&tx={3}&p={4}'.format(base_url, urllib.parse.quote(api), urllib.parse.quote(csrf),
                                                                     urllib.parse.quote(trans_id), urllib.parse.quote(b2b_signup_policy))

    confirm_response = place_request("GET", url, None, headers)

    if confirm_response.status_code != 200:
        return False
    else:
        new_cookies = get_cookies(confirm_response)
        response_text = confirm_response.text

        try:
            new_csrf = re.search('\"csrf\":"([^"]+)', response_text).group(1)
        except AttributeError as e:
            logging.debug("Alert: csrf not found! Trying to get by header x-ms-cpim-csrf. Exception: {0}".format(str(e)))
            try:
                new_csrf = new_cookies["x-ms-cpim-csrf"]
            except KeyError:
                if csrf_response_required:
                    return False
                new_csrf = None

        if new_csrf is None:
            if "id_token" in response_text:
                id_token = re.search(' id=\'id_token\' value=\'([^\']+)', response_text).group(1)
                return {
                    "ID_TOKEN": id_token,
                    "COOKIES": new_cookies
                }
            else:
                logging.debug("Alert: Response_text: {0}".format(response_text))
                return False

        return {
            "CSRF": new_csrf,
            "API": api,
            "TRANS_ID": trans_id,
            "COOKIES": merge_cookies(cookies, new_cookies)
        }


def confirm_email_request(params, last_response):
    logging.debug("Calling confirm_email_request...")
    confirm_email_response = confirm_request(params["BASE_SIGNUP_URL"], last_response["CSRF"], last_response["API"],
                                                 last_response["TRANS_ID"], params["B2B_SIGNUP_POLICY"], last_response["COOKIES"], True)

    if not confirm_email_response:
        print("\n{0}- Fail [confirm_email_request]".format(text.Red))
        return False
    else:
        return confirm_email_response


def confirm_otp_request(params, last_response):
    logging.debug("Calling confirm_otp_request...")
    confirm_opt_response = confirm_request(params["BASE_SIGNUP_URL"], last_response["CSRF"], last_response["API"],
                                               last_response["TRANS_ID"], params["B2B_SIGNUP_POLICY"], last_response["COOKIES"], True)

    if not confirm_opt_response:
        print("\n{0}- Fail [confirm_otp_request]".format(text.Red))
        return False
    else:
        return confirm_opt_response


def confirm_name_request(params, last_response):
    logging.debug("Calling confirm_name_request...")
    confirm_name_response = confirm_request(params["BASE_SIGNUP_URL"], last_response["CSRF"], last_response["API"],
                                                last_response["TRANS_ID"], params["B2B_SIGNUP_POLICY"], last_response["COOKIES"], True)

    if not confirm_name_response:
        print("\n{0}- Fail [confirm_name_request]".format(text.Red))
        return False
    else:
        return confirm_name_response


def confirm_password_request(params, last_response):
    logging.debug("Calling confirm_password_request...")
    confirm_password_response = confirm_request(params["BASE_SIGNUP_URL"], last_response["CSRF"], last_response["API"],
                                                    last_response["TRANS_ID"], params["B2B_SIGNUP_POLICY"], last_response["COOKIES"], False)

    if not confirm_password_response:
        print("\n{0}- Fail [confirm_password_request]".format(text.Red))
        return False
    else:
        return confirm_password_response


def confirm_account_request(params, last_response):
    logging.debug("Calling confirm_account_request...")
    confirm_account_response = confirm_request(params["BASE_ONBOARDING_URL"], last_response["CSRF"], last_response["API"],
                                                   last_response["TRANS_ID"], params["B2B_ONBOARDING_POLICY"], last_response["COOKIES"],
                                                   False)

    if not confirm_account_response:
        logging.debug("Alert: Fail [confirm_account_request].")
        return False
    else:
        return confirm_account_response
