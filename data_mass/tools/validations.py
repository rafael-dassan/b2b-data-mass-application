"""Validations tools for Data Mass use."""
from typing import Any, Optional, Union
from unicodedata import numeric


def validate_option_request_selection_for_structure_2(option: str):
    """
    Validate option menu selection.

    Parameters
    ----------
    option: str

    Returns
    -------
    bool
        Whenever an option is valid.
    """
    switcher = {
        "0": True,
        "1": True,
        "2": True
    }

    value = switcher.get(option, False)
    return value


def validate_zone_for_combos(zone: str) -> bool:
    """
    Validate zone for Combos.

    Parameters
    ----------
    zone : str

    Returns
    -------
    bool
        Whenever an option is valid.
    """
    switcher = {
        "AR": True,
        "BR": True,
        "CA": True,
        "DO": True,
        "MX": True
    }

    value = switcher.get(zone, False)

    return value


def validate_zone_for_combos_dt(zone: str) -> bool:
    """
    Validate zone for Combos DT.

    Parameters
    ----------
    zone : str

    Returns
    -------
    bool
        Whenever an option is valid.
    """
    switcher = {
        "BR": True,
        "DO": True,
        "AR": True,
        "CO": True,
        "ZA": True,
        "MX": True,
        "PE": True,
        "EC": True
    }

    return switcher.get(zone, False)


def validate_environment_user_creation(environment: str) -> bool:
    """
    Validate environment to User creation.

    Parameters
    ----------
    environment : str

    Returns
    -------
    bool
        Whenever an option is valid.
    """
    switcher = {
        "DT": True,
        "SIT": True,
        "UAT": True
    }

    return switcher.get(environment, False)


def validate_combo_structure(option: str) -> bool:
    """
    Validate combo type structure.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever an option is valid.
    """
    options = ["1", "2", "3", "4", "5"]

    if option in options:
        return True

    return False


def validate_country_menu_in_user_create_iam(zone: str) -> bool:
    """
    Validate country menu in user create iam.

    Parameter
    ---------
    zone : str

    Returns
    -------
    bool
        Whenever an option is valid.
    """
    switcher = {
        "BR": True,
        "CO": True,
        "DO": True,
        "MX": True,
        "EC": True,
        "PE": True,
        "ZA": True,
        "AR": True,
        "CA": True,
        "PA": True
    }

    return switcher.get(zone, False)


def validate_environment_menu_in_user_create_iam(environment: str) -> bool:
    """
    Validate environment menu in user create iam.

    Parameter
    ---------
    environment : str

    Returns
    -------
    bool
        Whenever an option is valid.
    """
    switcher = {
        "QA": True,
        "SIT": True,
        "UAT": True
    }

    return switcher.get(environment, False)


def validate_month(month: str):
    """
    Validate month.

    Parameter
    ---------
    environment : str

    Returns
    -------
    bool
        Whenever an option is valid.
    """
    switcher = {
        "01": True,
        "02": True,
        "03": True,
        "04": True,
        "05": True,
        "06": True,
        "07": True,
        "08": True,
        "09": True,
        "10": True,
        "11": True,
        "12": True
    }

    value = switcher.get(month, False)

    return value


def validate_years_credit_statement(year: int) -> Union[str, int]:
    """
    Validate years credit statement.

    Parameters
    ----------
    year : int

    Returns
    -------
    error_0 : str
        `year` size is empty.
    not_number : str
        `year` value is not a number.
    error_4 : str
        `year` size is not in the correct 4-character format.
    True : bool
        A valid option.
    """
    if len(year) == 0:
        return "error_0"
    elif (len(year) > 0) and not is_number(year):
        return "not_number"
    elif len(year) < 4:
        return "error_4"
    elif is_number(year):
        return True


def validate_invoice_id(invoice_id: str) -> Union[bool, str]:
    """
    Validate invoice id.

    Parameters
    ----------
    invoice_id : str

    Returns
    -------
    error_0 : str
        `invoice_id` size is empty.
    True : bool
        Whenever is a valid option.
    """
    size_invoice_id = len(invoice_id)

    if size_invoice_id == 0:
        return "error_0"

    return True


