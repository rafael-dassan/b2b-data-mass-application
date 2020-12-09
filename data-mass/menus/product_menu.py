# Local application imports
from classes.text import text
from validations import validate_product_operations_structure, validate_get_products


def print_product_operations_menu():
    print(text.default_text_color + '\nProduct operations')
    print(text.default_text_color + str(1), text.Yellow + 'Create/update product')
    print(text.default_text_color + str(2), text.Yellow + 'Associate products to an account')
    print(text.default_text_color + str(3), text.Yellow + 'Input inventory to product')
    print(text.default_text_color + str(4), text.Yellow + 'Input recommendations to an account')
    print(text.default_text_color + str(5), text.Yellow + 'Input empties discounts')
    option = input(text.default_text_color + '\nPlease select: ')
    while validate_product_operations_structure(option) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nProduct operations')
        print(text.default_text_color + str(1), text.Yellow + 'Create/update product')
        print(text.default_text_color + str(2), text.Yellow + 'Associate products to an account')
        print(text.default_text_color + str(3), text.Yellow + 'Input inventory to product')
        print(text.default_text_color + str(4), text.Yellow + 'Input recommendations to an account')
        print(text.default_text_color + str(5), text.Yellow + 'Input empties discounts')
        option = input(text.default_text_color + '\nPlease select: ')

    return option


def print_product_quantity_menu(all_products_zone):
    while True:
        try:
            qtd = int(input(text.default_text_color + 'Number of products you want to add (Maximum: '
                            + str(len(all_products_zone)) + '): '))
            while qtd <= 0:
                print(text.Red + '\n- The product quantity must be more than 0\n')
                qtd = int(input(text.default_text_color + '\nNumber of products you want to add (Maximum: '
                                + str(len(all_products_zone)) + '): '))
            break
        except ValueError:
            print(text.Red + '\n- The product quantity must be Numeric\n')

    return qtd


def print_get_products_menu():
    print(text.default_text_color + '\nWhich option to retrieve products information do you want?')
    print(text.default_text_color + str(1), text.Yellow + 'Products information by account')
    print(text.default_text_color + str(2), text.Yellow + 'Products inventory information by account')
    print(text.default_text_color + str(3), text.Yellow + 'Products information by zone')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_get_products(structure) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nWhich option to retrieve products information do you want?')
        print(text.default_text_color + str(1), text.Yellow + 'Products information by account')
        print(text.default_text_color + str(2), text.Yellow + 'Products inventory information by account')
        print(text.default_text_color + str(3), text.Yellow + 'Products information by zone')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure

