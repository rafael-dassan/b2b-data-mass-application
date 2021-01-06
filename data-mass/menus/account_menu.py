# Local application imports
from classes.text import text
from validations import validate_yes_no_option, validate_account_name, validate_payments_method, validate_account, \
    validate_accounts, validate_account_operations_structure


def print_account_operations_menu():
    print(text.default_text_color + '\nAccount operations')
    print(text.default_text_color + str(1), text.Yellow + 'Create/update account')
    print(text.default_text_color + str(2), text.Yellow + 'Create/update delivery window')
    print(text.default_text_color + str(3), text.Yellow + 'Create/update credit information')
    print(text.default_text_color + str(4), text.Yellow + 'Update account name')
    print(text.default_text_color + str(5), text.Yellow + 'Update account status')
    print(text.default_text_color + str(6), text.Yellow + 'Update minimum order type/value')
    print(text.default_text_color + str(7), text.Yellow + 'Update payment method')
    option = input(text.default_text_color + '\nPlease select: ')
    while validate_account_operations_structure(option) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nAccount operations')
        print(text.default_text_color + str(1), text.Yellow + 'Create/update account')
        print(text.default_text_color + str(2), text.Yellow + 'Create/update delivery window')
        print(text.default_text_color + str(3), text.Yellow + 'Create/update credit information')
        print(text.default_text_color + str(4), text.Yellow + 'Update account name')
        print(text.default_text_color + str(5), text.Yellow + 'Update account status')
        print(text.default_text_color + str(6), text.Yellow + 'Update minimum order type/value')
        print(text.default_text_color + str(7), text.Yellow + 'Update payment method')
        option = input(text.default_text_color + '\nPlease select: ')

    return option


def print_minimum_order_menu():
    option = input(text.default_text_color + 'Do you want to include the minimum order parameter? y/N: ')
    while validate_yes_no_option(option.upper()) is False:
        print(text.Red + '\n- Invalid option\n')
        option = input(text.default_text_color + 'Do you want to include the minimum order parameter? y/N: ')

    return option.upper()


def print_minimum_order_type_menu():
    minimum_order_type = input(
        text.default_text_color + 'Minimum order type (1. Product quantity / 2. Order volume / 3. Order total): ')
    while minimum_order_type == '' or (int(minimum_order_type) != 1 and int(minimum_order_type) != 2
                                       and int(minimum_order_type) != 3):
        print(text.Red + '\n- Invalid option\n')
        minimum_order_type = input(
            text.default_text_color + 'Minimum order type (1. Product quantity / 2. Order volume / 3. Order total): ')

    switcher = {
        '1': 'PRODUCT_QUANTITY',
        '2': 'ORDER_VOLUME',
        '3': 'ORDER_TOTAL'
    }

    minimum_order_type = switcher.get(minimum_order_type, 'false')

    return minimum_order_type


def print_minimum_order_value_menu():
    minimum_order_value = input(text.default_text_color + 'Minimum order value: ')
    while minimum_order_value == '' or int(minimum_order_value) <= 0:
        print(text.Red + '\n- SKU quantity must be greater than 0\n')
        minimum_order_value = input(text.default_text_color + 'Minimum order value: ')

    return minimum_order_value


def print_account_status_menu():
    option = input(
        text.default_text_color + 'Account status (1. Active / 2. Blocked): ')
    while option == '' and option != '1' and option != '2':
        print(text.Red + '\n- Invalid option')
        option = input(
            text.default_text_color + '\nAccount status (1. Active / 2. Blocked): ')

    switcher = {
        '1': 'ACTIVE',
        '2': 'BLOCKED'
    }

    status = switcher.get(option, 'false')

    return status


# Print account name menu
def print_account_name_menu():
    name = input(text.default_text_color + 'Account name: ')
    while validate_account_name(name) is False:
        print(text.Red + '\n- The account name should not be empty')
        name = input(text.default_text_color + 'Account name: ')

    return name


def print_account_enable_empties_loan_menu():
    option = input(
        text.default_text_color + 'Would you like to enable the loan of empties for this account? (1. Yes / 2. No): ')
    while option == '' and option != '1' and option != '2':
        print(text.Red + '\n- Invalid option')
        option = input(
            text.default_text_color + 'Would you like to enable the loan of empties for this account? (1. Yes / '
                                      '2. No): ')

    return {
        '1': True,
        '2': False
    }.get(option, 'false')


# Print alternative delivery date menu application
def print_alternative_delivery_date_menu():
    option = input(text.default_text_color + 'Do you want to register an alternative delivery date? y/N: ')
    while validate_yes_no_option(option.upper()) is False:
        print(text.Red + '\n- Invalid option')
        option = input(text.default_text_color + '\nDo you want to register an alternative delivery date? y/N: ')

    return option


# Print delivery cost (interest) menu
def print_include_delivery_cost_menu():
    option = input(text.default_text_color + '\nDo you want to add delivery fee (interest)? y/N: ')
    while validate_yes_no_option(option.upper()) is False:
        print(text.Red + '\n- Invalid option')
        option = input(text.default_text_color + '\nDo you want to add delivery fee (interest)? y/N: ')

    return option


