def valid_country(country):
    switcher = {
        "AR": True,
        "BR": True,
        "CL": True,
        "DO": True,
        "ZA": True,
        "CO": True
    }

    return switcher.get(country, False)

def valid_environment(environment):
    switcher = {
        "SIT": True,
        "UAT": True,
        "DEV": True,
        "QA": True,
    }

    return switcher.get(environment, False)

def valid_parameters(parameters):
    if len(parameters) != 4:
        return False

    return True

def valid_execution_type(execution_type):
    switcher = {
        "all": True,
        "common": True
    }

    return switcher.get(execution_type, False)
