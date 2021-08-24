import logging
import re
from uuid import uuid1, uuid4

from data_mass.classes.text import text
from data_mass.common import place_request
from data_mass.user.utils import get_cookies, get_cookies_header


def authorize_iam(params):
    payload = {
        "response_mode": "form_post",
        "ui_locales": "es",
        "response_type": "id_token",
        "redirect_uri": params["REDIRECT_URL"],
        "client_id": params["CLIENT_ID"],
        "uuid_nonce": uuid4().hex,
        "state": f'{params["B2B_SIGNIN_POLICY"]}-{uuid4().hex}',
        "scope": "openid"
    }

    url = f'{params["BASE_SIGNIN_URL"]}/oauth2/authorize'
    authorize_response = place_request("POST", url, payload, None)

    logging.debug(
        f"Logon :: authorize() :: \
        Response................: {authorize_response}"    
    )

    if authorize_response.status_code != 200:
        print((
            f"\n{text.Red}- Fail [authorize_load_request]. "
            f"Response status: {authorize_response.status_code}. "
            f"Response message: {authorize_response.text}"
        ))

        return False

    response_text = authorize_response.text
    csrf = re.search('\"csrf\":"([^"]+)', response_text).group(1)
    api = re.search('\"api\":"([^"]+)', response_text).group(1)
    trans_id = re.search('\"transId\":"([^"]+)', response_text).group(1)

    logging.debug(f"Logon :: authorize() :: CSRF....................: {csrf}")
    logging.debug(f"Logon :: authorize() :: API.....................: {api}")
    logging.debug(
        f"Logon :: authorize() :: TRANS_ID................: {trans_id}"
    )

    if len(csrf) == 0 | len(api) == 0 | len(trans_id) == 0:
        return False

    data = {
        "CSRF": csrf,
        "API": api,
        "TRANS_ID": trans_id,
        "COOKIES": get_cookies(authorize_response)
    }

    return data


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
        "nonce": uuid1().hex,
        "state": "{0}-{1}".format(params["B2B_SIGNUP_POLICY"], uuid1().hex),
        "scope": "openid"
    }

    url = f'{params["BASE_SIGNUP_URL"]}/oauth2/v2.0/authorize'
    authorize_load_response = place_request("GET", url, data, None)
    response_text = authorize_load_response.text
    if authorize_load_response.status_code != 200:
        print(
            f"{text.Red}- Fail [authorize_load_request]. \n"
            f"Response code: {authorize_load_response.status_code}.\n"
            f"Response message: {response_text}"
        )
        return False

    try:
        csrf = re.search('\"csrf\":"([^"]+)', response_text).group(1)
        api = re.search('\"api\":"([^"]+)', response_text).group(1)
        trans_id = re.search('\"transId\":"([^"]+)', response_text).group(1)
    except AttributeError as e:
        print(
            f"{text.Red}- Fail [authorize_load_request]. Exception: {str(e)}"
        )
        return False

    if len(csrf) == 0 | len(api) == 0 | len(trans_id) == 0:
        print(
            f"{text.Red}- Fail [authorize_load_request]. Invalid response."
        )
        return False
    else:
        return {
            "CSRF": csrf,
            "API": api,
            "TRANS_ID": trans_id,
            "COOKIES": get_cookies(authorize_load_response)
        }


def authorize_account_request(params, last_response):
    logging.debug("Calling authorize_account_request...")
    data = {
        "response_mode": "form_post",
        "ui_locales": "es",
        "response_type": "id_token",
        "redirect_uri": params["REDIRECT_URL"],
        "client_id": params["CLIENT_ID"],
        "nonce": uuid1().hex,
        "state": f'{params["B2B_ONBOARDING_POLICY"]}-{uuid1().hex}',
        "scope": "openid"
    }

    headers = {
        "Cookie": get_cookies_header(last_response["COOKIES"])
    }

    url = f'{params["BASE_ONBOARDING_URL"]}/oauth2/authorize'

    authorize_account_response = place_request("GET", url, data, headers)
    response_text = authorize_account_response.text
    if authorize_account_response.status_code != 200:
        print(
            f"\n{text.Red}- Fail [authorize_account_request].\n"
            f"Response status: {authorize_account_response.status_code}.\n"
            f"Response message: {response_text}."
        )
        return False

    csrf = re.search('\"csrf\":"([^"]+)', response_text).group(1)
    api = re.search('\"api\":"([^"]+)', response_text).group(1)
    trans_id = re.search('\"transId\":"([^"]+)', response_text).group(1)

    if len(csrf) == 0 | len(api) == 0 | len(trans_id) == 0:
        return False
    else:
        return {
            "CSRF": csrf,
            "API": api,
            "TRANS_ID": trans_id,
            "COOKIES": get_cookies(authorize_account_response)
        }