# Print payment method menu
def print_payment_method_menu(zone):
    payment_cash = ['CASH']

    if zone == 'BR':
        payment_method = input(text.default_text_color + 'Choose the payment method (1. CASH / 2. BANK SLIP / 3. CHECK'
                                                         ' / 4. CASH, BANK SLIP, CHECK): ')
        while validate_payments_method(payment_method) != 'true':
            if validate_payments_method(payment_method) == 'error_0':
                print(text.Red + '\n- Payments Method should not be empty')
                payment_method = input(text.default_text_color + 'Choose the payment method (1. CASH / 2. BANK SLIP /'
                                                                 ' 3. CHECK / 4. CASH, BANK SLIP, CHECK): ')
            elif validate_payments_method(payment_method) == 'not_number':
                print(text.Red + '\n- Payments Method should be numeric')
                payment_method = input(text.default_text_color + 'Choose the payment method (1. CASH / 2. BANK SLIP /'
                                                                 ' 3. CHECK / 4. CASH, BANK SLIP, CHECK): ')
            elif validate_payments_method(payment_method) == 'not_payments_method':
                print(text.Red + '\n- Payments Method should be 1, 2 or 3')
                payment_method = input(text.default_text_color + 'Choose the payment method (1. CASH / 2. BANK SLIP /'
                                                                 ' 3. CHECK / 4. CASH, BANK SLIP, CHECK): ')

        payment_credit = ['BANK_SLIP']
        payment_check = ['CHECK']
        payment_list = ['CASH', 'BANK_SLIP', 'CHECK']

        switcher = {
            '1': payment_cash,
            '2': payment_credit,
            '3': payment_check,
            '4': payment_list,
        }

        value = switcher.get(payment_method, 'false')
        return value

    elif zone == 'DO' or zone == 'CO' or zone == 'EC' or zone == 'PE':
        payment_method = input(
            text.default_text_color + 'Choose the payment method (1. CASH / 2. CREDIT / 3. CASH, CREDIT): ')
        while validate_payments_method(payment_method) != 'true':
            if validate_payments_method(payment_method) == 'error_0':
                print(text.Red + '\n- Payments Method should not be empty')
                payment_method = input(
                    text.default_text_color + 'Choose the payment method (1. CASH / 2. CREDIT / 3. CASH, CREDIT): ')
            elif validate_payments_method(payment_method) == 'not_number':
                print(text.Red + '\n- Payments Method should be numeric')
                payment_method = input(
                    text.default_text_color + 'Choose the payment method (1. CASH / 2. CREDIT / 3. CASH, CREDIT): ')
            elif validate_payments_method(payment_method) == 'not_payments_method':
                print(text.Red + '\n- Payments Method should be 1, 2 or 3')
                payment_method = input(
                    text.default_text_color + 'Choose the payment method (1. CASH / 2. CREDIT / 3. CASH, CREDIT): ')

        payment_credit = ['CREDIT']
        payment_list = ['CASH', 'CREDIT']

        switcher = {
            '1': payment_cash,
            '2': payment_credit,
            '3': payment_list
        }

        value = switcher.get(payment_method, 'false')
        return value

    else:
        return payment_cash


# Print Account ID menu
#   validate_string_account -- For microservices, a character number pattern was determined
#   for account creation, however not all zones use this pattern (e.g. AR, CH, CO).
#   Therefore, for simulation, this parameter was created to allow using accounts that do not
#   follow this pattern of more than 10 characters
def print_account_id_menu(zone):
    abi_id = str(input(text.default_text_color + 'Account ID: '))
    attempt = 0
    while validate_account(abi_id, zone) != 'true' and attempt <= 2:
        if validate_account(abi_id, zone) == 'error_0':
            print(text.Red + '\n- Account ID should not be empty')
            if attempt < 2:
                abi_id = str(input(text.default_text_color + 'Account ID: '))
        if validate_account(abi_id, zone) == 'error_10':
            print(text.Red + '\n- Account ID must contain at least 10 characters')
            if attempt < 2:
                abi_id = str(input(text.default_text_color + 'Account ID: '))
        elif validate_account(abi_id, zone) == 'not_number':
            print(text.Red + '\n- The account ID must be Numeric')
            if attempt < 2:
                abi_id = str(input(text.default_text_color + 'Account ID: '))
        elif validate_account(abi_id, zone) == 'error_cnpj_cpf':
            print(text.Red + '\n- Account ID must contain at least 11 or 14 characters')
            if attempt < 2:
                abi_id = str(input(text.default_text_color + 'Account ID: '))
        attempt = attempt + 1
    if attempt == 3:
        print(text.Yellow + '\n- You have reached maximum attempts')
        return 'false'
    else:
        return abi_id


def print_get_account_operations_menu():
    print(text.default_text_color + '\nAccount operations')
    print(text.default_text_color + str(1), text.Yellow + 'All information from one account')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_accounts(structure) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nAccount operations')
        print(text.default_text_color + str(1), text.Yellow + 'All information from one account')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure
