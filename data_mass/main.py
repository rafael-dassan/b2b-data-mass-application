from datetime import datetime, timedelta
from math import inf
from random import random, sample

import click
import pyperclip

from data_mass.accounts import *
from data_mass.algo_selling import *
from data_mass.category_magento import *
from data_mass.combos import *
from data_mass.common import *
from data_mass.credit import add_credit_to_account_microservice
from data_mass.deals import *
from data_mass.delivery_window import *
from data_mass.enforcement import *
from data_mass.files import create_file_api
from data_mass.invoices import *
from data_mass.menus.account_menu import (
    delivery_window_menu,
    print_account_enable_empties_loan_menu,
    print_account_id_menu,
    print_account_name_menu,
    print_account_operations_menu,
    print_account_status_menu,
    print_alternative_delivery_date_menu,
    print_get_account_operations_menu,
    print_include_delivery_cost_menu,
    print_minimum_order_menu,
    print_payment_method_menu
    )
from data_mass.menus.algo_selling_menu import print_recommender_type_menu
from data_mass.menus.deals_menu import (
    print_deals_operations_menu,
    print_discount_percentage_menu,
    print_discount_range_menu,
    print_free_good_quantity_menu,
    print_free_good_redemption_menu,
    print_interactive_combos_quantity_range_menu,
    print_interactive_combos_quantity_range_menu_v2,
    print_max_quantity_menu,
    print_minimum_quantity_menu,
    print_option_sku_menu,
    print_partial_free_good_menu,
    print_stepped_discount_ranges_menu,
    print_stepped_free_good_ranges_menu
    )
from data_mass.menus.inventory_menu import (
    print_inventory_option_menu,
    print_inventory_sku_quantity_menu
    )
from data_mass.menus.invoice_menu import (
    print_invoice_id_menu,
    print_invoice_operations_menu,
    print_invoice_payment_method_menu,
    print_invoice_status_menu,
    print_invoice_status_menu_retriever
    )
from data_mass.menus.order_menu import (
    print_allow_cancellable_order_menu,
    print_get_order_menu,
    print_order_id_menu,
    print_order_operations_menu,
    print_order_status_menu
    )
from data_mass.menus.product_menu import (
    print_get_products_menu,
    print_product_operations_menu
    )
from data_mass.menus.rewards_menu import (
    print_rewards_challenges_menu,
    print_rewards_menu,
    print_rewards_program_menu,
    print_rewards_transactions_menu
    )
from data_mass.menus.supplier_menu import (
    print_attribute_primitive,
    print_attribute_type,
    print_create_attribute_menu,
    print_create_supplier_category_menu,
    print_environment_menu_supplier,
    print_max_cardinality,
    print_min_cardinality,
    print_new_attribute,
    print_new_page
    )
from data_mass.orders import *
from data_mass.product.inventory import *
from data_mass.product.magento import *
from data_mass.product.products import *
from data_mass.rewards.rewards import (
    associate_dt_combos_to_poc,
    disenroll_poc_from_program,
    display_program_rules_skus,
    enroll_poc_to_program
    )
from data_mass.rewards.rewards_challenges import (
    create_mark_complete_challenge,
    create_purchase_challenge,
    create_take_photo_challenge,
    remove_challenge
    )
from data_mass.rewards.rewards_programs import (
    create_new_program,
    patch_program_root_field,
    remove_program_dt_combos,
    update_program_dt_combos
    )
from data_mass.rewards.rewards_transactions import (
    create_points_removal,
    create_redemption,
    create_rewards_offer
    )
from data_mass.rewards.rewards_utils import flow_create_order_rewards
from data_mass.simulation import (
    process_simulation_microservice,
    request_order_simulation
    )
from data_mass.supplier.attribute import (
    check_if_attribute_exist,
    create_attribute_enum,
    create_attribute_group,
    create_attribute_primitive_type,
    create_legacy_attribute_container,
    create_legacy_attribute_package,
    create_legacy_root_attribute,
    delete_attribute_supplier,
    display_all_attribute,
    display_specific_attribute,
    edit_attribute_type,
    search_all_attribute,
    search_specific_attribute
    )
from data_mass.supplier.category import (
    check_if_supplier_category_exist,
    create_association_attribute_with_category,
    create_legacy_category,
    create_root_category,
    create_sub_category_supplier,
    display_all_category,
    display_specific_category,
    search_all_category,
    search_specific_category
    )
from data_mass.supplier.product import create_product_supplier
from data_mass.user.creation import create_user
from data_mass.user.deletion import delete_user_v3
from data_mass.validations import is_number, validate_yes_no_option

TEXT_GREEN = text.Green


def show_menu():
    clear_terminal()
    print_welcome_script()
    selection_structure = print_structure_menu()
    option = print_available_options(selection_structure)
    if selection_structure == '1':
        switcher = {
            '0': finish_application,
            '1': account_menu,
            '2': product_menu,
            '3': order_menu,
            '4': deals_menu,
            '5': input_combos_menu,
            '6': invoice_menu,
            '7': create_rewards_to_account,
            '8': create_credit_statement_menu
        }
    elif selection_structure == '2':
        switcher = {
            '0': finish_application,
            '1': check_simulation_service_account_microservice_menu,
            '2': account_information_menu,
            '3': product_information_menu,
            '4': deals_information_menu,
            '5': order_information_menu,
            '6': recommender_information_menu,
            '7': retrieve_available_invoices_menu,
            '8': retriever_sku_menu
        }
    elif selection_structure == '3':
        switcher = {
            '0': finish_application,
            # '1': token_generator_jwt,
            '1': token_generator_root,
            '2': token_generator_inclusion,
            '3': token_generator_basic
        }
    elif selection_structure == '4':
        switcher = {
            '0': finish_application,
            '1': get_categories_menu,
            '2': associate_product_to_category_menu,
            '3': create_categories_menu
        }
    elif selection_structure == '5':
        switcher = {
            '0': finish_application,
            '1': registration_user_iam,
            '2': delete_user_iam
        }
    elif selection_structure == '6':
        switcher = {
            '0': finish_application,
            '1': create_attribute_menu,
            '2': create_category_supplier_menu,
            '3': attribute_associated_category_menu,
            '4': delete_attribute_menu,
            '5': edit_attribute_type_menu,
            '6': create_product_menu
        }
    elif selection_structure == '7':
        switcher = {
            '0': finish_application,
            '1': search_specific_attribute_menu,
            '2': search_all_attribute_menu,
            '3': search_specific_category_menu,
            '4': search_all_category_menu,
        }
    else:
        finish_application()

    function = switcher.get(option, '')

    if function != '':
        function()

    print_finish_application_menu()


def deals_information_menu():
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    abi_id = print_account_id_menu(zone)
    if not abi_id:
        print_finish_application_menu()

    account = check_account_exists_microservice(abi_id, zone, environment)
    if not account:
        print_finish_application_menu()

    deals = request_get_deals_promo_fusion_service(zone, environment, abi_id)
    if deals:
        display_deals_information_promo_fusion(abi_id, deals)
    else:
        print_finish_application_menu()


def product_information_menu():
    selection_structure = print_get_products_menu()
    environment = print_environment_menu()

    switcher = {
        '1': 'PRODUCT',
        '2': 'INVENTORY',
        '3': 'PRODUCT_ZONE',
    }

    products_type = switcher.get(selection_structure, False)

    if products_type == 'PRODUCT':
        zone = print_zone_menu_for_ms()
        abi_id = print_account_id_menu(zone)
        if not abi_id:
            print_finish_application_menu()
        account = check_account_exists_microservice(abi_id, zone, environment)
        if not account:
            print_finish_application_menu()

        product_offers = request_get_products_by_account_microservice(abi_id, zone, environment)
        if not product_offers:
            print_finish_application_menu()
        elif product_offers == 'not_found':
            print(text.Red + '\n- [Catalog Service] There is no product associated with the account ' + abi_id)
            print_finish_application_menu()

        display_product_information(product_offers)

    elif products_type == 'INVENTORY':
        zone = print_zone_menu_for_ms()
        abi_id = print_account_id_menu(zone)
        if not abi_id:
            print_finish_application_menu()

        account = check_account_exists_microservice(abi_id, zone, environment)
        if not account:
            print_finish_application_menu()
        delivery_center_id = account[0]['deliveryCenterId']

        product_offers = request_get_account_product_assortment(abi_id, zone, environment, delivery_center_id)
        if not product_offers:
            print_finish_application_menu()
        elif product_offers == 'not_found':
            print(text.Red + '\n- [Product Assortment Service] There is no product associated with the account ' + abi_id)
            print_finish_application_menu()

        inventory = get_delivery_center_inventory(environment, zone, abi_id, delivery_center_id, product_offers)
        if not inventory:
            print_error_delivery_center_inventory(delivery_center_id)
            print_finish_application_menu()
        else:
            display_inventory_by_account(inventory)

    else:
        zone = print_zone_menu_for_ms()

        products = request_get_products_microservice(zone, environment)
        if not products:
            print_finish_application_menu()

        display_items_information_zone(products)


