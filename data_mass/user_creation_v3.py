# Standard library imports
import re
import urllib.parse
import uuid
import base64
import logging

# Third party imports
import pyotp

# Local application imports
from .classes.text import text
from .common import place_request
from .user_v3 import get_iam_b2c_params


def authenticate_user_iam(environment, country, user_name, password):
    params = get_iam_b2c_params(environment, country)

    logging.debug("Calling logon_authorize_request...")
    authorize_iam_response = authorize_iam(params)
    if authorize_iam_response == "false":
        return "false"

    logging.debug("Calling logon_selfasserted_request...")
    self_asserted_response = self_asserted_logon_request(user_name, password, params, authorize_iam_response)
    if self_asserted_response == "false" or self_asserted_response == "wrong_password":
        return self_asserted_response

    logging.debug("Calling logon_confirmed_request...")
    id_token = confirmed_logon_request(params, self_asserted_response)
    if id_token == "false":
        return "false"

    return id_token


def authorize_iam(params):
    payload = {
        "response_mode": "form_post",
        "ui_locales": "es",
        "response_type": "id_token",
        "redirect_uri": params["REDIRECT_URL"],
        "client_id": params["CLIENT_ID"],
        "uuid_nonce": uuid.uuid4().hex,
        "state": "{0}-{1}".format(params["B2B_SIGNIN_POLICY"], uuid.uuid4().hex),
        "scope": "openid"
    }

    url = params["BASE_SIGNIN_URL"] + "/oauth2/authorize"

    authorize_response = place_request("POST", url, payload, None)

    logging.debug("Logon :: authorize() :: Response................: {response}".format(response=authorize_response))

    if authorize_response.status_code != 200:
        print("\n{0}- Fail [authorize_load_request]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                                         authorize_response.status_code,
                                                                                                         authorize_response.text))
        return "false"

    response_text = authorize_response.text
    csrf = re.search('\"csrf\":"([^"]+)', response_text).group(1)
    api = re.search('\"api\":"([^"]+)', response_text).group(1)
    trans_id = re.search('\"transId\":"([^"]+)', response_text).group(1)

    logging.debug("Logon :: authorize() :: CSRF....................: {csrf}".format(csrf=csrf))
    logging.debug("Logon :: authorize() :: API.....................: {api}".format(api=api))
    logging.debug("Logon :: authorize() :: TRANS_ID................: {trans_id}".format(trans_id=trans_id))

    if len(csrf) == 0 | len(api) == 0 | len(trans_id) == 0:
        return "false"

    data = {
        "CSRF": csrf,
        "API": api,
        "TRANS_ID": trans_id,
        "COOKIES": get_cookies(authorize_response)
    }

    return data


def self_asserted_logon_request(user_name, password, params, authorize_response):
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

    logging.debug("Logon :: self_asserted() :: Response................: {response}".format(response=response))

    if response.status_code != 200:
        print("\n{0}- Fail [logon_selfasserted_request]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                                             response.status_code,
                                                                                                             response.text))
        return "false"

    response_text = response.text
    logging.debug("Logon :: self_asserted() :: Response Text...........: {text}".format(text=response_text))
    data = response.json()
    status = data["status"]

    if status == "400":
        if "@registration_link" in response_text:
            logging.debug("Alert: The user doesn't exist.")
        if "@reset_password_link" in response_text:
            print("\n{0}- Fail [logon_selfasserted_request]. The user exists but the password is wrong".format(text.Red))
            return "wrong_password"

    logging.debug("Logon :: self_asserted() :: JSON Status.............: {status}".format(status=status))

    data = {
        "CSRF": authorize_response["CSRF"],
        "API": authorize_response["API"],
        "TRANS_ID": authorize_response["TRANS_ID"],
        "COOKIES": merge_cookies(authorize_response["COOKIES"], get_cookies(response))
    }

    return data


def confirmed_logon_request(params, self_asserted_response):
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
        print("\n{0}- Fail [logon_confirmed_request]. Response status: {1}. Response message: {2}".format(text.Red, response.status_code,
                                                                                                          response.text))
        return "false"

    response_text = response.text
    logging.debug("Logon :: confirmed() :: Response Text...........: {text}".format(text=response_text))

    if "id_token" in response_text:
        id_token = re.search(' id=\'id_token\' value=\'([^\']+)', response_text).group(1)
        logging.debug("Logon :: confirmed() :: Response Text...........: {text}".format(text=response_text))
        logging.debug("Logon :: confirmed() :: ID Token................: {value}".format(value=id_token))
        return id_token
    return "false"


