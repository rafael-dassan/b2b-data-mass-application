import logging

from data_mass.user.assertion import assert_logon_request
from data_mass.user.authorization import authorize_iam
from data_mass.user.confirmation import confirm_logon_request
from data_mass.user.user import get_iam_b2c_params


def authenticate_user_iam(environment: str, country: str, user_name: str, password: str):
    params = get_iam_b2c_params(environment, country)

    logging.debug("Calling logon_authorize_request...")
    authorize_iam_response = authorize_iam(params)
    if not authorize_iam_response:
        return False

    logging.debug("Calling logon_selfasserted_request...")
    self_asserted_response = assert_logon_request(
        user_name=user_name,
        password=password,
        params=params,
        authorize_response=authorize_iam_response
    )

    if not self_asserted_response or self_asserted_response == "wrong_password":
        return self_asserted_response

    logging.debug("Calling logon_confirmed_request...")
    id_token = confirm_logon_request(
        params=params,
        self_asserted_response=self_asserted_response
    )

    if not id_token:
        return False

    return id_token
