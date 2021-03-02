# Local application imports
from classes.text import text
from validations import validate_rewards, validate_rewards_transactions, validate_rewards_programs, \
    validate_rewards_challenges

# Print rewards menu
def print_rewards_menu():
    print(text.default_text_color + str(1), text.Yellow + 'Create a new program')
    print(text.default_text_color + str(2), text.Yellow + 'Update an existing program')
    print(text.default_text_color + str(3), text.Yellow + 'Enroll a POC to a program')
    print(text.default_text_color + str(4), text.Yellow + 'Disenroll a POC from a program')
    print(text.default_text_color + str(5), text.Yellow + 'Associate Redeem Products (DT Combos) to a POC')
    print(text.default_text_color + str(6), text.Yellow + 'Create a transaction to a POC')
    print(text.default_text_color + str(7), text.Yellow + 'Create/Delete Rewards challenges')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_rewards(structure) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + str(1), text.Yellow + 'Create a new program')
        print(text.default_text_color + str(2), text.Yellow + 'Update an existing program')
        print(text.default_text_color + str(3), text.Yellow + 'Enroll a POC to a program')
        print(text.default_text_color + str(4), text.Yellow + 'Disenroll a POC from a program')
        print(text.default_text_color + str(5), text.Yellow + 'Associate Redeem Products (DT Combos) to a POC')
        print(text.default_text_color + str(6), text.Yellow + 'Create a transaction to a POC')
        print(text.default_text_color + str(7), text.Yellow + 'Create/Delete Rewards challenges')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure

# Print rewards transactions menu
def print_rewards_transactions_menu():
    print(text.default_text_color + str(1), text.Yellow + 'Create a REDEMPTION transaction to a POC')
    print(text.default_text_color + str(2), text.Yellow + 'Create a REWARDS_OFFER transaction to a POC')
    print(text.default_text_color + str(3), text.Yellow + 'Create a POINTS_REMOVAL transaction to a POC')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_rewards_transactions(structure) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + str(1), text.Yellow + 'Create a REDEMPTION transaction to a POC')
        print(text.default_text_color + str(2), text.Yellow + 'Create a REWARDS_OFFER transaction to a POC')
        print(text.default_text_color + str(3), text.Yellow + 'Create a POINTS_REMOVAL transaction to a POC')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure

# Print rewards program menu
def print_rewards_program_menu():
    print(text.default_text_color + str(1), text.Yellow + 'Update an existing program - Add DT Combos from zone')
    print(text.default_text_color + str(2), text.Yellow + 'Update an existing program - Initial Balance')
    print(text.default_text_color + str(3), text.Yellow + 'Update an existing program - Redeem Limit')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_rewards_programs(structure) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + str(1), text.Yellow + 'Update an existing program - Add DT Combos from zone')
        print(text.default_text_color + str(2), text.Yellow + 'Update an existing program - Initial Balance')
        print(text.default_text_color + str(3), text.Yellow + 'Update an existing program - Redeem Limit')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure

# Print rewards challenges menu
def print_rewards_challenges_menu():
    print(text.default_text_color + str(1), text.Yellow + 'Create a TAKE_PHOTO challenge')
    print(text.default_text_color + str(2), text.Yellow + 'Create a MARK_COMPLETE challenge')
    print(text.default_text_color + str(3), text.Yellow + 'Create a PURCHASE challenge')
    print(text.default_text_color + str(4), text.Yellow + 'Create a PURCHASE_MULTIPLE challenge')
    print(text.default_text_color + str(5), text.Yellow + 'Delete a challenge')
    structure = input(text.default_text_color + '\nPlease select: ')
    while validate_rewards_challenges(structure) is False:
        print(text.Red + '\n- Invalid option')
        print(text.default_text_color + str(1), text.Yellow + 'Create a TAKE_PHOTO challenge')
        print(text.default_text_color + str(2), text.Yellow + 'Create a MARK_COMPLETE challenge')
        print(text.default_text_color + str(3), text.Yellow + 'Create a PURCHASE challenge')
        print(text.default_text_color + str(4), text.Yellow + 'Create a PURCHASE_MULTIPLE challenge')
        print(text.default_text_color + str(5), text.Yellow + 'Delete a challenge')
        structure = input(text.default_text_color + '\nPlease select: ')

    return structure