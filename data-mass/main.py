from account import create_account_ms, check_account_exists_microservice, display_account_information
from credit import add_credit_to_account_microservice
from delivery_window import create_delivery_window_microservice, validateAlternativeDeliveryDate
from beer_recommender import *
from inventory import *
from invoice import check_if_order_exist, order_info, create_invoice_request
from order import *
from combos import *
from deals import *
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
            '3': inputCreditAccountMicroserviceMenu,
            '4': inputDeliveryWindowAccountMicroserviceMenu,
            '5': input_recommendation_to_account_menu,
            '6': inputInventoryToProduct,
            '7': input_orders_to_account,
            '8': inputDealsMenu,
            '9': inputCombosMenu,
            '10': create_item_menu,
            '11': create_invoice
        }
    elif selection_structure == '2':
        switcher = {
            '0': finishApplication,
            '1': check_simulation_service_account_microservice_menu,
            '2': check_simulation_service_mdw_menu,
            '3': account_information_menu,
            '4': product_information_menu,
            '5': deals_information_menu
        }
    elif selection_structure == '3':
        switcher = {
            '0': finishApplication,
            '1': create_user_magento_menu,
            '2': registration_user_iam,
            '3': associateUserToAccount
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

    account = check_account_exists_microservice(abi_id, zone, environment)

    if account == 'false':
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif len(account) == 0:
        print(text.Red + '\n- [Account] The account ' + abi_id + ' does not exist')
        printFinishApplicationMenu()

    if zone == 'AR' or zone == 'CL':
        display_deals_information_promotion(abi_id, zone.upper(), environment.upper())
    else:
        display_deals_information_promo_fusion(abi_id, zone.upper(), environment.upper())


def product_information_menu():
    zone = print_zone_menu_data_searching()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)

    account = check_account_exists_microservice(abi_id, zone, environment)

    if account == 'false':
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif len(account) == 0:
        print(text.Red + '\n- [Account] The account ' + abi_id + ' does not exist')
        printFinishApplicationMenu()

    product_offers = request_get_products_by_account_microservice(abi_id, zone, environment)
    if len(product_offers) == 0:
        print(text.Red + '\n- [Product Offers] The account ' + abi_id + ' does not have products')
        printFinishApplicationMenu()
    else:
        display_product_information(product_offers)


def account_information_menu():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)

    account = check_account_exists_microservice(abi_id, zone, environment)

    if account == 'false':
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif len(account) == 0:
        print(text.Red + '\n- [Account] The account ' + abi_id + ' does not exist')
        printFinishApplicationMenu()

    display_account_information(account)


# Input Orders to account
def input_orders_to_account():
    zone = print_zone_menu_for_order()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == 'false':
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif len(account) == 0:
        print(text.Red + '\n- [Account] The account ' + abi_id + ' does not exist')
        printFinishApplicationMenu()

    print(text.default_text_color + '\nChecking enabled products for the account ' + abi_id + '. It may take a while...')

    # Call function to check if the account has products inside
    products_inventory_account = request_get_offers_microservice(abi_id, zone.upper(), environment.upper(), account[0]['deliveryCenterId'], True)

    if len(products_inventory_account) != 0:
        # Call function to configure prefix and order number size in the database sequence
        order_params = configure_order_params(zone.upper(), environment.upper(), 1)

        if order_params == 'false':
            print(text.Red + '\n- [Order Creation] Something went wrong when configuring order params, please try again')
            printFinishApplicationMenu()
        else:
            # Call function to create the Order
            create_order = create_order_account(abi_id, zone.upper(), environment.upper(), account[0]['deliveryCenterId'])

            if create_order == 'error_len':
                print(text.Red + '\n- [Order Creation] The account must have at least two enabled products to proceed')
                printFinishApplicationMenu()
            elif create_order == 'false':
                print(text.Red + '\n- [Order Creation] Something went wrong, please try again')
                printFinishApplicationMenu()
            elif create_order == 'true':
                # Call function to re-configure prefix and order number size to the previous format
                order_params = configure_order_params(zone.upper(), environment.upper(), 2)
                printFinishApplicationMenu()
    else:
        print(text.Red + '\n- [Order Creation] The account has no products inside. Use the menu option 02 to add them first')
        printFinishApplicationMenu()


