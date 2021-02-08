from account import *
from attribute_supplier import create_attribute_enum, check_if_attribute_exist, create_attribute_group, \
    create_attribute_primitive_type
from common import *
from credit import add_credit_to_account_microservice
from deals import *
from delivery_window import *
from algo_selling import *
from files import create_file_api
from inventory import *
from invoice import *
from menus.account_menu import print_account_operations_menu, print_minimum_order_menu, print_account_status_menu, \
    print_account_name_menu, print_account_enable_empties_loan_menu, print_alternative_delivery_date_menu, \
    print_include_delivery_cost_menu, print_payment_method_menu, print_account_id_menu, \
    print_get_account_operations_menu, delivery_window_menu
from menus.algo_selling_menu import print_recommender_type_menu
from menus.deals_menu import print_deals_operations_menu, print_discount_percentage_menu, print_minimum_quantity_menu, \
    print_max_quantity_menu, print_option_sku_menu, print_partial_free_good_menu, \
    print_free_good_redemption_menu, print_free_good_quantity_menu, print_interactive_combos_quantity_range_menu, \
    print_interactive_combos_quantity_range_menu_v2, print_stepped_free_good_ranges_menu, \
    print_stepped_discount_ranges_menu, print_discount_range_menu
from menus.invoice_menu import print_invoice_operations_menu, print_invoice_status_menu, print_invoice_id_menu, \
    print_invoice_payment_method_menu, print_invoice_status_menu_retriever
from menus.order_menu import print_order_operations_menu, print_allow_cancellable_order_menu, print_get_order_menu, \
    print_order_id_menu, print_order_status_menu
