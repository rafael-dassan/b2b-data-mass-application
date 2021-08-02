from datetime import datetime, timedelta

import click

from data_mass.account.accounts import check_account_exists_microservice
from data_mass.classes.text import text
from data_mass.common import (
    validate_user_entry_date,
    validate_yes_no_change_date
)
from data_mass.menus.order_menu import print_order_status_menu
from data_mass.product.utils import get_items_associated_account
from data_mass.rewards.rewards import flow_create_order_rewards, get_rewards


def create_order_rewards_redeem(
    account_id: str, zone: str, environment: str
) -> None:
    """
    Collect user prompt, call the process of order creation
     and print the returned orders.

    Parameters
    ----------
    account_id : str
        POC unique identifier
    zone : str
        e.g., AR, BR, DO, etc
    environment : str
        e.g., DEV, SIT, UAT
    """
    account = check_account_exists_microservice(
            account_id=account_id,
            zone=zone,
            environment=environment
        )
    if not account:
        return None

    order_status = print_order_status_menu()

    valid_acc = get_rewards(
        account_id=account_id,
        zone=zone,
        environment=environment
    )
    if not valid_acc:
        return None

    option_change_date = validate_yes_no_change_date()
    if option_change_date.upper() == "Y":
        delivery_date = validate_user_entry_date(
            'Enter Date for Delivery-Date (YYYY-mm-dd)'
        )
    else:
        tomorrow = datetime.today() + timedelta(1)
        delivery_date = str(datetime.date(tomorrow))

    qty_orders = click.prompt(
        'Please enter the quantity of orders to create (max. 20)',
        type=click.IntRange(1, 20)
    )

    items_list = get_items_associated_account(
        account_id=account_id,
        zone=zone,
        environment=environment,
        qty_lists=qty_orders
    )
    if not items_list:
        return None

    response = flow_create_order_rewards(
        zone=zone,
        environment=environment,
        account=account,
        items_list=items_list,
        order_status=order_status,
        quantity_orders=qty_orders,
        delivery_date=delivery_date
    )
    if response:
        print(f"{text.Green}The result: ")
        for index, order in enumerate(response, start=1):
            print(f"{index} - {order}")
