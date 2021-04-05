# Local application imports
from data_mass.classes.text import text
from data_mass.validations import validate_recommendation_type


def print_recommender_type_menu():
    print(text.default_text_color + '\nAlgo Selling operations')
    print(text.default_text_color + str(1), text.Yellow + 'Quick order')
    print(text.default_text_color + str(2), text.Yellow + 'Up sell')
    print(text.default_text_color + str(3), text.Yellow + 'Forgotten items')
    print(text.default_text_color + str(4), text.Yellow + 'Standard recommendations (all use cases)')
    print(text.default_text_color + str(5), text.Yellow + 'Input combos for Quick order')
    option = input(text.default_text_color + '\nPlease select: ')
    while validate_recommendation_type(option) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + '\nAlgo selling operations')
        print(text.default_text_color + str(1), text.Yellow + 'Quick order')
        print(text.default_text_color + str(2), text.Yellow + 'Up sell')
        print(text.default_text_color + str(3), text.Yellow + 'Forgotten items')
        print(text.default_text_color + str(4), text.Yellow + 'Standard recommendations (all use cases)')
        print(text.default_text_color + str(5), text.Yellow + 'Input combos for Quick order')
        option = input(text.default_text_color + '\nPlease select: ')

    return option
