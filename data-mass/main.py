from account import *
from credit import add_credit_to_account_microservice
from delivery_window import create_delivery_window_microservice, validate_alternative_delivery_date
from beer_recommender import *
from inventory import *
from invoice import *
from order import *
from combos import *
from rewards import *
from category_magento import *
from products_magento import *
import user_creation_magento as user_magento
import user_creation_v3 as user_v3
from simulation import process_simulation_microservice, process_simulation_middleware


def showMenu():
    clearTerminal()
    printWelcomeScript()
    selection_structure = print_structure_menu()
    option = print_available_options(selection_structure)
    if selection_structure == '1':
        switcher = {
            '0': finishApplication,
            '1': create_account_menu,
            '2': input_products_to_account_menu,
            '3': input_credit_menu,
            '4': input_delivery_window_menu,
            '5': input_recommendation_to_account_menu,
            '6': input_inventory_to_product,
            '7': input_orders_to_account,
            '8': input_deals_menu,
            '9': input_combos_menu,
            '10': create_item_menu,
            '11': create_invoice_menu,
            '12': create_rewards_to_account
        }
    elif selection_structure == '2':
        switcher = {
            '0': finishApplication,
            '1': check_simulation_service_account_microservice_menu,
            '2': check_simulation_service_mdw_menu,
            '3': account_information_menu,
            '4': product_information_menu,
            '5': deals_information_menu,
            '6': order_information_menu,
            '7': recommender_information_menu
        }
    elif selection_structure == '3':
        switcher = {
            '0': finishApplication,
            '1': create_user_magento_menu,
            '2': registration_user_iam,
            '3': associateUserToAccount,
            '4': get_categories_menu,
            '5': associate_product_to_category_menu,
            '6': create_categories_menu
        }
    else:
        finishApplication()

    function = switcher.get(option, '')

    if function != '':
        function()

    printFinishApplicationMenu()


def deals_information_menu():
    zone = print_zone_menu_data_searching_deals()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()

    account = check_account_exists_microservice(abi_id, zone, environment)
    if account == 'false':
        printFinishApplicationMenu()

    if zone == 'CL' or zone == 'ZA':
        deals = request_get_deals_promotion_service(abi_id, zone, environment)
        if deals != 'false':
            display_deals_information_promotion(abi_id, deals)
    else:
        deals = request_get_deals_promo_fusion_service(zone, environment, abi_id)
        if deals != 'false':
            display_deals_information_promo_fusion(abi_id, deals)


def product_information_menu():
    selection_structure = print_get_products_menu()
    environment = printEnvironmentMenu()

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
            printFinishApplicationMenu()
        account = check_account_exists_microservice(abi_id, zone, environment)
        if account == 'false':
            printFinishApplicationMenu()

        product_offers = request_get_products_by_account_microservice(abi_id, zone, environment)
        if product_offers == 'false':
            printFinishApplicationMenu()
        elif product_offers == 'not_found':
            print(text.Red + '\n- [Catalog Service] There is no product associated with the account ' + abi_id)
            printFinishApplicationMenu()

        display_product_information(product_offers)

    elif products_type == 'INVENTORY':
        zone = print_zone_menu_for_inventory()
        abi_id = print_account_id_menu(zone)
        if abi_id == 'false':
            printFinishApplicationMenu()
        
        account = check_account_exists_microservice(abi_id, zone, environment)
        if account == 'false':
            printFinishApplicationMenu()

        delivery_center_id = account[0]['deliveryCenterId']
        display_inventory_by_account(zone, environment, abi_id, delivery_center_id)

    else:
        zone = print_zone_menu_for_ms()

        products = request_get_products_microservice(zone, environment)
        if products == 'false':
            printFinishApplicationMenu()

        display_items_information_zone(zone, environment, products)


