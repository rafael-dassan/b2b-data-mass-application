import json
import os
import sys

from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.tools.utils import (
    finish_application,
    is_blank,
)
from data_mass.tools.validations import (
    validate_combo_structure,
    validate_environment,
    validate_environment_menu_in_user_create_iam,
    validate_environment_user_creation,
    validate_month,
    validate_option_request_selection,
    validate_option_request_selection_for_structure_2,
    validate_structure,
    validate_supplier_menu_structure,
    validate_supplier_search_menu_structure,
    validate_years_credit_statement,
    validate_zone_for_interactive_combos_ms,
    validate_zone_for_ms,
)


# Print init menu
def print_available_options(selection_structure):
    if selection_structure == '1':
        print(text.default_text_color + str(0), text.Yellow + 'Close application')
        print(text.default_text_color + str(1), text.Yellow + 'Account')
        print(text.default_text_color + str(2), text.Yellow + 'Product')
        print(text.default_text_color + str(3), text.Yellow + 'Orders')
        print(text.default_text_color + str(4), text.Yellow + 'Deals')
        print(text.default_text_color + str(5), text.Yellow + 'Input combos')
        print(text.default_text_color + str(6), text.Yellow + 'Invoice')
        print(text.default_text_color + str(7), text.Yellow + 'Create rewards')
        print(text.default_text_color + str(8), text.Yellow + 'Create credit statement')
        selection = input(text.default_text_color + '\nPlease select: ')
        while not validate_option_request_selection(selection):
            print(text.Red + '\n- Invalid option\n')
            print(text.default_text_color + str(0), text.Yellow + 'Close application')
            print(text.default_text_color + str(1), text.Yellow + 'Account')
            print(text.default_text_color + str(2), text.Yellow + 'Product')
            print(text.default_text_color + str(3), text.Yellow + 'Orders')
            print(text.default_text_color + str(4), text.Yellow + 'Deals')
            print(text.default_text_color + str(5), text.Yellow + 'Input combos')
            print(text.default_text_color + str(6), text.Yellow + 'Invoice')
            print(text.default_text_color + str(7), text.Yellow + 'Create rewards')
            print(text.default_text_color + str(8), text.Yellow + 'Create credit statement')
            selection = input(text.default_text_color + '\nPlease select: ')
    elif selection_structure == '2':
        print(text.default_text_color + str(0), text.Yellow + 'Close application')
        print(text.default_text_color + str(1), text.Yellow + 'Order simulation via Microservice')
        print(text.default_text_color + str(2), text.Yellow + 'POC information')
        print(text.default_text_color + str(3), text.Yellow + 'Product information')
        print(text.default_text_color + str(4), text.Yellow + 'Deals information by account')
        print(text.default_text_color + str(5), text.Yellow + 'Order information by account')
        print(text.default_text_color + str(6), text.Yellow + 'Recommender information by account')
        print(text.default_text_color + str(7), text.Yellow + 'Retrieve available invoices')
        print(text.default_text_color + str(8), text.Yellow + 'SKUs for Reward Shopping')
        selection = input(text.default_text_color + '\nPlease select: ')
        while not validate_option_request_selection(selection):
            print(text.Red + '\n- Invalid option\n')
            print(text.default_text_color + str(0), text.Yellow + 'Close application')
            print(text.default_text_color + str(1), text.Yellow + 'Order simulation via Microservice')
            print(text.default_text_color + str(2), text.Yellow + 'POC information')
            print(text.default_text_color + str(3), text.Yellow + 'Product information')
            print(text.default_text_color + str(4), text.Yellow + 'Deals information')
            print(text.default_text_color + str(5), text.Yellow + 'Order information by account')
            print(text.default_text_color + str(6), text.Yellow + 'Recommender information by account')
            print(text.default_text_color + str(7), text.Yellow + 'Retrieve available invoices')
            print(text.default_text_color + str(8), text.Yellow + 'SKUs for Reward Shopping')
            selection = input(text.default_text_color + '\nPlease select: ')
    elif selection_structure == '3':
        print(text.default_text_color + str(0), text.Yellow + 'Close application')
        print(text.default_text_color + str(1), text.Yellow + 'List categories')
        print(text.default_text_color + str(2), text.Yellow + 'Associate product to category')
        print(text.default_text_color + str(3), text.Yellow + 'Create category')
        selection = input(text.default_text_color + '\nPlease select: ')
        while not validate_option_request_selection(selection):
            print(text.Red + '\n- Invalid option\n')
            print(text.default_text_color + str(0), text.Yellow + 'Close application')
            print(text.default_text_color + str(1), text.Yellow + 'List categories')
            print(text.default_text_color + str(2), text.Yellow + 'Associate product to category')
            print(text.default_text_color + str(3), text.Yellow + 'Create category')
            selection = input(text.default_text_color + '\nPlease select: ')
    elif selection_structure == '4':
        print(text.default_text_color + str(0), text.Yellow + 'Close application')
        print(text.default_text_color + str(1), text.Yellow + 'Create User')
        print(text.default_text_color + str(2), text.Yellow + 'Delete User')
        selection = input(text.default_text_color + '\nPlease select: ')
        while not validate_option_request_selection_for_structure_2(selection):
            print(text.Red + '\n- Invalid option\n')
            print(text.default_text_color + str(0), text.Yellow + 'Close application')
            print(text.default_text_color + str(1), text.Yellow + 'Create User')
            print(text.default_text_color + str(2), text.Yellow + 'Delete User')
            selection = input(text.default_text_color + '\nPlease select: ')
    elif selection_structure == '5':
        print(text.default_text_color + str(0), text.Yellow + 'Close application')
        print(text.default_text_color + str(1), text.Yellow + 'Create Attribute')
        print(text.default_text_color + str(2), text.Yellow + 'Create Category')
        print(text.default_text_color + str(3), text.Yellow + 'Create association between attribute and category')
        print(text.default_text_color + str(4), text.Yellow + 'Delete Attribute')
        print(text.default_text_color + str(5), text.Yellow + 'Edit Attribute Type')
        print(text.default_text_color + str(6), text.Yellow + 'Create Product')
        print(text.default_text_color + str(7), text.Yellow + 'Create Legacy Data')
        selection = input(text.default_text_color + '\nPlease select: ')
        while not validate_supplier_menu_structure(selection):
            print(text.Red + '\n- Invalid option\n')
            print(text.default_text_color + str(0), text.Yellow + 'Close application')
            print(text.default_text_color + str(1), text.Yellow + 'Create Attribute')
            print(text.default_text_color + str(2), text.Yellow + 'Create Category')
            print(text.default_text_color + str(3), text.Yellow + 'Create association between attribute and category')
            print(text.default_text_color + str(4), text.Yellow + 'Delete Attribute')
            print(text.default_text_color + str(5), text.Yellow + 'Edit Attribute Type')
            print(text.default_text_color + str(6), text.Yellow + 'Create Product')
            print(text.default_text_color + str(7), text.Yellow + 'Create Legacy Data')
            selection = input(text.default_text_color + '\nPlease select: ')
    elif selection_structure == '6':
        print(text.default_text_color + str(0), text.Yellow + 'Close application')
        print(text.default_text_color + str(1), text.Yellow + 'Search a specific attribute')
        print(text.default_text_color + str(2), text.Yellow + 'Search all attributes')
        print(text.default_text_color + str(3), text.Yellow + 'Search a specific category')
        print(text.default_text_color + str(4), text.Yellow + 'Search all category')
        selection = input(text.default_text_color + '\nPlease select: ')
        while not validate_supplier_search_menu_structure(selection):
            print(text.Red + '\n- Invalid option\n')
            print(text.default_text_color + str(0), text.Yellow + 'Close application')
            print(text.default_text_color + str(1), text.Yellow + 'Search a specific attribute')
            print(text.default_text_color + str(2), text.Yellow + 'Search all attributes')
            print(text.default_text_color + str(3), text.Yellow + 'Search a specific category')
            print(text.default_text_color + str(4), text.Yellow + 'Search all category')
            selection = input(text.default_text_color + '\nPlease select: ')
    else:
        finish_application()

    return selection


