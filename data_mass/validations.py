from unicodedata import numeric


def validate_yes_no_option(option):
    options = ['Y', 'N']
    return option in options


# Validate length of account name
def validate_account_name(name):
    if len(name) == 0:
        return False
    else:
        return name


def validate_payments_method(payments_method, zone=None):
    size_payments_method = len(payments_method)

    if size_payments_method == 0:
        return 'error_0'
    elif (size_payments_method > 0) and not is_number(payments_method):
        return 'not_number'
    elif (int(payments_method) != 1) and (int(payments_method) != 2) and (int(payments_method) != 3) \
            and (int(payments_method) != 4):
        return 'not_payments_method'
    elif zone == "AR" and int(payments_method) != 1:
        return 'not_payments_method'   
    else:
        return True


# Validate if value is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# Validate length of Account ID
def validate_account(account_id, zone):
    size_account_id = len(account_id)

    if size_account_id == 0:
        return 'error_0'
    elif (size_account_id > 0) and not is_number(account_id):
        return 'not_number'
    elif (zone == 'DO') and is_number(account_id) and (size_account_id < 10):
        return 'error_10'
    elif (zone == 'BR') and ((size_account_id == 11) or (size_account_id == 14)):
        return True
    elif (zone == 'BR') and ((size_account_id != 11) or (size_account_id != 14)):
        return 'error_cnpj_cpf'
    elif is_number(account_id):
        return True


# Validate account sub-menus for Data Searching
def validate_accounts(option):
    options = ['1']
    return option in options


def validate_deals_options(option):
    options = ['1', '2', '3', '4', '5', '6', '7']
    return option in options


def validate_option_sku(option):
    options = ['1', '2']
    return option in options


def validate_zone_for_interactive_combos_ms(zone):
    return {
        'BR': True,
        'CO': True,
        'AR': True,
        'DO': True,
        'CA': True,
        'PA': True,
        'PY': True
    }.get(zone, False)


def validate_zone_for_ms(zone):
    return {
        'AR': True,
        'BR': True,
        'CA': True,
        'CO': True,
        'DO': True,
        'EC': True,
        'MX': True,
        'PA': True,
        'PE': True,
        'PY': True,
        'ZA': True
    }.get(zone, False)


def validate_environment(environment):
    environments = ['DEV', 'SIT', 'UAT']
    return environment in environments


def validate_invoice_options(option):
    options = ['1', '2', '3']
    return option in options


def validate_invoice_status(option):
    options = ['1', '2', '3']
    return option in options


def validate_invoice_payment_method(option):
    options = ['1', '2']
    return option in options


def validate_account_operations_structure(option):
    options = ['1', '2', '3', '4', '5', '6', '7']
    return option in options


def validate_product_operations_structure(option):
    options = ['1', '2', '3', '4', '5', '6']
    return option in options


def validate_recommendation_type(option):
    options = ['1', '2', '3', '4', '5']
    return option in options


def validate_get_products(option):
    options = ['1', '2', '3']
    return option in options


def validate_structure(option):
    options = ['1', '2', '3', '4', '5', '6', '7']
    return option in options


def validate_rewards(selection):
    options = ['1', '2', '3', '4', '5', '6', '7']
    return selection in options


def validate_rewards_transactions(selection):
    options = ['1', '2', '3']
    return selection in options


def validate_rewards_programs(selection):
    options = ['1', '2', '3', '4']
    return selection in options


def validate_rewards_challenges(selection):
    options = ['1', '2', '3', '4', '5']
    return selection in options


def validate_orders(option):
    options = ['1', '2']
    return option in options


def validate_order_status(option):
    options = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    return option in options


def validate_order_sub_menu(option):
    options = ['1', '2']
    return option in options


# Validate option menu selection
def validate_option_request_selection(selection):
    return {
        '0': True,
        '1': True,
        '2': True,
        '3': True,
        '4': True,
        '5': True,
        '6': True,
        '7': True,
        '8': True,
        '9': True,
        '10': True,
        '11': True
    }.get(selection, False)


def validate_delivery_window_structure(option):
    options = ['1', '2']
    return option in options


def validate_supplier_menu_structure(selection):
    return {
       '0': True,
       '1': True,
       '2': True,
       '3': True,
       '4': True,
       '5': True,
       '6': True,
       '7': True
    }.get(selection, False)


def validate_option_att(selection):
    options = ['1', '2']
    return selection in options


def validate_attribute_menu_structure(selection, is_enum):
    option = ['1', '2', '3']
    if not is_enum:
        option.append('4')
    return selection in option


def validate_supplier_category_menu_structure(selection):
    option = ['1', '2']
    return selection in option


def validate_supplier_search_menu_structure(selection):
    return {
       '0': True,
       '1': True,
       '2': True,
       '3': True,
       '4': True
    }.get(selection, False)


def validate_option_type(selection):
    options = ['1', '2', '3']
    return selection in options


def validate_sku(sku_id, enabled_skus):
    return sku_id in enabled_skus


def validate_environment_supplier(environment):
    environments = ['DEV', 'SIT', 'UAT', 'LOCAL']
    return environment in environments