def account_information_menu():
    selection_structure = print_get_account_menu()
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()

    switcher = {
        '1': 'ONE_ACCOUNT',
        '2': 'ALL_ACCOUNT',
        '3': 'ACCOUNT_PRODUCT'
    }

    account_type = switcher.get(selection_structure, 'false')

    if account_type == 'ONE_ACCOUNT':
        abi_id = print_account_id_menu(zone)
        if abi_id == 'false':
            printFinishApplicationMenu()
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account == 'false':
            printFinishApplicationMenu()

        display_account_information(account)
    elif account_type == 'ALL_ACCOUNT':
        account = check_account_exists_microservice('', zone, environment)
        if account == 'false':
            printFinishApplicationMenu()
        display_all_account_info(account)
    else:
        print(text.default_text_color + '\nThis process can take some time... ')

        account = check_account_exists_microservice('', zone, environment)
        if account == 'false':
            printFinishApplicationMenu()
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
    zone = print_zone_menu_for_rewards()
    environment = printEnvironmentMenu()

    switcher = {
        '1': 'NEW_PROGRAM',
        '2': 'UPDATE_BALANCE',
        '3': 'ENROLL_POC',
        '4': 'ADD_CHALLENGE',
        '5': 'ADD_REDEEM'
    }

    reward_option = switcher.get(selection_structure, 'false')

    # Option to create a new program
    if reward_option == 'NEW_PROGRAM':

        create_pgm = create_new_program(zone, environment)

        if create_pgm == 'error_len_sku':
            print(text.Red + '\n- [Rewards] The zone must have at least 20 products to proceed')
            printFinishApplicationMenu()
        elif create_pgm == 'error_len_combo':
            print(text.Red + '\n- [Rewards] The zone must have combos available to proceed')
            printFinishApplicationMenu()
        elif create_pgm == 'error_found':
            printFinishApplicationMenu()
        else:
            print(text.Green + '\n- [Rewards] The new program has been successfully created. ID: ' + create_pgm)
            printFinishApplicationMenu()

    # Option to enroll POC to a program
    elif reward_option == 'ENROLL_POC':   
        
        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account == 'false':
            printFinishApplicationMenu()
        
        enroll_poc = enroll_poc_to_program(abi_id, zone, environment)

        if enroll_poc == 'pgm_not_found':
            print(text.Red + '\n- [Rewards] This zone does not have a program created. Please use the menu option "Create new program" to create it')
        elif enroll_poc == 406:
            print(text.Red + '\n- [Rewards] There are no Reward programs available for this account')
        elif enroll_poc == 409:
            print(text.Red + '\n- [Rewards] This account already have a Reward program enrolled to it')
        elif enroll_poc == 201:
            print(text.Green + '\n- [Rewards] The account has been successfully enrolled to a rewards program')

        printFinishApplicationMenu()

    # Option to input challenges to a specific zone
    elif reward_option == 'ADD_CHALLENGE':
           
        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account == 'false':
            printFinishApplicationMenu()
    
        add_challenge = input_challenge_to_zone(abi_id, zone, environment)

        if add_challenge == 'false':
            print(text.Red + '\n- [Rewards] Something went wrong, please try again')

        printFinishApplicationMenu()

    # Option to update initial balance of a program
    elif reward_option == 'UPDATE_BALANCE':

        update_balance = update_program_balance(zone, environment)

        if update_balance == 'no_confirm' or update_balance == 'error':
            printFinishApplicationMenu()
        elif update_balance == 'no_program':
            print(text.Red + '\n- [Rewards] There is no rewards program available for this zone')
        else:
            print(text.Green + '\n- [Rewards] The program ' + update_balance + ' has been successfully updated.')

        printFinishApplicationMenu()

    # Option to input redeem products to an account       
    elif reward_option == 'ADD_REDEEM': 

        abi_id = print_account_id_menu(zone)

        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone, environment)

        if account != 'false':
            input_redeem_products(abi_id, zone, environment)
        else:
            printFinishApplicationMenu()


