from data_mass.user.assertion import (
    assert_account_request,
    assert_email_request,
    assert_name_request,
    assert_otp_request,
    assert_password_request
)
from data_mass.user.authorization import (
    authorize_account_request,
    authorize_load_request
)
from data_mass.user.confirmation import (
    confirm_account_request,
    confirm_email_request,
    confirm_name_request,
    confirm_otp_request,
    confirm_password_request
)
from data_mass.user.user import get_iam_b2c_params


def create_user(environment, country, email, password, account_id, tax_id):
    params = get_iam_b2c_params(environment, country)

    authorize_load_response = authorize_load_request(params)
    if not authorize_load_response:
        return False

    self_asserted_email_response = assert_email_request(
        email,
        params,
        authorize_load_response
    )

    if not self_asserted_email_response or self_asserted_email_response == "user_exists":
        return False

    confirmed_email_response = confirm_email_request(
        params,
        self_asserted_email_response
    )

    if not confirmed_email_response:
        return False

    self_asserted_otp_response = assert_otp_request(
        email,
        params,
        confirmed_email_response
    )

    if not self_asserted_otp_response:
        return False

    confirmed_otp_response = confirm_otp_request(
        params,
        self_asserted_otp_response
    )

    if not confirmed_otp_response:
        return False

    self_asserted_name_response = assert_name_request(
        email,
        params,
        confirmed_otp_response
    )

    if not self_asserted_name_response:
        return False

    confirmed_name_response = confirm_name_request(
        params,
        self_asserted_name_response
    )

    if not confirmed_name_response:
        return False

    self_asserted_password_response = assert_password_request(
        password,
        params,
        confirmed_name_response
    )

    if not self_asserted_password_response:
        return False

    confirmed_password_response = confirm_password_request(
        params,
        self_asserted_password_response
    )

    if not confirmed_password_response:
        return False

    authorize_account_response = authorize_account_request(
        params,
        confirmed_password_response
    )

    if not authorize_account_response:
        return False

    self_asserted_account_response = assert_account_request(
        account_id,
        tax_id,
        params,
        authorize_account_response
    )

    if not self_asserted_account_response:
        return False

    if not confirm_account_request(params, self_asserted_account_response):
        return False

    return True