def print_error_delivery_center_inventory(delivery_id: str):
    print(
        f'{text.Red}\n'
        f'Error while trying to retrive inventory for "{delivery_id}".'
    )


def account_information_menu():
    operation = print_get_account_operations_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()

    return {
        '1': lambda: flow_get_account(zone, environment)
    }.get(operation, lambda: None)()


def flow_get_account(zone, environment):
    account_id = print_account_id_menu(zone)
    if not account_id:
        print_finish_application_menu()

    account = check_account_exists_microservice(account_id, zone, environment)
    if not account:
        print_finish_application_menu()

    display_account_information(account)


# Input Rewards to account
def create_rewards_to_account():
    selection_structure = print_rewards_menu()
    
    if selection_structure == '2':
        selection_structure = print_rewards_program_menu()
        switcher = {
            '1': 'ADD_COMBOS',
            '2': 'REMOVE_COMBOS',
            '3': 'UPDATE_BALANCE',
            '4': 'UPDATE_REDEEM_LIMIT',
        }
    elif selection_structure == '6':
        selection_structure = print_rewards_transactions_menu()
        switcher = {
            '1': 'CREATE_REDEMPTION',
            '2': 'CREATE_REWARDS_OFFER',
            '3': 'CREATE_POINTS_REMOVAL',
            '4': 'CREATE_ORDER_REWARDS'
        }
    elif selection_structure == '7':
        selection_structure = print_rewards_challenges_menu()
        switcher = {
            '1': 'CREATE_TAKE_PHOTO',
            '2': 'CREATE_MARK_COMPLETE',
            '3': 'CREATE_PURCHASE',
            '4': 'CREATE_PURCHASE_MULTIPLE',
            '5': 'DELETE_CHALLENGE'
        }
    else:
        switcher = {
            '1': 'NEW_PROGRAM',
            '3': 'ENROLL_POC',
            '4': 'DISENROLL_POC',
            '5': 'ADD_REDEEM',
        }

    reward_option = switcher.get(selection_structure, False)
 
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()

    # Option to create a new program
    if reward_option == 'NEW_PROGRAM':
        create_new_program(zone, environment)
        print_finish_application_menu()
    
    # Option to update a program DT combos according to the DT combos from the zone
    elif reward_option == 'ADD_COMBOS':
        update_program_dt_combos(zone, environment)
        print_finish_application_menu()
    
    # Option to remove nonexistent DT combos from the program
    elif reward_option == 'REMOVE_COMBOS':
        remove_program_dt_combos(zone, environment)
        print_finish_application_menu()

    # Option to update initial balance of a program
    elif reward_option == 'UPDATE_BALANCE':
        patch_program_root_field(zone, environment, 'initial_balance')
        print_finish_application_menu()

    # Option to update the program redeem limit
    elif reward_option == 'UPDATE_REDEEM_LIMIT':
        patch_program_root_field(zone, environment, 'redeem_limit')
        print_finish_application_menu()

    # Option to enroll a POC to a rewards program
    elif reward_option == 'ENROLL_POC':
        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account:
            enroll_poc_to_program(abi_id, zone, environment, account)

        print_finish_application_menu()

    # Option to disenroll a POC from a program
    elif reward_option == 'DISENROLL_POC':

        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account:
            disenroll_poc_from_program(abi_id, zone, environment)
            
        print_finish_application_menu()

    # Option to associate redeem products to an account
    elif reward_option == 'ADD_REDEEM':

        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account:
            associate_dt_combos_to_poc(abi_id, zone, environment)
        
        print_finish_application_menu()
    
    # Option to create a REDEMPTION transaction to a POC
    elif reward_option == 'CREATE_REDEMPTION':
        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account:
            create_redemption(abi_id, zone, environment)
            
        print_finish_application_menu()
    
    # Option to create a REWARDS_OFFER transaction to a POC
    elif reward_option == 'CREATE_REWARDS_OFFER':
        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account:
            create_rewards_offer(abi_id, zone, environment)
            
        print_finish_application_menu()

    # Option to create a POINTS_REMOVAL transaction to a POC
    elif reward_option == 'CREATE_POINTS_REMOVAL':
        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account:
            create_points_removal(abi_id, zone, environment)
            
        print_finish_application_menu()

    elif reward_option == 'CREATE_ORDER_REWARDS':
        account_id = print_account_id_menu(zone)
        if not account_id:
            print_finish_application_menu()

        account = check_account_exists_microservice(
            account_id=account_id,
            zone=zone,
            environment=environment
        )
        if not account:
            print_finish_application_menu()

        order_status = print_order_status_menu()

        # TODO:check_if_account is valid for the rewards

        qty_orders = click.prompt(
            'Please entet the quantity of orders to create',
            type=click.IntRange(0, inf)
        )
        response = flow_create_order_rewards(
            zone=zone,
            environment=environment,
            account=account,
            item_list=item_list,
            order_status=order_status,
            quantity_orders=qty_orders,
            )
        if response:
            # TODO: points balance
            print(
                TEXT_GREEN
                + f"\n- Order {response.get('orderNumber')} created successfully"
            )
            
        print_finish_application_menu()

    # Option to create a TAKE_PHOTO challenge for zone
    elif reward_option == 'CREATE_TAKE_PHOTO':
        create_take_photo_challenge(zone, environment)
        print_finish_application_menu()
    
    # Option to create a MARK_COMPLETE challenge for zone
    elif reward_option == 'CREATE_MARK_COMPLETE':
        create_mark_complete_challenge(zone, environment)
        print_finish_application_menu()

    # Option to create a PURCHASE challenge for zone
    elif reward_option == 'CREATE_PURCHASE':
        create_purchase_challenge(zone, environment, False)
        print_finish_application_menu()
    
    # Option to create a PURCHASE_MULTIPLE challenge for zone
    elif reward_option == 'CREATE_PURCHASE_MULTIPLE':
        create_purchase_challenge(zone, environment, True)
        print_finish_application_menu()

    # Option to DELETE a challenge
    elif reward_option == 'DELETE_CHALLENGE':
        remove_challenge(zone, environment)
        print_finish_application_menu()
    

def order_menu():
    operation = print_order_operations_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    account_id = print_account_id_menu(zone)

    if not account_id:
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if not account:
        print_finish_application_menu()
    delivery_center_id = account[0]['deliveryCenterId']

    # Call function to check if the account has products inside
    product_offers = request_get_offers_microservice(
        account_id=account_id,
        zone=zone,
        environment=environment
    )
    if not product_offers:
        print_finish_application_menu()
    elif product_offers == 'not_found':
        print(
            text.Red
            + '\n- There is no product associated'
            f'with the account {account_id}'
        )
        print_finish_application_menu()

    if operation != '2':
        unique_sku = {item['sku'] for item in product_offers}
        unique_sku = sample(list(unique_sku), len(unique_sku))
        order_status = print_order_status_menu()
        print(
            TEXT_GREEN
            + f"The account has {len(unique_sku)} products associated!"
        )
        quantity = click.prompt(
            f'{text.default_text_color}'
            'Quantity of products you want to include in this order',
            type=click.IntRange(1, len(unique_sku)),
        )

        item_list = []
        for sku in unique_sku[:quantity]:
            data = {'sku': sku, 'itemQuantity': randint(0, 10)} 
            item_list.append(data)

    return {
        '1': lambda: flow_create_order(
            zone,
            environment,
            account_id,
            delivery_center_id,
            order_status,
            item_list
        ),
        '2': lambda: flow_create_changed_order(
            zone,
            environment,
            account_id
        ),
    }.get(operation, lambda: None)()