# Input orders to account
def input_orders_to_account():
    selection_structure = print_orders_menu()
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()

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
        printFinishApplicationMenu()

    if selection_structure == '1' or selection_structure == '2' or selection_structure == '4':
        # Call function to check if the account has products inside
        product_offers = request_get_offers_microservice(abi_id, zone, environment)
        if product_offers == 'false':
            printFinishApplicationMenu()
        elif product_offers == 'not_found':
            print(text.Red + '\n- [Catalog Service] There is no product associated with the account ' + abi_id)
            printFinishApplicationMenu()

        if order_status == 'ACTIVE':
            allow_order_cancel = print_allow_cancellable_order_menu()
        else:
            allow_order_cancel = 'N'

        # Call function to configure prefix and order number size in the database sequence
        if 'false' == configure_order_params(zone, environment, 5, 'DM-ORDER-'):
            printFinishApplicationMenu()

        sku_list = list()
        aux_index = 0
        while len(sku_list) < 2:
            sku = product_offers[aux_index]['sku']
            sku_list.append(sku)
            aux_index += 1

        # Call function to create the Order according to the 'order_option' parameter (active or cancelled)
        response = create_order_account(abi_id, zone, environment, order_status, sku_list, allow_order_cancel)
        if response != 'false':
            print(text.Green + '\n- Order ' + response.get('orderNumber') + ' created successfully')
            # Call function to re-configure prefix and order number size to the previous format
            if 'false' == configure_order_params(zone, environment, 9, '00'):
                printFinishApplicationMenu()
        else:
            printFinishApplicationMenu()
    else:
        order_id = print_order_id_menu()
        order_data = check_if_order_exists(abi_id, zone, environment, order_id)
        if order_data == 'false':
            printFinishApplicationMenu()
        elif order_data == 'empty':
            print(text.Red + '\n- [Order Service] The account ' + abi_id + ' does not have orders')
            printFinishApplicationMenu()
        elif order_data == 'not_found':
            print(text.Red + '\n- [Order Service] The order ' + order_id + ' does not exist')
            printFinishApplicationMenu()

        statuses = ['DENIED', 'CANCELLED', 'DELIVERED', 'PARTIAL_DELIVERY', 'PENDING_CANCELLATION']
        if order_data[0]['status'] in statuses:
            print(text.Red + '\n- This order cannot be changed. Order status: ' + order_data[0]['status'])
            printFinishApplicationMenu()

        if len(order_data[0]['items']) == 1 and order_data[0]['items'][0]['quantity'] == 1:
            print(text.Red + '\n- It\'s not possible to change this order because the order has only one '
                             'product with quantity equals 1')
            printFinishApplicationMenu()

        response = change_order(zone, environment, order_data)
        if response == 'success':
            print(text.Green + '\n- Order ' + order_id + ' was changed successfully')
        else:
            printFinishApplicationMenu()


# Create an item for a specific Zone
def create_item_menu():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    item_data = get_item_input_data()

    response = create_item(zone, environment, item_data)
    if response is not None:
        print(text.Green + '\n- [Item Service] The item was created successfully')
        print(text.default_text_color + '- Item ID: ' + response.get('sku') + ' / Item name: ' + response.get('name'))


# Place request for simulation service in microservice
def check_simulation_service_account_microservice_menu():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone, environment)

    if account == 'false':
        printFinishApplicationMenu()

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
    input_order_empties = input(text.default_text_color + "Would you like to include a new empties sku for simulation? (y/n) ")
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
    printFinishApplicationMenu()


# Place request for simulation service in middleware
def check_simulation_service_mdw_menu():
    zone = print_zone_simulation_menu("true")
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone, environment)

    if account == 'false':
        printFinishApplicationMenu()

    order_items = list()
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

            temp_product_data = {"sku": sku, "quantity": quantity}
            order_items.append(temp_product_data)
            more_sku = input(text.default_text_color + "Would you like to include more skus for simulation? (y/N) ")

    # Payment Method menu
    payment_method = print_payment_method_simulation_menu(zone)
    process_simulation_middleware(zone, environment, abi_id, account, order_items, payment_method)
    printFinishApplicationMenu()


