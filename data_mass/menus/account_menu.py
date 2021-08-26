import click

# Local application imports
from data_mass.classes.text import text
from data_mass.validations import (
    validate_account,
    validate_account_email_owner,
    validate_account_name,
    validate_account_operations_structure,
    validate_accounts,
    validate_delivery_window_structure,
    validate_payments_method,
    validate_yes_no_option
)

DEFAULT_TEXT_COLOR = text.default_text_color
YELLOW = text.Yellow
INVALID_OPTION = f"{text.Red}\n- Invalid option"


def print_account_operations_menu():
    print(DEFAULT_TEXT_COLOR + '\nAccount operations')
    print(DEFAULT_TEXT_COLOR + str(1), YELLOW + 'Create/update account')
    print(DEFAULT_TEXT_COLOR + str(2), YELLOW + 'Create/update delivery window')
    print(DEFAULT_TEXT_COLOR + str(3), YELLOW + 'Create/update credit information')
    print(DEFAULT_TEXT_COLOR + str(4), YELLOW + 'Update account name')
    print(DEFAULT_TEXT_COLOR + str(5), YELLOW + 'Update account status')
    print(DEFAULT_TEXT_COLOR + str(6), YELLOW + 'Update minimum order type/value')
    print(DEFAULT_TEXT_COLOR + str(7), YELLOW + 'Update payment method')
    print(DEFAULT_TEXT_COLOR + str(8), YELLOW + 'Update rewards eligibility')
    option = input(DEFAULT_TEXT_COLOR + '\nPlease select: ')
    while validate_account_operations_structure(option) is False:
        print(f"{text.Red}\n- Invalid option")
        print(DEFAULT_TEXT_COLOR + '\nAccount operations')
        print(DEFAULT_TEXT_COLOR + str(1), YELLOW + 'Create/update account')
        print(DEFAULT_TEXT_COLOR + str(2), YELLOW + 'Create/update delivery window')
        print(DEFAULT_TEXT_COLOR + str(3), YELLOW + 'Create/update credit information')
        print(DEFAULT_TEXT_COLOR + str(4), YELLOW + 'Update account name')
        print(DEFAULT_TEXT_COLOR + str(5), YELLOW + 'Update account status')
        print(DEFAULT_TEXT_COLOR + str(6), YELLOW + 'Update minimum order type/value')
        print(DEFAULT_TEXT_COLOR + str(7), YELLOW + 'Update payment method')
        print(DEFAULT_TEXT_COLOR + str(8), YELLOW + 'Update rewards eligibility')
        option = input(DEFAULT_TEXT_COLOR + '\nPlease select: ')

    return option


def delivery_window_menu():
    print(f"{DEFAULT_TEXT_COLOR}\nDelivery window options:")
    print(f"{DEFAULT_TEXT_COLOR}1 {YELLOW}Create default delivery window")
    print(
        f"{DEFAULT_TEXT_COLOR}2 "
        f"{YELLOW}Create delivery window with specific date"
    )
    print(
        f"{DEFAULT_TEXT_COLOR}3 "
        f"{YELLOW}Create delivery window with range date"
    )
    option = input(f"{DEFAULT_TEXT_COLOR}\nPlease select: ")
    while not validate_delivery_window_structure(option):
        print(INVALID_OPTION)
        print(f"{DEFAULT_TEXT_COLOR}\nDelivery window options:")
        print(f"{DEFAULT_TEXT_COLOR}1 {YELLOW}Create default delivery window")
        print(
            f"{DEFAULT_TEXT_COLOR}2 "
            f"{YELLOW}Create delivery window with specific date"
        )
        print(
            f"{DEFAULT_TEXT_COLOR}3 "
            f"{YELLOW}Create delivery window with range date"
        )
        option = input(f"{DEFAULT_TEXT_COLOR}\nPlease select: ")
    return option


def print_order_menu(order_type: str = "Minimum"):
    option = input(f"{DEFAULT_TEXT_COLOR}Do you want to include the {order_type.lower()} order parameter? y/N: ")
    while validate_yes_no_option(option.upper()) is False:
        print(INVALID_OPTION)
        option = input(f"{DEFAULT_TEXT_COLOR}Do you want to include the {order_type.lower()} order parameter? y/N: ")

    return option.upper()


