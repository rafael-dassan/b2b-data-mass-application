from account import *
from common import *
from credit import add_credit_to_account_microservice
from credit_statement import create_credit_statement
from deals import *
from delivery_window import *
from beer_recommender import *
from inventory import *
from invoice import *
from menus.account_menu import print_account_operations_menu, print_minimum_order_menu, print_account_status_menu, \
    print_account_name_menu, print_account_enable_empties_loan_menu, print_alternative_delivery_date_menu, \
    print_include_delivery_cost_menu, print_payment_method_menu, print_account_id_menu, print_get_account_menu
from menus.deals_menu import print_deals_operations_menu, print_discount_value_menu, print_minimum_quantity_menu, \
    print_max_quantity_menu, print_free_good_quantity_range_menu, print_option_sku_menu, print_partial_free_good_menu, \
    print_free_good_redemption_menu, print_free_good_quantity_menu, print_index_range_menu, print_discount_range_menu
from menus.invoice_menu import print_invoice_operations_menu, print_invoice_status_menu, print_invoice_id_menu, \
    print_invoice_payment_method_menu, print_invoice_status_menu_retriever
from order import *
from combos import *
from products import *
from rewards import *
from category_magento import *
from products_magento import *
import user_creation_magento as user_magento
import user_creation_v3 as user_v3
import user_delete_v3 as user_delete_v3
from simulation import process_simulation_microservice
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
            '2': input_products_to_account_menu,
            '3': input_recommendation_to_account_menu,
            '4': input_inventory_to_product,
            '5': input_orders_to_account,
            '6': deals_menu,
            '7': input_combos_menu,
            '8': create_item_menu,
            '9': invoice_menu,
            '10': create_rewards_to_account,
            '11': create_credit_statement_menu
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
            '1': create_user_magento_menu,
            '2': associateUserToAccount,
            '3': get_categories_menu,
            '4': associate_product_to_category_menu,
            '5': create_categories_menu
        }
    elif selection_structure == '4':
        switcher = {
            '0': finish_application,
            '1': registration_user_iam,
            '2': delete_user_iam
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
    selection_structure = print_get_account_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()

    switcher = {
        '1': 'ONE_ACCOUNT',
        '2': 'ALL_ACCOUNT',
        '3': 'ACCOUNT_PRODUCT'
    }

    account_type = switcher.get(selection_structure, 'false')

    if account_type == 'ONE_ACCOUNT':
        abi_id = print_account_id_menu(zone)
        if abi_id == 'false':
            print_finish_application_menu()
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account == 'false':
            print_finish_application_menu()

        display_account_information(account)
    elif account_type == 'ALL_ACCOUNT':
        account = check_account_exists_microservice('', zone, environment)
        if account == 'false':
            print_finish_application_menu()
        display_all_account_info(account)
    else:
        print(text.default_text_color + '\nThis process can take some time... ')

        account = check_account_exists_microservice('', zone, environment)
        if account == 'false':
            print_finish_application_menu()
        account_info_list = list()
        for i in range(len(account)):
            account_id = account[i]['accountId']
            product = request_get_offers_microservice(account_id, zone, environment)
            if product != 'false' or product != 'not_found':
                account_info = {
                    'Account ID': account_id,
                    'Tax ID': account[i]['taxId'],
                    'Poc Name': account[i]['name']
                }
                account_info_list.append(account_info)

        display_account_with_products(account_info_list)


# Input Rewards to account
def create_rewards_to_account():
    selection_structure = print_rewards_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()

    switcher = {
        '1': 'NEW_PROGRAM',
        '2': 'UPDATE_BALANCE',
        '3': 'ENROLL_POC',
        '4': 'ADD_CHALLENGE',
        '5': 'ADD_REDEEM',
        '6': 'DELETE_ENROLL_POC'
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


# Input orders to account
def input_orders_to_account():
    selection_structure = print_orders_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        print_finish_application_menu()

    switcher = {
        '1': 'ACTIVE',
        '2': 'CANCELLED',
        '3': 'CHANGED',
        '4': 'DELIVERED'
    }

    order_status = switcher.get(selection_structure, 'false')

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone, environment)
    if account == 'false':
        print_finish_application_menu()

    if selection_structure == '2' or selection_structure == '4':
        # Call function to check if the account has products inside
        product_offers = request_get_offers_microservice(abi_id, zone, environment)
        if product_offers == 'false':
            print_finish_application_menu()
        elif product_offers == 'not_found':
            print(text.Red + '\n- [Catalog Service] There is no product associated with the account ' + abi_id)
            print_finish_application_menu()

        allow_order_cancel = 'N'

        # Call function to configure prefix and order number size in the database sequence
        if 'false' == configure_order_params(zone, environment, 5, 'DM-ORDER-'):
            print_finish_application_menu()

        sku_list = list()
        aux_index = 0
        while len(sku_list) < 2:
            sku = product_offers[aux_index]['sku']
            sku_list.append(sku)
            aux_index += 1

        # Call function to create the Order according to the 'order_option' parameter (active or cancelled)
        response = create_order_account(abi_id, zone, environment, order_status, sku_list, allow_order_cancel, 'N')
        if response != 'false':
            print(text.Green + '\n- Order ' + response.get('orderNumber') + ' created successfully')
            # Call function to re-configure prefix and order number size to the previous format
            if 'false' == configure_order_params(zone, environment, 9, '00'):
                print_finish_application_menu()
        else:
            print_finish_application_menu()
    elif selection_structure == '1':
        allow_order_cancel = print_allow_cancellable_order_menu()
        order_items = list()

        # Call function to configure prefix and order number size in the database sequence
        if 'false' == configure_order_params(zone, environment, 5, 'DM-ORDER-'):
            print_finish_application_menu()

        input_order_item = input(text.default_text_color + 'Would you like to include a new sku for this order? y/N: ')
        while input_order_item.upper() != 'Y' and input_order_item.upper() != 'N':
            print(text.Red + '\n- Invalid option\n')
            input_order_item = input(text.default_text_color + 'Would you like to include a new sku for this order? y/N: ')

        if input_order_item.upper() == 'Y':
            more_sku = 'Y'
            while more_sku.upper() == 'Y':
                sku = input(text.default_text_color + 'Inform sku for this order: ')
                quantity = input(text.default_text_color + 'Inform sku quantity for  this order: ')
                while is_number(quantity) == 'false':
                    print(text.Red + '\n- Invalid quantity\n')
                    quantity = input(text.default_text_color + 'Inform sku quantity for  this order: ')

                temp_product_data = {'sku': sku, 'quantity': quantity}
                order_items.append(temp_product_data)
                more_sku = input(text.default_text_color + 'Would you like to include a new sku for this order? y/N: ')

            response = create_order_account(abi_id, zone, environment, order_status, order_items, allow_order_cancel,
                                            more_sku)
            if response != 'false':
                print(text.Green + '\n- Order ' + response.get('orderNumber') + ' created successfully')
                # Call function to re-configure prefix and order number size to the previous format
                if 'false' == configure_order_params(zone, environment, 9, '00'):
                    print_finish_application_menu()
            else:
                print_finish_application_menu()
        else:
            more_sku = 'N'
            # Call function to check if the account has products inside
            product_offers = request_get_offers_microservice(abi_id, zone, environment)
            if product_offers == 'false':
                print_finish_application_menu()
            elif product_offers == 'not_found':
                print(text.Red + '\n- [Catalog Service] There is no product associated with the account ' + abi_id)
                print_finish_application_menu()

            # Call function to configure prefix and order number size in the database sequence
            if 'false' == configure_order_params(zone, environment, 5, 'DM-ORDER-'):
                print_finish_application_menu()

            sku_list = list()
            aux_index = 0
            while len(sku_list) < 2:
                sku = product_offers[aux_index]['sku']
                sku_list.append(sku)
                aux_index += 1

            # Call function to create the Order according to the 'order_option' parameter (active or cancelled)
            response = create_order_account(abi_id, zone, environment, order_status, sku_list, allow_order_cancel,
                                            more_sku)
            if response != 'false':
                print(text.Green + '\n- Order ' + response.get('orderNumber') + ' created successfully')
                # Call function to re-configure prefix and order number size to the previous format
                if 'false' == configure_order_params(zone, environment, 9, '00'):
                    print_finish_application_menu()
            else:
                print_finish_application_menu()
    else:
        order_id = print_order_id_menu()
        order_data = check_if_order_exists(abi_id, zone, environment, order_id)
        if order_data == 'false':
            print_finish_application_menu()
        elif order_data == 'empty':
            print(text.Red + '\n- [Order Service] The account ' + abi_id + ' does not have orders')
            print_finish_application_menu()
        elif order_data == 'not_found':
            print(text.Red + '\n- [Order Service] The order ' + order_id + ' does not exist')
            print_finish_application_menu()

        statuses = ['DENIED', 'CANCELLED', 'DELIVERED', 'PARTIAL_DELIVERY', 'PENDING_CANCELLATION']
        if order_data[0]['status'] in statuses:
            print(text.Red + '\n- This order cannot be changed. Order status: ' + order_data[0]['status'])
            print_finish_application_menu()

        if len(order_data[0]['items']) == 1 and order_data[0]['items'][0]['quantity'] == 1:
            print(text.Red + '\n- It\'s not possible to change this order because the order has only one '
                             'product with quantity equals 1')
            print_finish_application_menu()

        response = change_order(zone, environment, order_data)
        if response == 'success':
            print(text.Green + '\n- Order ' + order_id + ' was changed successfully')
        else:
            print_finish_application_menu()


# Create an item for a specific Zone
def create_item_menu():
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    item_data = get_item_input_data()

    response = create_item(zone, environment, item_data)
    if response is not None:
        print(text.Green + '\n- [Item Service] The item was created successfully')
        print(text.default_text_color + '- Item ID: ' + response.get('sku') + ' / Item name: ' + response.get('name'))


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

    process_simulation_microservice(zone, environment, abi_id, account, order_items, order_combos, empties_skus,
                                    payment_method, payment_term)
    print_finish_application_menu()


# Input inventory (stock) to products
def input_inventory_to_product():
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        print_finish_application_menu()

    # Check if the account exists
    account = check_account_exists_microservice(abi_id, zone, environment)

    if account == 'false':
        print_finish_application_menu()

    # Check if the account has products
    product_assortment = request_get_account_product_assortment(abi_id, zone, environment,
                                                                account[0]['deliveryCenterId'])

    if product_assortment == 'false':
        print_finish_application_menu()
    elif product_assortment == 'not_found':
        print(text.Red + '\n- [Product Assortment Service] There is no product associated with the account ' + abi_id)
        print_finish_application_menu()

    # Call function to display the SKUs on the screen
    inventory = display_available_products_account(abi_id, zone, environment, account[0]['deliveryCenterId'])
    if inventory == 'true':
        print(text.Green + '\n- The inventory has been added successfully for the account ' + abi_id)
    elif inventory == 'error_len':
        print(text.Red + '\n- There are no products available for the account ' + abi_id)
        print_finish_application_menu()
    else:
        print_finish_application_menu()


# Input beer recommender by account on Microservice
def input_recommendation_to_account_menu():
    recommender_type = print_recommender_type_menu()
    zone = print_zone_menu_for_ms()
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

    enabled_skus = list()
    aux_index = 0
    while aux_index < len(product_offers):
        sku = product_offers[aux_index]['sku']
        enabled_skus.append(sku)
        aux_index = aux_index + 1

    if len(enabled_skus) < 25:
        print(text.Red + '\n- The account must have at least 25 enabled products to proceed')
        print_finish_application_menu()

    if recommender_type == 'QUICK_ORDER':
        quick_order_response = request_quick_order(zone, environment, abi_id, enabled_skus)
        if quick_order_response == 'success':
            print(text.Green + '\n- Quick order items added successfully')
        else:
            print_finish_application_menu()
    elif recommender_type == 'CROSS_SELL_UP_SELL':
        sell_up_response = request_sell_up(zone, environment, abi_id, enabled_skus)
        if sell_up_response == 'success':
            print(text.Green + '\n- Up sell items added successfully')
            print(text.Yellow + '- Up sell trigger: Add 3 of any products to the cart / Cart viewed with a product '
                                'inside')
        else:
            print_finish_application_menu()
    elif recommender_type == 'FORGOTTEN_ITEMS':
        forgotten_items_response = request_forgotten_items(zone, environment, abi_id, enabled_skus)
        if forgotten_items_response == 'success':
            print(text.Green + '\n- Forgotten items added successfully')
        else:
            print_finish_application_menu()
    elif recommender_type == 'COMBOS_QUICKORDER':
        combos_quickorder_response = input_combos_quickorder(zone, environment, abi_id)
        if combos_quickorder_response == 'success':
            print(text.Green + '\n- Combos for quick order added successfully')
        else:
            print_finish_application_menu()
    else:
        if 'success' == create_all_recommendations(zone, environment, abi_id, enabled_skus):
            print(text.Green + '\n- All recommendation use cases were added (quick order, up sell and forgotten items)')
            print(text.Yellow + '- Up sell trigger: Add 3 of any products to the cart / Cart viewed with a product '
                                'inside')


def deals_menu():
    operation = print_deals_operations_menu()
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
    while len(sku_list) <= 2:
        index_offers = randint(0, (len(product_offers) - 1))
        product_data = product_offers[index_offers]
        sku_list.append(product_data)

    if option_sku == '1':
        sku = input(text.default_text_color + 'SKU: ')
        item_enabled = check_item_enabled(sku, zone, environment)
        while not item_enabled:
            sku = input(text.default_text_color + '\nSKU: ')
            item_enabled = check_item_enabled(sku, zone, environment)
    else:
        sku = sku_list[0]['sku']

    return {
        '1': lambda: flow_create_discount(zone, environment, account_id, sku),
        '2': lambda: flow_create_stepped_discount(zone, environment, account_id, sku),
        '3': lambda: flow_create_stepped_discount_with_limit(zone, environment, account_id, sku),
        '4': lambda: flow_create_free_good(zone, environment, account_id, sku_list),
        '5': lambda: flow_create_stepped_free_good(zone, environment, account_id, sku)
    }.get(operation, lambda: None)()


def flow_create_discount(zone, environment, account_id, sku):
    minimum_quantity = print_minimum_quantity_menu()
    discount_value = print_discount_value_menu()

    response = create_discount(account_id, sku, zone, environment, discount_value, minimum_quantity)
    if response != 'false':
        print(text.Green + '\n- Deal {deal_id} created successfully'.format(deal_id=response))
    else:
        print_finish_application_menu()


def flow_create_stepped_discount(zone, environment, account_id, sku):
    index_range = print_index_range_menu()
    discount_range = print_discount_range_menu()

    response = create_stepped_discount(account_id, sku, zone, environment, index_range, discount_range)
    if response != 'false':
        print(text.Green + '\n- Deal {deal_id} created successfully'.format(deal_id=response))
    else:
        print_finish_application_menu()


def flow_create_stepped_discount_with_limit(zone, environment, account_id, sku):
    # Default index range (from 1 to 9999 products)
    default_index_range = [1, 9999]

    discount_range = print_discount_range_menu(1)
    max_quantity = print_max_quantity_menu(default_index_range)

    response = create_stepped_discount_with_limit(account_id, sku, zone, environment, default_index_range,
                                                  discount_range, max_quantity)
    if response != 'false':
        print(text.Green + '\n- Deal {deal_id} created successfully'.format(deal_id=response))
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
    if response != 'false':
        print(text.Green + '\n- Deal {deal_id} created successfully'.format(deal_id=response))
    else:
        print_finish_application_menu()


def flow_create_stepped_free_good(zone, environment, account_id, sku):
    index_range = print_index_range_menu()
    quantity_range = print_free_good_quantity_range_menu()

    response = create_stepped_free_good(account_id, sku, zone, environment, index_range, quantity_range)
    if response != 'false':
        print(text.Green + '\n- Deal {deal_id} created successfully'.format(deal_id=response))
    else:
        print_finish_application_menu()


# Input combos to an account
def input_combos_menu():
    selection_structure = print_combos_menu()

    if selection_structure == '3':
        zone = print_zone_menu_for_combos('DT')
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
            print(text.Yellow + '- Please, run the cron job `abinbev_combos_service_importer` to import your combo, so '
                                'it can be used in the front-end applications')

    if selection_structure != '5' and response != 'false':
        print(text.Green + '\n- Combo ' + response + ' successfully registered')
        print(text.Yellow + '- Please, run the cron job `abinbev_combos_service_importer` to import your combo, so '
                            'it can be used in the front-end applications')

    if (zone == 'DO' or zone == 'CO') and selection_structure != '5' and response != 'false':
        print(
            text.Yellow + '\n- Also on Magento Admin, turn the new combos `enable` through the menu `Catalog -> Products`')

    print_finish_application_menu()


def input_products_to_account_menu():
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        print_finish_application_menu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone, environment)

    if account == 'false':
        print_finish_application_menu()

    delivery_center_id = account[0]['deliveryCenterId']

    proceed = 'N'
    products = request_get_offers_microservice(abi_id, zone, environment)
    if products == 'false':
        print_finish_application_menu()
    elif products == 'not_found':
        proceed = 'Y'
    else:
        proceed = input(text.Yellow + '\n- [Account] The account ' + str(abi_id) + ' already have products, do you '
                                                                                   'want to proceed? y/N: ').upper()
        if proceed == '':
            proceed = 'N'

    if proceed == 'Y':
        all_products_zone = request_get_products_microservice(zone, environment)
        if all_products_zone == 'false':
            print_finish_application_menu()

        # Call add products to account function
        add_products = add_products_to_account_microservice(abi_id, zone, environment, delivery_center_id,
                                                            all_products_zone)
        if add_products != 'success':
            print(text.Red + '\n- [Products] Something went wrong, please try again')
            print_finish_application_menu()

        products = request_get_account_product_assortment(abi_id, zone, environment, delivery_center_id)
        if products == 'false':
            print_finish_application_menu()
        elif products == 'not_found':
            print(text.Red + '\n- [Product Assortment Service] There is no product associated with the account '
                      + abi_id)
            print_finish_application_menu()

        skus_id = list()
        aux_index = 0
        while aux_index <= (len(products) - 1):
            skus_id.append(products[aux_index])
            aux_index = aux_index + 1

        update_sku = update_sku_inventory_microservice(zone, environment, delivery_center_id, skus_id)

        if update_sku != 'true':
            print_finish_application_menu()