def flow_create_order(
    zone: str,
    environment: str,
    account_id: str,
    delivery_center_id: str,
    order_status: str,
    item_list: list
    ):
    """
    Create a dataflow to match business rules.

    Parameters
    ----------
    zone : str
        e.g., AR, BR, DO, etc
    environment : str
        e.g., DEV, SIT, UAT
    account_id : str
        POC unique identifier
    delivery_center_id : str
        POC's delivery center
    order_status : str
        order status e.g. Placed, Pending, Confirmed, etc
    item_list : list
        list of items
    """

    if order_status == 'PLACED':
        allow_order_cancel = print_allow_cancellable_order_menu()
    else:
        allow_order_cancel = 'N'


    if order_status == 'DELIVERED':
        # Sets the format of the delivery date of the order (current date and time less one day)
        delivery_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        option_change_date = validate_yes_no_change_date()
        if option_change_date.upper() == "Y": 
            delivery_date = validate_user_entry_date(
                'Enter Date for Delivery-Date (YYYY-mm-dd)'
        )
        else:
            tomorrow = datetime.today() + timedelta(1)
            delivery_date = str(datetime.date(tomorrow)) 

    order_items = request_order_simulation(
        zone=zone,
        environment=environment,
        account_id=account_id,
        delivery_center_id=delivery_center_id,
        items=item_list,
        combos=[],
        empties=[],
        payment_method='CASH',
        payment_term=0,
        delivery_date=delivery_date
    )
    if not order_items:
        print_finish_application_menu()

    response = request_order_creation(
        account_id=account_id,
        delivery_center_id=delivery_center_id,
        zone=zone,
        environment=environment,
        allow_order_cancel=allow_order_cancel,
        order_items=order_items,
        order_status=order_status,
        delivery_date=delivery_date
    )

    if response:
        print(
            text.Green 
            + f'\n- Order {response.get("orderNumber")} '
            'created successfully'
        )

    print_finish_application_menu()


def flow_create_changed_order(
    zone: str,
    environment: str,
    account_id: int
    ):
    """
    Create a dataflow to match business rules.

    Parameters
    ----------
    zone : str
        e.g., AR, BR, DO, etc
    environment : str
        e.g., DEV, SIT, UAT
    account_id : int
        POC unique identifier
    """

    order_id = print_order_id_menu()
    order_data = check_if_order_exists(account_id, zone, environment, order_id)
    if not order_data:
        print_finish_application_menu()
    elif order_data == "empty":
        print(text.Red + f"\n- The account {account_id} does not have orders")
        print_finish_application_menu()
    elif order_data == "not_found":
        print(text.Red + f"\n- The order {order_id} does not exist")
        print_finish_application_menu()

    statuses = [
        "DENIED",
        "CANCELLED",
        "DELIVERED",
        "PARTIAL_DELIVERY",
        "PENDING_CANCELLATION",
        "INVOICED",
        "IN_TRANSIT",
    ]

    if order_data[0]["status"] in statuses:
        print(
            text.Red + "\n- This order cannot be changed. "
            f'Order status: {order_data[0]["status"]}'
        )
        print_finish_application_menu()

    if (
        len(order_data[0]["items"]) == 1
        and order_data[0]["items"][0]["quantity"] == 1
    ):
        print(
            text.Red
            + "\n- It's not possible to change this order because it has "
            "only one product with quantity equals 1"
        )
        print_finish_application_menu()

    delivery_date = (
        order_data[0]["delivery"]["date"]
        if order_data[0]["delivery"]["date"]
        else ""
    )

    print(
        text.Green + "The Delivery-Date is " + f"{text.Blue}{delivery_date}!"
    )
    option_change_date = validate_yes_no_change_date(
        question="Change Delivery Date? y/N: "
    )
    if option_change_date.upper() == "Y":
        delivery_date = validate_user_entry_date(
            "Change Delivery-Date (YYYY-mm-dd)!"
        )

    order_data[0]["delivery"]["date"] = delivery_date

    response = request_changed_order_creation(zone, environment, order_data)
    if response == 'success':
        print(TEXT_GREEN + f'\n- The order {order_id} was changed successfully')
    else:
        print_finish_application_menu()


# Place request for simulation service in microservice
def check_simulation_service_account_microservice_menu():
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    abi_id = print_account_id_menu(zone)
    if not abi_id:
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone, environment)

    if not account:
        print_finish_application_menu()

    order_items = list()
    order_combos = list()
    empties_skus = list()

    # input normal sku in simulation
    input_order_item = input(text.default_text_color + "Would you like to include a new sku for simulation? (y/n) ")
    while input_order_item.upper() != "Y" and input_order_item.upper() != "N":
        print(text.Red + "\n- Invalid option\n")
        input_order_item = input(text.default_text_color + "Would you like to include a new sku for simulation? (y/n) ")

    if input_order_item.upper() == "Y":
        more_sku = "Y"
        while more_sku.upper() == "Y":
            sku = input(text.default_text_color + "Inform sku for simulation: ")
            quantity = input(text.default_text_color + "Inform sku quantity for simulation: ")
            while not is_number(quantity):
                print(text.Red + "\n- Invalid quantity\n")
                quantity = input(text.default_text_color + "Inform sku quantity for simulation: ")

            temp_product_data = {"sku": sku, "itemQuantity": quantity}
            order_items.append(temp_product_data)
            more_sku = input(text.default_text_color + "Would you like to include more skus for simulation? (y/N) ")

    # input combo sku in simulation
    input_order_combo = input(text.default_text_color + "Would you like to include a new combo for simulation? (y/n) ")
    while input_order_combo.upper() != "Y" and input_order_combo.upper() != "N":
        print(text.Red + "\n- Invalid option\n")
        input_order_combo = input(
            text.default_text_color + "Would you like to include a new combo for simulation? (y/n) ")

    if input_order_combo.upper() == "Y":
        more_combo = "Y"
        while more_combo.upper() == "Y":
            sku = input(text.default_text_color + "Inform combo sku for simulation: ")
            quantity = input(text.default_text_color + "Inform combo sku quantity for simulation: ")
            while not is_number(quantity):
                print(text.Red + "\n- Invalid quantity\n")
                quantity = input(text.default_text_color + "Inform combo sku quantity for simulation: ")

            temp_combo_data = {"comboId": sku, "quantity": quantity}
            order_combos.append(temp_combo_data)
            more_combo = input(text.default_text_color + "Would you like to include more skus for simulation? (y/N) ")

    # input combo sku in simulation
    input_order_empties = input(
        text.default_text_color + "Would you like to include a new empties sku for simulation? (y/n) ")
    while input_order_empties.upper() != "Y" and input_order_empties.upper() != "N":
        print(text.Red + "\n- Invalid option\n")
        input_order_empties = input(
            text.default_text_color + "Would you like to include a new empties sku for simulation? (y/n) ")

    if input_order_empties.upper() == "Y":
        more_empties = "Y"
        while more_empties.upper() == "Y":
            sku = input(text.default_text_color + "Inform combo sku for simulation: ")
            quantity = input(text.default_text_color + "Inform combo sku quantity for simulation: ")
            while not is_number(quantity):
                print(text.Red + "\n- Invalid quantity\n")
                quantity = input(text.default_text_color + "Inform combo sku quantity for simulation: ")

            temp_empties_data = {"groupId": sku, "quantity": quantity}
            empties_skus.append(temp_empties_data)
            more_empties = input(text.default_text_color + "Would you like to include more skus for simulation? (y/N) ")

    # Payment Method menu
    payment_method = print_payment_method_simulation_menu(zone)
    if payment_method.upper() == "BANK_SLIP":
        payment_term = input(text.default_text_color + "Enter the number of days the bill will expire: ")
        while not is_number(payment_term):
            print(text.Red + "\n- Invalid number\n")
            payment_term = input(text.default_text_color + "Enter the number of days the bill will expire: ")
    else:
        payment_term = 0

    cart_response = request_order_simulation(zone, environment, abi_id, account[0]['deliveryCenterId'], order_items,
                                             order_combos, empties_skus, payment_method, payment_term)
    if cart_response:
        process_simulation_microservice(cart_response)
    else:
        print_finish_application_menu()