def validate_yes_no_option(option: str) -> bool:
    """
    Validate "yes" or "no" option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["Y", "N"]

    return option in options


def validate_account_name(name: str) -> Union[bool, str]:
    """
    Validate length of account name.

    Parameters
    ----------
    name : str

    Returns
    -------
    bool
        Whenever a name is valid.
    """
    # TODO: return `True` instead the name itself.
    if len(name) == 0:
        return False

    return name


def validate_payments_method(
        payments_method: list,
        zone: Optional[str] = None) -> Union[str, bool]:
    """
    Validate account operations structure option.

    Parameters
    ----------
    option : str

    Returns
    -------
    error_0 : str
        `payments_method` size is empty.
    not_number : str
        `payments_method` is not a number.
    not_payments_method : str
        Whenever a selected payment method is not valid one.
    True : bool
        If is a valid option.
    """
    size_payments_method = len(payments_method)

    if size_payments_method == 0:
        return "error_0"
    elif (size_payments_method > 0) and not is_number(payments_method):
        return "not_number"
    elif (int(payments_method) != 1) and (int(payments_method) != 2) and (int(payments_method) != 3) \
            and (int(payments_method) != 4):
        return "not_payments_method"
    elif zone == "AR" and int(payments_method) != 1:
        return "not_payments_method"
    else:
        return True


def is_number(string: str) -> bool:
    """
    Validate if a string is a number.

    Parameters
    ----------
    string : str

    Returns
    -------
    bool
        Whenever a string is a number.
    """
    try:
        float(string)
        return True
    except ValueError:
        pass

    try:
        numeric(string)
        return True
    except (TypeError, ValueError):
        pass

    return False


def validate_account(account_id: str, zone: str) -> Union[bool, str]:
    """
    Validate length of Account ID.

    Parameters
    ----------
    account_id : str
    zone : str

    Returns
    -------
    error_0 : str
        `payments_method` size is empty.
    not_number : str
        `payments_method` is not a number.
    error_10 : str
        If the account zone is DO, the account id must \
        have less than 10 characters.
    error_cnpj_cpf : str
        If the account zone is BR, the account id must \
        follow the same pattern as the CPF or CNPJ
    True : bool
        `account_id` is a valid account.
    """
    size_account_id = len(account_id)

    if size_account_id == 0:
        return "error_0"
    elif (size_account_id > 0) and not is_number(account_id):
        return "not_number"
    elif (zone == "DO") and is_number(account_id) and (size_account_id < 10):
        return "error_10"
    elif (zone == "BR") and ((size_account_id == 11) or (size_account_id == 14)):
        return True
    elif (zone == "BR") and ((size_account_id != 11) or (size_account_id != 14)):
        return "error_cnpj_cpf"
    elif is_number(account_id):
        return True


def validate_accounts(option: str) -> bool:
    """
    Validate account sub-menus for Data Searching.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1"]

    return option in options


def validate_deals_options(option: str) -> bool:
    """
    Validate deals options.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2", "3", "4", "5", "6", "7"]

    return option in options


def validate_option_sku(option: str) -> bool:
    """
    Validate sku option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2"]

    return option in options


def validate_zone_for_interactive_combos_ms(zone: str) -> bool:
    """
    Validate zone for interactive combos on microservice.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    return {
        "BR": True,
        "CO": True,
        "AR": True,
        "DO": True,
        "CA": True,
        "PA": True,
        "PY": True
    }.get(zone, False)


def validate_zone_for_ms(zone: str) -> bool:
    """
    Validate zone option for microservice.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    return {
        "AR": True,
        "BR": True,
        "CA": True,
        "CO": True,
        "DO": True,
        "EC": True,
        "MX": True,
        "PA": True,
        "PE": True,
        "PY": True,
        "ZA": True
    }.get(zone, False)


def validate_environment(environment: str) -> bool:
    """
    Validate environment option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    environments = ["DEV", "SIT", "UAT"]

    return environment in environments


def validate_invoice_options(option: str) -> bool:
    """
    Validate invoice option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2", "3"]

    return option in options