from menus.product_menu import print_product_operations_menu, print_get_products_menu
from order import *
from combos import *
from products import *
from rewards import *
from category_magento import *
from products_magento import *
import user_creation_v3 as user_v3
import user_delete_v3 as user_delete_v3
from simulation import process_simulation_microservice, request_order_simulation
from validations import validate_yes_no_option, validate_state, is_number


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
            '1': get_categories_menu,
            '2': associate_product_to_category_menu,
            '3': create_categories_menu
        }
    elif selection_structure == '4':
        switcher = {
            '0': finish_application,
            '1': registration_user_iam,
            '2': delete_user_iam
        }
    elif selection_structure == '5':
        switcher = {
            '0': finish_application,
            '1': create_attribute_menu,
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
    if abi_id == 'false':
        print_finish_application_menu()

    account = check_account_exists_microservice(abi_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()

    deals = request_get_deals_promo_fusion_service(zone, environment, abi_id)
    if deals != 'false':
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

    products_type = switcher.get(selection_structure, 'false')

    if products_type == 'PRODUCT':
        zone = print_zone_menu_for_ms()
        abi_id = print_account_id_menu(zone)
        if abi_id == 'false':
            print_finish_application_menu()
        account = check_account_exists_microservice(abi_id, zone, environment)
        if account == 'false':
            print_finish_application_menu()

        product_offers = request_get_products_by_account_microservice(abi_id, zone, environment)
        if product_offers == 'false':
            print_finish_application_menu()
        elif product_offers == 'not_found':
            print(text.Red + '\n- [Catalog Service] There is no product associated with the account ' + abi_id)
            print_finish_application_menu()

        display_product_information(product_offers)

    elif products_type == 'INVENTORY':
        zone = print_zone_menu_for_ms()
        abi_id = print_account_id_menu(zone)
        if abi_id == 'false':
            print_finish_application_menu()

        account = check_account_exists_microservice(abi_id, zone, environment)
        if account == 'false':
            print_finish_application_menu()

        delivery_center_id = account[0]['deliveryCenterId']
        display_inventory_by_account(zone, environment, abi_id, delivery_center_id)

    else:
        zone = print_zone_menu_for_ms()

        products = request_get_products_microservice(zone, environment)
        if products == 'false':
            print_finish_application_menu()

        display_items_information_zone(products)


def account_information_menu():
    operation = print_get_account_operations_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()

    return {
        '1': lambda: flow_get_account(zone, environment)
    }.get(operation, lambda: None)()


def flow_get_account(zone, environment):
    account_id = print_account_id_menu(zone)
    if account_id == 'false':
        print_finish_application_menu()

    account = check_account_exists_microservice(account_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()

    display_account_information(account)


# Input Rewards to account
def create_rewards_to_account():
    selection_structure = print_rewards_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()

    switcher = {
        '1': 'NEW_PROGRAM',
        '2': 'UPDATE_BALANCE',
        '3': 'UPDATE_COMBOS',
        '4': 'ENROLL_POC',
        '5': 'ADD_CHALLENGE',
        '6': 'ADD_REDEEM',
        '7': 'DELETE_ENROLL_POC',
        '8': 'ADD_TRANSACTIONS',
    }

    reward_option = switcher.get(selection_structure, 'false')

    # Option to create a new program
    if reward_option == 'NEW_PROGRAM':

        create_pgm = create_new_program(zone, environment)

        if create_pgm == 'error_len_sku':
            print(text.Red + '\n- [Rewards] The zone must have at least 20 products to proceed')
            print_finish_application_menu()
        elif create_pgm == 'error_len_combo':
            print(text.Red + '\n- [Rewards] The zone must have combos available to proceed')
            print_finish_application_menu()
        elif create_pgm == 'error_found' or create_pgm == 'false':
            print_finish_application_menu()
        else:
            print(text.Green + '\n- [Rewards] The new program has been successfully created. ID: ' + create_pgm)
            print_finish_application_menu()

    # Option to enroll POC to a program
    elif reward_option == 'ENROLL_POC':

        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account == 'false':
            print_finish_application_menu()

        enroll_poc = enroll_poc_to_program(abi_id, zone, environment)

        if enroll_poc == 'pgm_not_found':
            print(
                text.Red + '\n- [Rewards] This zone does not have a program created. Please use the menu option "Create new program" to create it')
        elif enroll_poc == 406:
            print(text.Red + '\n- [Rewards] There are no Reward programs available for this account')
        elif enroll_poc == 409:
            print(text.Red + '\n- [Rewards] This account already have a Reward program enrolled to it')
        elif enroll_poc == 201:
            print(text.Green + '\n- [Rewards] The account has been successfully enrolled to a rewards program')

        print_finish_application_menu()

    # Option to input challenges to a specific zone
    elif reward_option == 'ADD_CHALLENGE':

        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account == 'false':
            print_finish_application_menu()

        add_challenge = input_challenge_to_zone(abi_id, zone, environment)

        if add_challenge == 'false':
            print(text.Red + '\n- [Rewards] Something went wrong, please try again')

        print_finish_application_menu()

    # Option to update initial balance of a program
    elif reward_option == 'UPDATE_BALANCE':

        update_balance = update_program_balance(zone, environment)

        if update_balance == 'no_confirm' or update_balance == 'error':
            print_finish_application_menu()
        elif update_balance == 'no_program':
            print(text.Red + '\n- [Rewards] There is no rewards program available for this zone')
        else:
            print(text.Green + '\n- [Rewards] The program ' + update_balance + ' has been successfully updated.')

        print_finish_application_menu()

    # Option to input redeem products to an account
    elif reward_option == 'ADD_REDEEM':

        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account != 'false':
            input_redeem_products(abi_id, zone, environment)
            print_finish_application_menu()
        else:
            print_finish_application_menu()

    # Option to delete a POC enrollment
    elif reward_option == 'DELETE_ENROLL_POC':

        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account == 'false':
            print_finish_application_menu()
       
        delete_enroll_poc = delete_enroll_poc_to_program(abi_id, zone, environment)

        if delete_enroll_poc == 'pgm_not_found':
            print(text.Red + '\n- [Rewards] This zone does not have a program created. Please use the menu option "Create new program" to create it')
        elif delete_enroll_poc == 204:
            print(text.Green + '\n- [Rewards] The enrollment has been deleted for this account from the rewards program')

        print_finish_application_menu()
    
     # Option to ADD a Transaction to a POC
    elif reward_option == 'ADD_TRANSACTIONS':
        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account == 'false':
            print_finish_application_menu()

        input_transactions = input_transactions_to_account(abi_id, zone, environment)

        if input_transactions == 'pgm_not_found':
            print(text.Red + '\n- [Rewards] This zone does not have a program created. Please use the menu option "Create new program" to create it')
        elif input_transactions == 'post_error':
            print(text.Red + '\n- [Rewards] Failure when input a transaction to account')
        elif input_transactions == 201:
            print(text.Green + '\n- [Rewards] The transactions has been included for this account from the rewards program')

        print_finish_application_menu()

    elif reward_option == 'UPDATE_COMBOS':
        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)
        if account == 'false':
            print_finish_application_menu()

        update_dt_combos = update_dt_combos_rewards(zone, environment, abi_id)

        if update_dt_combos == 201:
            print(text.Green + '\n- [Rewards] The program has been successfully updated.')
        elif update_dt_combos == 'no_program':
            print(text.Red + '\n-Error: POC not enrolled at a program')
        elif update_dt_combos == 'none':
            print("\nThere is nothing to update, please insert a DT combo first")
        else:
            print(text.Red + '\n-Error: ' + str(update_dt_combos))

        print_finish_application_menu()


def order_menu():
    operation = print_order_operations_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    account_id = print_account_id_menu(zone)

    if account_id == 'false':
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()
    delivery_center_id = account[0]['deliveryCenterId']

    # Call function to check if the account has products inside
    product_offers = request_get_offers_microservice(account_id, zone, environment)
    if product_offers == 'false':
        print_finish_application_menu()
    elif product_offers == 'not_found':
        print(text.Red + '\n- There is no product associated with the account {account_id}'
              .format(account_id=account_id))
        print_finish_application_menu()

    if operation != '2':
        order_status = print_order_status_menu()

        quantity = int(input(text.default_text_color + 'Quantity of products you want to include in this order: '))
        while is_number(quantity) == 'false':
            quantity = int(input(text.default_text_color + 'Quantity of products you want to include in this order: '))

        item_list = list()
        while len(item_list) < quantity:
            index_offers = randint(0, (len(product_offers) - 1))
            sku = product_offers[index_offers]['sku']
            data = {'sku': sku, 'itemQuantity': randint(0, 10)}
            item_list.append(data)

    return {
        '1': lambda: flow_create_order(zone, environment, account_id, delivery_center_id, order_status, item_list),
        '2': lambda: flow_create_changed_order(zone, environment, account_id),
    }.get(operation, lambda: None)()


def flow_create_order(zone, environment, account_id, delivery_center_id, order_status, item_list):
    if order_status == 'PLACED':
        allow_order_cancel = print_allow_cancellable_order_menu()
    else:
        allow_order_cancel = 'N'

    # Call function to configure prefix and order number size in the database sequence
    if 'false' == configure_order_params(zone, environment, account_id, 8, 'DM-{zone}-'.format(zone=zone)):
        print_finish_application_menu()

    order_items = request_order_simulation(zone, environment, account_id, delivery_center_id, item_list, None, None,
                                           'CASH', 0)
    if order_items == 'false':
        print_finish_application_menu()

    response = request_order_creation(account_id, delivery_center_id, zone, environment, allow_order_cancel,
                                      order_items, order_status)
    if response != 'false':
        print(text.Green + '\n- Order ' + response.get('orderNumber') + ' created successfully')
        # Call function to re-configure prefix and order number size according to the zone's format
        order_prefix_params = get_order_prefix_params(zone)
        if 'false' == configure_order_params(zone, environment, account_id, order_prefix_params.get('order_number_size'),
                                             order_prefix_params.get('prefix')):
            print_finish_application_menu()


def flow_create_changed_order(zone, environment, account_id):
    order_id = print_order_id_menu()
    order_data = check_if_order_exists(account_id, zone, environment, order_id)
    if order_data == 'false':
        print_finish_application_menu()
    elif order_data == 'empty':
        print(text.Red + '\n- The account {account_id} does not have orders'.format(account_id=account_id))
        print_finish_application_menu()
    elif order_data == 'not_found':
        print(text.Red + '\n- The order {order_id} does not exist'.format(order_id=order_id))
        print_finish_application_menu()

    statuses = ['DENIED', 'CANCELLED', 'DELIVERED', 'PARTIAL_DELIVERY', 'PENDING_CANCELLATION', 'INVOICED',
                'IN_TRANSIT']

    if order_data[0]['status'] in statuses:
        print(text.Red + '\n- This order cannot be changed. Order status: {order_status}'
              .format(order_status=order_data[0]['status']))
        print_finish_application_menu()

    if len(order_data[0]['items']) == 1 and order_data[0]['items'][0]['quantity'] == 1:
        print(text.Red + '\n- It\'s not possible to change this order because it has only one product with '
                         'quantity equals 1')
        print_finish_application_menu()

    response = request_changed_order_creation(zone, environment, order_data)
    if response == 'success':
        print(text.Green + '\n- The order {order_id} was changed successfully'.format(order_id=order_id))
    else:
        print_finish_application_menu()


# Place request for simulation service in microservice
def check_simulation_service_account_microservice_menu():
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone, environment)

    if account == 'false':
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
            while is_number(quantity) == "false":
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
            while is_number(quantity) == "false":
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
            while is_number(quantity) == "false":
                print(text.Red + "\n- Invalid quantity\n")
                quantity = input(text.default_text_color + "Inform combo sku quantity for simulation: ")

            temp_empties_data = {"groupId": sku, "quantity": quantity}
            empties_skus.append(temp_empties_data)
            more_empties = input(text.default_text_color + "Would you like to include more skus for simulation? (y/N) ")

    # Payment Method menu
    payment_method = print_payment_method_simulation_menu(zone)
    if payment_method.upper() == "BANK_SLIP":
        payment_term = input(text.default_text_color + "Enter the number of days the bill will expire: ")
        while is_number(payment_term) == "false":
            print(text.Red + "\n- Invalid number\n")
            payment_term = input(text.default_text_color + "Enter the number of days the bill will expire: ")
    else:
        payment_term = 0

    cart_response = request_order_simulation(zone, environment, abi_id, account[0]['deliveryCenterId'], order_items,
                                             order_combos, empties_skus, payment_method, payment_term)
    if cart_response != 'false':
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

    if account_id == 'false':
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()

    option_sku = print_option_sku_menu()

    # Request POC's associated products
    product_offers = request_get_offers_microservice(account_id, zone, environment)
    if product_offers == 'false':
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
        '1': lambda: flow_create_discount(zone, environment, account_id, sku, operation),
        '2': lambda: flow_create_stepped_discount(zone, environment, account_id, sku, operation),
        '3': lambda: flow_create_stepped_discount_with_limit(zone, environment, account_id, sku, operation),
        '4': lambda: flow_create_free_good(zone, environment, account_id, sku_list, operation),
        '5': lambda: flow_create_stepped_free_good(zone, environment, account_id, sku, operation),
        '6': lambda: flow_create_interactive_combos(zone, environment, account_id, sku_list, operation),
        '7': lambda: flow_create_interactive_combos_v2(zone, environment, account_id, sku_list, operation)
    }.get(operation, lambda: None)()


