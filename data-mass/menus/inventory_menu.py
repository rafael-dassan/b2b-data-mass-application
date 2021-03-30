from itertools import repeat
from multiprocessing import Pool
from classes.text import text
from products import get_sku_name
from validations import validate_yes_no_option, validate_sku


def print_inventory_option_menu():
    option = input('\n{0}Do you want to choose which product will have the stock updated? y/N: '.format(text.Yellow))
    while validate_yes_no_option(option.upper()) is False:
        print('\n{0}- Invalid option'.format(text.Red))
        option = input('\n{0}Do you want to choose which product will have the stock updated? y/N: '.format(text.Yellow))

    return option.upper()


def print_inventory_sku_quantity_menu(zone, environment, products):
    len_products = len(products)
    if len_products > 0:
        with Pool(20) as pool:
            sku_name = pool.starmap(get_sku_name, zip(repeat(zone), repeat(environment), products))

    aux = 0
    while aux < len_products:
        if not products[aux]:
            aux = aux + 1
        else:
            print('\n{0}SKU: {1}{2} || {3}'.format(text.default_text_color, text.Blue, products[aux], sku_name[aux].upper()))
            aux = aux + 1

    sku_id = input('\n{0}Input the SKU you want to add inventory: '.format(text.default_text_color))
    while validate_sku(sku_id, products) is False:
        print('\n{0}- Invalid option'.format(text.Red))
        sku_id = input('\n{0}Input the SKU you want to add inventory: '.format(text.default_text_color))

    sku_quantity = input('\n{0}Inventory quantity: '.format(text.default_text_color))
    while not sku_quantity.isdigit():
        print('\n{0}- Invalid option'.format(text.Red))
        sku_quantity = input('\n{0}Inventory quantity: '.format(text.default_text_color))

    return {
        'sku': sku_id,
        'quantity': sku_quantity
    }