# Create an item for a specific Zone
def create_item_menu():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    item_data = get_item_input_data()

    response = create_item(zone.upper(), environment.upper(), item_data)
    if response != None:
        print(text.Green + '\n- [Item Service] The item was created successfully')
        print(text.default_text_color + '- Item ID: ' + response.get('sku') + ' / Item name: ' + response.get('name'))


# Place request for simulation service in microservice
def check_simulation_service_account_microservice_menu():
    zone = print_zone_simulation_menu("false")
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == 'false':
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif len(account) == 0:
        print(text.Red + '\n- [Account] The account ' + abi_id + ' does not exist')
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
        input_order_combo = input(text.default_text_color + "Would you like to include a new combo for simulation? (y/n) ")

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
        input_order_empties = input(text.default_text_color + "Would you like to include a new empties sku for simulation? (y/n) ")

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
    payment_method = print_payment_method_simulation_menu(zone.upper())
    if payment_method.upper() == "BANK_SLIP":
        payment_term = input(text.default_text_color + "Enter the number of days the bill will expire: ")
        while is_number(payment_term) == "false":
            print(text.Red + "\n- Invalid number\n")
            payment_term = input(text.default_text_color + "Enter the number of days the bill will expire: ")
    else:
        payment_term = 0

    process_simulation_microservice(zone, environment, abi_id, account, order_items, order_combos, empties_skus, payment_method, payment_term)
    printFinishApplicationMenu()


# Place request for simulation service in middleware
def check_simulation_service_mdw_menu():
    zone = print_zone_simulation_menu("true")
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == 'false':
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif len(account) == 0:
        print(text.Red + '\n- [Account] The account ' + abi_id + ' does not exist')
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
    payment_method = print_payment_method_simulation_menu(zone.upper())
    process_simulation_middleware(zone, environment, abi_id, account, order_items, payment_method)
    printFinishApplicationMenu()


# Input Inventory to a SKU
def inputInventoryToProduct():
    zone = print_zone_menu_for_inventory()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == 'false':
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif len(account) == 0:
        print(text.Red + '\n- [Account] The account ' + abi_id + ' does not exist')
        printFinishApplicationMenu()

    # Call function to check if the account has products inside
    products_inventory_account = request_get_account_product_assortment(abi_id, zone.upper(), environment.upper(), account[0]['deliveryCenterId'])

    if len(products_inventory_account) > 0:
        # Call function to display the SKUs on the screen
        product_offers = display_available_products_account(abi_id, zone.upper(), environment.upper(), account[0]['deliveryCenterId'])

        if product_offers == "true":
            print(text.Green + "\n- [Inventory] The inventory of the SKU has been added successfully.")
        else:
            if product_offers == "error_len":
                print(text.Red + "\n- [Inventory] There are no products available in the chosen account.")
                printFinishApplicationMenu()
            else:
                print(text.Red + "\n- [Inventory] Something went wrong, please try again.")
                printFinishApplicationMenu()
    else:
        print(text.Red + "\n- [Inventory] The account has no products inside. Use the menu option 02 to add them first.")
        printFinishApplicationMenu()


# Input beer recommender by account on Microservice
def input_recommendation_to_account_menu():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == 'false':
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif len(account) == 0:
        print(text.Red + '\n- [Account] The account ' + abi_id + ' does not exist')
        printFinishApplicationMenu()

    # Call function to add Beer Recommender to the account
    beer_recommender = create_beer_recommender_microservice(abi_id, zone.upper(), environment.upper(), account[0]['deliveryCenterId'])

    if beer_recommender == 'true':
        print(text.Green + '\n- [Algo Selling] All recommended products were added successfully')
        print(text.Yellow + '\n- [Algo Selling] **  UP SELL TRIGGERS: Products Added to Cart: 03  /  Cart Viewed with Products: 01  **')
    else:
        if beer_recommender == 'error25':
            print(text.Red + '\n- [Algo Selling] The account must have at least 25 enabled products to proceed')
            printFinishApplicationMenu()
        else:
            print(text.Red + '\n- [Algo Selling] Something went wrong, please try again')
            printFinishApplicationMenu()