def flow_create_discount(zone, environment, account_id, sku, operation):
    minimum_quantity = print_minimum_quantity_menu()
    discount_value = print_discount_percentage_menu()

    response = create_discount(account_id, sku, zone, environment, discount_value, minimum_quantity, operation)
    if response != 'false':
        print(text.Green + '\n- Deal {deal_id} created successfully'.format(deal_id=response))
    else:
        print_finish_application_menu()


def flow_create_stepped_discount(zone, environment, account_id, sku, operation):
    ranges = print_stepped_discount_ranges_menu()

    response = create_stepped_discount(account_id, sku, zone, environment, ranges, operation)
    if response != 'false':
        print(text.Green + '\n- Deal {deal_id} created successfully'.format(deal_id=response))
    else:
        print_finish_application_menu()


def flow_create_stepped_discount_with_limit(zone, environment, account_id, sku, operation):
    # Default index range (from 1 to 9999 products)
    default_index_range = [1, 9999]

    discount_range = print_discount_range_menu(1)
    max_quantity = print_max_quantity_menu(default_index_range)

    response = create_stepped_discount_with_limit(account_id, sku, zone, environment, default_index_range,
                                                  discount_range, max_quantity, operation)
    if response != 'false':
        print(text.Green + '\n- Deal {deal_id} created successfully'.format(deal_id=response))
    else:
        print_finish_application_menu()


