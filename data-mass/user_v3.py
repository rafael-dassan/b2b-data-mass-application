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
        },
        "CA": {
            "REDIRECT_URL": "com.abi.bees.canada://oauth/redirect",
            "CLIENT_ID": "db2c51ee-28c6-42c7-b73f-9dde1a3a172b"
        },
        "PA": {
            "REDIRECT_URL": "com.abi.bees.panama://oauth/redirect",
            "CLIENT_ID": "8f104034-2aa1-4ca9-88c1-8ec2964fb5a4"
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
        },
        "CA": {
            "REDIRECT_URL": "com.abi.bees.canada://oauth/redirect",
            "CLIENT_ID": "ca40d468-d8d7-443b-bd68-abaf13217b11"
        },
        "PA": {
            "REDIRECT_URL": "com.abi.bees.panama://oauth/redirect",
            "CLIENT_ID": "81a16250-678d-46a4-ad0b-b36311cf0a96"
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
