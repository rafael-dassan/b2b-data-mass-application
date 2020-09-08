import re
import urllib.parse
import pyotp
import base64
from common import *
import uuid


def get_iam_b2c_params(environment, country):
    country_policy = country.upper()
    if environment == 'UAT':
        return get_iam_b2c_params_uat(country_policy)
    else:
        return get_iam_b2c_params_sit(country_policy)


def get_iam_b2c_params_uat(country):
    b2b_server_name = 'b2biamgbusuat1.b2clogin.com'
    b2b_path = 'b2biamgbusuat1.onmicrosoft.com'
    b2b_signin_policy = 'B2C_1A_SigninMobile_{0}'.format(country)
    b2b_signup_policy = 'B2C_1A_SignUp_{0}'.format(country)
    b2b_onboarding_policy = 'B2C_1A_Onboarding_{0}'.format(country)
    params = {
        'B2B_SERVER_NAME': b2b_server_name,
        'B2B_PATH': b2b_path,
        'REDIRECT_URL': 'com.abi.bees.colombia://oauth/redirect',
        'CLIENT_ID': 'f1d909d8-f72a-40cd-a7ff-fec8e5b033fc',
        'B2B_SIGNIN_POLICY': b2b_signin_policy,
        'B2B_SIGNUP_POLICY': b2b_signup_policy,
        'B2B_ONBOARDING_POLICY': b2b_onboarding_policy,
        'OTP_SECRET': '1NcRfUjXn2r4u7x!A%D*G-KaPdSgVkYp',
        'OTP_INTERVAL': 600,
        'BASE_SIGNIN_URL': 'https://{0}/{1}/{2}'.format(b2b_server_name, b2b_path, b2b_signin_policy),
        'BASE_SIGNUP_URL': 'https://{0}/{1}/{2}'.format(b2b_server_name, b2b_path, b2b_signup_policy),
        'BASE_ONBOARDING_URL': 'https://{0}/{1}/{2}'.format(b2b_server_name, b2b_path, b2b_onboarding_policy)}
    return params


def get_iam_b2c_params_sit(country):
    b2b_server_name = 'b2biamgbussit1.b2clogin.com'
    b2b_path = 'b2biamgbussit1.onmicrosoft.com'
    b2b_signin_policy = 'B2C_1A_SigninMobile_{0}'.format(country)
    b2b_signup_policy = 'B2C_1A_SignUp_{0}'.format(country)
    b2b_onboarding_policy = 'B2C_1A_Onboarding_{0}'.format(country)
    params = {
        'B2B_SERVER_NAME': b2b_server_name,
        'B2B_PATH': b2b_path,
        'REDIRECT_URL': 'com.abi.bees.colombia://oauth/redirect',
        'CLIENT_ID': '70eb36b1-2894-4f1d-b08a-4a1f982a38da',
        'B2B_SIGNIN_POLICY': b2b_signin_policy,
        'B2B_SIGNUP_POLICY': b2b_signup_policy,
        'B2B_ONBOARDING_POLICY': b2b_onboarding_policy,
        'OTP_SECRET': '1NcRfUjXn2r4u7x!A%D*G-KaPdSgVkYp',
        'OTP_INTERVAL': 600,
        'BASE_SIGNIN_URL': 'https://{0}/{1}/{2}'.format(b2b_server_name, b2b_path, b2b_signin_policy),
        'BASE_SIGNUP_URL': 'https://{0}/{1}/{2}'.format(b2b_server_name, b2b_path, b2b_signup_policy),
        'BASE_ONBOARDING_URL': 'https://{0}/{1}/{2}'.format(b2b_server_name, b2b_path, b2b_onboarding_policy)}
    return params