def flow_create_free_good(zone, environment, account_id, sku_list, operation):
    partial_free_good = print_partial_free_good_menu(zone)
    need_to_buy_product = print_free_good_redemption_menu(partial_free_good)

    if need_to_buy_product == 'Y':
        minimum_quantity = print_minimum_quantity_menu()
        quantity = print_free_good_quantity_menu()
    else:
        minimum_quantity = 1
        quantity = print_free_good_quantity_menu()

    response = create_free_good(account_id, sku_list, zone, environment, minimum_quantity, quantity,
                                partial_free_good, need_to_buy_product, operation)
    if response != 'false':
        print(text.Green + '\n- Deal {deal_id} created successfully'.format(deal_id=response))
    else:
        print_finish_application_menu()


def flow_create_stepped_free_good(zone, environment, account_id, sku, operation):
    ranges = print_stepped_free_good_ranges_menu()

    response = create_stepped_free_good(account_id, sku, zone, environment, ranges, operation)
    if response != 'false':
        print(text.Green + '\n- Deal {deal_id} created successfully'.format(deal_id=response))
    else:
        print_finish_application_menu()


# Interactive combos v1
def flow_create_interactive_combos(zone, environment, account_id, sku, operation):
    index_range = print_interactive_combos_quantity_range_menu()

    response = create_interactive_combos(account_id, sku, zone, environment, index_range, operation)

    if response != 'false':
        print(text.Green + '\n- Deal {deal_id} created successfully'.format(deal_id=response))
    else:
        print_finish_application_menu()


# Interactive combos v2
def flow_create_interactive_combos_v2(zone, environment, account_id, sku, operation):
    index_range = print_interactive_combos_quantity_range_menu_v2()

    response = create_interactive_combos_v2(account_id, sku, zone, environment, index_range, operation)

    if response != 'false':
        print(text.Green + '\n- Deal {deal_id} created successfully'.format(deal_id=response))
    else:
        print_finish_application_menu()


# Input combos to an account
def input_combos_menu():
    selection_structure = print_combos_menu()

    if selection_structure == '3':
        zone = print_zone_menu_for_ms()
    else:
        zone = print_zone_menu_for_combos()

    environment = print_environment_menu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone, environment)

    if account == 'false':
        print_finish_application_menu()

    product_offers = request_get_offers_microservice(abi_id, zone, environment)
    if product_offers == 'false':
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
        response = input_combo_free_good_only(abi_id, zone, environment, sku)

    # Reset combo consumption to zero
    else:
        combo_id = print_combo_id_menu()
        combo = check_combo_exists_microservice(abi_id, zone, environment, combo_id)
        update_combo = update_combo_consumption(abi_id, zone, environment, combo_id)

        if combo != 'false' and update_combo != 'false':
            print(text.Green + '\n- Combo consumption for ' + combo_id + ' was successfully updated')

    if selection_structure != '5' and response != 'false':
        print(text.Green + '\n- Combo ' + response + ' successfully registered')

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
        '5': lambda: flow_input_empties_discounts(zone, environment)
    }.get(operation, lambda: None)()


def flow_create_product(zone, environment):
    item_data = get_item_input_data()

    response = create_product(zone, environment, item_data)
    if response == 'false':
        print_finish_application_menu()
    else:
        print(text.Green + '\n- The product {sku} - {product_name} was created successfully'
              .format(sku=response.get('sku'), product_name=response.get('name')))


def flow_associate_products_to_account(zone, environment):
    account_id = print_account_id_menu(zone)

    if account_id == 'false':
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)

    if account == 'false':
        print_finish_application_menu()
    delivery_center_id = account[0]['deliveryCenterId']

    proceed = 'N'
    products = request_get_offers_microservice(account_id, zone, environment)
    if products == 'false':
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
        if all_products_zone == 'false':
            print_finish_application_menu()

        # Call add products to account function
        add_products = add_products_to_account_microservice(account_id, zone, environment, delivery_center_id,
                                                            all_products_zone)
        if add_products != 'success':
            print(text.Red + '\n- [Products] Something went wrong, please try again')
            print_finish_application_menu()

        products = request_get_account_product_assortment(account_id, zone, environment, delivery_center_id)
        if products == 'false':
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

        inventory_response = update_sku_inventory_microservice(zone, environment, delivery_center_id, skus_id)

        if inventory_response == 'false':
            print_finish_application_menu()


def flow_input_inventory_to_product(zone, environment):
    account_id = print_account_id_menu(zone)

    if account_id == 'false':
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)

    if account == 'false':
        print_finish_application_menu()
    delivery_center_id = account[0]['deliveryCenterId']

    # Call function to display the SKUs on the screen
    inventory = display_available_products_account(account_id, zone, environment, delivery_center_id)
    if inventory == 'true':
        print(text.Green + '\n- The inventory has been added successfully for the account {account_id}'
              .format(account_id=account_id))
    elif inventory == 'error_len':
        print(text.Red + '\n- There are no products available for the account {account_id}'
              .format(account_id=account_id))
        print_finish_application_menu()
    elif inventory == 'false':
        print_finish_application_menu()
    else:
        print_finish_application_menu()