def create_user(environment, country, email, password, account_id, tax_id):
    params = get_iam_b2c_params(environment, country)

    authorize_load_response = authorize_load_request(params)
    if authorize_load_response == "false":
        return "false"

    self_asserted_email_response = self_asserted_email_request(
        email, params, authorize_load_response)
    if self_asserted_email_response == "false" or self_asserted_email_response == "user_exists":
        return "false"

    confirmed_email_response = confirmed_email_request(
        params, self_asserted_email_response)
    if confirmed_email_response == "false":
        return "false"

    self_asserted_otp_response = self_asserted_otp_request(
        email, params, confirmed_email_response)
    if self_asserted_otp_response == "false":
        return "false"

    confirmed_otp_response = confirmed_otp_request(
        params, self_asserted_otp_response)
    if confirmed_otp_response == "false":
        return "false"

    self_asserted_name_response = self_asserted_name_request(
        email, params, confirmed_otp_response)
    if self_asserted_name_response == "false":
        return "false"

    confirmed_name_response = confirmed_name_request(
        params, self_asserted_name_response)
    if confirmed_name_response == "false":
        return "false"

    self_asserted_password_response = self_asserted_password_request(
        password, params, confirmed_name_response)
    if self_asserted_password_response == "false":
        return "false"

    confirmed_password_response = confirmed_password_request(
        params, self_asserted_password_response)
    if confirmed_password_response == "false":
        return "false"

    authorize_account_response = authorize_account_request(
        params, confirmed_password_response)
    if authorize_account_response == "false":
        return "false"

    self_asserted_account_response = self_asserted_account_request(
        account_id, tax_id, params, authorize_account_response)
    if self_asserted_account_response == "false":
        return "false"

    if "false" == confirmed_account_request(params, self_asserted_account_response):
        return "false"

    return "success"


def get_cookies(response):
    cookies = {}
    for c in response.cookies:
        cookies[c.name] = c.value
    return cookies


def merge_cookies(cookies1, cookies2):
    cookies = {}
    for key in cookies1.keys():
        cookies[key] = cookies1[key]
    for key in cookies2.keys():
        cookies[key] = cookies2[key]
    return cookies


def get_cookies_header(cookies):
    cookies_header = []
    for key in cookies.keys():
        cookies_header.append("{0}={1}".format(key, cookies[key]))
    return "; ".join(cookies_header)


def self_assert_response_error(self_assert_response):
    if self_assert_response.status_code != 200:
        return False

    response_text = self_assert_response.text
    try:
        status = re.search('\"status\":"([^"]+)', response_text).group(1)
        return int(status) != 200
    except AttributeError:
        print("\n{0}- Fail [self_assert_response_body]. Invalid response.".format(text.Red))
        return False


def authorize_load_request(params):
    logging.debug("Calling authorize_load_request...")

    data = {
        "response_mode": "form_post",
        "ui_locales": "es",
        "prompt": "login",
        "referral": "decision_screen",
        "response_type": "id_token",
        "redirect_uri": params["REDIRECT_URL"],
        "client_id": params["CLIENT_ID"],
        "nonce": uuid.uuid1().hex,
        "state": "{0}-{1}".format(params["B2B_SIGNUP_POLICY"], uuid.uuid1().hex),
        "scope": "openid"
    }

    authorize_load_response = place_request("GET", params["BASE_SIGNUP_URL"] + "/oauth2/authorize", data, None)
    response_text = authorize_load_response.text
    if authorize_load_response.status_code != 200:
        print("\n{0}- Fail [authorize_load_request]. Response code: {1}. Response message: {2}".format(text.Red,
                                                                                                       authorize_load_response.status_code,
                                                                                                       response_text))
        return "false"

    try:
        csrf = re.search('\"csrf\":"([^"]+)', response_text).group(1)
        api = re.search('\"api\":"([^"]+)', response_text).group(1)
        trans_id = re.search('\"transId\":"([^"]+)', response_text).group(1)
    except AttributeError as e:
        print("\n{0}- Fail [authorize_load_request]. Exception: {1}".format(text.Red, str(e)))
        return "false"

    if len(csrf) == 0 | len(api) == 0 | len(trans_id) == 0:
        print("\n{0}- Fail [authorize_load_request]. Invalid response.".format(text.Red))
        return "false"
    else:
        return {
            "CSRF": csrf,
            "API": api,
            "TRANS_ID": trans_id,
            "COOKIES": get_cookies(authorize_load_response)
        }