# Input Deals to an account
def inputDealsMenu():
    selectionStructure = printDealsMenu()
    zone = print_zone_menu_for_deals()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)

    switcher = {
        "1": "DISCOUNT",
        "2": "STEPPED_DISCOUNT",
        "3": "FREE_GOOD",
        "4": "STEPPED_FREE_GOOD",
        "5": "STEPPED_DISCOUNT"
    }

    deal_type = switcher.get(selectionStructure, "false")

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == 'false':
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif len(account) == 0:
        print(text.Red + '\n- [Account] The account ' + abi_id + ' does not exist')
        printFinishApplicationMenu()

    accounts = list()
    accounts.append(abi_id)

    # For Zones which use the microservice integration
    product_offers = request_get_offers_microservice(abi_id, zone, environment, account[0]['deliveryCenterId'], True)

    if len(product_offers) == 0:
        print(text.Red + "\n- [Products] The account " + str(abi_id) + " has no available products for purchase")
        printFinishApplicationMenu()

    if zone.upper() == "CO" or zone.upper() == "MX":
        skus = list()
        while len(skus) <= 1:
            index_offers = randint(0, (len(product_offers) - 1))
            product = product_offers[index_offers]
            product_sku = product['sku']

            # Check if the SKU is enabled on Items MS
            deal_sku = check_item_enabled(product_sku, zone.upper(), environment.upper(), True)
            while deal_sku == False:
                index_offers = randint(0, (len(product_offers) - 1))
                product = product_offers[index_offers]
                product_sku = product['sku']
                deal_sku = check_item_enabled(product_sku, zone.upper(), environment.upper(), True)

            skus.append(product)
    else:
        index_offers = randint(0, (len(product_offers) - 1))
        product = product_offers[index_offers]

        if zone.upper() == "ZA":
            product_sku = product
        else:
            product_sku = product['sku']
        # Check if the SKU is enabled on Items MS
        deal_sku = check_item_enabled(product_sku, zone.upper(), environment.upper(), True)
        while deal_sku == False:
            index_offers = randint(0, (len(product_offers) - 1))
            product = product_offers[index_offers]
            if zone.upper() == "ZA":
                product_sku = product
            else:
                product_sku = product['sku']

            deal_sku = check_item_enabled(product_sku, zone.upper(), environment.upper(), True)

        skus = list()
        skus.append(product)

    if zone.upper() != "ZA":
        deal_sku = skus[0]['sku']

    if selectionStructure == "1":
        input_discount_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone.upper(), environment.upper())
    elif selectionStructure == "2":
        input_stepped_discount_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone.upper(), environment.upper())
    elif selectionStructure == "3":
        input_free_good_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone.upper(), environment.upper())
    elif selectionStructure == "4":
        input_stepped_free_good_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone.upper(), environment.upper())
    else:
        input_stepped_discount_with_qtd_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone.upper(), environment.upper())

    printFinishApplicationMenu()