def print_minimum_order_type_menu():
    minimum_order_type = input(
        DEFAULT_TEXT_COLOR + 'Minimum order type (1. Product quantity / 2. Order volume / 3. Order total): ')
    while minimum_order_type == '' or (int(minimum_order_type) != 1 and int(minimum_order_type) != 2
                                       and int(minimum_order_type) != 3):
        print(INVALID_OPTION)
        minimum_order_type = input(
            DEFAULT_TEXT_COLOR + 'Minimum order type (1. Product quantity / 2. Order volume / 3. Order total): ')

    switcher = {
        '1': 'PRODUCT_QUANTITY',
        '2': 'ORDER_VOLUME',
        '3': 'ORDER_TOTAL'
    }

    minimum_order_type = switcher.get(minimum_order_type, False)

    return minimum_order_type


def print_order_value_menu(order_type: str = "Minimum"):
    minimum_order_value = input(f"{DEFAULT_TEXT_COLOR}{order_type} order value: ")

    while minimum_order_value == '' or int(minimum_order_value) <= 0:
        print(text.Red + '\n- SKU quantity must be greater than 0\n')
        minimum_order_value = input(f"{DEFAULT_TEXT_COLOR}{order_type} order value: ")

    return minimum_order_value


def print_account_status_menu():
    option = input(
        DEFAULT_TEXT_COLOR + 'Account status (1. Active / 2. Blocked): ')
    while option == '' and option != '1' and option != '2':
        print(INVALID_OPTION)
        option = input(
            DEFAULT_TEXT_COLOR + '\nAccount status (1. Active / 2. Blocked): ')

    switcher = {
        '1': 'ACTIVE',
        '2': 'BLOCKED'
    }

    status = switcher.get(option, False)

    return status


def print_account_name_menu():
    """
    Print account name menu.

    Returns
    -------
    str: name prompt by the user.
    """
    name = input(DEFAULT_TEXT_COLOR + 'Account name: ')
    while not validate_account_name(name):
        print(text.Red + '\n- The account name should not be empty')
        name = input(DEFAULT_TEXT_COLOR + 'Account name: ')
    return name


def print_owner_fisrt_name_menu():
    """
    Print account owner first name prompt.

    Returns
    -------
    str: name prompt by the user.
    """
    first_name = input(DEFAULT_TEXT_COLOR + 'Account name: ')
    while not validate_account_name(first_name):
        print(text.Red + '\n- The account name should not be empty')
        first_name = input(DEFAULT_TEXT_COLOR + 'Account name: ')
    return first_name


def print_owner_last_name_menu():
    """
    Print account owner last name prompt.

    Returns
    -------
    str: last name prompt by the user.
    """
    last_name = input(DEFAULT_TEXT_COLOR + 'Account last name: ')
    while not validate_account_name(last_name):
        print(text.Red + '\n- The last name should not be empty')
        last_name = input(DEFAULT_TEXT_COLOR + 'Account last name: ')
    return last_name


def print_account_email_owner_menu():
    """
    Prompt account e-mail owner.

    Returns
    -------
    ownder : dict
    """
    email = input(f"{DEFAULT_TEXT_COLOR}Account e-mail owner: ")
    while not validate_account_email_owner(email):
        print(text.Red + '\n- The account e-mail is not valid')
        email = input(f"{DEFAULT_TEXT_COLOR}Account e-mail owner: ")
    return email


def print_account_enable_empties_loan_menu():
    option = input(
        DEFAULT_TEXT_COLOR + 'Would you like to enable the loan of empties for this account? (1. Yes / 2. No): ')
    while option == '' and option != '1' and option != '2':
        print(INVALID_OPTION)
        option = input(
            DEFAULT_TEXT_COLOR + 'Would you like to enable the loan of empties for this account? (1. Yes / '
                                      '2. No): ')

    return {
        '1': True,
        '2': False
    }.get(option, False)