def authenticate_user_iam(environment, country, user_name, password):
    params = get_iam_b2c_params(environment, country)

    logging.debug("Calling logon_authorize_request...")
    authorize_iam_response = authorize_iam(params)
    if authorize_iam_response == "fail":
        return "fail"

    logging.debug("Calling logon_selfasserted_request...")
    self_asserted_response = self_asserted_logon_request(user_name, password, params, authorize_iam_response)
    if self_asserted_response == "fail" or self_asserted_response == "wrong_password":
        return self_asserted_response

    logging.debug("Calling logon_confirmed_request...")
    id_token = confirmed_logon_request(params, self_asserted_response)
    if id_token == "fail":
        return "fail"

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

    authorize_response = place_request("POST", params["BASE_SIGNIN_URL"] + "/oauth2/authorize", payload, None)

    logging.debug("  Logon :: authorize() :: Response................: {response}".format(response=authorize_response))

    if authorize_response.status_code != 200:
        print("- Fail on user creation v3 [authorize_load_request]: status_code {0}.".format(
            authorize_response.status_code))
        return "fail"

    response_text = authorize_response.text

    csrf = re.search('\"csrf\":"([^"]+)', response_text).group(1)
    api = re.search('\"api\":"([^"]+)', response_text).group(1)
    trans_id = re.search('\"transId\":"([^"]+)', response_text).group(1)

    logging.debug("  Logon :: authorize() :: CSRF....................: {csrf}".format(csrf=csrf))
    logging.debug("  Logon :: authorize() :: API.....................: {api}".format(api=api))
    logging.debug("  Logon :: authorize() :: TRANS_ID................: {trans_id}".format(trans_id=trans_id))

    if len(csrf) == 0 | len(api) == 0 | len(trans_id) == 0:
        return "fail"

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

    response = place_request(
        "POST",
        params["BASE_SIGNIN_URL"] + "/{0}?tx={1}&p={2}".format(
            urllib.parse.quote(authorize_response["API"]),
            urllib.parse.quote(authorize_response["TRANS_ID"]),
            urllib.parse.quote(params["B2B_SIGNIN_POLICY"])),
        payload,
        headers)

    logging.debug("  Logon :: self_asserted() :: Response................: {response}".format(response=response))

    if response.status_code != 200:
        print("- Fail on user logon v3 [logon_selfasserted_request]: status_code {0}.".format(
            response.status_code))
        return "fail"

    response_text = response.text

    logging.debug("  Logon :: self_asserted() :: Response Text...........: {text}".format(text=response_text))

    data = response.json()
    status = data["status"]

    if status == "400":
        if "@registration_link" in response_text:
            print("Alert: The user doesn't exist.")
        if "@reset_password_link" in response_text:
            print("Alert: Fail on user logon v3 [logon_selfasserted_request]: The user exists - the password is wrong.")
            return "wrong_password"

    logging.debug("  Logon :: self_asserted() :: JSON Status.............: {status}".format(status=status))

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

    logging.debug("  Logon :: confirmed() :: Response................: {response}".format(response=response))

    if response.status_code != 200:
        print("- Fail on user logon v3 [logon_confirmed_request]: status_code {0}.".format(
            response.status_code))
        return "fail"

    response_text = response.text

    logging.debug("  Logon :: confirmed() :: Response Text...........: {text}".format(text=response_text))

    if "id_token" in response_text:
        id_token = re.search(' id=\'id_token\' value=\'([^\']+)', response_text).group(1)

        logging.debug("  Logon :: confirmed() :: Response Text...........: {text}".format(text=response_text))
        logging.debug("  Logon :: confirmed() :: ID Token................: {value}".format(value=id_token))

        return id_token

    return "fail"