# Input combos by account
def inputCombosMenu():
    selectionStructure = printCombosMenu()
    zone = print_zone_menu_for_deals()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == 'false':
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif len(account) == 0:
        print(text.Red + '\n- [Account] The account ' + abi_id + ' does not exist')
        printFinishApplicationMenu()

    product_offers = request_get_offers_microservice(abi_id, zone, environment, account[0]['deliveryCenterId'], True)

    if len(product_offers) == 0:
        print(text.Red + "\n- [Products] The account " + str(abi_id) + " has no products available for purchase")
        printFinishApplicationMenu()

    index_offers = randint(0, (len(product_offers) - 1))
    sku = product_offers[index_offers]['sku']

    # Check if the SKU is enabled on Items MS
    combo_item = check_item_enabled(sku, zone.upper(), environment.upper(), True)
    while combo_item == False:
        index_offers = randint(0, (len(product_offers) - 1))
        sku = product_offers[index_offers]['sku']
        combo_item = check_item_enabled(sku, zone.upper(), environment.upper(), True)

    if selectionStructure == "1":
        while True:
            try:
                discount_value = int(input(text.default_text_color + "Discount percentage (%): "))
                break
            except ValueError:
                print(text.Red + "\n- Invalid value")

        response = input_combo_type_discount(abi_id, zone, environment, combo_item, discount_value)

        if response != "success":
            print(text.Red + "\n- [Combo] Something went wrong while creating the combo")
            printFinishApplicationMenu()

    elif selectionStructure == "2":
        combo_free_good = list()
        auxIndex = 0
        while auxIndex < 3:
            index_offers = randint(0, (len(product_offers) - 1))
            sku = product_offers[index_offers]['sku']

            # Check if the SKU is enabled on Items MS
            combo_item = check_item_enabled(sku, zone.upper(), environment.upper(), True)
            while combo_item == False:
                index_offers = randint(0, (len(product_offers) - 1))
                sku = product_offers[index_offers]['sku']
                combo_item = check_item_enabled(sku, zone.upper(), environment.upper(), True)

            combo_free_good.append(combo_item)
            auxIndex = auxIndex + 1

        response = input_combo_type_free_good(abi_id, zone, environment, combo_item, combo_free_good)

        if response != "success":
            print(text.Red + "\n- [Combo] Something went wrong while creating the combo")
            printFinishApplicationMenu()

    else:
        combo_free_good = list()
        auxIndex = 0
        while auxIndex < 3:
            index_offers = randint(0, (len(product_offers) - 1))
            sku = product_offers[index_offers]['sku']

            # Check if the SKU is enabled on Items MS
            combo_item = check_item_enabled(sku, zone.upper(), environment.upper(), True)
            while combo_item == False:
                index_offers = randint(0, (len(product_offers) - 1))
                sku = product_offers[index_offers]['sku']
                combo_item = check_item_enabled(sku, zone.upper(), environment.upper(), True)

            combo_free_good.append(combo_item)
            auxIndex = auxIndex + 1

        response = input_combo_free_good_only(abi_id, zone, environment, combo_free_good)

        if response != "success":
            print(text.Red + "\n- [Combo] Something went wrong while creating the combo")
            printFinishApplicationMenu()


# Input credit account on microservice
def inputCreditAccountMicroserviceMenu():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == 'false':
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif len(account) == 0:
        print(text.Red + '\n- [Account] The account ' + abi_id + ' does not exist')
        printFinishApplicationMenu()

    credit = input(text.default_text_color + "Desire credit (Default 5000): ")
    balance = input(text.default_text_color + "Desire balance (Default 15000): ")

    # Call add credit to account function
    credit = add_credit_to_account_microservice(abi_id, zone.upper(), environment.upper(), credit, balance)

    if credit == "success":
        print(text.Green + "\n- Credit added successfully")
    else:
        print(text.Red + "\n- [Credit] Something went wrong, please try again")

    printFinishApplicationMenu()


def input_products_to_account_menu():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == 'false':
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif len(account) == 0:
        print(text.Red + '\n- [Account] The account ' + abi_id + ' does not exist')
        printFinishApplicationMenu()

    products = request_get_offers_microservice(abi_id, zone.upper(), environment.upper(), account[0]['deliveryCenterId'], True)

    proceed = 'N'
    if len(products) != 0:
        proceed = input(text.Yellow + '\n- [Account] The account ' + str(abi_id) + ' already have products, do you want to proceed? y/N: ').upper()
        if proceed == '':
            proceed = 'N'
    elif len(products) == 0:
        proceed = 'Y'
    else:
        printFinishApplicationMenu()

    if proceed == 'Y':
        # Call add products to account function
        add_products = add_products_to_account_microservice(abi_id, zone.upper(), environment.upper(), account[0]['deliveryCenterId'])
        if add_products != 'success':
            print(text.Red + '\n- [Products] Something went wrong, please try again')
            printFinishApplicationMenu()


