# Local application imports
from classes.text import text
from validations import validate_deals_options, validate_option_sku


def print_deals_operations_menu():
    print(text.default_text_color + '\nDeals operations')
    print(text.default_text_color + str(1), text.Yellow + 'Create deal type discount')
    print(text.default_text_color + str(2), text.Yellow + 'Create deal type stepped discount')
    print(text.default_text_color + str(3), text.Yellow + 'Create deal type stepped discount with limit')
    print(text.default_text_color + str(4), text.Yellow + 'Create deal type free good')
    print(text.default_text_color + str(5), text.Yellow + 'Create deal type stepped free good')
    print(text.default_text_color + str(6), text.Yellow + 'Create deal type Interactive Combos v1')
    print(text.default_text_color + str(7), text.Yellow + 'Create deal type Interactive Combos v2')
    option = input(text.default_text_color + '\nPlease select: ')
    while validate_deals_options(option) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nDeals operations')
        print(text.default_text_color + str(1), text.Yellow + 'Create deal type discount')
        print(text.default_text_color + str(2), text.Yellow + 'Create deal type stepped discount')
        print(text.default_text_color + str(3), text.Yellow + 'Create deal type stepped discount with limit')
        print(text.default_text_color + str(4), text.Yellow + 'Create deal type free good')
        print(text.default_text_color + str(5), text.Yellow + 'Create deal type stepped free good')
        print(text.default_text_color + str(6), text.Yellow + 'Create deal type Interactive Combos v1')
        print(text.default_text_color + str(7), text.Yellow + 'Create deal type Interactive Combos v2')
        option = input(text.default_text_color + '\nPlease select: ')

    return option


def print_discount_percentage_menu():
    while True:
        try:
            discount_value = float(input(text.default_text_color + 'Discount percentage (%): '))
            break
        except ValueError:
            print(text.Red + '\n- Invalid value')

    return discount_value


def print_index_range_menu(indexes=4):
    index_list = list()
    for x in range(indexes):
        range_index = input(text.default_text_color + 'Range index #' + str(x) + ': ')
        while range_index == '' or int(range_index) <= 0:
            print(text.Red + '\n- Range index must be greater than 0')
            range_index = input(text.default_text_color + '\nRange index #' + str(x) + ': ')

        index_list.append(range_index)

    return index_list


def print_discount_range_menu(indexes=2):
    index_list = list()
    for x in range(indexes):
        discount_value = input(text.default_text_color + 'Discount value for index #' + str(x) + ': ')
        while discount_value == '' or float(discount_value) <= 0:
            print(text.Red + '\n- Discount value must be greater than 0')
            discount_value = input(text.default_text_color + '\nDiscount value for index #' + str(x) + ': ')

        index_list.append(discount_value)

    return index_list


def print_minimum_quantity_menu():
    minimum_quantity = input(text.default_text_color + 'Desired quantity needed to buy to get a discount/free good: ')
    while minimum_quantity == '' or int(minimum_quantity) <= 0:
        print(text.Red + '\n- Minimum quantity must be greater than 0')
        minimum_quantity = input(text.default_text_color + 'Desired quantity needed to buy to get a discount/free '
                                                           'good: ')

    return minimum_quantity


def print_max_quantity_menu(default_index_range):
    index_init = int(default_index_range[0])
    index_end = int(default_index_range[1])

    max_quantity = input(text.default_text_color + 'Maximum quantity: ')
    while True:
        if len(max_quantity) == 0 or index_init > int(max_quantity) or int(max_quantity) >= index_end:
            print(text.Red + '\n- Minimum quantity must be between {index_init} and {index_end}'
                  .format(index_init=index_init, index_end=index_end - 1))
            max_quantity = input(text.default_text_color + 'Maximum quantity: ')
        else:
            break

    return max_quantity


def print_free_good_quantity_menu():
    quantity = input(text.default_text_color + 'Desired quantity of free goods to offer: ')
    while quantity == '' or int(quantity) <= 0:
        print(text.Red + '\n- SKU quantity must be greater than 0')
        quantity = input(text.default_text_color + 'Desired quantity of free goods to offer: ')

    return quantity