# Print welcome menu
def print_welcome_script():
    print(text.BackgroundLightYellow + text.Bold + text.Black)
    print("╭──────────────────────────────────╮")
    print("│ 🝝                               │")
    print("│   ANTARCTICA AUTOMATION SCRIPT   │")
    print("│                               🝝 │")
    print("╰──────────────────────────────────╯")
    print(text.BackgroundDefault + text.ResetBold + text.default_text_color + "\n")


# Print structure menu
def print_structure_menu():
    print(text.default_text_color + str(1), text.Yellow + 'Data creation - Microservice')
    print(text.default_text_color + str(2), text.Yellow + 'Data searching - Microservice')
    print(text.default_text_color + str(3), text.Yellow + 'Data creation - Magento')
    print(text.default_text_color + str(4), text.Yellow + 'Data creation - IAM')
    print(text.default_text_color + str(5), text.Yellow + 'Data creation - Supplier/PIM')
    print(text.default_text_color + str(6), text.Yellow + 'Data searching - Supplier/PIM')
    print(text.default_text_color + str(7), text.Yellow + 'Close application')
    structure = input(text.default_text_color + '\nPlease choose an option: ')
    while validate_structure(structure) is False:
        print(text.Red + '\n- Invalid option\n')
        print(text.default_text_color + str(1), text.Yellow + 'Data creation - Microservice')
        print(text.default_text_color + str(2), text.Yellow + 'Data searching - Microservice')
        print(text.default_text_color + str(3), text.Yellow + 'Data creation - Magento')
        print(text.default_text_color + str(4), text.Yellow + 'Data creation - IAM')
        print(text.default_text_color + str(5), text.Yellow + 'Data creation - Supplier/PIM')
        print(text.default_text_color + str(6), text.Yellow + 'Data searching - Supplier/PIM')
        print(text.default_text_color + str(7), text.Yellow + 'Close application')
        structure = input(text.default_text_color + '\nPlease choose an option: ')

    return structure


