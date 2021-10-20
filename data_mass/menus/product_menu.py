# Local application imports
from data_mass.classes.text import text
from data_mass.common import get_confirmation_option
from data_mass.validations import (
    validate_get_products,
    validate_product_operations_structure,
    validate_yes_no_option
)


def print_product_operations_menu(zone):
    if zone == "US":
        print(text.default_text_color + '\nProduct operations')
        print(text.default_text_color + str(1), text.Yellow + 'Create/update product')
        print(text.default_text_color + str(2), text.Yellow + 'Associate products to an account')
        print(text.default_text_color + str(3), text.Yellow + 'Input inventory to product')
        print(text.default_text_color + str(4), text.Yellow + 'Input recommendations to an account')
        option = input(text.default_text_color + '\nPlease select: ')
        while validate_product_operations_structure(option, zone) is False:
            print(text.Red + '\n- Invalid option')
            print(text.default_text_color + '\nProduct operations')
            print(text.default_text_color + str(1), text.Yellow + 'Create/update product')
            print(text.default_text_color + str(2), text.Yellow + 'Associate products to an account')
            print(text.default_text_color + str(3), text.Yellow + 'Input inventory to product')
            print(text.default_text_color + str(4), text.Yellow + 'Input recommendations to an account')
            option = input(text.default_text_color + '\nPlease select: ')

        return option
    print(text.default_text_color + '\nProduct operations')
    print(text.default_text_color + str(1), text.Yellow + 'Create/update product')
    print(text.default_text_color + str(2), text.Yellow + 'Associate products to an account')
    print(text.default_text_color + str(3), text.Yellow + 'Input inventory to product')
    print(text.default_text_color + str(4), text.Yellow + 'Input recommendations to an account')
    print(text.default_text_color + str(5), text.Yellow + 'Input empties discounts')
    print(text.default_text_color + str(6), text.Yellow + 'Input an SKU Limit to account')
    option = input(text.default_text_color + '\nPlease select: ')
    while validate_product_operations_structure(option, zone) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nProduct operations')
        print(text.default_text_color + str(1), text.Yellow + 'Create/update product')
        print(text.default_text_color + str(2), text.Yellow + 'Associate products to an account')
        print(text.default_text_color + str(3), text.Yellow + 'Input inventory to product')
        print(text.default_text_color + str(4), text.Yellow + 'Input recommendations to an account')
        print(text.default_text_color + str(5), text.Yellow + 'Input empties discounts')
        print(text.default_text_color + str(6), text.Yellow + 'Input an SKU Limit to account')
        option = input(text.default_text_color + '\nPlease select: ')

    return option

def print_product_quantity_menu(all_products_zone):
    while True:
        try:
            qtd = int(input('{0}Number of products you want to add (Maximum: {1}): '.format(text.default_text_color,
                                                                                            str(len(all_products_zone)))))
            while qtd <= 0:
                print('\n{0}- The product quantity must be more than 0\n'.format(text.Red))
                qtd = int(input('{0}Number of products you want to add (Maximum: {1}): '.format(text.default_text_color,
                                                                                                str(len(all_products_zone)))))
            break
        except ValueError:
            print('\n{0}- The product quantity must be Numeric\n'.format(text.Red))

    return qtd

def print_skus_specification_menu(): 
    will_specify_skus = input(text.default_text_color + '\nDo you want to specify the skus? y/N: ')
    return get_confirmation_option(will_specify_skus, print_skus_specification_menu)

def get_skus_to_associate():
    input_entry = input('Please type the skus separated by commas (example: SKU1, SKU2, SKU3): ')
    skus = input_entry.split(',')
    if(len(skus) == 0):
        print('Invalid entry, please try again')
        return get_skus_to_associate()
        
    return skus


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


def print_is_returnable_menu():
    is_returnable = input('{0}Is it returnable? y/N: '.format(text.default_text_color)).upper()
    while validate_yes_no_option(is_returnable) is False:
        print('\n{0}- Invalid option\n'.format(text.Red))
        is_returnable = input('{0}Is it returnable? y/N: '.format(text.default_text_color)).upper()

    return {
        'Y': True,
        'N': False
    }.get(is_returnable, False)


def print_is_narcotic_menu():
    is_narcotic = input('{0}Is it a narcotic product? y/N: '.format(text.default_text_color)).upper()
    while validate_yes_no_option(is_narcotic) is False:
        print('\n{0}- Invalid option\n'.format(text.Red))
        is_narcotic = input('{0}Is it a narcotic product? y/N: '.format(text.default_text_color)).upper()

    return {
        'Y': True,
        'N': False
    }.get(is_narcotic, False)


def print_is_alcoholic_menu():
    is_alcoholic = input('{0}Is it an alcoholic product? y/N: '.format(text.default_text_color)).upper()
    while validate_yes_no_option(is_alcoholic) is False:
        print('\n{0}- Invalid option\n'.format(text.Red))
        is_alcoholic = input('{0}Is it an alcoholic product? y/N: '.format(text.default_text_color)).upper()

    return {
        'Y': True,
        'N': False
    }.get(is_alcoholic, False)
