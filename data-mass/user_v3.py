# Standard library imports
import re
import logging
import urllib


def get_iam_b2c_environment_uat(environment):
    return environment == "UAT"


def get_iam_b2c_params(environment, country):
    b2c_country_params = get_iam_b2c_country_params(environment, country)
    b2c_azure_params = get_iam_b2c_azure_params(environment)
    b2c_policy_params = get_iam_b2c_policy_params(country)

    b2b_server_name = b2c_azure_params["B2B_SERVER_NAME"]
    b2b_path = b2c_azure_params["B2B_PATH"]
    b2b_signin_policy = b2c_policy_params["B2B_SIGNIN_POLICY"]
    b2b_signup_policy = b2c_policy_params["B2B_SIGNUP_POLICY"]
    b2b_onboarding_policy = b2c_policy_params["B2B_ONBOARDING_POLICY"]

    params = {
        "B2B_SERVER_NAME": b2b_server_name,
        "B2B_PATH": b2b_path,
        "B2B_SIGNIN_POLICY": b2b_signin_policy,
        "B2B_SIGNUP_POLICY": b2b_signup_policy,
        "B2B_ONBOARDING_POLICY": b2b_onboarding_policy,
        "OTP_SECRET": "1NcRfUjXn2r4u7x!A%D*G-KaPdSgVkYp",
        "OTP_INTERVAL": 600,
        "BASE_SIGNIN_URL": "https://{0}/{1}/{2}".format(b2b_server_name, b2b_path, b2b_signin_policy),
        "BASE_SIGNUP_URL": "https://{0}/{1}/{2}".format(b2b_server_name, b2b_path, b2b_signup_policy),
        "BASE_ONBOARDING_URL": "https://{0}/{1}/{2}".format(b2b_server_name, b2b_path, b2b_onboarding_policy),
        "REDIRECT_URL": b2c_country_params["REDIRECT_URL"],
        "CLIENT_ID": b2c_country_params["CLIENT_ID"],
        "AZURE_CLIENT_ID": b2c_azure_params["AZURE_CLIENT_ID"],
        "AZURE_CLIENT_SECRET": b2c_azure_params["AZURE_CLIENT_SECRET"]
    }
    return params


def get_iam_b2c_country_params(environment, country):
    if get_iam_b2c_environment_uat(environment):
        return get_iam_b2c_country_params_uat(country)
    else:
        return get_iam_b2c_country_params_sit(country)


def get_iam_b2c_country_params_uat(country):
    params = {
        "BR": {
            "REDIRECT_URL": "com.abi.parceiro-ambev://oauth/redirect",
            "CLIENT_ID": "442357fe-e514-4919-816c-4baa02b41a6f"
        },
        "CO": {
            "REDIRECT_URL": "com.abi.bees.colombia://oauth/redirect",
            "CLIENT_ID": "f1d909d8-f72a-40cd-a7ff-fec8e5b033fc"
        },
        "DO": {
            "REDIRECT_URL": "com.abi.socio-cerveceria://oauth/redirect",
            "CLIENT_ID": "2fb9932f-5ac2-4f9d-91d7-35ea363cde34"
        },
        "MX": {
            "REDIRECT_URL": "com.abi.bees.mexico://oauth/redirect",
            "CLIENT_ID": "1841724c-1311-47e9-8894-a5a0e8a44197"
        },
        "EC": {
            "REDIRECT_URL": "com.abi.bees.ecuador://oauth/redirect",
            "CLIENT_ID": "e0f49717-83f3-4777-8bb7-510541203312"
        },
        "PE": {
            "REDIRECT_URL": "com.abi.bees.peru://oauth/redirect",
            "CLIENT_ID": "d8cfa150-0ad2-43f1-a85e-2d4e634f5f72"
        },
        "ZA": {
            "REDIRECT_URL": "com.abi.sab-connect://oauth/redirect",
            "CLIENT_ID": "499bf4c3-5c26-4e21-8ad8-c01957937cd5"
        },
        "AR": {
            "REDIRECT_URL": "com.abi.Quilmes://oauth/redirect",
            "CLIENT_ID": "f7e20a58-35a2-47f8-bb73-1735dd354d20"
        }
    }
    return params[country]