# Input inventory (stock) to products
def input_inventory_to_product():
    zone = print_zone_menu_for_inventory()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()

    # Check if the account exists
    account = check_account_exists_microservice(abi_id, zone, environment)

    if account == 'false':
        printFinishApplicationMenu()

    # Check if the account has products
    product_assortment = request_get_account_product_assortment(abi_id, zone, environment,
                                                                account[0]['deliveryCenterId'])

    if product_assortment == 'false':
        printFinishApplicationMenu()
    elif product_assortment == 'not_found':
        print(text.Red + '\n- [Product Assortment Service] There is no product associated with the account ' + abi_id)
        printFinishApplicationMenu()

    # Call function to display the SKUs on the screen
    inventory = display_available_products_account(abi_id, zone, environment, account[0]['deliveryCenterId'])
    if inventory == 'true':
        print(text.Green + '\n- The inventory has been added successfully for the account ' + abi_id)
    elif inventory == 'error_len':
        print(text.Red + '\n- There are no products available for the account ' + abi_id)
        printFinishApplicationMenu()
    else:
        printFinishApplicationMenu()


# Input beer recommender by account on Microservice
def input_recommendation_to_account_menu():
    recommendation_type = print_recommendation_type_menu()
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone, environment)
    if account == 'false':
        printFinishApplicationMenu()

    product_offers = request_get_offers_microservice(abi_id, zone, environment)
    if product_offers == 'false':
        printFinishApplicationMenu()
    elif product_offers == 'not_found':
        print(text.Red + '\n- [Catalog Service] There is no product associated with the account ' + abi_id)
        printFinishApplicationMenu()

    enabled_skus = list()
    aux_index = 0
    while aux_index < len(product_offers):
        sku = product_offers[aux_index]['sku']
        enabled_skus.append(sku)
        aux_index = aux_index + 1

    if len(enabled_skus) < 25:
        print(text.Red + '\n- The account must have at least 25 enabled products to proceed')
        printFinishApplicationMenu()

    if recommendation_type == 'QUICK_ORDER':
        quick_order_response = request_quick_order(zone, environment, abi_id, enabled_skus)
        if quick_order_response == 'success':
            print(text.Green + '\n- Quick order items added successfully')
        else:
            printFinishApplicationMenu()
    elif recommendation_type == 'CROSS_SELL_UP_SELL':
        sell_up_response = request_sell_up(zone, environment, abi_id, enabled_skus)
        if sell_up_response == 'success':
            print(text.Green + '\n- Up sell items added successfully')
            print(text.Yellow + '- Up sell trigger: Add 3 of any products to the cart / Cart viewed with a product '
                                'inside')
        else:
            printFinishApplicationMenu()
    elif recommendation_type == 'FORGOTTEN_ITEMS':
        forgotten_items_response = request_forgotten_items(zone, environment, abi_id, enabled_skus)
        if forgotten_items_response == 'success':
            print(text.Green + '\n- Forgotten items added successfully')
        else:
            printFinishApplicationMenu()
    else:
        if 'success' == create_all_recommendations(zone, environment, abi_id, enabled_skus):
            print(text.Green + '\n- All recommendation use cases were added (quick order, up sell and forgotten items)')
            print(text.Yellow + '- Up sell trigger: Add 3 of any products to the cart / Cart viewed with a product '
                                'inside')