def self_asserted_email_request(email, params, authorize_load_response):
    logging.debug("Calling self_asserted_email_request...")

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

    self_asserted_email_response = place_request("POST", url, data, headers)

    if self_assert_response_error(self_asserted_email_response):
        print("\n{0}- Fail [self_asserted_email_request]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                                              self_asserted_email_response
                                                                                                              .status_code,
                                                                                                              self_asserted_email_response
                                                                                                              .text))
        if "Esta cuenta ya existe" in self_asserted_email_response.text or "There is another user with this user name" in \
                self_asserted_email_response.text:
            return "user_exists"
        return "false"
    else:
        return {
            "CSRF": authorize_load_response["CSRF"],
            "API": authorize_load_response["API"],
            "TRANS_ID": authorize_load_response["TRANS_ID"],
            "COOKIES": merge_cookies(authorize_load_response["COOKIES"], get_cookies(self_asserted_email_response))
        }


def confirmed_request(base_url, csrf, api, trans_id, b2b_signup_policy, cookies, csrf_response_required):
    headers = {"Cookie": get_cookies_header(cookies)}

    url = '{0}/api/{1}/confirmed?csrf_token={2}&tx={3}&p={4}'.format(base_url, urllib.parse.quote(api), urllib.parse.quote(csrf),
                                                                     urllib.parse.quote(trans_id), urllib.parse.quote(b2b_signup_policy))

    confirmed_response = place_request("GET", url, None, headers)

    if confirmed_response.status_code != 200:
        return "false"
    else:
        new_cookies = get_cookies(confirmed_response)
        response_text = confirmed_response.text

        try:
            new_csrf = re.search('\"csrf\":"([^"]+)', response_text).group(1)
        except AttributeError as e:
            logging.debug("Alert: csrf not found! Trying to get by header x-ms-cpim-csrf. Exception: {0}".format(str(e)))
            try:
                new_csrf = new_cookies["x-ms-cpim-csrf"]
            except KeyError:
                if csrf_response_required:
                    return "false"
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
                return "false"

        return {
            "CSRF": new_csrf,
            "API": api,
            "TRANS_ID": trans_id,
            "COOKIES": merge_cookies(cookies, new_cookies)
        }


def confirmed_email_request(params, last_response):
    logging.debug("Calling confirmed_email_request...")
    confirmed_email_response = confirmed_request(params["BASE_SIGNUP_URL"], last_response["CSRF"], last_response["API"],
                                                 last_response["TRANS_ID"], params["B2B_SIGNUP_POLICY"], last_response["COOKIES"], True)

    if confirmed_email_response == "false":
        print("\n{0}- Fail [confirmed_email_request]".format(text.Red))
        return "false"
    else:
        return confirmed_email_response


def generate_otp(otp_secret, otp_interval, email):
    secret = otp_secret + email
    bytes_secret = bytes(secret, "utf8")
    base64_secret = base64.b32encode(bytes_secret)
    totp = pyotp.TOTP(base64_secret, interval=otp_interval).now()
    logging.debug("OTP generated: {0}".format(totp))
    return totp


def self_asserted_otp_request(email, params, confirmed_email_response):
    logging.debug("Calling self_asserted_otp_request...")
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

    self_asserted_otp_response = place_request("GET", url, data, headers)

    if self_asserted_otp_response.status_code != 200:
        print("\n{0}- Fail [self_asserted_otp_request]. Response status: {1}. Response message: {2}".format(text.Red),
              self_asserted_otp_response.status_code, self_asserted_otp_response.text)
        return "false"
    else:
        return {
            "CSRF": confirmed_email_response["CSRF"],
            "API": confirmed_email_response["API"],
            "TRANS_ID": confirmed_email_response["TRANS_ID"],
            "COOKIES": merge_cookies(confirmed_email_response["COOKIES"], get_cookies(self_asserted_otp_response))
        }


def confirmed_otp_request(params, last_response):
    logging.debug("Calling confirmed_otp_request...")
    confirmed_opt_response = confirmed_request(params["BASE_SIGNUP_URL"], last_response["CSRF"], last_response["API"],
                                               last_response["TRANS_ID"], params["B2B_SIGNUP_POLICY"], last_response["COOKIES"], True)

    if confirmed_opt_response == "false":
        print("\n{0}- Fail [confirmed_otp_request]".format(text.Red))
        return "false"
    else:
        return confirmed_opt_response


def self_asserted_name_request(email, params, confirmed_otp_response):
    logging.debug("Calling self_asserted_name_request...")

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

    self_asserted_name_response = place_request("POST", url, data, headers)

    if self_assert_response_error(self_asserted_name_response):
        print("\n{0}- Fail [self_asserted_name_request]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                                             self_asserted_name_response
                                                                                                             .status_code,
                                                                                                             self_asserted_name_response
                                                                                                             .text))
        return "false"
    else:
        return {
            "CSRF": confirmed_otp_response["CSRF"],
            "API": confirmed_otp_response["API"],
            "TRANS_ID": confirmed_otp_response["TRANS_ID"],
            "COOKIES": merge_cookies(confirmed_otp_response["COOKIES"], get_cookies(self_asserted_name_response))
        }