def deals_menu():
    operation = print_deals_operations_menu()

    # For Interactive Combos
    if operation == '6' or operation == '7':
        zone = print_zone_for_interactive_combos_menu_for_ms()
    else:
        zone = print_zone_menu_for_ms()

    environment = print_environment_menu()
    account_id = print_account_id_menu(zone)

    if not account_id:
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if not account:
        print_finish_application_menu()

    option_sku = print_option_sku_menu()

    # Request POC's associated products
    product_offers = request_get_offers_microservice(account_id, zone, environment)
    if not product_offers:
        print_finish_application_menu()
    elif product_offers == 'not_found':
        print(text.Red + '\n- [Catalog Service] There is no product associated with the account {account_id}'
              .format(account_id=account_id))
        print_finish_application_menu()

    sku_list = list()
    # Interactive combos:
    if operation == '6' or operation == '7':
        while len(sku_list) <= 3:
            index_offers = randint(0, (len(product_offers) - 1))
            product_data = product_offers[index_offers]
            sku_list.append(product_data)

    else:
        while len(sku_list) <= 2:
            index_offers = randint(0, (len(product_offers) - 1))
            product_data = product_offers[index_offers]
            sku_list.append(product_data)

    if option_sku == '1':
        if operation == '6' or operation == '7':
            sku_list.clear()
            for y in range(3):
                sku = input(text.default_text_color + 'SKU: ')
                sku_id = sku.strip()
                for i in range(len(product_offers)):
                    if product_offers[i]['sku'] == sku_id:
                        sku_list.append(product_offers[i])

                if len(sku_list) == 0:
                    print(text.Red + '\n- The SKU {sku_id} is not associated with the account {account_id} or it doesn`t exist'
                          .format(sku_id=sku_id, account_id=account_id))
                    print_finish_application_menu()

            if len(sku_list) == 3:
                if sku_list[0] == sku_list[1] or sku_list[1] == sku_list[2] or sku_list[2] == sku_list[0]:
                            print(text.Red + '\n It is not possible to insert interactive combos using the same SKU')
                            print_finish_application_menu()
        else:
            sku = input(text.default_text_color + 'SKU: ')
            sku_id = sku.strip()
            sku_list.clear()
            for i in range(len(product_offers)):
                if product_offers[i]['sku'] == sku_id:
                    sku_list.append(product_offers[i])
            if len(sku_list) == 0:
                print(text.Red + '\n- The SKU {sku_id} is not associated with the account {account_id} or it doesn`t exist'
                      .format(sku_id=sku_id, account_id=account_id))
                print_finish_application_menu()

    else:
        sku = sku_list[0]['sku']

    return {
        '1': lambda: flow_create_discount(zone, environment, account_id, sku),
        '2': lambda: flow_create_stepped_discount(zone, environment, account_id, sku),
        '3': lambda: flow_create_stepped_discount_with_limit(zone, environment, account_id, sku),
        '4': lambda: flow_create_free_good(zone, environment, account_id, sku_list),
        '5': lambda: flow_create_stepped_free_good(zone, environment, account_id, sku),
        '6': lambda: flow_create_interactive_combos(zone, environment, account_id, sku_list),
        '7': lambda: flow_create_interactive_combos_v2(zone, environment, account_id, sku_list)
    }.get(operation, lambda: None)()


def flow_create_discount(zone, environment, account_id, sku):
    minimum_quantity = print_minimum_quantity_menu()
    discount_value = print_discount_percentage_menu()

    response = create_discount(account_id, sku, zone, environment, discount_value, minimum_quantity)
    if response:
        print(TEXT_GREEN + f'\n- Deal {response} created successfully')
    else:
        print_finish_application_menu()


def flow_create_stepped_discount(zone, environment, account_id, sku):
    ranges = print_stepped_discount_ranges_menu()

    response = create_stepped_discount(account_id, sku, zone, environment, ranges)
    if response:
        print(TEXT_GREEN + f'\n- Deal {response} created successfully')
    else:
        print_finish_application_menu()


def flow_create_stepped_discount_with_limit(zone, environment, account_id, sku):
    # Default index range (from 1 to 9999 products)
    default_index_range = [1, 9999]

    discount_range = print_discount_range_menu(1)
    max_quantity = print_max_quantity_menu(default_index_range)

    response = create_stepped_discount_with_limit(account_id, sku, zone, environment, default_index_range,
                                                  discount_range, max_quantity)
    if response:
        print(TEXT_GREEN + f'\n- Deal {response} created successfully')
    else:
        print_finish_application_menu()


def flow_create_free_good(zone, environment, account_id, sku_list):
    partial_free_good = print_partial_free_good_menu(zone)
    need_to_buy_product = print_free_good_redemption_menu(partial_free_good)

    if need_to_buy_product == 'Y':
        minimum_quantity = print_minimum_quantity_menu()
        quantity = print_free_good_quantity_menu()
    else:
        minimum_quantity = 1
        quantity = print_free_good_quantity_menu()

    response = create_free_good(account_id, sku_list, zone, environment, minimum_quantity, quantity,
                                partial_free_good, need_to_buy_product)
    if response:
        print(TEXT_GREEN + f'\n- Deal {response} created successfully')
    else:
        print_finish_application_menu()


def flow_create_stepped_free_good(zone, environment, account_id, sku):
    ranges = print_stepped_free_good_ranges_menu()

    response = create_stepped_free_good(account_id, sku, zone, environment, ranges)
    if response:
        print(TEXT_GREEN + f'\n- Deal {response} created successfully')
    else:
        print_finish_application_menu()


# Interactive combos v1
def flow_create_interactive_combos(zone, environment, account_id, sku):
    index_range = print_interactive_combos_quantity_range_menu()

    response = create_interactive_combos(account_id, sku, zone, environment, index_range)

    if response:
        print(TEXT_GREEN + f'\n- Deal {response} created successfully')
    else:
        print_finish_application_menu()


# Interactive combos v2
def flow_create_interactive_combos_v2(zone, environment, account_id, sku):
    index_range = print_interactive_combos_quantity_range_menu_v2()

    response = create_interactive_combos_v2(account_id, sku, zone, environment, index_range)

    if response:
        print(TEXT_GREEN + f'\n- Deal {response} created successfully')
    else:
        print_finish_application_menu()


# Input combos to an account
def input_combos_menu():
    selection_structure = print_combos_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()

    abi_id = print_account_id_menu(zone)
    if not abi_id:
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone, environment)

    if not account:
        print_finish_application_menu()

    product_offers = request_get_offers_microservice(abi_id, zone, environment)
    if not product_offers:
        print_finish_application_menu()
    elif product_offers == 'not_found':
        print(text.Red + '\n- [Catalog Service] There is no product associated with the account ' + abi_id)
        print_finish_application_menu()

    index_offers = randint(0, (len(product_offers) - 1))
    sku = product_offers[index_offers]['sku']

    # Combo type discount
    if selection_structure == '1':
        while True:
            try:
                discount_value = int(input(text.default_text_color + 'Discount percentage (%): '))
                break
            except ValueError:
                print(text.Red + '\n- Invalid value')

        response = input_combo_type_discount(abi_id, zone, environment, sku, discount_value)

    # Combo type free good
    elif selection_structure == '2':
        response = input_combo_type_free_good(abi_id, zone, environment, sku)

    # Combo type digital trade
    elif selection_structure == '3':
        response = input_combo_type_digital_trade(abi_id, zone, environment)

    # Combo type only free goods
    elif selection_structure == '4':
        response = input_combo_only_free_good(abi_id, zone, environment, sku)

    # Reset combo consumption to zero
    else:
        combo_id = print_combo_id_menu()
        combo = check_combo_exists_microservice(abi_id, zone, environment, combo_id)
        update_combo = update_combo_consumption(abi_id, zone, environment, combo_id)

        if combo and update_combo:
            print(TEXT_GREEN + '\n- Combo consumption for ' + combo_id + ' was successfully updated')

    if selection_structure != '5' and response:
        print(TEXT_GREEN + '\n- Combo ' + response + ' successfully registered')

    print_finish_application_menu()


def product_menu():
    operation = print_product_operations_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()

    return {
        '1': lambda: flow_create_product(zone, environment),
        '2': lambda: flow_associate_products_to_account(zone, environment),
        '3': lambda: flow_input_inventory_to_product(zone, environment),
        '4': lambda: flow_input_recommended_products_to_account(zone, environment),
        '5': lambda: flow_input_empties_discounts(zone, environment),
        '6': lambda: flow_input_sku_limit(zone, environment)
    }.get(operation, lambda: None)()


def flow_create_product(zone, environment):
    item_data = get_item_input_data()

    response = create_product(zone, environment, item_data)
    if not response:
        print_finish_application_menu()
    else:
        print(TEXT_GREEN + '\n- The product {sku} - {product_name} was created successfully'
              .format(sku=response.get('sku'), product_name=response.get('name')))