def flow_input_recommended_products_to_account(zone, environment):
    account_id = print_account_id_menu(zone)
    if account_id == 'false':
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()

    product_offers = request_get_offers_microservice(account_id, zone, environment)
    if product_offers == 'false':
        print_finish_application_menu()
    elif product_offers == 'not_found':
        print(text.Red + '\n- [Catalog Service] There is no product associated with the account {account_id}'
              .format(account_id=account_id))
        print_finish_application_menu()

    items = list()
    index = 0
    while index <= 9:
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
        print(text.Green + '\n- Quick order items added successfully')
    else:
        print_finish_application_menu()


def flow_input_products_up_sell(zone, environment, account_id, items):
    if 'success' == request_sell_up(zone, environment, account_id, items):
        print(text.Green + '\n- Up sell items added successfully')
        print(text.Yellow + '- Up sell trigger: Add 3 of any products to the cart / Cart viewed with a product inside')
    else:
        print_finish_application_menu()


def flow_input_products_forgotten_items(zone, environment, account_id, items):
    if 'success' == request_forgotten_items(zone, environment, account_id, items):
        print(text.Green + '\n- Forgotten items added successfully')
    else:
        print_finish_application_menu()


def flow_input_all_recommendation_use_cases(zone, environment, account_id, items):
    if 'success' == create_all_recommendations(zone, environment, account_id, items):
        print(text.Green + '\n- All recommendation use cases were added (quick order, up sell and forgotten items)')
        print(text.Yellow + '- Up sell trigger: Add 3 of any products to the cart / Cart viewed with a product inside')
    else:
        print_finish_application_menu()


def flow_input_combo_quick_order(zone, environment, account_id):
    if 'success' == input_combos_quick_order(zone, environment, account_id):
        print(text.Green + '\n- Combos for quick order added successfully')
    else:
        print_finish_application_menu()


def flow_input_empties_discounts(zone, environment):
    account_id = print_account_id_menu(zone)

    if account_id == 'false':
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)

    if account == 'false':
        print_finish_application_menu()

    switcher = {
        'CO': '000000000003500159',
        'MX': '000000000002000162',
        'EC': '000000000003500612',
        'PE': '000000000003500192'
    }

    empty_sku = switcher.get(zone, 'false')
    if empty_sku == 'false':
        print(text.Red + '\n- Empties discounts it not enabled for {country}'.format(country=zone))
        print_finish_application_menu()

    while True:
        try:
            discount_value = int(input(text.default_text_color + 'Discount value: '))
            break
        except ValueError:
            print(text.Red + '\n- Invalid value')

    response = request_empties_discounts_creation(account_id, zone, environment, empty_sku, discount_value)
    if response == 'false':
        print_finish_application_menu()
    else:
        print(text.Green + '\n- Discount value for the empty SKU added successfully')


def account_menu():
    operation = print_account_operations_menu()
    if operation == '2':
        option = delivery_window_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    account_id = print_account_id_menu(zone)

    if account_id == 'false':
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
    state = validate_state(zone)
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
                                                state, account_status, enable_empties_loan)

    if create_account_response == 'success':
        print(text.Green + '\n- Your account {account_id} has been created successfully'.format(account_id=account_id))

        # Input default credit to the account so it won't be `null` in the Account Service database
        if 'false' == add_credit_to_account_microservice(account_id, zone, environment, 0, 0):
            print_finish_application_menu()
    else:
        print_finish_application_menu()


def flow_create_delivery_window(zone, environment, account_id, option):
    allow_flexible_delivery_dates = ['BR', 'ZA', 'MX']
    allow_delivery_cost = ['BR', 'MX']

    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()
    account_data = account[0]

    is_alternative_delivery_date = 'false'
    if zone in allow_flexible_delivery_dates:
        # Validate if is alternative delivery window
        is_alternative_delivery_date = print_alternative_delivery_date_menu()

        if is_alternative_delivery_date.upper() == 'Y':
            is_alternative_delivery_date = 'true'
        else:
            is_alternative_delivery_date = 'false'

    # Call add delivery window to account function
    delivery_window = create_delivery_window_microservice(zone, environment, account_data,
                                                              is_alternative_delivery_date, option)

    if delivery_window == 'success':
        print(text.Green + '\n- Delivery window created successfully for the account {account_id}'
              .format(account_id=account_id))

        # Check if delivery cost (interest) should be included
        if is_alternative_delivery_date == 'true' and zone in allow_delivery_cost:
            option_include_delivery_cost = print_include_delivery_cost_menu()
            if option_include_delivery_cost.upper() == 'Y':
                delivery_cost_values = get_delivery_cost_values(option_include_delivery_cost)
                delivery_cost = create_delivery_fee_microservice(zone, environment, account_data,
                                                                 delivery_cost_values)
                if delivery_cost == 'success':
                    print(text.Green + '\n- Delivery cost (interest) added successfully for the account {account_id}'
                          .format(account_id=account_id))
            else:
                print_finish_application_menu()
    else:
        print_finish_application_menu()


