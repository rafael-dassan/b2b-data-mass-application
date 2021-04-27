import logging
import re
import urllib

from data_mass.classes.text import text
from data_mass.common import place_request
from data_mass.user.utils import (
    generate_otp,
    get_cookies,
    get_cookies_header,
    merge_cookies
    )


def assert_logon_request(user_name, password, params, authorize_response):
    payload = {
        "signInName": user_name,
        "password": password,
        "request_type": "RESPONSE"
    }

    headers = {
        "X-CSRF-TOKEN": authorize_response["CSRF"],
        "Cookie": get_cookies_header(authorize_response["COOKIES"])
    }

    url = params["BASE_SIGNIN_URL"] + "/{0}?tx={1}&p={2}".format(urllib.parse.quote(authorize_response["API"]),
                                                                 urllib.parse.quote(authorize_response["TRANS_ID"]),
                                                                 urllib.parse.quote(params["B2B_SIGNIN_POLICY"]))

    response = place_request("POST", url, payload, headers)

    logging.debug("Logon :: asserted() :: Response................: {response}".format(response=response))

    if response.status_code != 200:
        print("\n{0}- Fail [logon_selfassert_request]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                                             response.status_code,
                                                                                                             response.text))
        return False

    response_text = response.text
    logging.debug("Logon :: asserted() :: Response Text...........: {text}".format(text=response_text))
    data = response.json()
    status = data["status"]

    if status == "400":
        if "@registration_link" in response_text:
            logging.debug("Alert: The user doesn't exist.")
        if "@reset_password_link" in response_text:
            print("\n{0}- Fail [assert_logon_request]. The user exists but the password is wrong".format(text.Red))
            return "wrong_password"

    logging.debug("Logon :: asserted() :: JSON Status.............: {status}".format(status=status))

    data = {
        "CSRF": authorize_response["CSRF"],
        "API": authorize_response["API"],
        "TRANS_ID": authorize_response["TRANS_ID"],
        "COOKIES": merge_cookies(authorize_response["COOKIES"], get_cookies(response))
    }

    return data


def assert_response_error(assert_response):
    if assert_response.status_code != 200:
        return False

    response_text = assert_response.text
    try:
        status = re.search('\"status\":"([^"]+)', response_text).group(1)
        return int(status) != 200
    except AttributeError:
        print("\n{0}- Fail [assert_response_body]. Invalid response.".format(text.Red))
        return False


def assert_email_request(email, params, authorize_load_response):
    logging.debug("Calling assert_email_request...")

    data = {
        "email": email,
        "phone": "",
        "acceptTermsCheckOnSignup": "yes",
        "request_type": "RESPONSE"
    }

    headers = {
        "X-CSRF-TOKEN": authorize_load_response["CSRF"],
        "Cookie": get_cookies_header(authorize_load_response["COOKIES"])
    }

    url = params["BASE_SIGNUP_URL"] + "/{0}?tx={1}&p={2}".format(urllib.parse.quote(authorize_load_response["API"]),
                                                                 urllib.parse.quote(authorize_load_response["TRANS_ID"]),
                                                                 urllib.parse.quote(params["B2B_SIGNUP_POLICY"]))

    assert_email_response = place_request("POST", url, data, headers)

    if assert_response_error(assert_email_response):
        print("\n{0}- Fail [assert_email_request]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                                              assert_email_response
                                                                                                              .status_code,
                                                                                                              assert_email_response
                                                                                                              .text))
        if "Esta cuenta ya existe" in assert_email_response.text or "There is another user with this user name" in \
                assert_email_response.text:
            return "user_exists"
        return False
    else:
        return {
            "CSRF": authorize_load_response["CSRF"],
            "API": authorize_load_response["API"],
            "TRANS_ID": authorize_load_response["TRANS_ID"],
            "COOKIES": merge_cookies(authorize_load_response["COOKIES"], get_cookies(assert_email_response))
        }


def assert_otp_request(email, params, confirmed_email_response):
    logging.debug("Calling assert_otp_request...")
    data = {
        "readonlyEmail": urllib.parse.quote(email),
        "otp": generate_otp(params["OTP_SECRET"], params["OTP_INTERVAL"], email),
        "request_type": "RESPONSE"
    }

    headers = {
        "X-CSRF-TOKEN": confirmed_email_response["CSRF"],
        "Cookie": get_cookies_header(confirmed_email_response["COOKIES"])
    }

    url = params["BASE_SIGNUP_URL"] + "/{0}?tx={1}&p={2}".format(urllib.parse.quote(confirmed_email_response["API"]),
                                                                 urllib.parse.quote(confirmed_email_response["TRANS_ID"]),
                                                                 urllib.parse.quote(params["B2B_SIGNUP_POLICY"]))

    assert_otp_response = place_request("GET", url, data, headers)

    if assert_otp_response.status_code != 200:
        print("\n{0}- Fail [assert_otp_request]. Response status: {1}. Response message: {2}".format(text.Red),
              assert_otp_response.status_code, assert_otp_response.text)
        return False
    else:
        return {
            "CSRF": confirmed_email_response["CSRF"],
            "API": confirmed_email_response["API"],
            "TRANS_ID": confirmed_email_response["TRANS_ID"],
            "COOKIES": merge_cookies(confirmed_email_response["COOKIES"], get_cookies(assert_otp_response))
        }


