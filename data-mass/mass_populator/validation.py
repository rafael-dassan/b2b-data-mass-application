def valid_country(country):
    switcher = {
        "AR": True,
        "BR": True,
        "CO": True,
        "DO": True,
        "EC": True,
        "MX": True,
        "PE": True,
        "ZA": True
    }
    return switcher.get(country, False)


def valid_environment(environment):
    switcher = {
        "SIT": True,
        "UAT": True,
        "DEV": True
    }
    return switcher.get(environment, False)


def valid_parameters(parameters):
    if len(parameters) != 4:
        return False
    return True


def valid_execution_type(execution_type):
    switcher = {
        "gateway": True,
        "regression": True,
        "test": True,
        "product": True,
        "rewards": True
    }
    return switcher.get(execution_type, False)