def flow_associate_products_to_account(zone, environment):
    account_id = print_account_id_menu(zone)

    if not account_id:
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)

    if not account:
        print_finish_application_menu()
    delivery_center_id = account[0]['deliveryCenterId']

    proceed = 'N'
    products = request_get_offers_microservice(account_id, zone, environment)
    if not products:
        print_finish_application_menu()
    elif products == 'not_found':
        proceed = 'Y'
    else:
        proceed = input(text.Yellow + '\n- [Account] The account {account_id} already have products, do you want '
                                      'to proceed? y/N: '.format(account_id=account_id)).upper()
        if proceed == '':
            proceed = 'N'

    if proceed == 'Y':
        all_products_zone = request_get_products_microservice(zone, environment)
        if not all_products_zone:
            print_finish_application_menu()

        # Call add products to account function
        add_products = add_products_to_account_microservice(account_id, zone, environment, delivery_center_id,
                                                            all_products_zone)
        if add_products != 'success':
            print(text.Red + '\n- [Products] Something went wrong, please try again')
            print_finish_application_menu()

        products = request_get_account_product_assortment(account_id, zone, environment, delivery_center_id)
        if not products:
            print_finish_application_menu()
        elif products == 'not_found':
            print(text.Red + '\n- [Product Assortment Service] There is no product associated with the account '
                             '{account_id}'.format(account_id=account_id))
            print_finish_application_menu()

        skus_id = list()
        aux_index = 0
        while aux_index <= (len(products) - 1):
            skus_id.append(products[aux_index])
            aux_index = aux_index + 1

        inventory_response = request_inventory_creation(zone, environment, account_id, delivery_center_id, skus_id)

        if not inventory_response:
            print_finish_application_menu()


def flow_input_inventory_to_product(zone, environment):
    account_id = print_account_id_menu(zone)

    if not account_id:
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)

    if not account:
        print_finish_application_menu()
    delivery_center_id = account[0]['deliveryCenterId']

    products = request_get_offers_microservice(account_id, zone, environment)
    if products == 'not_found':
        print(f'\n{text.Red}- [Catalog Service] There is no product associated with the account {account_id}')
        print_finish_application_menu()
    elif not products:
        print_finish_application_menu()

    sku_list = list()
    for i in range(len(products)):
        sku_list.append(products[i]['sku'])

    option = print_inventory_option_menu()
    if option == 'N':
        inventory = request_inventory_creation(zone, environment, account_id, delivery_center_id, sku_list)
    else:
        get_inventory_response = get_delivery_center_inventory(environment, zone, account_id, delivery_center_id, sku_list)
        if not get_inventory_response:
            print_finish_application_menu()
        else:
            inventory_information = print_inventory_sku_quantity_menu(zone, environment, sku_list)
            inventory = request_inventory_creation(zone, environment, account_id, delivery_center_id, sku_list, inventory_information
                                                   .get('sku'), inventory_information.get('quantity'))

    if inventory:
        print(f'\n{TEXT_GREEN}- The inventory has been added successfully for the account {account_id}')
    else:
        print_finish_application_menu()


def flow_input_sku_limit(zone, environment):
    account_id = print_account_id_menu(zone)

    if not account_id:
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)

    if not account:
        print_finish_application_menu()
    delivery_center_id = account[0]['deliveryCenterId']

    # Call function to display the SKUs on the screen
    enforcement = display_available_products(account_id, zone, environment, delivery_center_id)
    if enforcement:
            print(TEXT_GREEN + '\n- The SKU Limit has been added successfully for the account {account_id}'
                .format(account_id=account_id))
    elif enforcement == 'error_len':
            print(text.Red + '\n- There are no products available for the account {account_id}'
                .format(account_id=account_id))
            print_finish_application_menu()
    elif not enforcement:
            print_finish_application_menu()
    else:
            print_finish_application_menu()


def flow_input_recommended_products_to_account(zone, environment):
    account_id = print_account_id_menu(zone)
    if not account_id:
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if not account:
        print_finish_application_menu()

    product_offers = request_get_offers_microservice(account_id, zone, environment)
    if not product_offers:
        print_finish_application_menu()
    elif product_offers == 'not_found':
        print(text.Red + '\n- [Catalog Service] There is no product associated with the account {account_id}'
              .format(account_id=account_id))
        print_finish_application_menu()

    items = list()
    index = 0
    max_range = 10
    if len(product_offers) < max_range:
        max_range = len(product_offers)

    while index < max_range:
        sku = product_offers[index]['sku']
        items.append(sku)
        index = index + 1

    operation = print_recommender_type_menu()

    return {
        '1': lambda: flow_input_products_quick_order(zone, environment, account_id, items),
        '2': lambda: flow_input_products_up_sell(zone, environment, account_id, items),
        '3': lambda: flow_input_products_forgotten_items(zone, environment, account_id, items),
        '4': lambda: flow_input_all_recommendation_use_cases(zone, environment, account_id, items),
        '5': lambda: flow_input_combo_quick_order(zone, environment, account_id)
    }.get(operation, lambda: None)()


def flow_input_products_quick_order(zone, environment, account_id, items):
    if 'success' == request_quick_order(zone, environment, account_id, items):
        print(TEXT_GREEN + '\n- Quick order items added successfully')
    else:
        print_finish_application_menu()


def flow_input_products_up_sell(zone, environment, account_id, items):
    if 'success' == request_sell_up(zone, environment, account_id, items):
        print(TEXT_GREEN + '\n- Up sell items added successfully')
        print(text.Yellow + '- Up sell trigger: Add 3 of any products to the cart / Cart viewed with a product inside')
    else:
        print_finish_application_menu()


def flow_input_products_forgotten_items(zone, environment, account_id, items):
    if 'success' == request_forgotten_items(zone, environment, account_id, items):
        print(TEXT_GREEN + '\n- Forgotten items added successfully')
    else:
        print_finish_application_menu()


def flow_input_all_recommendation_use_cases(zone, environment, account_id, items):
    if 'success' == create_all_recommendations(zone, environment, account_id, items):
        print(TEXT_GREEN + '\n- All recommendation use cases were added (quick order, up sell and forgotten items)')
        print(text.Yellow + '- Up sell trigger: Add 3 of any products to the cart / Cart viewed with a product inside')
    else:
        print_finish_application_menu()


def flow_input_combo_quick_order(zone, environment, account_id):
    if 'success' == input_combos_quick_order(zone, environment, account_id):
        print(TEXT_GREEN + '\n- Combos for quick order added successfully')
    else:
        print_finish_application_menu()


def flow_input_empties_discounts(zone, environment):
    account_id = print_account_id_menu(zone)

    if not account_id:
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)

    if not account:
        print_finish_application_menu()

    switcher = {
        'CO': '000000000003500159',
        'MX': '000000000002000162',
        'EC': '000000000003500612',
        'PE': '000000000003500192'
    }

    empty_sku = switcher.get(zone, False)
    if not empty_sku:
        print(text.Red + f'\n- Empties discounts it not enabled for {zone}')
        print_finish_application_menu()

    while True:
        try:
            discount_value = int(input(text.default_text_color + 'Discount value: '))
            break
        except ValueError:
            print(text.Red + '\n- Invalid value')

    response = request_empties_discounts_creation(account_id, zone, environment, empty_sku, discount_value)
    if not response:
        print_finish_application_menu()
    else:
        print(TEXT_GREEN + '\n- Discount value for the empty SKU added successfully')


def account_menu():
    operation = print_account_operations_menu()
    if operation == '2':
        option = delivery_window_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    account_id = print_account_id_menu(zone)

    if not account_id:
        print_finish_application_menu()

    return {
        '1': lambda: flow_create_account(zone, environment, account_id),
        '2': lambda: flow_create_delivery_window(zone, environment, account_id, option),
        '3': lambda: flow_create_credit_information(zone, environment, account_id),
        '4': lambda: flow_update_account_name(zone, environment, account_id),
        '5': lambda: flow_update_account_status(zone, environment, account_id),
        '6': lambda: flow_update_account_minimum_order(zone, environment, account_id),
        '7': lambda: flow_update_account_payment_method(zone, environment, account_id)
    }.get(operation, lambda: None)()


def flow_create_account(zone, environment, account_id):
    name = print_account_name_menu()
    payment_method = print_payment_method_menu(zone)
    delivery_address = get_account_delivery_address(zone)
    account_status = print_account_status_menu()
    option_include_minimum_order = print_minimum_order_menu()

    if option_include_minimum_order == 'Y':
        minimum_order = get_minimum_order_info()
    else:
        minimum_order = None

    if zone == 'MX':
        enable_empties_loan = print_account_enable_empties_loan_menu()
    else:
        enable_empties_loan = False

    # Call create account function
    create_account_response = create_account_ms(account_id, name, payment_method, minimum_order, zone, environment,
                                                delivery_address, account_status, enable_empties_loan)

    if create_account_response:
        print(TEXT_GREEN + f'\n- Your account {account_id} has been created successfully')

        # Input default credit to the account so it won't be `null` in the Account Service database
        if False == add_credit_to_account_microservice(account_id, zone, environment, 0, 0):
            print_finish_application_menu()
    else:
        print_finish_application_menu()