# Print combos menu
def print_combos_menu():
    print(text.default_text_color + '\nWhich type of combo do you want to create?')
    print(text.default_text_color + str(1), text.Yellow + 'Input combo type discount')
    print(text.default_text_color + str(2), text.Yellow + 'Input combo type free good')
    print(text.default_text_color + str(3), text.Yellow + 'Input combo type digital trade')
    print(text.default_text_color + str(4), text.Yellow + 'Input combo with only free goods')
    print(text.default_text_color + str(5), text.Yellow + 'Reset combo consumption to zero')
    structure = input(text.default_text_color + '\nPlease select: ')
    while not validate_combo_structure(structure):
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nWhich type of combo do you want to create?')
        print(text.default_text_color + str(1), text.Yellow + 'Input combo type discount')
        print(text.default_text_color + str(2), text.Yellow + 'Input combo type free good')
        print(text.default_text_color + str(3), text.Yellow + 'Input combo type digital trade')
        print(text.default_text_color + str(4), text.Yellow + 'Input combo with only free goods')
        print(text.default_text_color + str(5), text.Yellow + 'Reset combo consumption to zero')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure


# Print zone menu for Microservice
def print_zone_menu_for_ms():
    zone = input(text.default_text_color + 'Zone (e.g., AR, BR, CO): ')
    while validate_zone_for_ms(zone.upper()) is False:
        print(text.Red + '\n- {0} is not a valid zone\n'.format(zone.upper()))
        zone = input(text.default_text_color + 'Zone (e.g., AR, BR, CO): ')

    return zone.upper()


