# Local application imports
from classes.text import text
from validations import validate_orders, validate_yes_no_option, validate_order_sub_menu, validate_order_status


def print_order_operations_menu():
    print(text.default_text_color + '\nOrder operations')
    print(text.default_text_color + str(1), text.Yellow + 'Create an order')
    print(text.default_text_color + str(2), text.Yellow + 'Create changed order')
    print(text.default_text_color + str(3), text.Yellow + 'Update delivery date of an order')
    operation = input(text.default_text_color + '\nPlease select: ')
    while validate_orders(operation) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nOrder operations')
        print(text.default_text_color + str(1), text.Yellow + 'Create an order')
        print(text.default_text_color + str(2), text.Yellow + 'Create changed order')
        print(text.default_text_color + str(3), text.Yellow + 'Update delivery date of an order')
        operation = input(text.default_text_color + '\nPlease select: ')

    return operation


def print_order_status_menu():
    print(text.default_text_color + '\nOrder statuses')
    print(text.default_text_color + str(1), text.Yellow + 'Placed')
    print(text.default_text_color + str(2), text.Yellow + 'Pending')
    print(text.default_text_color + str(3), text.Yellow + 'Confirmed')
    print(text.default_text_color + str(4), text.Yellow + 'Cancelled')
    print(text.default_text_color + str(5), text.Yellow + 'Delivered')
    print(text.default_text_color + str(6), text.Yellow + 'Invoiced')
    print(text.default_text_color + str(7), text.Yellow + 'Denied')
    print(text.default_text_color + str(8), text.Yellow + 'Modified')
    print(text.default_text_color + str(9), text.Yellow + 'In Transit')
    print(text.default_text_color + str(10), text.Yellow + 'Partial Delivery')
    print(text.default_text_color + str(11), text.Yellow + 'Pending Cancellation')
    status = input(text.default_text_color + '\nPlease select: ')
    while validate_order_status(status) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nOrder statuses')
        print(text.default_text_color + str(1), text.Yellow + 'Placed')
        print(text.default_text_color + str(2), text.Yellow + 'Pending')
        print(text.default_text_color + str(3), text.Yellow + 'Confirmed')
        print(text.default_text_color + str(4), text.Yellow + 'Cancelled')
        print(text.default_text_color + str(5), text.Yellow + 'Delivered')
        print(text.default_text_color + str(6), text.Yellow + 'Invoiced')
        print(text.default_text_color + str(7), text.Yellow + 'Denied')
        print(text.default_text_color + str(8), text.Yellow + 'Modified')
        print(text.default_text_color + str(9), text.Yellow + 'In Transit')
        print(text.default_text_color + str(10), text.Yellow + 'Partial Delivery')
        print(text.default_text_color + str(11), text.Yellow + 'Pending Cancellation')
        status = input(text.default_text_color + '\nPlease select: ')

    return {
        '1': 'PLACED',
        '2': 'PENDING',
        '3': 'CONFIRMED',
        '4': 'CANCELLED',
        '5': 'DELIVERED',
        '6': 'INVOICED',
        '7': 'DENIED',
        '8': 'MODIFIED',
        '9': 'IN_TRANSIT',
        '10': 'PARTIAL_DELIVERY',
        '11': 'PENDING_CANCELLATION',
    }.get(status, 'false')


def print_allow_cancellable_order_menu():
    option = input(text.default_text_color + 'Do you want to make this order cancellable? y/N: ')
    while validate_yes_no_option(option.upper()) is False:
        print(text.Red + '\n- Invalid option')
        option = input(text.default_text_color + '\nDo you want to make this order cancellable? y/N: ')

    return option.upper()


def print_get_order_menu():
    print(text.default_text_color + '\nWhich option to retrieve orders do you want?')
    print(text.default_text_color + str(1), text.Yellow + 'Specific order information by account')
    print(text.default_text_color + str(2), text.Yellow + 'All order information by account')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_order_sub_menu(structure) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nWhich option to retrieve orders do you want?')
        print(text.default_text_color + str(1), text.Yellow + 'Specific order information by account')
        print(text.default_text_color + str(2), text.Yellow + 'All order information by account')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure


def print_order_id_menu():
    order_id = input(text.default_text_color + 'Order ID: ')

    while True:
        if len(order_id) == 0:
            print(text.Red + '\n- Order ID should not be empty')
        else:
            break

        order_id = input(text.default_text_color + 'Order ID: ')

    return order_id