# Input Deals to an account
def input_deals_menu():
    selection_structure = print_deals_menu()
    zone = print_zone_menu_for_deals()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()

    option_sku = print_option_sku(zone)

    switcher = {
        '1': 'DISCOUNT',
        '2': 'STEPPED_DISCOUNT',
        '3': 'FREE_GOOD',
        '4': 'STEPPED_FREE_GOOD',
        '5': 'STEPPED_DISCOUNT'
    }

    deal_type = switcher.get(selection_structure, 'false')

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone, environment)
    if account == 'false':
        printFinishApplicationMenu()

    # Request POC's associated products
    product_offers = request_get_offers_microservice(abi_id, zone, environment)
    if product_offers == 'false':
        printFinishApplicationMenu()
    elif product_offers == 'not_found':
        print(text.Red + '\n- [Catalog Service] There is no product associated with the account ' + abi_id)
        printFinishApplicationMenu()

    sku_list = list()
    while len(sku_list) <= 2:
        index_offers = randint(0, (len(product_offers) - 1))
        product_data = product_offers[index_offers]
        sku = product_data['sku']

        # Check if the SKU is enabled on Items MS
        item_enabled = check_item_enabled(sku, zone, environment)
        while not item_enabled:
            index_offers = randint(0, (len(product_offers) - 1))
            product_data = product_offers[index_offers]
            sku = product_data['sku']
            item_enabled = check_item_enabled(sku, zone, environment)

        sku_list.append(product_data)

    if option_sku == '1':
        sku = input(text.default_text_color + 'SKU: ')
        item_enabled = check_item_enabled(sku, zone, environment)
        while not item_enabled:
            sku = input(text.default_text_color + '\nSKU: ')
            item_enabled = check_item_enabled(sku, zone, environment)
    else:
        sku = sku_list[0]['sku']

    if selection_structure == '1':
        response = input_discount_to_account(abi_id, sku, deal_type, zone, environment)
    elif selection_structure == '2':
        response = input_stepped_discount_to_account(abi_id, sku, deal_type, zone, environment)
    elif selection_structure == '3':
        response = input_free_good_to_account(abi_id, sku, sku_list, deal_type, zone, environment)
    elif selection_structure == '4':
        response = input_stepped_free_good_to_account(abi_id, sku, deal_type, zone, environment)
    else:
        response = input_stepped_discount_with_qtd_to_account(abi_id, sku, deal_type, zone, environment)

    if response != 'false':
        print(text.Green + '\n- Deal ' + response + ' created successfully')
        if zone == 'ZA':
            print(text.Yellow + '- Please, run the cron jobs `webjump_discount_import` and `webjump_discount_update_'
                                'online_customers` to import your deal')
    else:
        printFinishApplicationMenu()


# Input combos to an account
def input_combos_menu():
    selection_structure = print_combos_menu()

    if selection_structure == '3':
        zone = print_zone_menu_for_combos('DT')
    else:
        zone = print_zone_menu_for_combos()   
        
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone, environment)

    if account == 'false':
        printFinishApplicationMenu()

    product_offers = request_get_offers_microservice(abi_id, zone, environment)
    if product_offers == 'false':
        printFinishApplicationMenu()
    elif product_offers == 'not_found':
        print(text.Red + '\n- [Catalog Service] There is no product associated with the account ' + abi_id)
        printFinishApplicationMenu()

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

    if  selection_structure != '5' and response != 'false':
            print(text.Green + '\n- Combo ' + response + ' successfully registered')
            print(text.Yellow + '- Please, run the cron job `abinbev_combos_service_importer` to import your combo, so '
                                'it can be used in the front-end applications')
    
    if (zone == 'DO' or zone == 'CO') and selection_structure != '5' and response != 'false':
        print(text.Yellow + '\n- Also on Magento Admin, turn the new combos `enable` through the menu `Catalog -> Products`')
        
    printFinishApplicationMenu()


# Input credit to account
def input_credit_menu():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()

    # Check if account exists
    account = check_account_exists_microservice(abi_id, zone, environment)

    if account == 'false':
        printFinishApplicationMenu()

    credit = input(text.default_text_color + 'Desired credit available (Default 5000): ')
    balance = input(text.default_text_color + 'Desired credit balance (Default 15000): ')

    # Add credit to account
    credit = add_credit_to_account_microservice(abi_id, zone, environment, credit, balance)

    if credit == 'success':
        print(text.Green + '\n- Credit added successfully for account ' + abi_id)
    else:
        printFinishApplicationMenu()