def create_user(environment, country, email, password, account_id, tax_id):
    params = get_iam_b2c_params(environment, country)

    authorize_load_response = authorize_load_request(params)
    if authorize_load_response == "fail":
        return "fail"

    self_asserted_email_response = self_asserted_email_request(email, params, authorize_load_response)
    if self_asserted_email_response == "fail":
        return "fail"

    confirmed_email_response = confirmed_email_request(params, self_asserted_email_response)
    if confirmed_email_response == "fail":
        return "fail"

    self_asserted_otp_response = self_asserted_otp_request(email, params, confirmed_email_response)
    if self_asserted_otp_response == "fail":
        return "fail"

    confirmed_otp_response = confirmed_otp_request(params, self_asserted_otp_response)
    if confirmed_otp_response == "fail":
        return "fail"

    self_asserted_name_response = self_asserted_name_request(email, params, confirmed_otp_response)
    if self_asserted_name_response == "fail":
        return "fail"

    confirmed_name_response = confirmed_name_request(params, self_asserted_name_response)
    if confirmed_name_response == "fail":
        return "fail"

    self_asserted_password_response = self_asserted_password_request(password, params, confirmed_name_response)
    if self_asserted_password_response == "fail":
        return "fail"

    confirmed_password_response = confirmed_password_request(params, self_asserted_password_response)
    if confirmed_password_response == "fail":
        return "fail"

    authorize_account_response = authorize_account_request(params, confirmed_password_response)
    if authorize_account_response == "fail":
        return "fail"

    self_asserted_account_response = self_asserted_account_request(
        account_id, tax_id, params, authorize_account_response)
    if self_asserted_account_response == "fail":
        return "fail"

    confirmed_account_request(params, self_asserted_account_response)

    # Verifying the created account
    authenticate_user_iam_response = authenticate_user_iam(environment, country, email, password)
    if authenticate_user_iam_response == "wrong_password" or authenticate_user_iam_response == "fail":
        return "fail"
    else:
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
        print("- Fail on user creation v3 [self_assert_response_body]. Invalid response.")
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

    if authorize_load_response.status_code != 200:
        print("- Fail on user creation v3 [authorize_load_request]: status_code {0}.".format(
            authorize_load_response.status_code))
        return "fail"

    response_text = authorize_load_response.text
    try:
        csrf = re.search('\"csrf\":"([^"]+)', response_text).group(1)
        api = re.search('\"api\":"([^"]+)', response_text).group(1)
        trans_id = re.search('\"transId\":"([^"]+)', response_text).group(1)
    except AttributeError:
        print("- Fail on user creation v3 [authorize_load_request]: Invalid response.")
        return "fail"

    if len(csrf) == 0 | len(api) == 0 | len(trans_id) == 0:
        print("- Fail on user creation v3 [authorize_load_request]: Invalid response.")
        return "fail"
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
        "request_type": "RESPONSE"
    }

    headers = {
        "X-CSRF-TOKEN": authorize_load_response["CSRF"],
        "Cookie": get_cookies_header(authorize_load_response["COOKIES"])
    }

    self_asserted_email_response = place_request(
        "POST",
        params["BASE_SIGNUP_URL"] + "/{0}?tx={1}&p={2}".format(
            urllib.parse.quote(authorize_load_response["API"]),
            urllib.parse.quote(authorize_load_response["TRANS_ID"]),
            urllib.parse.quote(params["B2B_SIGNUP_POLICY"])),
        data,
        headers)

    if self_assert_response_error(self_asserted_email_response):
        print("- Fail on user creation v3 [self_asserted_email_request]: status_code {0}. Body {1}.".format(
            self_asserted_email_response.status_code, self_asserted_email_response.text))
        return "fail"
    else:
        return {
            "CSRF": authorize_load_response["CSRF"],
            "API": authorize_load_response["API"],
            "TRANS_ID": authorize_load_response["TRANS_ID"],
            "COOKIES": merge_cookies(authorize_load_response["COOKIES"], get_cookies(self_asserted_email_response))
        }