def assert_name_request(email, params, confirmed_otp_response):
    logging.debug("Calling assert_name_request...")

    prefix_email = email.split("@")[0]
    data = {
        "givenName": prefix_email,
        "surname": prefix_email,
        "request_type": "RESPONSE"
    }

    headers = {
        "X-CSRF-TOKEN": confirmed_otp_response["CSRF"],
        "Cookie": get_cookies_header(confirmed_otp_response["COOKIES"])
    }

    url = params["BASE_SIGNUP_URL"] + "/{0}?tx={1}&p={2}".format(urllib.parse.quote(confirmed_otp_response["API"]),
                                                                 urllib.parse.quote(confirmed_otp_response["TRANS_ID"]),
                                                                 urllib.parse.quote(params["B2B_SIGNUP_POLICY"]))

    assert_name_response = place_request("POST", url, data, headers)

    if assert_response_error(assert_name_response):
        print("\n{0}- Fail [assert_name_request]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                                             assert_name_response
                                                                                                             .status_code,
                                                                                                             assert_name_response
                                                                                                             .text))
        return False
    else:
        return {
            "CSRF": confirmed_otp_response["CSRF"],
            "API": confirmed_otp_response["API"],
            "TRANS_ID": confirmed_otp_response["TRANS_ID"],
            "COOKIES": merge_cookies(confirmed_otp_response["COOKIES"], get_cookies(assert_name_response))
        }


def assert_password_request(password, params, confirmed_name_response):
    logging.debug("Calling assert_password_request...")
    data = {
        "newPassword": password,
        "request_type": "RESPONSE"
    }

    headers = {
        "X-CSRF-TOKEN": confirmed_name_response["CSRF"],
        "Cookie": get_cookies_header(confirmed_name_response["COOKIES"])
    }

    url = params["BASE_SIGNUP_URL"] + "/{0}?tx={1}&p={2}".format(urllib.parse.quote(confirmed_name_response["API"]),
                                                                 urllib.parse.quote(confirmed_name_response["TRANS_ID"]),
                                                                 urllib.parse.quote(params["B2B_SIGNUP_POLICY"]))

    assert_password_response = place_request("POST", url, data, headers)

    if assert_response_error(assert_password_response):
        # TODO: Check with the IAM team and validate why the response is
        # returned with code 200, even when an 400 error occurs, for example.
        # And, also check, regarding the password pattern.

        print(
            f"\n{text.Red}"
            "- Fail [assert_password_request]. "
            f"Response status: {assert_password_response.status_code}. "
            f"Response message: {assert_password_response.text}"
        )

        print(
            f"\n{text.Red}"
            "- [Suggestion]"
            " Password should contain alphanumeric special character and capital letter."
        )
        return False

    return {
        "CSRF": confirmed_name_response["CSRF"],
        "API": confirmed_name_response["API"],
        "TRANS_ID": confirmed_name_response["TRANS_ID"],
        "COOKIES": merge_cookies(confirmed_name_response["COOKIES"], get_cookies(assert_password_response))
    }


def assert_account_request(account_id, tax_id, params, authorize_account_response):
    logging.debug("Calling assert_account_request...")
    data = {
        "extension_accountid": account_id,
        "extension_value": tax_id,
        "request_type": "RESPONSE"
    }

    headers = {
        "X-CSRF-TOKEN": authorize_account_response["CSRF"],
        "Cookie": get_cookies_header(authorize_account_response["COOKIES"])
    }

    url = params["BASE_ONBOARDING_URL"] + "/{0}?tx={1}&p={2}".format(urllib.parse.quote(authorize_account_response["API"]),
                                                                     urllib.parse.quote(authorize_account_response["TRANS_ID"]),
                                                                     urllib.parse.quote(params["B2B_ONBOARDING_POLICY"]))

    assert_account_response = place_request("POST", url, data, headers)
    if assert_response_error(assert_account_response):
        print("\n{0}- Fail [assert_account_request]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                                assert_account_response.status_code,
                                                                                                assert_account_response.text))
        return False
    else:
        return {
            "CSRF": authorize_account_response["CSRF"],
            "API": authorize_account_response["API"],
            "TRANS_ID": authorize_account_response["TRANS_ID"],
            "COOKIES": merge_cookies(authorize_account_response["COOKIES"], get_cookies(assert_account_response))
        }