def get_iam_b2c_country_params_sit(country):
    params = {
        "BR": {
            "REDIRECT_URL": "com.abi.parceiro-ambev://oauth/redirect",
            "CLIENT_ID": "4a5ba64b-5053-439b-b29f-27cae493699f"
        },
        "CO": {
            "REDIRECT_URL": "com.abi.bees.colombia://oauth/redirect",
            "CLIENT_ID": "70eb36b1-2894-4f1d-b08a-4a1f982a38da"
        },
        "DO": {
            "REDIRECT_URL": "com.abi.socio-cerveceria://oauth/redirect",
            "CLIENT_ID": "a416b8f5-4061-4984-a2f7-a6dca86e68ae"
        },
        "MX": {
            "REDIRECT_URL": "com.abi.bees.mexico://oauth/redirect",
            "CLIENT_ID": "32a701c0-fbd0-481b-9028-809a0a1468f5"
        },
        "EC": {
            "REDIRECT_URL": "com.abi.bees.ecuador://oauth/redirect",
            "CLIENT_ID": "1d11cc25-779f-458e-a64b-8f4e42b0c8fd"
        },
        "PE": {
            "REDIRECT_URL": "com.abi.bees.peru://oauth/redirect",
            "CLIENT_ID": "be042e86-59a4-410e-baf4-77bfaca00774"
        },
        "ZA": {
            "REDIRECT_URL": "com.abi.sab-connect://oauth/redirect",
            "CLIENT_ID": "2cca5cb9-b89d-4986-a427-63af29d0149d"
        },
        "AR": {
            "REDIRECT_URL": "com.abi.Quilmes://oauth/redirect",
            "CLIENT_ID": "2ff1221e-a82d-49c5-8d22-b48db8bc07f6"
        }
    }
    return params[country]


def get_iam_b2c_azure_params(environment):
    if get_iam_b2c_environment_uat(environment):
        return get_iam_b2c_azure_params_uat()
    else:
        return get_iam_b2c_azure_params_sit()


def get_iam_b2c_azure_params_uat():
    params = {
        "B2B_SERVER_NAME": "b2biamgbusuat1.b2clogin.com",
        "B2B_PATH": "b2biamgbusuat1.onmicrosoft.com",
        "AZURE_CLIENT_ID": "0b102fc8-9835-4f67-8c7b-cf2731609d8b",
        "AZURE_CLIENT_SECRET": "nwAyfc5RLg_UJ~5~G_u7EGL~Kn7yR~TZ2Q"
    }
    return params


def get_iam_b2c_azure_params_sit():
    params = {
        "B2B_SERVER_NAME": "b2biamgbussit1.b2clogin.com",
        "B2B_PATH": "b2biamgbussit1.onmicrosoft.com",
        "AZURE_CLIENT_ID": "c1459bb4-3e89-434e-b2ef-77abcb333c43",
        "AZURE_CLIENT_SECRET": "FIyzZ7vwOS~1jlO_iP0b1~38_yQkMwN~o4"
    }
    return params


def get_iam_b2c_policy_params(country):
    params = {
        "B2B_SIGNIN_POLICY": "B2C_1A_SigninMobile_{0}".format(country),
        "B2B_SIGNUP_POLICY": "B2C_1A_SignUp_{0}".format(country),
        "B2B_ONBOARDING_POLICY": "B2C_1A_Onboarding_{0}".format(country)
    }
    return params


def get_b2c_ropc_params(country, environment):
    b2c_azure_params = get_iam_b2c_azure_params(environment)
    b2b_server_name = b2c_azure_params['B2B_SERVER_NAME']
    b2b_path = b2c_azure_params['B2B_PATH']

    client_id = get_b2c_web_application_id(country, environment)

    request_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    request_body = {
        'username': 'qm.team.{0}+b2clogin@mailinator.com'.format(country).lower(),
        'password': 'Password1',
        'grant_type': 'password',
        'client_id': client_id,
        'response_type': 'token id_token',
        'scope': 'openid {0}'.format(client_id)
    }

    params = {
        'request_url': 'https://{0}/{1}/B2C_1A_ROPC_{2}/oauth2/v2.0/token'.format(b2b_server_name, b2b_path, country),
        'request_body': urllib.parse.urlencode(request_body),
        'request_headers': request_headers
    }

    return params


def get_b2c_web_application_id(country, environment):
    if get_iam_b2c_environment_uat(environment):
        return get_b2c_web_application_id_uat(country)
    else:
        return get_b2c_web_application_id_sit(country)


def get_b2c_web_application_id_uat(country):
    params = {
        'AR': 'fba61bce-50d5-426c-b7cb-2915d577d784',
        'BR': 'e4502f2d-c14a-426f-8149-08954f4a9df5',
        'CO': '7d659ba2-1a3c-4a09-b62e-308aad83bb67',
        'DO': '197968bd-f5fa-492d-a8d0-36e6b6126fd9',
        'EC': '1359f5e5-09c7-4937-93f9-52656df3654a',
        'MX': '1cf501fc-2977-4178-ab2b-0f2bd07cd057',
        'PE': '6dfc84ba-e587-41e4-83c7-7ad21b214361',
        'ZA': '9fa1e0e1-7c61-4d6c-a422-976547b6cb89'
    }

    return params[country]


def get_b2c_web_application_id_sit(country):
    params = {
        'AR': '',
        'BR': '',
        'CO': '9a362195-d403-4b37-acd4-5133f5d028e4',
        'DO': '',
        'EC': '',
        'MX': '',
        'PE': '',
        'ZA': ''
    }

    return params[country]
