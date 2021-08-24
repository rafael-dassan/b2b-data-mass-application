AUTH_REDIRECT = "://oauth/redirect"
BASE_REDIRECT = "com.abi.bees."

def get_iam_b2c_params(environment, country):
    b2c_country_params = get_iam_b2c_country_params(environment, country)
    b2c_azure_params = get_iam_b2c_azure_params(environment)
    b2c_policy_params = get_iam_b2c_policy_params(country)

    b2b_server_name = b2c_azure_params["B2B_SERVER_NAME"]
    b2b_path = b2c_azure_params["B2B_PATH"]
    b2b_signin_policy = b2c_policy_params["B2B_SIGNIN_POLICY"]
    b2b_signup_policy = b2c_policy_params["B2B_SIGNUP_POLICY"]
    b2b_onboarding_policy = b2c_policy_params["B2B_ONBOARDING_POLICY"]

    base_url = f"https://{b2b_server_name}/{b2b_path}/"

    params = {
        "B2B_SERVER_NAME": b2b_server_name,
        "B2B_PATH": b2b_path,
        "B2B_SIGNIN_POLICY": b2b_signin_policy,
        "B2B_SIGNUP_POLICY": b2b_signup_policy,
        "B2B_ONBOARDING_POLICY": b2b_onboarding_policy,
        "OTP_SECRET": "1NcRfUjXn2r4u7x!A%D*G-KaPdSgVkYp",
        "OTP_INTERVAL": 600,
        "BASE_SIGNIN_URL": f"{base_url}{b2b_signin_policy}",
        "BASE_SIGNUP_URL": f"{base_url}{b2b_signup_policy}",
        "BASE_ONBOARDING_URL": f"{base_url}{b2b_onboarding_policy}",
        "REDIRECT_URL": b2c_country_params["REDIRECT_URL"],
        "CLIENT_ID": b2c_country_params["CLIENT_ID"],
        "AZURE_CLIENT_ID": b2c_azure_params["AZURE_CLIENT_ID"],
        "AZURE_CLIENT_SECRET": b2c_azure_params["AZURE_CLIENT_SECRET"]
    }
    return params


def get_iam_b2c_country_params(environment, country):
    iam_b2c_country_params = {
        "QA": get_iam_b2c_country_params_qa(country),
        "SIT": get_iam_b2c_country_params_sit(country),
        "UAT": get_iam_b2c_country_params_uat(country)
    }
    return iam_b2c_country_params[environment]


def get_iam_b2c_country_params_uat(country):
    params = {
        "AR": {
            "REDIRECT_URL": f"com.abi.Quilmes{AUTH_REDIRECT}",
            "CLIENT_ID": "f7e20a58-35a2-47f8-bb73-1735dd354d20"
        },
        "BR": {
            "REDIRECT_URL": f"com.abi.parceiro-ambev{AUTH_REDIRECT}",
            "CLIENT_ID": "442357fe-e514-4919-816c-4baa02b41a6f"
        },
        "US": {
            "REDIRECT_URL": f"{BASE_REDIRECT}unitedstates{AUTH_REDIRECT}",
            "CLIENT_ID": "PENDING MIGRATION" #TODO: does not have client id yet
        },
        "CO": {
            "REDIRECT_URL": f"{BASE_REDIRECT}colombia{AUTH_REDIRECT}",
            "CLIENT_ID": "f1d909d8-f72a-40cd-a7ff-fec8e5b033fc"
        },
        "DO": {
            "REDIRECT_URL": f"com.abi.socio-cerveceria{AUTH_REDIRECT}",
            "CLIENT_ID": "2fb9932f-5ac2-4f9d-91d7-35ea363cde34"
        },
        "EC": {
            "REDIRECT_URL": f"{BASE_REDIRECT}ecuador{AUTH_REDIRECT}",
            "CLIENT_ID": "e0f49717-83f3-4777-8bb7-510541203312"
        },
        "MX": {
            "REDIRECT_URL": f"{BASE_REDIRECT}mexico{AUTH_REDIRECT}",
            "CLIENT_ID": "1841724c-1311-47e9-8894-a5a0e8a44197"
        },
        "PA": {
            "REDIRECT_URL": f"{BASE_REDIRECT}panama{AUTH_REDIRECT}",
            "CLIENT_ID": "8f104034-2aa1-4ca9-88c1-8ec2964fb5a4"
        },
        "PE": {
            "REDIRECT_URL": f"{BASE_REDIRECT}peru{AUTH_REDIRECT}",
            "CLIENT_ID": "d8cfa150-0ad2-43f1-a85e-2d4e634f5f72"
        },
        "PY": {
            "REDIRECT_URL": f"{BASE_REDIRECT}paraguay{AUTH_REDIRECT}",
            "CLIENT_ID": "f0a743c3-4c9f-49c9-8a13-6a7fba9acec1"
        },
        "SV": {
            "REDIRECT_URL": f"{BASE_REDIRECT}elsalvador{AUTH_REDIRECT}",
            "CLIENT_ID": "c14de1b3-c530-42b2-a9de-00a16748f897"
        },
        "UY": {
            "REDIRECT_URL": f"{BASE_REDIRECT}uruguay{AUTH_REDIRECT}",
            "CLIENT_ID": "PENDING" #TODO: does not have client id yet
        },
        "ZA": {
            "REDIRECT_URL": f"com.abi.sab-connect{AUTH_REDIRECT}",
            "CLIENT_ID": "499bf4c3-5c26-4e21-8ad8-c01957937cd5"
        }
    }
    return params[country]


