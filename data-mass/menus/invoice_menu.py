# Local application imports
from classes.text import text
from validations import validate_invoice_options, validate_invoice_status, validate_invoice_payment_method


def print_invoice_operations_menu():
    print(text.default_text_color + '\nInvoice operations')
    print(text.default_text_color + str(1), text.Yellow + 'Create new invoice')
    print(text.default_text_color + str(2), text.Yellow + 'Update invoice status')
    print(text.default_text_color + str(3), text.Yellow + 'Update invoice payment method')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_invoice_options(structure) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nInvoice operations')
        print(text.default_text_color + str(1), text.Yellow + 'Create new invoice')
        print(text.default_text_color + str(2), text.Yellow + 'Update invoice status')
        print(text.default_text_color + str(3), text.Yellow + 'Update invoice payment method')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure


def print_invoice_status_menu():
    status = input(text.default_text_color + 'Invoice status (1. Open / 2. Closed): ')
    while validate_invoice_status(status) is False:
        print(text.Red + '\n- Invalid option')
        status = input(text.default_text_color + 'Invoice status (1. Open / 2. Closed): ')

    if status == '1':
        return 'OPEN'
    else:
        return 'CLOSED'


def print_invoice_id_menu():
    invoice_id = input(text.default_text_color + 'Invoice ID: ')

    while True:
        if len(invoice_id) == 0:
            print(text.Red + '\n- Invoice ID should not be empty')
        else:
            break

        invoice_id = input(text.default_text_color + 'Invoice ID: ')

    return invoice_id


def print_invoice_payment_method_menu():
    payment_method = input(text.default_text_color + 'Payment method (1. Cash / 2. Credit): ')
    while validate_invoice_payment_method(payment_method) is False:
        print(text.Red + '\n- Invalid option')
        payment_method = input(text.default_text_color + 'Payment method (1. Cash / 2. Credit): ')

    if payment_method == '1':
        return 'CASH'
    else:
        return 'CREDIT'