def confirmed_name_request(params, last_response):
    logging.debug("Calling confirmed_name_request...")
    confirmed_name_response = confirmed_request(params["BASE_SIGNUP_URL"], last_response["CSRF"], last_response["API"],
                                                last_response["TRANS_ID"], params["B2B_SIGNUP_POLICY"], last_response["COOKIES"], True)

    if confirmed_name_response == "false":
        print("\n{0}- Fail [confirmed_name_request]".format(text.Red))
        return "false"
    else:
        return confirmed_name_response


def self_asserted_password_request(password, params, confirmed_name_response):
    logging.debug("Calling self_asserted_password_request...")
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

    self_asserted_password_response = place_request("POST", url, data, headers)

    if self_assert_response_error(self_asserted_password_response):
        print("\n{0}- Fail [self_asserted_password_request]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                            self_asserted_password_response.status_code,
                                                                                            self_asserted_password_response.text))
        return "false"
    else:
        return {
            "CSRF": confirmed_name_response["CSRF"],
            "API": confirmed_name_response["API"],
            "TRANS_ID": confirmed_name_response["TRANS_ID"],
            "COOKIES": merge_cookies(confirmed_name_response["COOKIES"], get_cookies(self_asserted_password_response))
        }


def confirmed_password_request(params, last_response):
    logging.debug("Calling confirmed_password_request...")
    confirmed_password_response = confirmed_request(params["BASE_SIGNUP_URL"], last_response["CSRF"], last_response["API"],
                                                    last_response["TRANS_ID"], params["B2B_SIGNUP_POLICY"], last_response["COOKIES"], False)

    if confirmed_password_response == "false":
        print("\n{0}- Fail [confirmed_password_request]".format(text.Red))
        return "false"
    else:
        return confirmed_password_response


def authorize_account_request(params, last_response):
    logging.debug("Calling authorize_account_request...")
    data = {
        "response_mode": "form_post",
        "ui_locales": "es",
        "response_type": "id_token",
        "redirect_uri": params["REDIRECT_URL"],
        "client_id": params["CLIENT_ID"],
        "nonce": uuid.uuid1().hex,
        "state": "{0}-{1}".format(params["B2B_ONBOARDING_POLICY"], uuid.uuid1().hex),
        "scope": "openid"
    }

    headers = {
        "Cookie": get_cookies_header(last_response["COOKIES"])
    }

    url = '{0}/oauth2/authorize'.format(params["BASE_ONBOARDING_URL"])

    authorize_account_response = place_request("GET", url, data, headers)
    response_text = authorize_account_response.text
    if authorize_account_response.status_code != 200:
        print("\n{0}- Fail [authorize_account_request]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                                            authorize_account_response
                                                                                                            .status_code, response_text))
        return "false"

    csrf = re.search('\"csrf\":"([^"]+)', response_text).group(1)
    api = re.search('\"api\":"([^"]+)', response_text).group(1)
    trans_id = re.search('\"transId\":"([^"]+)', response_text).group(1)

    if len(csrf) == 0 | len(api) == 0 | len(trans_id) == 0:
        return "false"
    else:
        return {
            "CSRF": csrf,
            "API": api,
            "TRANS_ID": trans_id,
            "COOKIES": get_cookies(authorize_account_response)
        }


def self_asserted_account_request(account_id, tax_id, params, authorize_account_response):
    logging.debug("Calling self_asserted_account_request...")
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

    self_asserted_account_response = place_request("POST", url, data, headers)
    if self_assert_response_error(self_asserted_account_response):
        print("\n{0}- Fail [self_asserted_account_request]. Response status: {1}. Response message: {2}".format(text.Red,
                                                                                                self_asserted_account_response.status_code,
                                                                                                self_asserted_account_response.text))
        return "false"
    else:
        return {
            "CSRF": authorize_account_response["CSRF"],
            "API": authorize_account_response["API"],
            "TRANS_ID": authorize_account_response["TRANS_ID"],
            "COOKIES": merge_cookies(authorize_account_response["COOKIES"], get_cookies(self_asserted_account_response))
        }


def confirmed_account_request(params, last_response):
    logging.debug("Calling confirmed_account_request...")
    confirmed_account_response = confirmed_request(params["BASE_ONBOARDING_URL"], last_response["CSRF"], last_response["API"],
                                                   last_response["TRANS_ID"], params["B2B_ONBOARDING_POLICY"], last_response["COOKIES"],
                                                   False)

    if confirmed_account_response == "false":
        logging.debug("Alert: Fail [confirmed_account_request].")
        return "false"
    else:
        return confirmed_account_response
