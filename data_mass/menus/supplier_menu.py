from data_mass.classes.text import text
from data_mass.validations import validate_supplier_category_menu_structure, \
    validate_attribute_menu_structure, validate_option_att, \
    validate_option_type, validate_environment_supplier


def print_create_supplier_category_menu():
    print(text.default_text_color + str(1), text.Yellow + 'Create category root')
    print(text.default_text_color + str(2), text.Yellow + 'Create subCategory')
    print(text.default_text_color + str(3), text.Yellow + 'Create legacy category')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_supplier_category_menu_structure(structure) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + str(1), text.Yellow + 'Create category root')
        print(text.default_text_color + str(2), text.Yellow + 'Create subCategory')
        print(text.default_text_color + str(3), text.Yellow + 'Create legacy category')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure


def print_create_attribute_menu():
    print(text.default_text_color + str(1), text.Yellow + 'Create attribute primitive type')
    print(text.default_text_color + str(2), text.Yellow + 'Create attribute ENUM type')
    print(text.default_text_color + str(3), text.Yellow + 'Create attribute GROUP type')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_attribute_menu_structure(structure, is_enum=True) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + str(1), text.Yellow + 'Create attribute primitive type')
        print(text.default_text_color + str(2), text.Yellow + 'Create attribute ENUM type')
        print(text.default_text_color + str(3), text.Yellow + 'Create attribute GROUP type')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure


def print_attribute_primitive(is_enum):
    print(text.default_text_color + str(1), text.Yellow + 'Create NUMERIC attribute')
    print(text.default_text_color + str(2), text.Yellow + 'Create TEXT attribute')
    print(text.default_text_color + str(3), text.Yellow + 'Create DATE attribute')
    if not is_enum:
        print(text.default_text_color + str(4), text.Yellow + 'Create BOOLEAN attribute')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_attribute_menu_structure(structure, is_enum) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + str(1), text.Yellow + 'Create NUMERIC attribute')
        print(text.default_text_color + str(2), text.Yellow + 'Create TEXT attribute')
        print(text.default_text_color + str(3), text.Yellow + 'Create DATE attribute')
        if not is_enum:
            print(text.default_text_color + str(4), text.Yellow + 'Create BOOLEAN attribute')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure


def print_attribute_enum():
    print(text.default_text_color + str(1), text.Yellow + 'Create ENUM NUMERIC')
    print(text.default_text_color + str(2), text.Yellow + 'Create ENUM TEXT')
    print(text.default_text_color + str(3), text.Yellow + 'Create ENUM DATE')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_attribute_menu_structure(structure, is_enum=True) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + str(1), text.Yellow + 'Create ENUM NUMERIC')
        print(text.default_text_color + str(2), text.Yellow + 'Create ENUM TEXT')
        print(text.default_text_color + str(3), text.Yellow + 'Create ENUM DATE')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure


def print_new_attribute():
    option = input(text.default_text_color + 'Do you want to input another attribute in this group? (1. Yes / 2. No): ')
    while validate_option_att(option) is False:
        print(text.Red + '\n- Invalid option')
        option = input(text.default_text_color + '\nDo you want to input another attribute in this group? '
                                                '(1. Yes / 2. No): ')

    return option


def print_min_cardinality():
    option = int(input(text.default_text_color + 'Min cardinality: '))
    while option < 0:
        print(text.Red + '\n- Invalid option')
        option = int(input(text.default_text_color + 'Min cardinality: '))
    return str(option)


def print_max_cardinality():
    option = int(input(text.default_text_color + 'Max cardinality: '))
    while option < 1:
        print(text.Red + '\n- Invalid option')
        option = int(input(text.default_text_color + 'Max cardinality: '))
    return str(option)


def print_new_page():
    option = input(text.default_text_color + 'Do you want to go to another page? (1. Yes / 2. No): ')
    while validate_option_att(option) is False:
        print(text.Red + '\n- Invalid option')
        option = input(text.default_text_color + '\nDo you want to go to another page? '
                                                '(1. Yes / 2. No): ')
    return option


def print_attribute_type():
    option = input(text.default_text_color + 'Which type do you want to change the attribute? (1. PRIMITIVE TYPE / 2. '
                                             'ENUM / 3. GROUP): ')
    while validate_option_type(option) is False:
        print(text.Red + '\n- Invalid option')
        option = input(text.default_text_color + 'Which type do you want to change the attribute? (1. PRIMITIVE TYPE '
                                                 '/ 2. ENUM / 3. GROUP): ')
    return option


def print_primitive_type():
    option = input(text.default_text_color + 'Which Primitive type do you want to change the attribute? (1. NUMERIC / 2. '
                                             'TEXT / 3. DATE): ')
    while validate_option_type(option) is False:
        print(text.Red + '\n- Invalid option')
        option = input(
            text.default_text_color + 'Which Primitive type do you want to change the attribute? (1. NUMERIC / 2. '
                                      'TEXT / 3. DATE): ')
    return option


# Print environment menu
def print_environment_menu_supplier():
    environment = input(text.default_text_color + 'Environment (LOCAL, DEV, SIT, UAT): ')
    while validate_environment_supplier(environment.upper()) is False:
        print(text.Red + '\n- {0} is not a valid environment\n'.format(environment.upper()))
        environment = input(text.default_text_color + 'Environment (LOCAL, DEV, SIT, UAT): ')

    return environment.upper()