def flow_create_delivery_window(zone, environment, account_id, option):
    allow_flexible_delivery_dates = ['BR', 'ZA', 'MX', 'DO', 'CO', 'PE', 'EC']
    allow_delivery_cost = ['BR', 'MX', 'DO', 'CO','PE', 'EC']

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if not account:
        print_finish_application_menu()
    account_data = account[0]

    is_alternative_delivery_date = False
    if zone in allow_flexible_delivery_dates:
        # Validate if is alternative delivery window
        is_alternative_delivery_date = print_alternative_delivery_date_menu()

        if is_alternative_delivery_date.upper() == 'Y':
            is_alternative_delivery_date = True
        else:
            is_alternative_delivery_date = False

    # Call add delivery window to account function
    delivery_window = create_delivery_window_microservice(zone, environment, account_data,
                                                              is_alternative_delivery_date, option)

    if delivery_window == 'success':
        print(TEXT_GREEN + '\n- Delivery window created successfully for the account {account_id}'
              .format(account_id=account_id))

        # Check if delivery cost (interest) should be included
        if is_alternative_delivery_date and zone in allow_delivery_cost:
            option_include_delivery_cost = print_include_delivery_cost_menu()
            if option_include_delivery_cost.upper() == 'Y':
                delivery_cost_values = get_delivery_cost_values(option_include_delivery_cost)
                delivery_cost = create_delivery_fee_microservice(zone, environment, account_data,
                                                                 delivery_cost_values)
                if delivery_cost == 'success':
                    print(TEXT_GREEN + '\n- Delivery cost (interest) added successfully for the account {account_id}'
                          .format(account_id=account_id))
            else:
                print_finish_application_menu()
    else:
        print_finish_application_menu()


def flow_create_credit_information(zone, environment, account_id):
    # Check if account exists
    account = check_account_exists_microservice(account_id, zone, environment)
    if not account:
        print_finish_application_menu()

    # Get credit information
    credit_info = get_credit_info()

    # Add credit to account
    credit = add_credit_to_account_microservice(account_id, zone, environment, credit_info.get('credit'),
                                                credit_info.get('balance'))
    if credit == 'success':
        print(TEXT_GREEN + f'\n- Credit added successfully for the account {account_id}')
    else:
        print_finish_application_menu()


def flow_update_account_name(zone, environment, account_id):
    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if not account:
        print_finish_application_menu()
    account_data = account[0]

    name = print_account_name_menu()

    minimum_order = get_minimum_order_list(account_data['minimumOrder'])

    create_account_response = create_account_ms(account_id, name, account_data['paymentMethods'],
                                                minimum_order, zone, environment,
                                                account_data['deliveryAddress'], account_data['status'],
                                                account_data['hasEmptiesLoan'])

    if create_account_response:
        print(TEXT_GREEN + '\n- Account name updated for the account {account_id}'
              .format(account_id=account_id))
    else:
        print_finish_application_menu()


def flow_update_account_status(zone, environment, account_id):
    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if not account:
        print_finish_application_menu()
    account_data = account[0]

    account_status = print_account_status_menu()

    minimum_order = get_minimum_order_list(account_data['minimumOrder'])

    create_account_response = create_account_ms(account_id, account_data['name'], account_data['paymentMethods'],
                                                minimum_order, zone, environment,
                                                account_data['deliveryAddress'], account_status,
                                                account_data['hasEmptiesLoan'])

    if create_account_response:
        print(TEXT_GREEN + '\n- Account status updated to {account_status} for the account {account_id}'
              .format(account_status=account_status, account_id=account_id))
    else:
        print_finish_application_menu()


def flow_update_account_minimum_order(zone, environment, account_id):
    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if not account:
        print_finish_application_menu()
    account_data = account[0]

    option_include_minimum_order = print_minimum_order_menu()

    if option_include_minimum_order == 'Y':
        minimum_order = get_minimum_order_info()
    else:
        minimum_order = None

    create_account_response = create_account_ms(account_id, account_data['name'], account_data['paymentMethods'],
                                                minimum_order, zone, environment,
                                                account_data['deliveryAddress'], account_data['status'],
                                                account_data['hasEmptiesLoan'])

    if create_account_response:
        print(TEXT_GREEN + '\n- Minimum order updated for the account {account_id}'
              .format(account_id=account_id))
    else:
        print_finish_application_menu()


def flow_update_account_payment_method(zone, environment, account_id):
    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if not account:
        print_finish_application_menu()
    account_data = account[0]

    payment_method = print_payment_method_menu(zone)

    minimum_order = get_minimum_order_list(account_data['minimumOrder'])

    create_account_response = create_account_ms(account_id, account_data['name'], payment_method,
                                                minimum_order, zone, environment,
                                                account_data['deliveryAddress'], account_data['status'],
                                                account_data['hasEmptiesLoan'])

    if create_account_response:
        print(TEXT_GREEN + '\n- Payment method updated for the account {account_id}'
              .format(account_id=account_id))
    else:
        print_finish_application_menu()


# Validate if chosen sku is valid
def validateSkuChosen(sku, listSkuOffers):
    countItems = 0
    while countItems < len(listSkuOffers):
        if listSkuOffers[countItems] == sku:
            return True

        countItems = countItems + 1

    return False


def registration_user_iam():
    """Flow to register user IAM
    Input Arguments:
        - Country
        - Environment
        - Email
        - Password
        - Account ID
        - Tax ID
    """
    country = print_zone_menu_for_ms()
    environment = print_environment_menu_in_user_create_iam()
    email = print_input_email()
    password = print_input_password()

    account_id = print_account_id_menu(country)

    if country == "BR":
        tax_id = account_id
    else:
        tax_id = print_input_tax_id()

    account_result = check_account_exists_microservice(account_id, country, environment)
    if not account_result:
        print_finish_application_menu()

    status_response = create_user(environment, country, email, password, account_id, tax_id)
    if status_response == "success":
        print(TEXT_GREEN + "\n- User IAM created successfully")
    else:
        print(text.Red + "\n- Something went wrong when creating a new user, please try again")
        print_finish_application_menu()


def delete_user_iam():
    """Flow to delete user IAM
    Input Arguments:
        - Country
        - Environment
        - Email
    """
    country = print_zone_menu_for_ms()
    environment = print_environment_menu_in_user_create_iam()
    email = print_input_email()

    status_response = delete_user_v3(environment, country, email)
    if status_response == "success":
        print(TEXT_GREEN + "\n- User IAM deleted successfully")
    elif status_response == "partial":
        print(text.Magenta + "\n- User IAM deleted partially")
    else:
        print(text.Red + "\n- Something went wrong when deleting an user, please try again")
        print_finish_application_menu()


def invoice_menu():
    operation = print_invoice_operations_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    account_id = print_account_id_menu(zone)

    if not account_id:
        print_finish_application_menu()

    account = check_account_exists_microservice(account_id, zone, environment)
    if not account:
        print_finish_application_menu()

    return {
        '1': lambda: flow_create_invoice(zone, environment, account_id),
        '2': lambda: flow_update_invoice_status(zone, environment, account_id),
        '3': lambda: flow_update_invoice_payment_method(zone, environment, account_id)
    }.get(operation, lambda: None)()


def flow_create_invoice(zone, environment, account_id):
    order_id = print_order_id_menu()

    response = check_if_order_exists(account_id, zone, environment, order_id)
    if not response or response == 'not_found':
        print_finish_application_menu()

    order_data = response[0]
    order_details = get_order_details(order_data)
    order_items = get_order_items(order_data, zone)
    invoice_status = print_invoice_status_menu()

    invoice_response = create_invoice_request(zone, environment, order_id, invoice_status, order_details, order_items)
    if invoice_response:
        print(TEXT_GREEN + f'\n- Invoice {invoice_response} created successfully')

        # Generate files for bank_slip and invoice (NF) only for Brazil
        if zone == 'BR':
            purposes = ['invoice', 'bank-slip']
            for i in range(len(purposes)):
                data = {'invoice_id': invoice_response}
                response = create_file_api(zone, environment, account_id, purposes[i], data)
                if not response:
                    print_finish_application_menu()
    else:
        print_finish_application_menu()