# For interactive combos
def print_zone_for_interactive_combos_menu_for_ms():
    zone = input(text.default_text_color + 'Zone (e.g., AR, BR, CO): ')
    while not validate_zone_for_interactive_combos_ms(zone.upper()):
        print(text.Red + '\n- {0} is not a valid zone\n'.format(zone.upper()))
        zone = input(text.default_text_color + 'Zone (e.g., AR, BR, CO): ')

    return zone.upper()


# Print environment menu
def print_environment_menu():
    environment = input(text.default_text_color + 'Environment (DEV, SIT, UAT): ')
    while validate_environment(environment.upper()) is False:
        print(text.Red + '\n- {0} is not a valid environment\n'.format(environment.upper()))
        environment = input(text.default_text_color + 'Environment (DEV, SIT, UAT): ')

    return environment.upper()


# Print environment menu for User creation
def print_environment_menu_user_creation():
    environment = input(text.default_text_color + "Environment (e.g., SIT, UAT): ")
    while not validate_environment_user_creation(environment.upper()):
        print(text.Red + "\n- {0} is not a valid environment")
        environment = input(text.default_text_color + "Environment (e.g., SIT, UAT): ")

    return environment.upper()


# Print user name menu
def print_input_email():
    email = input(text.default_text_color + "User email/UserPhone: ")
    while len(email) == 0:
        print(text.Red + "\n- The user email should not be empty")
        email = input(text.default_text_color + "User email/UserPhone: ")

    return email


# Print user password menu
def print_input_password():
    password = input(text.default_text_color + "User password: ")
    while len(password) == 0:
        print(text.Red + "\n- The user password should not be empty")
        password = input(text.default_text_color + "User password: ")

    return password


# Print user phone menu
def print_input_phone():
    return input(text.default_text_color + "User phone (optional): ")


def print_input_tax_id():
    """Validate tax_id
    Requirements:
        - Not empty
    """
    tax_id = input(text.default_text_color + "Tax ID: ")
    while is_blank(tax_id):
        print(text.Red + "\n- The tax ID should not be empty")
        tax_id = input(text.default_text_color + "Tax ID: ")
    return tax_id


def print_input_username():
    """Validate username
    Requirements:
        - Not empty
    """
    username = input(text.default_text_color + "Username: ")
    while is_blank(username):
        print(text.Red + "\n- The Username should not be empty")
        username = input(text.default_text_color + "Username: ")
    return username


def print_input_number_with_default(input_text, default_value=0):
    """Validate input number with default value"""
    while (True):
        input_number = input("{default_text_color}{input_text} - [default: {default_value}]: ".format(
            default_text_color=text.default_text_color,
            input_text=input_text, default_value=default_value)).strip() or str(default_value)

        if input_number.lstrip("-").isdigit():
            return int(input_number)


def print_input_number(input_text):
    """Validate input number"""
    while (True):
        input_number = input("{default_text_color}{input_text}: ".format(
            default_text_color=text.default_text_color,
            input_text=input_text)).strip()

        if input_number.lstrip("-").isdigit():
            return int(input_number)


def print_input_text(input_text):
    """Validate input text"""
    while (True):
        input_str = input("{default_text_color}{input_text}: ".format(
            default_text_color=text.default_text_color,
            input_text=input_text)).strip()

        if not is_blank(input_str):
            return input_str

def print_environment_menu_in_user_create_iam():
    """Print Environment Menu to Create User IAM
        Requirements:
        - QA
        - SIT
        - UAT
    """
    environment = input(text.default_text_color + 'Environment (QA, SIT, UAT): ')
    while not validate_environment_menu_in_user_create_iam(environment.upper()):
        print(text.Red + '\n- Invalid option')
        environment = input(text.default_text_color + 'Environment (QA, SIT, UAT): ')
    return environment.upper()


