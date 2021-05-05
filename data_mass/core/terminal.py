from subprocess import call, check_output
from time import sleep

from data_mass.classes.text import text


def _has_update() -> bool:
    """
    Check if the local branch is up-do-date\
    with upstream/origin branch.

    Returns
    -------
    bool
        Whenever is up-to-date or not.
    """
    up_to_date_message = "Your branch is up to date with"
    output = check_output(["git status -uno"], shell=True)
    output = output.decode("utf-8")

    for message in output.split("\n"):
        if up_to_date_message in message:
            return False

    return True


def _pull_changes():
    """Pull changes from Azure Repos"""
    print("Baixando atualizações")
    call(["git pull"], shell=True)
    print("Done")


def _instal_version():
    """Install Data Mass updates."""
    print("Instalando nova versão do Data Mass")
    call(["pip3 install ."], shell=True)
    print("Done")


def update_project():
    """Update Project"""
    print("Updating Data Mass...")
    _pull_changes()
    _instal_version()

    print(text.Green + "Data Mass is up-to-date.")


def check_for_update():
    if _has_update():
        message = \
            "Your Data Mass is out-of-date, do you want to update? [y/n]: "
        response = input(text.Yellow + message)

        if response.lower() == "y":
            update_project()
        else:
            print(text.Red + "You should update ...")
            sleep(3)