def flow_create_credit_information(zone, environment, account_id):
    # Check if account exists
    account = check_account_exists_microservice(account_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()

    # Get credit information
    credit_info = get_credit_info()

    # Add credit to account
    credit = add_credit_to_account_microservice(account_id, zone, environment, credit_info.get('credit'),
                                                credit_info.get('balance'))
    if credit == 'success':
        print(text.Green + '\n- Credit added successfully for the account {account_id}'.format(account_id=account_id))
    else:
        print_finish_application_menu()


def flow_update_account_name(zone, environment, account_id):
    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()
    account_data = account[0]

    name = print_account_name_menu()

    minimum_order = get_minimum_order_list(account_data['minimumOrder'])

    create_account_response = create_account_ms(account_id, name, account_data['paymentMethods'],
                                                minimum_order, zone, environment,
                                                account_data['deliveryAddress']['state'], account_data['status'],
                                                account_data['hasEmptiesLoan'])

    if create_account_response == 'success':
        print(text.Green + '\n- Account name updated for the account {account_id}'
              .format(account_id=account_id))
    else:
        print_finish_application_menu()


def flow_update_account_status(zone, environment, account_id):
    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()
    account_data = account[0]

    account_status = print_account_status_menu()

    minimum_order = get_minimum_order_list(account_data['minimumOrder'])

    create_account_response = create_account_ms(account_id, account_data['name'], account_data['paymentMethods'],
                                                minimum_order, zone, environment,
                                                account_data['deliveryAddress']['state'], account_status,
                                                account_data['hasEmptiesLoan'])

    if create_account_response == 'success':
        print(text.Green + '\n- Account status updated to {account_status} for the account {account_id}'
              .format(account_status=account_status, account_id=account_id))
    else:
        print_finish_application_menu()


def flow_update_account_minimum_order(zone, environment, account_id):
    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()
    account_data = account[0]

    option_include_minimum_order = print_minimum_order_menu()

    if option_include_minimum_order == 'Y':
        minimum_order = get_minimum_order_info()
    else:
        minimum_order = None

    create_account_response = create_account_ms(account_id, account_data['name'], account_data['paymentMethods'],
                                                minimum_order, zone, environment,
                                                account_data['deliveryAddress']['state'], account_data['status'],
                                                account_data['hasEmptiesLoan'])

    if create_account_response == 'success':
        print(text.Green + '\n- Minimum order updated for the account {account_id}'
              .format(account_id=account_id))
    else:
        print_finish_application_menu()


def flow_update_account_payment_method(zone, environment, account_id):
    # Call check account exists function
    account = check_account_exists_microservice(account_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()
    account_data = account[0]

    payment_method = print_payment_method_menu(zone)

    minimum_order = get_minimum_order_list(account_data['minimumOrder'])

    create_account_response = create_account_ms(account_id, account_data['name'], payment_method,
                                                minimum_order, zone, environment,
                                                account_data['deliveryAddress']['state'], account_data['status'],
                                                account_data['hasEmptiesLoan'])

    if create_account_response == 'success':
        print(text.Green + '\n- Payment method updated for the account {account_id}'
              .format(account_id=account_id))
    else:
        print_finish_application_menu()


# Print Finish Menu application
def print_finish_application_menu():
    option = input(text.default_text_color + '\nDo you want to finish the application? y/N: ')
    while validate_yes_no_option(option.upper()) is False:
        print(text.Red + '\n- Invalid option')
        option = input(text.default_text_color + '\nDo you want to finish the application? y/N: ')

    if option.upper() == 'Y':
        finish_application()
    else:
        show_menu()


# Validate if chosen sku is valid
def validateSkuChosen(sku, listSkuOffers):
    countItems = 0
    while countItems < len(listSkuOffers):
        if listSkuOffers[countItems] == sku:
            return "true"

        countItems = countItems + 1

    return "false"


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
    country = print_country_menu_in_user_create_iam()
    environment = print_environment_menu_in_user_create_iam()
    email = print_input_email()
    password = print_input_password()

    authenticate_response = user_v3.authenticate_user_iam(environment, country, email, password)

    if authenticate_response == "wrong_password":
        print(text.Green + "\n- The user already exists, but the password is wrong.")
        print_finish_application_menu()

    if authenticate_response != "fail":
        print(text.Green + "\n- The user already exists.")
        print_finish_application_menu()

    account_id = print_account_id_menu(country)

    if country == "BR":
        tax_id = account_id
    else:
        tax_id = print_input_tax_id()

    account_result = check_account_exists_microservice(account_id, country, environment)
    if account_result == "false":
        print_finish_application_menu()
    else:
        if account_result[0].get("status") != "ACTIVE":
            print(text.Red + "\n- The account isn't ACTIVE.")
            print_finish_application_menu()

    status_response = user_v3.create_user(environment, country, email, password, account_id, tax_id)
    if status_response == "success":
        print(text.Green + "\n- User IAM created successfully")
    else:
        print(text.Red + "\n- [User] Something went wrong, please try again")
        print_finish_application_menu()


def delete_user_iam():
    """Flow to delete user IAM
    Input Arguments:
        - Country
        - Environment
        - Email
    """
    country = print_country_menu_in_user_create_iam()
    environment = print_environment_menu_in_user_create_iam()
    email = print_input_email()

    status_response = user_delete_v3.delete_user_v3(environment, country, email)
    if status_response == "success":
        print(text.Green + "\n- User IAM deleted successfully")
    elif status_response == "partial":
        print(text.Magenta + "\n- User IAM deleted partially")
    else:
        print(text.Red + "\n- [Delete] Something went wrong, please try again")
        print_finish_application_menu()


def invoice_menu():
    operation = print_invoice_operations_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    account_id = print_account_id_menu(zone)

    if account_id == 'false':
        print_finish_application_menu()

    account = check_account_exists_microservice(account_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()

    return {
        '1': lambda: flow_create_invoice(zone, environment, account_id),
        '2': lambda: flow_update_invoice_status(zone, environment, account_id),
        '3': lambda: flow_update_invoice_payment_method(zone, environment, account_id)
    }.get(operation, lambda: None)()


def flow_create_invoice(zone, environment, account_id):
    order_id = print_order_id_menu()

    response = check_if_order_exists(account_id, zone, environment, order_id)
    if response == 'false' or response == 'not_found':
        print_finish_application_menu()

    order_data = response[0]
    order_details = get_order_details(order_data)
    order_items = get_order_items(order_data, zone)
    invoice_status = print_invoice_status_menu()

    invoice_response = create_invoice_request(zone, environment, order_id, invoice_status, order_details, order_items)
    if invoice_response != 'false':
        print(text.Green + '\n- Invoice {invoice_id} created successfully'.format(invoice_id=invoice_response))

        # Generate files for bank_slip and invoice (NF) only for Brazil
        if zone == 'BR':
            purposes = ['invoice', 'bank-slip']
            for i in range(len(purposes)):
                data = {'invoice_id': invoice_response}
                response = create_file_api(zone, environment, account_id, purposes[i], data)
                if response == 'false':
                    print_finish_application_menu()
    else:
        print_finish_application_menu()


def flow_update_invoice_status(zone, environment, account_id):
    invoice_id = print_invoice_id_menu()
    response = check_if_invoice_exists(account_id, invoice_id, zone, environment)

    if response == 'false':
        print_finish_application_menu()
    else:
        status = print_invoice_status_menu()
        invoice_response = update_invoice_request(zone, environment, account_id, invoice_id,
                                                  response['data'][0]['paymentType'], status)
        if invoice_response == 'false':
            print_finish_application_menu()
        else:
            print(text.Green + '\n- Invoice status updated to {invoice_status} for the invoice {invoice_id}'
                  .format(invoice_status=status, invoice_id=invoice_id))


def flow_update_invoice_payment_method(zone, environment, account_id):
    invoice_id = print_invoice_id_menu()
    response = check_if_invoice_exists(account_id, invoice_id, zone, environment)

    if response == 'false':
        print_finish_application_menu()
    else:
        payment_method = print_invoice_payment_method_menu()
        invoice_response = update_invoice_request(zone, environment, invoice_id, payment_method,
                                                  response['data'][0]['status'], account_id)
        if invoice_response == 'false':
            print_finish_application_menu()
        else:
            print(text.Green + '\n- Invoice payment method updated to {payment_method} for the invoice {invoice_id}'
                  .format(payment_method=payment_method, invoice_id=invoice_id))


def get_categories_menu():
    """Get categories
    Input Arguments:
        - Country (BR, DO, AR, CL, ZA, CO)
        - Environment (UAT, SIT)
        - Parent id (default: 0)
    """
    country = print_zone_menu_for_ms()
    environment = printEnvironmentMenuInUserCreation()
    parent_id = print_input_number_with_default('Parent id')

    # Get categories
    categories = get_categories(country, environment, parent_id)
    if categories:
        print("Categories: [id, name]")
        for category in categories:
            print("- {id}, {name}".format(id=category['id'], name=category['name']))
    else:
        print("{text_red}{not_found}".format(text_red=text.Red, not_found="Categories not found"))
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
    environment = printEnvironmentMenuInUserCreation()
    product_sku = print_input_text('Product SKU')
    category_id = print_input_number('Category ID')

    # Enable product
    enable_product_response = request_enable_product(country, environment, product_sku)
    if enable_product_response == 'false':
        print("{text_red}{fail}".format(text_red=text.Red, fail="Fail to enable product"))
        print_finish_application_menu()
    else:
        # Associate product to category
        response_associate_product_to_category = associate_product_to_category(country, environment, product_sku,
                                                                               category_id)
        if response_associate_product_to_category == 'false':
            print("{text_red}{fail}".format(text_red=text.Red, fail="Fail to associate product to category"))
            print_finish_application_menu()

    print("{text_green}{success}".format(text_green=text.Green,
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
    environment = printEnvironmentMenuInUserCreation()
    category_name = print_input_text('Category name')
    parent_id = print_input_number_with_default('Parent id')

    # Get categories
    categories = get_categories(country, environment, parent_id)
    category = [category for category in categories if category['name'] == category_name]
    if category:
        category = category[0]
        print("{text_green}{success}".format(text_green=text.Green, success="Category already exists"))
    else:
        # Create category
        category = create_category(country, environment, category_name, parent_id)
        if isinstance(category, str):
            print("{text_red}{not_found}".format(text_red=text.Red, not_found="Fail to create category"))
            print_finish_application_menu()
        else:
            print("{text_green}{success}".format(text_green=text.Green, success="Success to create category"))

    print("- {id}, {name}".format(id=category['id'], name=category['name']))


def order_information_menu():
    selection_structure = print_get_order_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        print_finish_application_menu()

    account = check_account_exists_microservice(abi_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()

    if selection_structure == '1':
        order_id = print_order_id_menu()
        orders = check_if_order_exists(abi_id, zone, environment, order_id)
        if orders == 'false':
            print_finish_application_menu()
        elif orders == 'empty':
            print(text.Red + '\n- [Order Service] The account ' + abi_id + ' does not have orders')
            print_finish_application_menu()
        elif orders == 'not_found':
            print(text.Red + '\n- [Order Service] The order ' + order_id + ' does not exist')
            print_finish_application_menu()

        display_specific_order_information(orders)
    else:
        orders = check_if_order_exists(abi_id, zone, environment, '')
        if orders == 'false':
            print_finish_application_menu()
        elif orders == 'empty':
            print(text.Red + '\n- [Order Service] The account ' + abi_id + ' does not have orders')
            print_finish_application_menu()

        display_all_order_information(orders)


def recommender_information_menu():
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        print_finish_application_menu()

    display_recommendations_by_account(zone, environment, abi_id)


def retrieve_available_invoices_menu():
    status = print_invoice_status_menu_retriever()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        print_finish_application_menu()
    account = check_account_exists_microservice(abi_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()
    invoice_info = get_invoices(zone, abi_id, environment)
    if invoice_info == 'false':
        print_finish_application_menu()
    print_invoices(invoice_info, status)


def retriever_sku_menu():
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    account_id = print_account_id_menu(zone)
    if account_id == 'false':
        print_finish_application_menu()

    account = check_account_exists_microservice(account_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()

    response = display_sku_rewards(zone, environment, account_id)
    if response == '200':
        print_finish_application_menu()
    else:
        print('\nError: ' + response.lstrip("false "))
        print_finish_application_menu()


def create_credit_statement_menu():
    zone = print_zone_credit_statement()
    environment = print_environment_menu()
    account_id = print_account_id_menu(zone)
    if account_id == 'false':
        print_finish_application_menu()

    account = check_account_exists_microservice(account_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()

    data = {
        'month': print_month_credit_statement(),
        'year': print_year_credit_statement()
    }

    response = create_file_api(zone, environment, account_id, 'credit-statement', data)
    if response == 'success':
        print(text.Green + '\n- Credit Statement created for the account {account_id}'.format(account_id=account_id))
    else:
        print_finish_application_menu()


def create_attribute_menu():

    selection_structure = print_create_attribute_menu()

    switcher = {
        '1': 'PRIMITIVE',
        '2': 'ENUM',
        '3': 'GROUP'
    }

    supplier_option = switcher.get(selection_structure, 'false')

    # Option to create a new program
    if supplier_option == 'PRIMITIVE':

        type_att = print_attribute_primitive()
        environment = print_environment_menu()

        switcher_type = {
            '1': 'NUMERIC',
            '2': 'TEXT',
            '3': 'DATE'
        }

        type_option = switcher_type.get(type_att, 'false')

        create_enum = create_attribute_primitive_type(environment, type_option)

        if create_enum != 'false':
            print(text.Green + '\n- [Attribute] The new {attribute_type} has been successfully created. '
                              'ID: {attribute}'.format(attribute_type=str(type_option),
                                                       attribute=create_enum))
            print_finish_application_menu()
        else:
            print_finish_application_menu()
    elif supplier_option == 'ENUM':
        type_att = print_attribute_primitive()
        environment = print_environment_menu()

        switcher_type = {
            '1': 'NUMERIC',
            '2': 'TEXT',
            '3': 'DATE'
        }

        type_option = switcher_type.get(type_att, 'false')
        create_primitive_attribute = create_attribute_enum(environment, type_option)

        if create_primitive_attribute != 'false':
            print(text.Green + '\n- [Attribute] The new {attribute_type} has been successfully created. '
                               'ID: {attribute}'.format(attribute_type=str(type_option),
                                                        attribute=create_primitive_attribute))
            print_finish_application_menu()
        else:
            print_finish_application_menu()
    elif supplier_option == 'GROUP':
        environment = print_environment_menu()
        list_att = insert_sub_attribute_group(environment)

        create_group = create_attribute_group(environment, list_att)

        if create_group != 'false':
            print(text.Green + '\n- [Attribute] The new {attribute_type} has been successfully created. '
                               'ID: {attribute}'.format(attribute_type=str(supplier_option),
                                                        attribute=create_group))
            print_finish_application_menu()
        else:
            print_finish_application_menu()


def insert_sub_attribute_group(environment):
    list_att = list()
    sub_att1 = input(text.default_text_color + 'Inform the first attribute in the group: ')
    valid_att = check_if_attribute_exist(environment, sub_att1)
    if valid_att == 'false':
        print_finish_application_menu()
    else:
        list_att.append(sub_att1)
    sub_att2 = input(text.default_text_color + 'Inform the second attribute in the group: ')
    valid_att2 = check_if_attribute_exist(environment, sub_att2)
    if valid_att2 == 'false':
        print_finish_application_menu()
    else:
        list_att.append(sub_att2)
    new_att = print_new_attribute()
    while new_att == '1':
        sub_att = input(text.default_text_color + 'Inform the another attribute in the group: ')
        valid_att = check_if_attribute_exist(environment, sub_att)
        if valid_att2 == 'false':
            new_att == '2'
            print_finish_application_menu()
        else:
            list_att.append(sub_att)
            new_att = print_new_attribute()
    return list_att


# Init
try:
    if __name__ == '__main__':
        show_menu()

except KeyboardInterrupt:
    sys.exit(0)