def confirmed_request(base_url, csrf, api, trans_id, b2b_signup_policy, cookies, csrf_response_required):
    headers = {
        "Cookie": get_cookies_header(cookies)
    }

    confirmed_response = place_request(
        "GET",
        base_url + "/api/{0}/confirmed?csrf_token={1}&tx={2}&p={3}".format(
            urllib.parse.quote(api),
            urllib.parse.quote(csrf),
            urllib.parse.quote(trans_id),
            urllib.parse.quote(b2b_signup_policy)),
        None,
        headers)

    if confirmed_response.status_code != 200:
        return "fail"
    else:
        new_cookies = get_cookies(confirmed_response)

        response_text = confirmed_response.text
        try:
            new_csrf = re.search('\"csrf\":"([^"]+)', response_text).group(1)
        except AttributeError:
            logging.debug("- Alert: csrf not found! Trying to get by header x-ms-cpim-csrf...")
            try:
                new_csrf = new_cookies["x-ms-cpim-csrf"]
            except KeyError:
                if csrf_response_required:
                    return "fail"
                new_csrf = None

        if new_csrf is None:
            if "id_token" in response_text:
                id_token = re.search(' id=\'id_token\' value=\'([^\']+)', response_text).group(1)
                return {
                    "ID_TOKEN": id_token,
                    "COOKIES": new_cookies
                }
            else:
                logging.debug("Alert: Response_text: " + response_text)
                return "fail"

        return {
            "CSRF": new_csrf,
            "API": api,
            "TRANS_ID": trans_id,
            "COOKIES": merge_cookies(cookies, new_cookies)
        }


def confirmed_email_request(params, last_response):
    logging.debug("Calling confirmed_email_request...")
    confirmed_email_response = confirmed_request(
        params["BASE_SIGNUP_URL"],
        last_response["CSRF"],
        last_response["API"],
        last_response["TRANS_ID"],
        params["B2B_SIGNUP_POLICY"],
        last_response["COOKIES"], True)

    if confirmed_email_response == "fail":
        print("- Fail on user creation v3 [confirmed_email_request].")
        return "fail"
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

    self_asserted_otp_response = place_request(
        "GET",
        params["BASE_SIGNUP_URL"] + "/{0}?tx={1}&p={2}".format(
            urllib.parse.quote(confirmed_email_response["API"]),
            urllib.parse.quote(confirmed_email_response["TRANS_ID"]),
            urllib.parse.quote(params["B2B_SIGNUP_POLICY"])),
        data,
        headers)

    if self_asserted_otp_response.status_code != 200:
        print("- Fail on user creation v3 [self_asserted_otp_request]: status_code {0}.".format(
            self_asserted_otp_response.status_code))
        return "fail"
    else:
        return {
            "CSRF": confirmed_email_response["CSRF"],
            "API": confirmed_email_response["API"],
            "TRANS_ID": confirmed_email_response["TRANS_ID"],
            "COOKIES": merge_cookies(confirmed_email_response["COOKIES"], get_cookies(self_asserted_otp_response))
        }


def confirmed_otp_request(params, last_response):
    logging.debug("Calling confirmed_otp_request...")
    confirmed_opt_response = confirmed_request(
        params["BASE_SIGNUP_URL"],
        last_response["CSRF"],
        last_response["API"],
        last_response["TRANS_ID"],
        params["B2B_SIGNUP_POLICY"],
        last_response["COOKIES"], True)

    if confirmed_opt_response == "fail":
        print("- Fail on user creation v3 [confirmed_otp_request].")
        return "fail"
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

    self_asserted_name_response = place_request(
        "POST",
        params["BASE_SIGNUP_URL"] + "/{0}?tx={1}&p={2}".format(
            urllib.parse.quote(confirmed_otp_response["API"]),
            urllib.parse.quote(confirmed_otp_response["TRANS_ID"]),
            urllib.parse.quote(params["B2B_SIGNUP_POLICY"])),
        data,
        headers)

    if self_assert_response_error(self_asserted_name_response):
        print("- Fail on user creation v3 [self_asserted_name_request]: status_code {0}. Body {1}.".format(
            self_asserted_name_response.status_code, self_asserted_name_response.text))
        return "fail"
    else:
        return {
            "CSRF": confirmed_otp_response["CSRF"],
            "API": confirmed_otp_response["API"],
            "TRANS_ID": confirmed_otp_response["TRANS_ID"],
            "COOKIES": merge_cookies(confirmed_otp_response["COOKIES"], get_cookies(self_asserted_name_response))
        }