def validate_invoice_status(option: str) -> bool:
    """
    Validate invoice status option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2", "3"]

    return option in options


def validate_invoice_payment_method(option: str) -> bool:
    """
    Validate invoice payment method option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2"]

    return option in options


def validate_account_operations_structure(option: str) -> bool:
    """
    Validate account operations structure option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2", "3", "4", "5", "6", "7"]

    return option in options


def validate_product_operations_structure(option: str) -> bool:
    """
    Validate product operations structure option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2", "3", "4", "5", "6"]

    return option in options


def validate_recommendation_type(option: str) -> bool:
    """
    Validate recommendation type option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2", "3", "4", "5"]

    return option in options


def validate_get_products(option: str) -> bool:
    """
    Validate get products option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2", "3"]

    return option in options


def validate_structure(option: str) -> bool:
    """
    Validate order sub menu option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2", "3", "4", "5", "6", "7"]

    return option in options


def validate_rewards(selection: str) -> bool:
    """
    Validate rewards option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2", "3", "4", "5", "6", "7"]

    return selection in options


def validate_rewards_transactions(selection: str) -> bool:
    """
    Validate rewards transactions option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2", "3"]

    return selection in options


def validate_rewards_programs(selection: str) -> bool:
    """
    Validate rewards programs option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2", "3", "4"]

    return selection in options


def validate_rewards_challenges(selection: str) -> bool:
    """
    Validate rewards challenges option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2", "3", "4", "5"]

    return selection in options


def validate_orders(option: str) -> bool:
    """
    Validate validate orders option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2"]

    return option in options


def validate_order_status(option: str) -> bool:
    """
    Validate order status option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = [
        "1", "2", "3", "4", "5", "6",
        "7", "8", "9", "10", "11"
    ]

    return option in options


def validate_order_sub_menu(option: str) -> bool:
    """
    Validate order sub menu option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2"]

    return option in options


def validate_option_request_selection(selection: str) -> bool:
    """
    Validate option request selection.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    return {
        "0": True,
        "1": True,
        "2": True,
        "3": True,
        "4": True,
        "5": True,
        "6": True,
        "7": True,
        "8": True,
        "9": True,
        "10": True,
        "11": True
    }.get(selection, False)


def validate_delivery_window_structure(option: str) -> bool:
    """
    Validate delivery window structure option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2"]

    return option in options


def validate_supplier_menu_structure(selection: str) -> bool:
    """
    Validate supplier menu structure option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    return {
       "0": True,
       "1": True,
       "2": True,
       "3": True,
       "4": True,
       "5": True,
       "6": True,
       "7": True
    }.get(selection, False)


def validate_option_att(selection: str) -> bool:
    """
    Validate attribute option.

    Parameters
    ----------
    selection : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2"]

    return selection in options


def validate_attribute_menu_structure(selection: str, is_enum: Any) -> bool:
    """
    Validate attribute menu structure option.

    Parameters
    ----------
    selection : str
    is_enum : ANy

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    option = ["1", "2", "3"]

    if not is_enum:
        option.append("4")

    return selection in option


def validate_supplier_category_menu_structure(selection: str) -> bool:
    """
    Validate supplier category menu structure option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    option = ["1", "2"]

    return selection in option


def validate_supplier_search_menu_structure(selection: str) -> bool:
    """
    Validate supplier search menu structure option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    return {
       "0": True,
       "1": True,
       "2": True,
       "3": True,
       "4": True
    }.get(selection, False)


def validate_option_type(selection: str):
    """
    Validate option type option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    options = ["1", "2", "3"]

    return selection in options


def validate_sku(sku_id: str, enabled_skus: list) -> bool:
    """
    Validate sku option.

    Parameters
    ----------
    sku_id : str
    enabled_skus : list

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    # TODO: stop using this method and use `in` keyword directly
    return sku_id in enabled_skus


def validate_environment_supplier(environment: str):
    """
    Validate environment supplier option.

    Parameters
    ----------
    option : str

    Returns
    -------
    bool
        Whenever a option is valid.
    """
    environments = ["DEV", "SIT", "UAT", "LOCAL"]

    return environment in environments
