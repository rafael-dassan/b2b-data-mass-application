# Standard library imports
from unicodedata import numeric


def validate_yes_no_option(option):
    options = ['Y', 'N']
    if option in options:
        return True
    else:
        return False


# Validate State in account creation flow
def validate_state(zone):
    return {
        'BR': 'RIO DE JANEIRO',
        'DO': 'SANTO DOMINGO',
        'ZA': 'FREE STATE',
        'CO': 'SAN ALBERTO',
        'MX': 'CIDADE DO MEXICO',
        'AR': 'CORRIENTES',
        'PE': 'SANTA CRUZ',
        'EC': 'GUAYAS'

    }.get(zone, 'false')


# Validate length of account name
def validate_account_name(name):
    if len(name) == 0:
        return False
    else:
        return name


def validate_payments_method(payments_method):
    size_payments_method = len(payments_method)

    if size_payments_method == 0:
        return 'error_0'
    elif (size_payments_method > 0) and (is_number(payments_method) == 'false'):
        return 'not_number'
    elif (int(payments_method) != 1) and (int(payments_method) != 2) and (int(payments_method) != 3) \
            and (int(payments_method) != 4):
        return 'not_payments_method'
    else:
        return 'true'


# Validate if value is a number
def is_number(s):
    try:
        float(s)
        return 'true'
    except ValueError:
        pass

    try:
        numeric(s)
        return 'true'
    except (TypeError, ValueError):
        pass

    return 'false'


# Validate length of Account ID
def validate_account(account_id, zone):
    size_account_id = len(account_id)

    if size_account_id == 0:
        return 'error_0'
    elif (size_account_id > 0) and (is_number(account_id) == 'false'):
        return 'not_number'
    elif (zone == 'DO') and (is_number(account_id) == 'true') and (size_account_id < 10):
        return 'error_10'
    elif (zone == 'BR') and ((size_account_id == 11) or (size_account_id == 14)):
        return 'true'
    elif (zone == 'BR') and ((size_account_id != 11) or (size_account_id != 14)):
        return 'error_cnpj_cpf'
    elif is_number(account_id) == 'true':
        return 'true'


# Validate account sub-menus for Data Searching
def validate_accounts(option):
    options = ['1', '2', '3']
    if option in options:
        return 'true'
    else:
        return 'false'


def validate_deals_options(option):
    valid_options = ['1', '2', '3', '4', '5']
    if option in valid_options:
        return True
    else:
        return False


def validate_option_sku(option):
    options = ['1', '2']
    if option in options:
        return 'true'
    else:
        return 'false'


def validate_zone_for_ms(zone):
    return {
        'BR': 'true',
        'DO': 'true',
        'ZA': 'true',
        'CO': 'true',
        'MX': 'true',
        'AR': 'true',
        'PE': 'true',
        'EC': 'true'
    }.get(zone, 'false')


def validate_environment(environment):
    environments = ['DEV', 'SIT', 'UAT']
    if environment in environments:
        return True
    else:
        return False


def validate_invoice_options(option):
    options = ['1', '2', '3']
    if option in options:
        return True
    else:
        return False


def validate_invoice_status(option):
    options = ['1', '2', '3']
    if option in options:
        return True
    else:
        return False


def validate_invoice_payment_method(option):
    options = ['1', '2']
    if option in options:
        return True
    else:
        return False


def validate_account_operations_structure(option):
    valid_options = ['1', '2', '3', '4', '5', '6', '7']
    if option in valid_options:
        return True
    else:
        return False


def validate_product_operations_structure(option):
    options = ['1', '2', '3', '4', '5']
    if option in options:
        return True
    else:
        return False


def validate_recommendation_type(option):
    options = ['1', '2', '3', '4', '5']
    if option in options:
        return True
    else:
        return False


def validate_get_products(option):
    options = ['1', '2', '3']
    if option in options:
        return True
    else:
        return False


def validate_structure(option):
    options = ['1', '2', '3', '4', '5']
    if option in options:
        return 'true'
    else:
        return 'false'


def validate_rewards(option):
    options = ['1', '2', '3', '4', '5', '6', '7']
    if option in options:
        return 'true'
    else:
        return 'false'


def validate_orders(option):
    options = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    if option in options:
        return 'true'
    else:
        return 'false'