def confirmed_name_request(params, last_response):
    logging.debug("Calling confirmed_name_request...")
    confirmed_name_response = confirmed_request(
        params["BASE_SIGNUP_URL"],
        last_response["CSRF"],
        last_response["API"],
        last_response["TRANS_ID"],
        params["B2B_SIGNUP_POLICY"],
        last_response["COOKIES"], True)

    if confirmed_name_response == "fail":
        print("- Fail on user creation v3 [confirmed_name_request].")
        return "fail"
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

    self_asserted_password_response = place_request(
        "POST",
        params["BASE_SIGNUP_URL"] + "/{0}?tx={1}&p={2}".format(
            urllib.parse.quote(confirmed_name_response["API"]),
            urllib.parse.quote(confirmed_name_response["TRANS_ID"]),
            urllib.parse.quote(params["B2B_SIGNUP_POLICY"])),
        data,
        headers)

    if self_assert_response_error(self_asserted_password_response):
        print("- Fail on user creation v3 [self_asserted_password_request]: status_code {0}. Body {1}.".format(
            self_asserted_password_response.status_code, self_asserted_password_response.text))
        return "fail"
    else:
        return {
            "CSRF": confirmed_name_response["CSRF"],
            "API": confirmed_name_response["API"],
            "TRANS_ID": confirmed_name_response["TRANS_ID"],
            "COOKIES": merge_cookies(confirmed_name_response["COOKIES"], get_cookies(self_asserted_password_response))
        }


def confirmed_password_request(params, last_response):
    logging.debug("Calling confirmed_password_request...")
    confirmed_password_response = confirmed_request(
        params["BASE_SIGNUP_URL"],
        last_response["CSRF"],
        last_response["API"],
        last_response["TRANS_ID"],
        params["B2B_SIGNUP_POLICY"],
        last_response["COOKIES"], False)

    if confirmed_password_response == "fail":
        print("- Fail on user creation v3 [confirmed_password_request].")
        return "fail"
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

    authorize_account_response = place_request("GET", params["BASE_ONBOARDING_URL"] + "/oauth2/authorize", data, headers)

    if authorize_account_response.status_code != 200:
        print("- Fail on user creation v3 [authorize_account_request]: status_code {0}.".format(
            authorize_account_response.status_code))
        return "fail"

    response_text = authorize_account_response.text
    csrf = re.search('\"csrf\":"([^"]+)', response_text).group(1)
    api = re.search('\"api\":"([^"]+)', response_text).group(1)
    trans_id = re.search('\"transId\":"([^"]+)', response_text).group(1)

    if len(csrf) == 0 | len(api) == 0 | len(trans_id) == 0:
        return "fail"
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

    self_asserted_account_response = place_request(
        "POST",
        params["BASE_ONBOARDING_URL"] + "/{0}?tx={1}&p={2}".format(
            urllib.parse.quote(authorize_account_response["API"]),
            urllib.parse.quote(authorize_account_response["TRANS_ID"]),
            urllib.parse.quote(params["B2B_ONBOARDING_POLICY"])),
        data,
        headers)

    if self_assert_response_error(self_asserted_account_response):
        print("- Fail on user creation v3 [self_asserted_account_request]: status_code {0}. Body {1}.".format(
            self_asserted_account_response.status_code, self_asserted_account_response.text))
        return "fail"
    else:
        return {
            "CSRF": authorize_account_response["CSRF"],
            "API": authorize_account_response["API"],
            "TRANS_ID": authorize_account_response["TRANS_ID"],
            "COOKIES": merge_cookies(authorize_account_response["COOKIES"], get_cookies(self_asserted_account_response))
        }


def confirmed_account_request(params, last_response):
    logging.debug("Calling confirmed_account_request...")
    confirmed_account_response = confirmed_request(
        params["BASE_ONBOARDING_URL"],
        last_response["CSRF"],
        last_response["API"],
        last_response["TRANS_ID"],
        params["B2B_ONBOARDING_POLICY"],
        last_response["COOKIES"], False)

    if confirmed_account_response == "fail":
        logging.debug("Alert: Fail on user creation v3 [confirmed_account_request].")
        return "fail"
    else:
        return confirmed_account_response