def flow_update_invoice_status(zone, environment, account_id):
    invoice_id = print_invoice_id_menu()
    response = check_if_invoice_exists(account_id, invoice_id, zone, environment)

    if not response:
        print_finish_application_menu()
    else:
        status = print_invoice_status_menu()
        invoice_response = update_invoice_request(zone, environment, account_id, invoice_id,
                                                  response['data'][0]['paymentType'], status)
        if not invoice_response:
            print_finish_application_menu()
        else:
            print(TEXT_GREEN + '\n- Invoice status updated to {invoice_status} for the invoice {invoice_id}'
                  .format(invoice_status=status, invoice_id=invoice_id))


def flow_update_invoice_payment_method(zone, environment, account_id):
    invoice_id = print_invoice_id_menu()
    response = check_if_invoice_exists(account_id, invoice_id, zone, environment)

    if not response:
        print_finish_application_menu()
    else:
        payment_method = print_invoice_payment_method_menu()
        invoice_response = update_invoice_request(zone, environment, account_id, invoice_id, payment_method,
                                                  response['data'][0]['status'])
        if not invoice_response:
            print_finish_application_menu()
        else:
            print(TEXT_GREEN + '\n- Invoice payment method updated to {payment_method} for the invoice {invoice_id}'
                  .format(payment_method=payment_method, invoice_id=invoice_id))

def token_generator_jwt():
    zone = print_zone_menu_for_ms()
    account_id = print_account_id_menu(zone)
    token_generator(jwt=True, account_id=account_id)

def token_generator_root():
    token_generator(root=True)

def token_generator_inclusion():
    token_generator(inclusion=True)

def token_generator_basic():
    token_generator()

def token_generator(jwt=False, root=False, inclusion=False, account_id=None):
    token = ""
    if jwt:
        # TODO This feature is temporarily disabled for security reasons.
        # token = generate_hmac_jwt(account_id)
        pass
    elif root:
        token = "Basic cm9vdDpyb290"
    elif inclusion:
        token = "Basic cmVsYXk6TVVRd3JENVplSEtB"
    else:
        token = "Basic cmVsYXk6cmVsYXk="

    
    print(text.Yellow + f'\n- Token generated: {token}')
    print(TEXT_GREEN + '\n- The token is on your clipboard.')    
    pyperclip.copy(token)


def get_categories_menu():
    """Get categories
    Input Arguments:
        - Country (BR, DO, AR, CL, ZA, CO)
        - Environment (UAT, SIT)
        - Parent id (default: 0)
    """
    country = print_zone_menu_for_ms()
    environment = print_environment_menu_user_creation()
    parent_id = print_input_number_with_default('Parent id')

    # Get categories
    categories = get_categories(country, environment, parent_id)
    if not categories:
        print_finish_application_menu()

    if categories:
        print("Categories: [id, name]")
        for category in categories:
            print("- {id}, {name}".format(id=category['id'], name=category['name']))
    else:
        print("\n{text_red}{not_found}".format(text_red=text.Red, not_found="Categories not found"))
        print_finish_application_menu()


def associate_product_to_category_menu():
    """Associate product to category
    Input Arguments:
        - Country (BR, DO, AR, ZA, CO)
        - Environment (UAT, SIT)
        - Product SKU
        - Category ID
    """
    country = print_zone_menu_for_ms()
    environment = print_environment_menu_user_creation()
    product_sku = print_input_text('Product SKU')
    category_id = print_input_number('Category ID')

    # Enable product
    enable_product_response = request_enable_product(country, environment, product_sku)
    if not enable_product_response:
        print("\n{text_red}{fail}".format(text_red=text.Red, fail="Fail to enable product"))
        print_finish_application_menu()
    else:
        # Associate product to category
        response_associate_product_to_category = associate_product_to_category(country, environment, product_sku,
                                                                               category_id)
        if not response_associate_product_to_category:
            print("\n{text_red}- {fail}".format(text_red=text.Red, fail="Fail to associate product to category"))
            print_finish_application_menu()

    print("\n{text_green}{success}".format(text_green=TEXT_GREEN,
                                         success="Success to enable and to associate product to category"))


def create_categories_menu():
    """Create categories
    Input Arguments:
        - Country (BR, DO, AR, ZA, CO)
        - Environment (UAT, SIT)
        - Category name
        - Parent id (default: 0)
    """
    country = print_zone_menu_for_ms()
    environment = print_environment_menu_user_creation()
    category_name = print_input_text('Category name')
    parent_id = print_input_number_with_default('Parent id')

    # Get categories
    categories = get_categories(country, environment, parent_id)
    if not categories:
        print_finish_application_menu()

    category = [category for category in categories if category['name'] == category_name]

    if category:
        category = category[0]
        print(f"{TEXT_GREEN}Category already exists")
    else:
        # Create category
        response = create_category(
            country=country,
            environment=environment,
            category_name=category_name,
            parent_id=parent_id
        )

        category = loads(response.text)

        if response.status_code == 200:
            print(f"{TEXT_GREEN}Success in creating category.")
        else:
            print(f"{text.Red}Fail to create category: \n")
            print(f"Status Code: {response.status_code} \n")
            print(f"Response: {category}")

            print_finish_application_menu()

    print(f"Id: {category['id']}")
    print(f"Name: {category['name']}")


def order_information_menu():
    selection_structure = print_get_order_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    abi_id = print_account_id_menu(zone)
    if not abi_id:
        print_finish_application_menu()

    account = check_account_exists_microservice(abi_id, zone, environment)
    if not account:
        print_finish_application_menu()

    if selection_structure == '1':
        order_id = print_order_id_menu()
        orders = check_if_order_exists(abi_id, zone, environment, order_id)
        if not orders or orders == 'not_found':
            print_finish_application_menu()

        display_specific_order_information(orders)
    else:
        orders = check_if_order_exists(abi_id, zone, environment, '')
        if not orders or orders == 'not_found':
            print_finish_application_menu()

        display_all_order_information(orders)


def recommender_information_menu():
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    account_id = print_account_id_menu(zone)
    if not account_id:
        print_finish_application_menu()

    case_id = 'QUICK_ORDER&useCase=FORGOTTEN_ITEMS&useCase=CROSS_SELL_UP_SELL'
    data = get_recommendation_by_account(account_id, zone, environment, case_id)
    if not data or data == 'not_found':
        print_finish_application_menu()

    display_recommendations_by_account(data)


def retrieve_available_invoices_menu():
    status = print_invoice_status_menu_retriever()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    abi_id = print_account_id_menu(zone)
    if not abi_id:
        print_finish_application_menu()
    account = check_account_exists_microservice(abi_id, zone, environment)
    if not account:
        print_finish_application_menu()
    invoice_info = get_invoices(zone, abi_id, environment)
    if not invoice_info:
        print_finish_application_menu()
    print_invoices(invoice_info, status)


def retriever_sku_menu():
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    account_id = print_account_id_menu(zone)
    if not account_id:
        print_finish_application_menu()

    account = check_account_exists_microservice(account_id, zone, environment)
    
    if account:
        display_program_rules_skus(zone, environment, account_id)
        
    print_finish_application_menu()


def create_credit_statement_menu():
    zone = print_zone_credit_statement()
    environment = print_environment_menu()
    account_id = print_account_id_menu(zone)
    if not account_id:
        print_finish_application_menu()

    account = check_account_exists_microservice(account_id, zone, environment)
    if not account:
        print_finish_application_menu()

    data = {
        'month': print_month_credit_statement(),
        'year': print_year_credit_statement()
    }

    response = create_file_api(zone, environment, account_id, 'credit-statement', data)
    if response == 'success':
        print(TEXT_GREEN + f'\n- Credit Statement created for the account {account_id}')
    else:
        print_finish_application_menu()