def get_iam_b2c_country_params_sit(country):
    params = {
        "AR": {
            "REDIRECT_URL": f"com.abi.Quilmes{AUTH_REDIRECT}",
            "CLIENT_ID": "2ff1221e-a82d-49c5-8d22-b48db8bc07f6"
        },
        "BR": {
            "REDIRECT_URL": f"com.abi.parceiro-ambev{AUTH_REDIRECT}",
            "CLIENT_ID": "4a5ba64b-5053-439b-b29f-27cae493699f"
        },
        "US": {
            "REDIRECT_URL": f"{BASE_REDIRECT}unitedstates{AUTH_REDIRECT}",
            "CLIENT_ID": "77ae3bb9-c4b1-45d8-959f-a2a0b6c5f5c8"
        },
        "CO": {
            "REDIRECT_URL": f"{BASE_REDIRECT}colombia{AUTH_REDIRECT}",
            "CLIENT_ID": "70eb36b1-2894-4f1d-b08a-4a1f982a38da"
        },
        "DO": {
            "REDIRECT_URL": f"com.abi.socio-cerveceria{AUTH_REDIRECT}",
            "CLIENT_ID": "a416b8f5-4061-4984-a2f7-a6dca86e68ae"
        },
        "EC": {
            "REDIRECT_URL": f"{BASE_REDIRECT}ecuador{AUTH_REDIRECT}",
            "CLIENT_ID": "1d11cc25-779f-458e-a64b-8f4e42b0c8fd"
        },
        "MX": {
            "REDIRECT_URL": f"{BASE_REDIRECT}mexico{AUTH_REDIRECT}",
            "CLIENT_ID": "32a701c0-fbd0-481b-9028-809a0a1468f5"
        },
        "PA": {
            "REDIRECT_URL": f"{BASE_REDIRECT}panama{AUTH_REDIRECT}",
            "CLIENT_ID": "81a16250-678d-46a4-ad0b-b36311cf0a96"
        },
        "PE": {
            "REDIRECT_URL": f"{BASE_REDIRECT}peru{AUTH_REDIRECT}",
            "CLIENT_ID": "be042e86-59a4-410e-baf4-77bfaca00774"
        },
        "PY": {
            "REDIRECT_URL": f"{BASE_REDIRECT}paraguay{AUTH_REDIRECT}",
            "CLIENT_ID": "14c66e8e-4820-4426-87e1-9eaa957654a7"
        },
        "SV": {
            "REDIRECT_URL": f"{BASE_REDIRECT}elsalvador{AUTH_REDIRECT}",
            "CLIENT_ID": "1cf64385-7461-466e-9caf-8017cd69be71"
        },
        "UY": {
            "REDIRECT_URL": f"{BASE_REDIRECT}uruguay{AUTH_REDIRECT}",
            "CLIENT_ID": "4fc8fc13-f714-4bb3-9233-98ad3f59a446"
        },
        "ZA": {
            "REDIRECT_URL": f"com.abi.sab-connect{AUTH_REDIRECT}",
            "CLIENT_ID": "2cca5cb9-b89d-4986-a427-63af29d0149d"
        }
    }
    return params[country]