def input_products_to_account_menu():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone, environment)

    if account == 'false':
        printFinishApplicationMenu()

    delivery_center_id = account[0]['deliveryCenterId']

    products = request_get_offers_microservice(abi_id, zone, environment)
    if products == 'false':
        printFinishApplicationMenu()
    elif products == 'not_found':
        print(text.Red + '\n- [Catalog Service] There is no product associated with the account ' + abi_id)
        printFinishApplicationMenu()

    proceed = 'N'
    if len(products) != 0:
        proceed = input(text.Yellow + '\n- [Account] The account ' + str(abi_id) + ' already have products, do you '
                                                                                   'want to proceed? y/N: ').upper()
        if proceed == '':
            proceed = 'N'
    elif len(products) == 0:
        proceed = 'Y'
    else:
        printFinishApplicationMenu()

    if proceed == 'Y':
        all_products_zone = request_get_products_microservice(zone, environment)
        if all_products_zone == 'false':
            printFinishApplicationMenu()

        # Call add products to account function
        add_products = add_products_to_account_microservice(abi_id, zone, environment, delivery_center_id,
                                                            all_products_zone)
        if add_products != 'success':
            print(text.Red + '\n- [Products] Something went wrong, please try again')
            printFinishApplicationMenu()

        if zone != 'BR' and zone != 'CL':
            products = request_get_account_product_assortment(abi_id, zone, environment, delivery_center_id)
            if products == 'false':
                printFinishApplicationMenu()
            elif products == 'not_found':
                print(text.Red + '\n- [Product Assortment Service] There is no product associated with the account '
                      + abi_id)
                printFinishApplicationMenu()

            skus_id = list()
            aux_index = 0
            while aux_index <= (len(products) - 1):
                skus_id.append(products[aux_index])
                aux_index = aux_index + 1

            update_sku = update_sku_inventory_microservice(zone, environment, delivery_center_id, skus_id)

            if update_sku != 'true':
                printFinishApplicationMenu()


def input_delivery_window_menu():
    zone = print_zone_menu_for_delivery_window()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone, environment)

    if account == 'false':
        printFinishApplicationMenu()

    if zone == 'BR' or zone == 'ZA':
        # Validate if is alternative delivery window
        is_alternative_delivery_date = print_alternative_delivery_date_menu()

        if is_alternative_delivery_date.upper() == 'Y':
            is_alternative_delivery_date = 'true'
        else:
            is_alternative_delivery_date = 'false'
    else:
        is_alternative_delivery_date = 'false'

    # Call add delivery window to account function
    delivery_window = create_delivery_window_microservice(zone, environment, account[0], is_alternative_delivery_date)

    if delivery_window == 'success':
        print(text.Green + '\n- Delivery window added successfully')
    else:
        printFinishApplicationMenu()


# Create Account menu for Zones using MS
def create_account_menu():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()
    name = printNameMenu()
    payment_method = printPaymentMethodMenu(zone)
    state = validate_state(zone)

    option_include = input(text.default_text_color + 'Do you want to include the minimum order parameter? y/N: ')
    while option_include == '' or validate_yes_no_option(option_include.upper()) == 'false':
        print(text.Red + '\n- Invalid option\n')
        option_include = input(text.default_text_color + 'Do you want to include the minimum order parameter? y/N: ')

    if option_include.upper() == 'Y':
        minimum_order = printMinimumOrderMenu()
    else:
        minimum_order = None

    # Call create account function
    create_account_response = create_account_ms(abi_id, name, payment_method, minimum_order, zone, environment, state)

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone, environment)

    if create_account_response == 'success' and account != 'false':
        print(text.Green + '\n- Your account has been created! Now register on Web or Mobile applications\n')
    else:
        printFinishApplicationMenu()

    delivery_center_id = account[0]['deliveryCenterId']

    all_products_zone = request_get_products_microservice(zone, environment)
    if all_products_zone == 'false':
        printFinishApplicationMenu()

    # Call add products to account function
    products = add_products_to_account_microservice(abi_id, zone, environment, delivery_center_id, all_products_zone)
    if products != 'success':
        print(text.Red + '\n\n- [Products] Something went wrong, please try again')
        printFinishApplicationMenu()

    if zone != 'BR' and zone != 'CL':
        products = request_get_account_product_assortment(abi_id, zone, environment, delivery_center_id)
        if products == 'false':
            printFinishApplicationMenu()
        elif products == 'not_found':
            print(text.Red + '\n- [Product Assortment Service] There is no product associated with the account '
                  + abi_id)
            printFinishApplicationMenu()

        skus_id = list()
        aux_index = 0

        while aux_index <= (len(products) - 1):
            skus_id.append(products[aux_index])
            aux_index = aux_index + 1

        update_sku = update_sku_inventory_microservice(zone, environment, delivery_center_id, skus_id)

        if update_sku != 'true':
            printFinishApplicationMenu()

    if zone == 'BR' or zone == 'ZA':
        # Validate if is alternative delivery window
        is_alternative_delivery_date = print_alternative_delivery_date_menu()

        if is_alternative_delivery_date.upper() == 'Y':
            is_alternative_delivery_date = 'true'
        else:
            is_alternative_delivery_date = 'false'
    else:
        is_alternative_delivery_date = 'false'

    # Call add delivery window to account function
    delivery_window = create_delivery_window_microservice(zone, environment, account[0], is_alternative_delivery_date)

    if delivery_window == 'success':
        print(text.Green + '\n- Delivery window added successfully')
    else:
        printFinishApplicationMenu()


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
        printFinishApplicationMenu()

    account_result = check_account_exists_microservice(account_id, country, env)
    if account_result == "false":
        printFinishApplicationMenu()
    else:
        if account_result[0].get("status") != "ACTIVE":
            print(text.Red + "\n- The account isn't ACTIVE.")
            printFinishApplicationMenu()

    status_response = user_magento.create_user(env, country, email, password, account_result[0], phone)
    if status_response == "success":
        print(text.Green + "\n- User created successfully")
    else:
        print(text.Red + "\n- [User] Something went wrong, please try again")
        printFinishApplicationMenu()

    printFinishApplicationMenu()


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
            printFinishApplicationMenu()

    # Check if account exists and is active
    account_result = check_account_exists_microservice(accountId, country, env)
    if account_result == "false":
        printFinishApplicationMenu()
    else:
        if account_result[0].get("status") != "ACTIVE":
            print(text.Red + "\n- The account isn't ACTIVE.")
            printFinishApplicationMenu()
    account = account_result[0]

    # Check if user exists
    user = user_magento.authenticate_user(env, country, email, password)
    if user == "fail":
        print(text.Red + "\n- Fail to authenticate user.")
        printFinishApplicationMenu()

    print(user_magento.associate_user_to_account(env, country, user, account))