def create_attribute_menu():

    selection_structure = print_create_attribute_menu()

    switcher = {
        '1': 'PRIMITIVE',
        '2': 'ENUM',
        '3': 'GROUP'
    }

    supplier_option = switcher.get(selection_structure, False)

    # Option to create a new program
    if supplier_option == 'PRIMITIVE':

        type_att = print_attribute_primitive(is_enum=False)
        environment = print_environment_menu_supplier()

        switcher_type = {
            '1': 'NUMERIC',
            '2': 'TEXT',
            '3': 'DATE',
            '4': 'BOOLEAN'
        }

        type_option = switcher_type.get(type_att, False)

        create_att = create_attribute_primitive_type(environment, type_option)

        if create_att:
            print(TEXT_GREEN + '\n- [Attribute] The new {attribute_type} has been successfully created. '
                              'ID: {attribute}'.format(attribute_type=str(type_option),
                                                       attribute=create_att))
            print_finish_application_menu()
        else:
            print_finish_application_menu()
    elif supplier_option == 'ENUM':
        type_att = print_attribute_primitive(is_enum=True)
        environment = print_environment_menu_supplier()

        switcher_type = {
            '1': 'NUMERIC',
            '2': 'TEXT',
            '3': 'DATE'
        }

        type_option = switcher_type.get(type_att, False)
        create_enum = create_attribute_enum(environment, type_option)

        if create_enum:
            print(TEXT_GREEN + '\n- [Attribute] The new {attribute_type} has been successfully created. '
                               'ID: {attribute}'.format(attribute_type=str(type_option),
                                                        attribute=create_enum))
            print_finish_application_menu()
        else:
            print_finish_application_menu()
    elif supplier_option == 'GROUP':
        environment = print_environment_menu_supplier()
        list_att = insert_sub_attribute_group(environment)

        create_group = create_attribute_group(environment, list_att)

        if create_group:
            print(TEXT_GREEN + '\n- [Attribute] The new {attribute_type} has been successfully created. '
                               'ID: {attribute}'.format(attribute_type=str(supplier_option),
                                                        attribute=create_group))
            print_finish_application_menu()
        else:
            print_finish_application_menu()


def insert_sub_attribute_group(environment):
    list_att = list()
    sub_att1 = input(text.default_text_color + 'Inform the first attribute in the group: ')
    valid_att = check_if_attribute_exist(environment, sub_att1)
    if not valid_att:
        print_finish_application_menu()
    else:
        list_att.append(sub_att1)
    sub_att2 = input(text.default_text_color + 'Inform the second attribute in the group: ')
    valid_att2 = check_if_attribute_exist(environment, sub_att2)
    if not valid_att2:
        print_finish_application_menu()
    else:
        list_att.append(sub_att2)
    new_att = print_new_attribute()
    while new_att == '1':
        sub_att = input(text.default_text_color + 'Inform the another attribute in the group: ')
        valid_att = check_if_attribute_exist(environment, sub_att)
        if not valid_att2:
            new_att == '2'
            print_finish_application_menu()
        else:
            list_att.append(sub_att)
            new_att = print_new_attribute()
    return list_att


def create_category_supplier_menu():
    selection_structure = print_create_supplier_category_menu()

    switcher = {
        '1': 'ROOT',
        '2': 'SUB',
        '3': 'LEGACY'
    }

    supplier_option = switcher.get(selection_structure, False)

    # Option to create a new program
    if supplier_option == 'ROOT':
        environment = print_environment_menu_supplier()
        create_category = create_root_category(environment)

        if create_category:
            print(TEXT_GREEN + '\n- [Category] The new root category has been successfully created. '
                               'ID: {category}'.format(category=create_category))
            print_finish_application_menu()
        else:
            print_finish_application_menu()
    elif supplier_option == 'SUB':
        environment = print_environment_menu_supplier()

        parent_id = input(text.default_text_color + '\nInform the parent category: ')
        check_cat = check_if_supplier_category_exist(environment, parent_id)
        if check_cat:
            create_sub_category = create_sub_category_supplier(environment, parent_id)
        else:
            print_finish_application_menu()

        if create_sub_category:
            print(TEXT_GREEN + '\n- [Category] The new subCategory has been successfully created. '
                               'ID: {category}'.format(category=create_sub_category))
            print_finish_application_menu()
        else:
            print_finish_application_menu()
    else:
        environment = print_environment_menu_supplier()
        category_name = input(text.default_text_color +
                                    'Which name do you want input in this category (Default: Legacy Category): ')
        if category_name == '':
            category_name = 'Legacy Category'
        legacy_category = create_legacy_category(environment, category_name)

        if legacy_category:
            print(TEXT_GREEN + '\n- [Category] The new legacy category has been successfully created. '
                               'ID: {category}'.format(category=legacy_category))
            print_finish_application_menu()
        else:
            print_finish_application_menu()


def attribute_associated_category_menu():
    environment = print_environment_menu_supplier()
    attribute_id = input(text.default_text_color + 'Inform the attribute id: ')
    valid_att = check_if_attribute_exist(environment, attribute_id)
    if not valid_att:
        print_finish_application_menu()
    else:
        category_id = input(text.default_text_color + 'Inform the category id: ')
        check_cat = check_if_supplier_category_exist(environment, category_id)
        if check_cat:
            min_cardinality = print_min_cardinality()
            max_cardinality = print_max_cardinality()
            association = create_association_attribute_with_category(environment, attribute_id, category_id, min_cardinality, max_cardinality)
            if association:
                print(TEXT_GREEN + '\n- [Association] The new association between attribute and categoty has been successfully created. '
                                   'ID: {association}'.format(association=association))
                print_finish_application_menu()
            else:
                print_finish_application_menu()
        else:
            print_finish_application_menu()


def delete_attribute_menu():
    environment = print_environment_menu_supplier()
    attribute_id = input(text.default_text_color + 'Inform the attribute id: ')
    valid_att = check_if_attribute_exist(environment, attribute_id)
    if not valid_att:
        print_finish_application_menu()
    else:
        delete = delete_attribute_supplier(environment, attribute_id)
        if delete:
            print(
                TEXT_GREEN + '\n- [Delete Attribute] The attribute: {attribute} has been successfully deleted. '
                .format(attribute=delete))
            print_finish_application_menu()
        else:
            print_finish_application_menu()


def search_specific_attribute_menu():
    environment = print_environment_menu_supplier()
    attribute_id = input(text.default_text_color + 'Inform the attribute id: ')
    result = search_specific_attribute(environment, attribute_id)
    if not result:
        print_finish_application_menu()
    else:
        display_specific_attribute(result)


def search_all_attribute_menu():
    environment = print_environment_menu_supplier()
    page_number = input(text.default_text_color + 'Wich page do you want: ')
    result = search_all_attribute(environment, page_number)
    if not result:
        print_finish_application_menu()
    else:
        display_all_attribute(result)
        is_new_page = print_new_page()
        while is_new_page == '1':
            page_number = int(input(text.default_text_color + 'Wich page do you want: '))
            result = search_all_attribute(environment, page_number)
            display_all_attribute(result)
            is_new_page = print_new_page()
            if is_new_page == '2':
                print_finish_application_menu()


def search_specific_category_menu():
    environment = print_environment_menu_supplier()
    category_id = input(text.default_text_color + 'Inform the category id: ')
    result = search_specific_category(environment, category_id)
    if not result:
        print_finish_application_menu()
    else:
        display_specific_category(result)


def search_all_category_menu():
    environment = print_environment_menu_supplier()
    page_number = input(text.default_text_color + 'Wich page do you want: ')
    result = search_all_category(environment, page_number)
    if not result:
        print_finish_application_menu()
    else:
        display_all_category(result)
        is_new_page = print_new_page()
        while is_new_page == '1':
            page_number = input(text.default_text_color + 'Wich page do you want: ')
            result = search_all_category(environment, page_number)
            display_all_category(result)
            is_new_page = print_new_page()
            if is_new_page == '2':
                print_finish_application_menu()


def edit_attribute_type_menu():
    environment = print_environment_menu_supplier()
    attribute_id = input(text.default_text_color + 'Inform the attribute id: ')
    valid_att = check_if_attribute_exist(environment, attribute_id)
    if not valid_att:
        print_finish_application_menu()
    else:
        attribute_type = print_attribute_type()

        if attribute_type == '3':
            values = insert_sub_attribute_group(environment)
        else:
            values = None

    result = edit_attribute_type(environment, attribute_id, attribute_type, values)
    if result:
        print(
            TEXT_GREEN + '\n- [Edit Attribute] The attribute: {attribute} has been successfully edit to the new type. '
            .format(attribute=attribute_id))
        print_finish_application_menu()
    else:
        print_finish_application_menu()


def create_product_menu():
    category_id = input(text.default_text_color + 'Category ID the product will be linked with: ')
    country = print_zone_menu_for_ms()
    environment = print_environment_menu_supplier()

    product = create_product_supplier(environment, category_id, country)
    if product:
        print(
            TEXT_GREEN + '\n- [Product] The new product has been successfully created. '
                         'ID: {product}'.format(product=product))
        print_finish_application_menu()
    else:
        print_finish_application_menu()


if __name__ == '__main__':
    try:
        show_menu()

    except (KeyboardInterrupt, EOFError):
        sys.exit(0)