def get_iam_b2c_country_params_qa(country):
    params = {
        "AR": {
            "REDIRECT_URL": f"com.abi.Quilmes{AUTH_REDIRECT}",
            "CLIENT_ID": "53305725-0200-49f0-80c4-6e70b4c44148"
        },
        "BR": {
            "REDIRECT_URL": f"com.abi.parceiro-ambev{AUTH_REDIRECT}",
            "CLIENT_ID": "421489e0-e644-4d18-9a79-7624b08ce6b0"
        },
        "US": {
            "REDIRECT_URL": f"{BASE_REDIRECT}unitedstates{AUTH_REDIRECT}",
            "CLIENT_ID": "3034f6e0-72f9-49be-943e-55bf1a7f0b9c"
        },
        "CO": {
            "REDIRECT_URL": f"{BASE_REDIRECT}colombia{AUTH_REDIRECT}",
            "CLIENT_ID": "f26757ab-8795-4f19-95fa-792373ae3474"
        },
        "DO": {
            "REDIRECT_URL": f"{BASE_REDIRECT}cerveceria{AUTH_REDIRECT}",
            "CLIENT_ID": "2ad5019f-376d-4f99-a9bf-80521264a66e"
        },
        "EC": {
            "REDIRECT_URL": f"{BASE_REDIRECT}ecuador{AUTH_REDIRECT}",
            "CLIENT_ID": "e0f49717-83f3-4777-8bb7-510541203312"
        },
        "MX": {
            "REDIRECT_URL": f"{BASE_REDIRECT}mexico{AUTH_REDIRECT}",
            "CLIENT_ID": "e14f916f-8b28-460e-adcf-f0dbbae66848"
        },
        "CA": {
            "REDIRECT_URL": f"{BASE_REDIRECT}canada{AUTH_REDIRECT}",
            "CLIENT_ID": "84394e98-c074-4ffb-9f84-c61bfc9cd682"
        },
        "PA": {
            "REDIRECT_URL": f"{BASE_REDIRECT}panama{AUTH_REDIRECT}",
            "CLIENT_ID": "1dc243f0-773e-4920-947e-d43aefff59bb"
        },
        "PE": {
            "REDIRECT_URL": f"{BASE_REDIRECT}peru{AUTH_REDIRECT}",
            "CLIENT_ID": "6467b1ca-ed3a-4a11-86a9-d4187f2e1e07"
        },
        "PY": {
            "REDIRECT_URL": f"{BASE_REDIRECT}paraguay{AUTH_REDIRECT}",
            "CLIENT_ID": "14c66e8e-4820-4426-87e1-9eaa957654a7"
        },
        "SV": {
            "REDIRECT_URL": f"{BASE_REDIRECT}elsalvador{AUTH_REDIRECT}",
            "CLIENT_ID": "6825bcad-aeae-4d36-8f7c-7af32d316f56"
        },
        "UY": {
            "REDIRECT_URL": f"{BASE_REDIRECT}uruguay{AUTH_REDIRECT}",
            "CLIENT_ID": "78ac7217-900d-4139-b064-43b9cdbc681c"
        },
        "ZA": {
            "REDIRECT_URL": f"com.abi.sab-connect{AUTH_REDIRECT}",
            "CLIENT_ID": "d427d243-2f42-40ff-849c-1d67d3590fa8"
        }
    }

    return params[country]


def get_iam_b2c_azure_params(environment):
    iam_b2c_environment = {
        "QA": get_iam_b2c_azure_params_qa(),
        "SIT": get_iam_b2c_azure_params_sit(),
        "UAT": get_iam_b2c_azure_params_uat()
    }
    return iam_b2c_environment[environment]


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


def get_iam_b2c_azure_params_qa():
    params = {
        "B2B_SERVER_NAME": "b2biamgbusqa1.b2clogin.com",
        "B2B_PATH": "b2biamgbusqa1.onmicrosoft.com",
        "AZURE_CLIENT_ID": "1285777d-20f2-4e39-8866-cb80d0b922e7",
        "AZURE_CLIENT_SECRET": "cbA9Pu8ejf_rPy1Kb0i5a~83_90zZ8g_Db"
    }

    return params


def get_iam_b2c_policy_params(country):
    params = {
        "B2B_SIGNIN_POLICY": f"B2C_1A_SigninMobile_{country}",
        "B2B_SIGNUP_POLICY": f"B2C_1A_SignUp_{country}",
        "B2B_ONBOARDING_POLICY": f"B2C_1A_Onboarding_{country}"
    }

    return params