# Print Finish Menu application
def printFinishApplicationMenu():
    finish = input(text.default_text_color + "\nDo you want to finish the application? y/N: ")
    while validate_yes_no_option(finish.upper()) == "false":
        print(text.Red + "\n- Invalid option")
        finish = input(text.default_text_color + "\nDo you want to finish the application? y/N: ")

    if finish.upper() == "Y":
        finishApplication()
    else:
        showMenu()


# Print alternative delivery date menu application
def print_alternative_delivery_date_menu():
    is_alternative_delivery_date = input(text.default_text_color + 'Do you want to register an alternative delivery '
                                                                   'date? y/N: ')
    while validate_alternative_delivery_date(is_alternative_delivery_date.upper()) == 'false':
        print(text.Red + '\n- Invalid option')
        is_alternative_delivery_date = input(text.default_text_color + '\nDo you want to register an alternative '
                                                                       'delivery date? y/N: ')

    return is_alternative_delivery_date


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
        printFinishApplicationMenu()

    if authenticate_response != "fail":
        print(text.Green + "\n- The user already exists.")
        printFinishApplicationMenu()

    account_id = print_account_id_menu(country)
    tax_id = print_input_tax_id()

    account_result = check_account_exists_microservice(account_id, country, environment)
    if account_result == "false":
        printFinishApplicationMenu()
    else:
        if account_result[0].get("status") != "ACTIVE":
            print(text.Red + "\n- The account isn't ACTIVE.")
            printFinishApplicationMenu()

    status_response = user_v3.create_user(environment, country, email, password, account_result[0], tax_id)
    if status_response == "success":
        print(text.Green + "\n- User IAM created successfully")
    else:
        print(text.Red + "\n- [User] Something went wrong, please try again")
        printFinishApplicationMenu()


def create_invoice_menu():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()

    account = check_account_exists_microservice(abi_id, zone, environment)
    if account == 'false':
        printFinishApplicationMenu()

    order_id = print_order_id_menu()

    response = check_if_order_exists(abi_id, zone, environment, order_id)
    if response == 'false':
        printFinishApplicationMenu()
    elif response == 'empty':
        print(text.Red + '\n- [Order Service] The account ' + abi_id + ' does not have orders')
        printFinishApplicationMenu()
    elif response == 'not_found':
        print(text.Red + '\n- [Order Service] The order ' + order_id + ' does not exist')
        printFinishApplicationMenu()

    status = print_invoice_status_menu()
    invoice_response = create_invoice_request(zone, environment, order_id, status, response[0])
    if invoice_response != 'false':
        print(text.Green + '\n- Invoice ' + invoice_response + ' created successfully')
        print(text.Yellow + '- Please, run the cron job `webjump_invoicelistabi_import_invoices` to import your '
                            'invoice, so it can be used in the front-end applications')
    else:
        printFinishApplicationMenu()