# Maximum and Mininum index for Interactive Combos v1
def print_interactive_combos_quantity_range_menu():
    index_list_min = list()
    index_list_max = list()
    index_dict = dict()
    index_dict['minimum'] = {}
    index_dict['maximum'] = {}

    for x in range(3):
        min_quantity = input(text.default_text_color + 'Type the ' + str(x + 1) + '° minimum value: ')
        while min_quantity == '' or int(min_quantity) < 0:
            print(text.Red + '\n- SKU minimum quantity must be greater than 0')
            min_quantity = input(text.default_text_color + '\nType the ' + str(x) + '° minimum value: ')

        index_list_min.append(min_quantity)

    index_dict['minimum'] = index_list_min

    for x in range(3):
        max_quantity = input(text.default_text_color + 'Type the ' + str(x + 1) + '° maximum value: ')
        while max_quantity == '' or int(max_quantity) <= 0:
            print(text.Red + '\n- SKU maximum quantity must be greater than 0')
            max_quantity = input(text.default_text_color + '\nType the ' + str(x) + '° maximum value:1'
                                                                                    ' ')

        index_list_max.append(max_quantity)

    index_dict['maximum'] = index_list_max
    return index_dict


# Maximum and Mininum index for Interactive Combos v2
def print_interactive_combos_quantity_range_menu_v2():
    index_list_min = list()
    index_list_max = list()
    index_dict = dict()
    index_dict['minimum'] = {}
    index_dict['maximum'] = {}

    for x in range(2):
        min_quantity = input(text.default_text_color + 'Type the ' + str(x + 1) + '° minimum value: ')
        while min_quantity == '' or int(min_quantity) < 0:
            print(text.Red + '\n- SKU minimum quantity must be greater than 0') 
            min_quantity = input(text.default_text_color + '\nType the ' + str(x) + '° minimum value: ')

        index_list_min.append(min_quantity)

    index_dict['minimum'] = index_list_min

    for x in range(3):
        max_quantity = input(text.default_text_color + 'Type the ' + str(x + 1) + '° maximum value: ')
        while max_quantity == '' or int(max_quantity) <= 0:
            print(text.Red + '\n- SKU maximum quantity must be greater than 0')
            max_quantity = input(text.default_text_color + '\nType the ' + str(x) + '° maximum value:'
                                                                                    ' ')

        index_list_max.append(max_quantity)

    index_dict['maximum'] = index_list_max
    return index_dict


def print_partial_free_good_menu(zone):
    if zone != 'BR':
        partial_free_good = 'N'
    else:
        partial_free_good = input(text.default_text_color + 'Would you like to register this free good as an optional'
                                                            ' SKU rescue?: (y/N): ')
        while partial_free_good.upper() != 'Y' and partial_free_good.upper() != 'N':
            print(text.Red + '\n- Invalid option')
            partial_free_good = input(text.default_text_color + 'Would you like to register this free good as an '
                                                                'optional SKU rescue? (y/N): ')

    return partial_free_good.upper()


def print_free_good_redemption_menu(partial_free_good):
    need_to_buy_product = 'Y'
    if partial_free_good == 'Y':
        need_to_buy_product = input(text.default_text_color + 'Would you like to link the redemption of an optional'
                                                              ' free good to the purchase of a sku? (y/N): ')
        while need_to_buy_product.upper() != 'Y' and need_to_buy_product.upper() != 'N':
            print(text.Red + '\n- Invalid option')
            need_to_buy_product = input(text.default_text_color + 'Would you like to link the redemption of an '
                                                                  'optional free good to the purchase of a sku? '
                                                                  '(y/N): ')

    return need_to_buy_product.upper()


def print_free_good_quantity_range_menu():
    index_list = list()
    for x in range(2):
        quantity_value = input(text.default_text_color + 'SKU quantity for index #' + str(x) + ': ')
        while quantity_value == '' or int(quantity_value) <= 0:
            print(text.Red + '\n- SKU quantity must be greater than 0')
            quantity_value = input(text.default_text_color + '\nSKU quantity for index #' + str(x) + ': ')

        index_list.append(quantity_value)

    return index_list


def print_option_sku_menu():
    option = input(text.default_text_color + 'Do you want to input this deal to a specific SKU? (1. Yes / 2. No): ')
    while validate_option_sku(option) is False:
        print(text.Red + '\n- Invalid option')
        option = input(text.default_text_color + '\nDo you want to input this deal to a specific SKU? (1. Yes / '
                                                 '2. No): ')

    return option