# Print alternative delivery date menu application
def print_alternative_delivery_date_menu():
    option = input(DEFAULT_TEXT_COLOR + 'Do you want to register an alternative delivery date? y/N: ')
    while not validate_yes_no_option(option.upper()):
        print(INVALID_OPTION)
        option = input(DEFAULT_TEXT_COLOR + '\nDo you want to register an alternative delivery date? y/N: ')

    return option


def print_include_delivery_cost_menu():
    """
    Print delivery cost (interest) menu.

    Returns
    -------
    str: user option.
    """
    option = input(
        f"{DEFAULT_TEXT_COLOR}\n"
        "Do you want to add delivery fee (interest/charge)? [y/N]: "
    )
    while not validate_yes_no_option(option.upper()):
        print(INVALID_OPTION)
        option = input(
            f"{DEFAULT_TEXT_COLOR}\n"
            "Do you want to add delivery fee (interest/charge)? y/N: "
        )
    return option


# Print payment method menu
def print_payment_method_menu(zone):
    payment_cash = ['CASH']

    if zone == 'BR':
        menu = (
            "Choose the payment method: \n"
            f"{text.default_text_color}1. {text.Yellow}CASH\n"
            f"{text.default_text_color}2. {text.Yellow}BANK SLIP\n"
            f"{text.default_text_color}3. {text.Yellow}CREDIT_CARD_POS\n"
            f"{text.default_text_color}4. {text.Yellow}CHECK\n"
            f"{text.default_text_color}5. {text.Yellow}CASH, BANK SLIP, CHECK, CREDIT_CARD_POS\n"
            f"{text.default_text_color}Option: "
        )

        payment_method = input(text.default_text_color + menu)
        while validate_payments_method(payment_method) != True:
            if validate_payments_method(payment_method) == 'error_0':
                print(text.Red + '\n- Payments Method should not be empty')
                payment_method = input(text.default_text_color + menu)
            elif validate_payments_method(payment_method) == 'not_number':
                print(text.Red + '\n- Payments Method should be numeric')
                payment_method = input(text.default_text_color + menu)
            elif validate_payments_method(payment_method) == 'not_payments_method':
                print(text.Red + '\n- Payments Method should be 1, 2, 3, 4, or 5')
                payment_method = input(text.default_text_color + menu)

        payment_credit = ['BANK_SLIP']
        payment_credit_pos = ['CREDIT_CARD_POS']
        payment_check = ['CHECK']
        payment_list = [
            'CASH',
            'BANK_SLIP',
            'CREDIT_CARD_POS',
            'CHECK',
        ]

        switcher = {
            '1': payment_cash,
            '2': payment_credit,
            '3': payment_credit_pos,
            '4': payment_check,
            '5': payment_list,
        }

        value = switcher.get(payment_method, False)
        return value

    elif zone in ['AR', 'UY']:
        payment_option = 'Choose the payment method (1. CASH): '
        payment_method = input(
            DEFAULT_TEXT_COLOR + payment_option)
        while validate_payments_method(payment_method, zone) != True:
            if validate_payments_method(payment_method, zone) == 'error_0':
                print(text.Red + '\n- Payments Method should not be empty')
                payment_method = input(
                    DEFAULT_TEXT_COLOR + payment_option)
            elif validate_payments_method(payment_method, zone) == 'not_number':
                print(text.Red + '\n- Payments Method should be numeric')
                payment_method = input(
                    DEFAULT_TEXT_COLOR + payment_option)
            elif validate_payments_method(payment_method, zone) == 'not_payments_method' or payment_method != '1':
                print(text.Red + '\n- Payments Method should be 1')
                payment_method = input(
                    DEFAULT_TEXT_COLOR + payment_option)

        switcher = {
            '1': payment_cash
        }

        value = switcher.get(payment_method, False)
        return value

    else:
        payment_options = 'Choose the payment method (1. CASH / 2. CREDIT / 3. CASH, CREDIT): '
        payment_method = input(
            DEFAULT_TEXT_COLOR + payment_options)
        while validate_payments_method(payment_method) != True:
            if validate_payments_method(payment_method) == 'error_0':
                print(text.Red + '\n- Payments Method should not be empty')
                payment_method = input(
                    DEFAULT_TEXT_COLOR + payment_options)
            elif validate_payments_method(payment_method) == 'not_number':
                print(text.Red + '\n- Payments Method should be numeric')
                payment_method = input(
                    DEFAULT_TEXT_COLOR + payment_options)
            elif validate_payments_method(payment_method) == 'not_payments_method':
                print(text.Red + '\n- Payments Method should be 1, 2 or 3')
                payment_method = input(
                    DEFAULT_TEXT_COLOR + payment_options)

        payment_credit = ['CREDIT']
        payment_list = ['CASH', 'CREDIT']

        switcher = {
            '1': payment_cash,
            '2': payment_credit,
            '3': payment_list
        }

        value = switcher.get(payment_method, False)
        return value