def account_menu():
    operation = print_account_operations_menu()
    zone = print_zone_menu_for_ms()
    environment = print_environment_menu()
    account_id = print_account_id_menu(zone)

    if account_id == 'false':
        print_finish_application_menu()

    return {
        '1': lambda: flow_create_account(zone, environment, account_id),
        '2': lambda: flow_create_delivery_window(zone, environment, account_id),
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
    else:
        print_finish_application_menu()


def flow_create_delivery_window(zone, environment, account_id):
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
    delivery_window = create_delivery_window_microservice(zone, environment, account_data, is_alternative_delivery_date)

    if delivery_window == 'success':
        print(text.Green + '\n- Delivery window created successfully for the account {account_id}'
              .format(account_id=account_id))

        # Check if delivery cost (interest) should be included
        if is_alternative_delivery_date == 'true' and zone in allow_delivery_cost:
            option_include_delivery_cost = print_include_delivery_cost_menu()
            if option_include_delivery_cost.upper() == 'Y':
                delivery_cost_values = get_delivery_cost_values(option_include_delivery_cost)
                delivery_cost = create_delivery_fee_microservice(zone, environment, account_data, delivery_cost_values)
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


# Create User for zones in Microservice
def create_user_magento_menu():
    country = printCountryMenuInUserCreation()
    env = printEnvironmentMenuInUserCreation()
    account_id = print_account_id_menu(country)
    email = print_input_email()
    password = print_input_password()
    phone = print_input_phone()

    account_id_list = user_magento.get_user_accounts(env, country, email, password)
    if len(account_id_list) > 0:
        if account_id in account_id_list:
            print(text.Green + "\n- The user already exists with the same accountId: " + account_id)
        else:
            print(text.Red +
                  "\n- The user already exists but without the accountId informed: " + account_id)
        print_finish_application_menu()

    account_result = check_account_exists_microservice(account_id, country, env)
    if account_result == "false":
        print_finish_application_menu()
    else:
        if account_result[0].get("status") != "ACTIVE":
            print(text.Red + "\n- The account isn't ACTIVE.")
            print_finish_application_menu()

    status_response = user_magento.create_user(env, country, email, password, account_result[0], phone)
    if status_response == "success":
        print(text.Green + "\n- User created successfully")
    else:
        print(text.Red + "\n- [User] Something went wrong, please try again")
        print_finish_application_menu()

    print_finish_application_menu()


def associateUserToAccount():
    """ Associate user to account
    Input Arguments:
        - Country
        - Environment
        - Account ID
        - Email
        - Password
    """
    country = printCountryMenuInUserCreation()
    env = printEnvironmentMenuInUserCreation()
    accountId = print_account_id_menu(country)
    email = print_input_email()
    password = print_input_password()

    # Check if user has already associated to account
    account_id_list = user_magento.get_user_accounts(env, country, email, password)
    if len(account_id_list) > 0:
        if accountId in account_id_list:
            print(text.Green + "\n- The user already exists with the same accountId: " + accountId)
            print_finish_application_menu()

    # Check if account exists and is active
    account_result = check_account_exists_microservice(accountId, country, env)
    if account_result == "false":
        print_finish_application_menu()
    else:
        if account_result[0].get("status") != "ACTIVE":
            print(text.Red + "\n- The account isn't ACTIVE.")
            print_finish_application_menu()
    account = account_result[0]

    # Check if user exists
    user = user_magento.authenticate_user(env, country, email, password)
    if user == "fail":
        print(text.Red + "\n- Fail to authenticate user.")
        print_finish_application_menu()

    print(user_magento.associate_user_to_account(env, country, user, account))


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
    order_items = get_order_items(order_data)
    invoice_status = print_invoice_status_menu()

    invoice_response = create_invoice_request(zone, environment, order_id, invoice_status, order_details, order_items)
    if invoice_response == 'false':
        print_finish_application_menu()
    else:
        print(text.Green + '\n- Invoice {invoice_id} created successfully'.format(invoice_id=invoice_response))


def flow_update_invoice_status(zone, environment, account_id):
    invoice_id = print_invoice_id_menu()
    response = check_if_invoice_exists(account_id, invoice_id, zone, environment)

    if response == 'false':
        print_finish_application_menu()
    else:
        status = print_invoice_status_menu()
        invoice_response = update_invoice_request(zone, environment, invoice_id, response['data'][0]['paymentType'],
                                                  status)
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
                                                  response['data'][0]['status'])
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
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        print_finish_application_menu()

    display_sku_rewards(zone, environment, abi_id)


def create_credit_statement_menu():
    zone = print_zone_credit_statement()
    environment = print_environment_menu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        print_finish_application_menu()

    month = print_month_credit_statement()
    year = print_year_credit_statement()

    doc = create_credit_statement(zone, abi_id, environment, month, year)
    if doc == 'false':
        print_finish_application_menu()


# Init
try:
    if __name__ == '__main__':
        show_menu()

except KeyboardInterrupt:
    sys.exit(0)