# Menu for payment method simulation
def print_payment_method_simulation_menu(zone):
    if zone == 'BR':
        payment_choice = input(
            text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - BANK_SLIP ')
        while payment_choice != '1' and payment_choice != '2':
            print(text.Red + '\n- Invalid option\n')
            payment_choice = input(
                text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - BANK_SLIP ')

        if payment_choice == '1':
            payment_method = 'CASH'
        else:
            payment_method = 'BANK_SLIP'

    elif zone == 'DO' and zone == 'CO' or zone == 'EC' or zone == 'PE':
        payment_choice = input(text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - CREDIT ')
        while payment_choice != '1' and payment_choice != '2':
            print(text.Red + '\n- Invalid option\n')
            payment_choice = input(
                text.default_text_color + 'Select payment method for simulation: 1 - CASH, 2 - CREDIT ')

        if payment_choice == '1':
            payment_method = 'CASH'
        else:
            payment_method = 'CREDIT'
    else:
        payment_method = 'CASH'

    return payment_method


def print_combo_id_menu():
    combo_id = input(text.default_text_color + 'Combo ID: ')

    while len(combo_id) == 0:
        print(text.Red + '\n- Combo ID should not be empty')
        combo_id = input(text.default_text_color + 'Combo ID: ')
    return combo_id


def validate_zone_for_credit_statement(zone):
    if zone.upper() != 'ZA':
        return False
    else:
        return True


# Print zone menu for credit statement
def print_zone_credit_statement():
    zone = input(text.default_text_color + 'Zone (ZA): ')
    while not validate_zone_for_credit_statement(zone):
        print(text.Red + '\n- Invalid option\n')
        zone = input(text.default_text_color + 'Zone (ZA): ')

    return zone.upper()


def print_month_credit_statement():
    month = input(text.default_text_color + 'Which month do you want to create the document? (please put the number '
                                            'referent the month): ')
    if int(month) < 10:
        month = '0' + month

    while not validate_month(month):
        print(text.Red + '\n- Invalid option\n')
        month = input(text.default_text_color + 'Which month do you want to create the document? (please put the number'
                                                'referent the month): ')

    return month

def print_year_credit_statement():
    year = input(text.default_text_color + 'Which year do you want to create the document?: ')

    while validate_years_credit_statement(year) != True:
        if validate_years_credit_statement(year) == 'error_0':
            print(text.Red + '\n- Year should not be empty')
            year = input(text.default_text_color + 'Which year do you want to create the document?: ')
        if validate_years_credit_statement(year) == 'error_4':
            print(text.Red + '\n- Year must contain at least 4 characters')
            year = input(text.default_text_color + 'Which year do you want to create the document?: ')
        elif validate_years_credit_statement(year) == 'not_number':
            print(text.Red + '\n- The year must be Numeric')
            year = input(text.default_text_color + 'Which year do you want to create the document?: ')

    return year


def print_invoices(invoice_info, status):
    invoice_list = list()
    for i in invoice_info['data']:
        if i['status'] == status[0] or i['status'] == status[1]:
            invoice_values = {
                'Invoice ID': i['invoiceId'],
                'Product Quantity': i['itemsQuantity'],
                'Sub Total': i['subtotal'],
                'Tax': i['tax'],
                'Discount': i['discount'],
                'Total': i['total']
            }
            for j in range(i['itemsQuantity']):
                invoice_values.setdefault('SKU', []).append(i['items'][j-1]['sku'])
            invoice_list.append(invoice_values)
        else:
            continue
    if bool(invoice_list):
        print(text.default_text_color + '\nInvoice Information By Account  -  Status:' + status[1])
        print(tabulate(invoice_list, headers='keys', tablefmt='grid'))
    else:
        print(text.Red + '\nThere is no invoices with the status of ' + status[1] + ' for this account')
