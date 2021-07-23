from itertools import repeat
from multiprocessing import Pool

from data_mass.classes.text import text
from data_mass.product.service import get_sku_name
from data_mass.validations import validate_sku, validate_yes_no_option


def print_inventory_option_menu():
    option = input(f"{text.Yellow}\nDo you want to choose which product will have the stock updated? y/N: ")
    while validate_yes_no_option(option.upper()) is False:
        print(f"{text.Red}\n- Invalid option")
        option = input(f"{text.Yellow}\nDo you want to choose which product will have the stock updated? y/N: ")

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
            print(f"{text.default_text_color}\nSKU: {text.Blue}{products[aux]} || {str(sku_name[aux]).upper()}")
            aux = aux + 1

    sku_id = input(f"{text.default_text_color}\nInput the SKU you want to add inventory: ")
    while validate_sku(sku_id, products) is False:
        print(f"{text.Red}\n- Invalid option")
        sku_id = input(f"{text.default_text_color}\nInput the SKU you want to add inventory: ")

    sku_quantity = input(f"{text.default_text_color}\nInventory quantity: ")
    while not sku_quantity.isdigit():
        print(f"{text.Red}\n- Invalid option")
        sku_quantity = input(f"{text.default_text_color}\nInventory quantity: ")

    return {
        'sku': sku_id,
        'quantity': sku_quantity
    }