def inputDeliveryWindowAccountMicroserviceMenu():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == 'false':
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif len(account) == 0:
        print(text.Red + '\n- [Account] The account ' + abi_id + ' does not exist')
        printFinishApplicationMenu()

    if zone == 'BR':
        # Validate if is alternative delivery window
        isAlternativeDeliveryDate = printAlternativeDeliveryDateMenu()

        if isAlternativeDeliveryDate.upper() == 'Y':
            isAlternativeDeliveryDate = 'true'
        else:
            isAlternativeDeliveryDate = 'false'
    else:
        isAlternativeDeliveryDate = 'false'

    # Call add delivery window to account function
    delivery_window = create_delivery_window_microservice(abi_id, zone.upper(), environment.upper(), account[0], isAlternativeDeliveryDate)

    if delivery_window == "success":
        print(text.Green + "\n- Delivery window added successfully")
    else:
        print(text.Red + "\n- [DeliveryWindow] Something went wrong, please try again")

    printFinishApplicationMenu()


# Create Account menu for Zones using MS
def create_account_menu():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)
    name = printNameMenu()
    payment_method = printPaymentMethodMenu(zone.upper())
    state = validate_state(zone)

    option_include = input(text.default_text_color + 'Do you want to include the minimum order parameter? y/N: ')
    while option_include == "" or validate_yes_no_option(option_include.upper()) == 'false':
        print(text.Red + '\n- Invalid option\n')
        option_include = input(text.default_text_color + 'Do you want to include the minimum order parameter? y/N: ')

    if option_include.upper() == 'Y':
        minimum_order = printMinimumOrderMenu()
    else:
        minimum_order = None

    # Call create account function
    create_account_response = create_account_ms(abi_id, name, payment_method, minimum_order, zone.upper(), environment.upper(), state)

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if create_account_response == 'success' and account != 'false' or len(account) != 0:
        print(text.Green + '\n- Your account has been created! Now register on Web or Mobile applications')
    else:
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()

    # Call add products to account function
    products = add_products_to_account_microservice(abi_id, zone.upper(), environment.upper(), account[0]['deliveryCenterId'])

    if products != 'success':
        print(text.Red + "\n\n- [Products] Something went wrong, please try again")
        printFinishApplicationMenu()

    if zone == 'BR':
        # Validate if is alternative delivery window
        isAlternativeDeliveryDate = printAlternativeDeliveryDateMenu()

        if isAlternativeDeliveryDate.upper() == 'Y':
            isAlternativeDeliveryDate = 'true'
        else:
            isAlternativeDeliveryDate = 'false'
    else:
        isAlternativeDeliveryDate = 'false'

    # Call add delivery window to account function
    delivery_window = create_delivery_window_microservice(abi_id, zone.upper(), environment.upper(), account[0], isAlternativeDeliveryDate)

    if delivery_window == 'success':
        print(text.Green + '\n- Delivery window added successfully')
    else:
        print(text.Red + '\n- [DeliveryWindow] Something went wrong, please try again')

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
        print(text.Red + "\n- The account doesn't exist.")
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
        print(text.Red + "\n- The account doesn't exist.")
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
def printAlternativeDeliveryDateMenu():
    isAlternativeDeliveryDate = input(text.default_text_color + "\nDo you want to register an alternative delivery date? y/N: ")
    while validateAlternativeDeliveryDate(isAlternativeDeliveryDate.upper()) == "false":
        print(text.Red + "\n- Invalid option")
        isAlternativeDeliveryDate = input(text.default_text_color + "\nDo you want to register an alternative delivery date? y/N: ")

    return isAlternativeDeliveryDate


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
        print(text.Red + "\n- The account doesn't exist.")
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


def create_invoice():
    zone = print_zone_menu_for_ms()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu(zone)

    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == 'false':
        print(text.Red + '\n- [Account] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif len(account) == 0:
        print(text.Red + '\n- [Account] The account ' + abi_id + ' does not exist')
        printFinishApplicationMenu()

    order_id = input('Order Id: ')
    order = order_info(abi_id, zone.upper(), environment.upper(), order_id)

    if order == 'false':
        print(text.Red + '\n- [Order] Something went wrong, please try again')
        printFinishApplicationMenu()
    elif order == '[]':
        print(text.Red + '\n- [Order] The Order Id ' + order_id + ' does not exist')
        printFinishApplicationMenu()

    invoice = create_invoice_request(abi_id, zone.upper(), environment.upper(), order_id)


# Init
try:
    if __name__ == '__main__':
        showMenu()

except KeyboardInterrupt:
    sys.exit(0)