# Print Account ID menu
#   validate_string_account -- For microservices, a character number pattern was determined
#   for account creation, however not all zones use this pattern (e.g. AR, CH, CO).
#   Therefore, for simulation, this parameter was created to allow using accounts that do not
#   follow this pattern of more than 10 characters
def print_account_id_menu(zone):
    if zone in ["US", "CA"]:
        message = "Vendor Account Id: "
    else:
        message = "Account ID: "

    abi_id = str(input(DEFAULT_TEXT_COLOR + message))
    attempt = 0

    while validate_account(abi_id, zone) != True and attempt <= 2 and zone != "US":
        if validate_account(abi_id, zone) == 'error_0':
            print(text.Red + '\n- Account ID should not be empty')
            if attempt < 2:
                abi_id = str(input(DEFAULT_TEXT_COLOR + message))
        if validate_account(abi_id, zone) == 'error_10':
            print(text.Red + '\n- Account ID must contain at least 10 characters')
            if attempt < 2:
                abi_id = str(input(DEFAULT_TEXT_COLOR + message))
        elif validate_account(abi_id, zone) == 'not_number':
            print(text.Red + '\n- The account ID must be Numeric')
            if attempt < 2:
                abi_id = str(input(DEFAULT_TEXT_COLOR + message))
        elif validate_account(abi_id, zone) == 'error_cnpj_cpf':
            print(text.Red + '\n- Account ID must contain at least 11 or 14 characters')
            if attempt < 2:
                abi_id = str(input(DEFAULT_TEXT_COLOR + message))
        attempt = attempt + 1
    if attempt == 3:
        print(YELLOW + '\n- You have reached maximum attempts')
        return False
    else:
        return abi_id


def print_get_account_operations_menu():
    print(DEFAULT_TEXT_COLOR + '\nAccount operations')
    print(DEFAULT_TEXT_COLOR + str(1), YELLOW + 'All information from one account')
    structure = input(DEFAULT_TEXT_COLOR + '\nPlease select: ')
    while validate_accounts(structure) is False:
        print(INVALID_OPTION)
        print(DEFAULT_TEXT_COLOR + '\nAccount operations')
        print(DEFAULT_TEXT_COLOR + str(1), YELLOW + 'All information from one account')
        structure = input(DEFAULT_TEXT_COLOR + '\nPlease select: ')

    return structure


def print_eligible_rewards_menu():
    option = input(DEFAULT_TEXT_COLOR + 'Do you want to make this account eligible for rewards program? y/N: ')
    while validate_yes_no_option(option.upper()) is False:
        print(text.Red + '\n- Invalid option\n')
        option = input(DEFAULT_TEXT_COLOR + 'Do you want to make this account eligible for rewards program? y/N: ')

    if option.upper() == 'Y':
        return True
    else:
        return False


def print_input_owner_infos():
    user_choice = click.prompt(
        f"{text.LightYellow}"
        f"Would like to insert value for owner account? ",
        type=click.Choice(["y", "n"], case_sensitive=False),
    )
    if user_choice.upper() == "Y":
        owner_infos = {
            "email": print_account_email_owner_menu(),
            "first_name": print_owner_fisrt_name_menu(),
            "last_name": print_owner_last_name_menu(),
        }
    else:
        owner_infos = {
            "email": "test@mailinator.com",
            "first_name": "TEST OWNER FIRST NAME",
            "last_name": "TEST OWNER LAST NAME",
        }
    return owner_infos