def get_categories_menu():
    """Get categories
    Input Arguments:
        - Country (BR, DO, AR, CL, ZA, CO)
        - Environment (UAT, SIT)
        - Parent id (default: 0)
    """
    country = printCountryMenuInUserCreation()
    environment = printEnvironmentMenuInUserCreation()
    parent_id = print_input_number_with_default('Parent id')
    
    # Get categories 
    categories = get_categories(country, environment, parent_id)
    if categories:
        print("Categories: [id, name]")
        for category in categories:
            print("- {id}, {name}".format(id=category['id'],name=category['name']))
    else:
        print("{text_red}{not_found}".format(text_red=text.Red, not_found="Categories not found"))
        printFinishApplicationMenu()


def associate_product_to_category_menu():
    """Associate product to category
    Input Arguments:
        - Country (BR, DO, AR, CL, ZA, CO)
        - Environment (UAT, SIT)
        - Product SKU
        - Category ID
    """
    country = printCountryMenuInUserCreation()
    environment = printEnvironmentMenuInUserCreation()
    product_sku = print_input_text('Product SKU')
    category_id = print_input_number('Category ID')

    # Enable product
    enable_product_response = request_enable_product(country, environment, product_sku)
    if enable_product_response == 'false':
        print("{text_red}{fail}".format(text_red=text.Red, fail="Fail to enable product"))
        printFinishApplicationMenu()
    else:
        # Associate product to category
        response_associate_product_to_category = associate_product_to_category(country, environment, product_sku, category_id)
        if response_associate_product_to_category == 'false':
            print("{text_red}{fail}".format(text_red=text.Red, fail="Fail to associate product to category"))
            printFinishApplicationMenu()
    
    print("{text_green}{success}".format(text_green=text.Green, success="Success to enable and to associate product to category"))


def create_categories_menu():
    """Create categories
    Input Arguments:
        - Country (BR, DO, AR, CL, ZA, CO)
        - Environment (UAT, SIT)
        - Category name
        - Parent id (default: 0)
    """
    country = printCountryMenuInUserCreation()
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
            printFinishApplicationMenu()
        else:
            print("{text_green}{success}".format(text_green=text.Green, success="Success to create category"))

    print("- {id}, {name}".format(id=category['id'],name=category['name']))


def order_information_menu():
    selection_structure = print_get_order_menu()
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()

    account = check_account_exists_microservice(abi_id, zone, environment)
    if account == 'false':
        printFinishApplicationMenu()

    if selection_structure == '1':
        order_id = print_order_id_menu()
        orders = check_if_order_exists(abi_id, zone, environment, order_id)
        if orders == 'false':
            printFinishApplicationMenu()
        elif orders == 'empty':
            print(text.Red + '\n- [Order Service] The account ' + abi_id + ' does not have orders')
            printFinishApplicationMenu()
        elif orders == 'not_found':
            print(text.Red + '\n- [Order Service] The order ' + order_id + ' does not exist')
            printFinishApplicationMenu()

        display_specific_order_information(orders)
    else:
        orders = check_if_order_exists(abi_id, zone, environment, '')
        if orders == 'false':
            printFinishApplicationMenu()
        elif orders == 'empty':
            print(text.Red + '\n- [Order Service] The account ' + abi_id + ' does not have orders')
            printFinishApplicationMenu()

        display_all_order_information(orders)


def recommender_information_menu():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    if abi_id == 'false':
        printFinishApplicationMenu()

    display_recommendations_by_account(zone, environment, abi_id)


# Init
try:
    if __name__ == '__main__':
        showMenu()

except KeyboardInterrupt:
    sys.exit(0)
