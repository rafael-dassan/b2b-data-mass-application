from data_mass.classes.text import text
from data_mass.validations import (
    validate_rewards,
    validate_rewards_challenges,
    validate_rewards_programs,
    validate_rewards_transactions
    )

TEXT_COLOR_DEFAULT = text.default_text_color
TEXT_COLOR_YELLOW = text.Yellow


def reward_options_menu():
    """
    Print rewards menu
    """
    print(
        TEXT_COLOR_DEFAULT + str(1),
        f"{TEXT_COLOR_YELLOW} Create a new program",
    )
    print(
        TEXT_COLOR_DEFAULT + str(2),
        f"{TEXT_COLOR_YELLOW} Update an existing program",
    )
    print(
        TEXT_COLOR_DEFAULT + str(3),
        f"{TEXT_COLOR_YELLOW} Enroll a POC to a program",
    )
    print(
        TEXT_COLOR_DEFAULT + str(4),
        f"{TEXT_COLOR_YELLOW} Disenroll a POC from a program",
    )
    print(
        TEXT_COLOR_DEFAULT + str(5),
        f"{TEXT_COLOR_YELLOW} Associate Redeem Products (DT Combos) to a POC",
    )
    print(
        TEXT_COLOR_DEFAULT + str(6),
        f"{TEXT_COLOR_YELLOW} Create a transaction to a POC",
    )
    print(
        TEXT_COLOR_DEFAULT + str(7),
        f"{TEXT_COLOR_YELLOW} Create/Delete Rewards challenges",
    )


def print_rewards_menu():
    """
    Get user input option for rewards menu.

    Returns
    -------
    str
        input option by the user.
    """
    reward_options_menu()
    structure = input(TEXT_COLOR_DEFAULT + "\nPlease select: ")
    while validate_rewards(structure) is False:
        print(text.Red + "\n- Invalid option")
        reward_options_menu()
        structure = input(TEXT_COLOR_DEFAULT + "\nPlease select: ")

    return structure


def rewards_transactions_options_menu():
    """
    Print rewards transactions menu.
    """
    print(
        TEXT_COLOR_DEFAULT + str(1),
        f"{TEXT_COLOR_YELLOW} Create a REDEMPTION transaction to a POC",
    )
    print(
        TEXT_COLOR_DEFAULT + str(2),
        f"{TEXT_COLOR_YELLOW} Create a REWARDS_OFFER transaction to a POC",
    )
    print(
        TEXT_COLOR_DEFAULT + str(3),
        f"{TEXT_COLOR_YELLOW} Create a POINTS_REMOVAL transaction to a POC",
    )
    print(TEXT_COLOR_DEFAULT + str(4), f"{TEXT_COLOR_YELLOW} Create an ORDER")


def print_rewards_transactions_menu():
    """
    Get user input option for transactions menu.

    Returns
    -------
    str
        input option by the user.
    """
    rewards_transactions_options_menu()
    structure = input(TEXT_COLOR_DEFAULT + "\nPlease select: ")
    while not validate_rewards_transactions(structure):
        rewards_transactions_options_menu()
        structure = input(TEXT_COLOR_DEFAULT + "\nPlease select: ")

    return structure


def rewards_program_options_menu():
    """
    Print rewards program menu.
    """
    print(
        TEXT_COLOR_DEFAULT + str(1),
        f"{TEXT_COLOR_YELLOW} Update an existing program - Add DT "
        "Combos from zone",
    )
    print(
        TEXT_COLOR_DEFAULT + str(2),
        f"{TEXT_COLOR_YELLOW} Update an existing program - Remove "
        "nonexistent DT Combos from program",
    )
    print(
        TEXT_COLOR_DEFAULT + str(3),
        f"{TEXT_COLOR_YELLOW} Update an existing program - Initial Balance",
    )
    print(
        TEXT_COLOR_DEFAULT + str(4),
        f"{TEXT_COLOR_YELLOW} Update an existing program - Redeem Limit",
    )


def print_rewards_program_menu():
    """
    Get user input option for program menu.

    Returns
    -------
    str
        input option by the user.
    """
    rewards_program_options_menu()
    structure = input(TEXT_COLOR_DEFAULT + "\nPlease select: ")
    while validate_rewards_programs(structure) is False:
        print(text.Red + "\n- Invalid option")
        rewards_program_options_menu()
        structure = input(TEXT_COLOR_DEFAULT + "\nPlease select: ")

    return structure


def rewards_challenges_option_menu():
    """
    Print rewards challenges menu.
    """
    print(
        TEXT_COLOR_DEFAULT + str(1),
        f"{TEXT_COLOR_YELLOW} Create a TAKE_PHOTO challenge",
    )
    print(
        TEXT_COLOR_DEFAULT + str(2),
        f"{TEXT_COLOR_YELLOW} Create a MARK_COMPLETE challenge",
    )
    print(
        TEXT_COLOR_DEFAULT + str(3),
        f"{TEXT_COLOR_YELLOW} Create a PURCHASE challenge",
    )
    print(
        TEXT_COLOR_DEFAULT + str(4),
        f"{TEXT_COLOR_YELLOW} Create a PURCHASE_MULTIPLE challenge",
    )
    print(
        TEXT_COLOR_DEFAULT + str(5),
        f"{TEXT_COLOR_YELLOW} Delete a challenge",
    )


def print_rewards_challenges_menu():
    """
    Get user input option for challenges menu.

    Returns
    -------
    str
        input option by the user.
    """
    rewards_challenges_option_menu()
    structure = input(TEXT_COLOR_DEFAULT + "\nPlease select: ")
    while validate_rewards_challenges(structure) is False:
        print(text.Red + "\n- Invalid option")
        rewards_challenges_option_menu()
        structure = input(TEXT_COLOR_DEFAULT + "\nPlease select: ")

    return structure
