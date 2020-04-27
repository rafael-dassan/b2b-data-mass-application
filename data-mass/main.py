from account import create_account, check_account_exists_middleware, create_account_ms, check_account_exists_microservice
from products import *
from credit import add_credit_to_account, add_credit_to_account_microservice
from delivery_window import create_delivery_window_middleware, create_delivery_window_microservice, validateAlternativeDeliveryDate
from beer_recommender import *
from inventory import *
from common import *
from classes.text import text
from random import randint
from combos import *
from deals import *
import user_creation_v2 as user_v2
import user_creation_v3 as user_v3

def showMenu():
    clearTerminal()
    printWelcomeScript()
    selectionStructure = printStructureMenu()
    option = printAvailableOptions(selectionStructure)
    if selectionStructure == "1":
        switcher = {
            "0": finishApplication,
            "1": createAccountMdwMenu,
            "2": inputProductsAccountMdwMenu,
            "3": inputCreditAccountMdwMenu,
            "4": inputDeliveryWindowAccountMdwMenu
        }
    elif selectionStructure == "2":
        switcher = {
            "0": finishApplication,
            "1": createAccountMsMenu,
            "2": inputProductsAccountMicroserviceMenu,
            "3": inputCreditAccountMicroserviceMenu,
            "4": inputDeliveryWindowAccountMicroserviceMenu,
            "5": inputBeerRecommenderAccountMicroserviceMenu,
            "6": inputInventoryToProduct,
            "7": inputDealsMenu,
            "8": inputCombosMenu,
            "9": createUserMsMenu,
            "10": registration_user_iam
        }
    else:
        finishApplication()

    function = switcher.get(option, "")
    if function != "":
        function()
    
    printFinishApplicationMenu()

# Input Inventory to a SKU
def inputInventoryToProduct():
    zone = print_zone_menu_for_inventory()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        printFinishApplicationMenu()

    # Call function to check if the account has products inside
    products_inventory_account = check_products_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if products_inventory_account == "success":
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
def inputBeerRecommenderAccountMicroserviceMenu():
    zone = print_zone_menu_for_recommender()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        printFinishApplicationMenu()

    # Call function to add Beer Recommender to the account
    beer_recommender = create_beer_recommender_microservice(abi_id, zone.upper(), environment.upper(), account[0]['deliveryCenterId'])

    if beer_recommender == "true":
        print(text.Green + "\n- [Algo Selling] All recommended products were added successfully")
        print(text.Yellow+ "\n- [Algo Selling] **  UP SELL TRIGGERS: Products Added to Cart: 03  /  Cart Viewed with Products: 01  **")
    else:
        if beer_recommender == "error25":
            print(text.Red + "\n- [Algo Selling] The account must have at least 25 enabled products to proceed")
            printFinishApplicationMenu()
        else:
            print(text.Red + "\n- [Algo Selling] Something went wrong, please try again")
            printFinishApplicationMenu()
            
# Input Deals to an account
def inputDealsMenu():
    selectionStructure = printDealsMenu()
    zone = print_zone_menu_for_deals()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu()

    switcher = {
        "1": "DISCOUNT",
        "2": "STEPPED_DISCOUNT",
        "3": "FREE_GOOD",
        "4": "STEPPED_FREE_GOOD"
    }

    deal_type = switcher.get(selectionStructure, "false")

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        printFinishApplicationMenu()

    accounts = list()
    accounts.append(abi_id)

    if zone.upper() == "ZA":
        # For Zones which use the middleware integration
        productOffers = request_get_offers_middleware(abi_id, zone.upper(), environment.upper())
    else:
        # For Zones which use the microservice integration
        productOffers = request_get_offers_microservice(abi_id, zone, environment, account[0]["deliveryCenterId"])

    if len(productOffers) == 0:
        print(text.Red + "\n- [Products] The account " + str(abi_id) + " has no available products for purchase")
        printFinishApplicationMenu()

    indexOffers = randint(0, (len(productOffers) - 1))
    sku = productOffers[indexOffers]

    # Check if the SKU is enabled on Items MS
    deal_sku = check_item_enabled(sku, zone.upper(), environment.upper())
    while deal_sku == False:
        indexOffers = randint(0, (len(productOffers) - 1))
        sku = productOffers[indexOffers]
        deal_sku = check_item_enabled(sku, zone.upper(), environment.upper())

    skus = list()
    skus.append(deal_sku)
    
    if selectionStructure == "1": 
        input_discount_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone.upper(), environment.upper())
    elif selectionStructure == "2":
        input_stepped_discount_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone.upper(), environment.upper()) 
    elif selectionStructure == "3":
        input_free_good_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone.upper(), environment.upper())
    else:
        input_stepped_free_good_to_account(abi_id, accounts, deal_sku, skus, deal_type, zone.upper(), environment.upper())

    printFinishApplicationMenu()
            
# Input combos by account
def inputCombosMenu():
    selectionStructure = printCombosMenu()
    zone = print_zone_menu_for_combos()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu()
    
    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        printFinishApplicationMenu()

    productOffers = request_get_offers_microservice(abi_id, zone, environment, account[0]['deliveryCenterId'])

    if len(productOffers) == 0:
        print(text.Red + "\n- [Products] The account " + str(abi_id) + " has no products available for purchase")
        printFinishApplicationMenu()

    indexOffers = randint(0, (len(productOffers) - 1))
    sku = productOffers[indexOffers]

    # Check if the SKU is enabled on Items MS
    combo_item = check_item_enabled(sku, zone.upper(), environment.upper())
    while combo_item == False:
        indexOffers = randint(0, (len(productOffers) - 1))
        sku = productOffers[indexOffers]
        combo_item = check_item_enabled(sku, zone.upper(), environment.upper())
    
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
            indexOffers = randint(0, (len(productOffers) - 1))
            sku = productOffers[indexOffers]

            # Check if the SKU is enabled on Items MS
            combo_item = check_item_enabled(sku, zone.upper(), environment.upper())
            while combo_item == False:
                indexOffers = randint(0, (len(productOffers) - 1))
                sku = productOffers[indexOffers]
                combo_item = check_item_enabled(sku, zone.upper(), environment.upper())

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
            indexOffers = randint(0, (len(productOffers) - 1))
            sku = productOffers[indexOffers]

            # Check if the SKU is enabled on Items MS
            combo_item = check_item_enabled(sku, zone.upper(), environment.upper())
            while combo_item == False:
                indexOffers = randint(0, (len(productOffers) - 1))
                sku = productOffers[indexOffers]
                combo_item = check_item_enabled(sku, zone.upper(), environment.upper())
                
            combo_free_good.append(combo_item)
            auxIndex = auxIndex + 1

        response = input_combo_free_good_only(abi_id, zone, environment, combo_free_good)

        if response != "success":
            print(text.Red + "\n- [Combo] Something went wrong while creating the combo")
            printFinishApplicationMenu()

# Input credit account on microservice
def inputCreditAccountMicroserviceMenu():
    zone = printZoneMenu("false")
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
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

def inputProductsAccountMicroserviceMenu():
    zone = printZoneMenu("false")
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu()
    
    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        printFinishApplicationMenu()
    
    products = check_products_account_exists_microservice(abi_id, zone.upper(), environment.upper())
    proceed = "n"
    if products == "success":
        proceed = input(text.Yellow + "\n- [Account] The account " + str(abi_id) + " already have products, do you want to proceed? y/N: ")
        if proceed == "":
            proceed = "n"
    elif products == "false":
        proceed = "y"
    else:
        print(text.Red + "\n- [Products] Something went wrong, please try again")
        printFinishApplicationMenu()

    if proceed.upper() == "Y":
        # Call add products to account function
        addProducts = add_products_to_account_microservice(abi_id, zone.upper(), environment.upper(), account[0]['deliveryCenterId'])
        if addProducts == "success":
            print(text.Green + "\n\n- Products added successfully")
        else:
            print(text.Red + "\n\n- [Products] Something went wrong, please try again")
            printFinishApplicationMenu()

def inputDeliveryWindowAccountMicroserviceMenu():
    zone = printZoneMenu("false")
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        printFinishApplicationMenu()
    
    # Validate if is alternative delivery window
    isAlternativeDeliveryDate = printAlternativeDeliveryDateMenu()

    if isAlternativeDeliveryDate.upper() == "Y":
        isAlternativeDeliveryDate = "true"
    else:
        isAlternativeDeliveryDate = "false"
    
    # Call add delivery window to account function
    delivery_window = create_delivery_window_microservice(abi_id, zone.upper(), environment.upper(), account[0], isAlternativeDeliveryDate)

    if delivery_window == "success":
        print(text.Green + "\n- Delivery window added successfully")
    else:
        print(text.Red + "\n- [DeliveryWindow] Something went wrong, please try again")

    printFinishApplicationMenu()

def inputDeliveryWindowAccountMdwMenu():
    zone = printZoneMenu()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu()

    # Call check account exists function
    account = check_account_exists_middleware(abi_id, zone.upper(), environment.upper())

    if account == "success":
        # Call add delivery window to account function
        delivery_window = create_delivery_window_middleware(abi_id, zone.upper(), environment.upper())
        if delivery_window == "success":
            print(text.Green + "\n- Delivery window added successfully")
        else:
            print(text.Red + "\n- [DeliveryWindow] Something went wrong, please try again")
            printFinishApplicationMenu()
    elif account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        printFinishApplicationMenu()
    else:
        print(text.Red + "\n- [Account] Something went wrong, please try again")
        printFinishApplicationMenu()

def inputCreditAccountMdwMenu():
    zone = printZoneMenu()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu()
    
    # Call check account exists function
    account = check_account_exists_middleware(abi_id, zone.upper(), environment.upper())

    if account == "success":
        credit = input(text.default_text_color + "Desire credit (Default 5000): ")
        balance = input(text.default_text_color + "Desire balance (Default 15000): ")

        # Call add credit to account function
        credit = add_credit_to_account(abi_id, zone.upper(), environment.upper(), credit, balance)
        if credit == "success":
            print(text.Green + "\n- Credit added successfully")
        else:
            print(text.Red + "\n- [Credit] Something went wrong, please try again")
            printFinishApplicationMenu()
    elif account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        printFinishApplicationMenu()
    else:
        print(text.Red + "\n- [Account] Something went wrong, please try again")
        printFinishApplicationMenu()

def inputProductsAccountMdwMenu():
    zone = printZoneMenu()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu()

    # Call check account exists function
    account = check_account_exists_middleware(abi_id, zone.upper(), environment.upper())

    if account == "success":
        products = check_products_account_exists_middleware(abi_id, zone.upper(), environment.upper())
        proceed = "n"
        if products == "success":
            proceed = input(text.Yellow + "\n- [Account] The account " + str(abi_id) + " already have products, do you want to proceed? y/N: ")
            if proceed == "":
                proceed = "n"
        elif products == "false":
            proceed = "y"
        else:
            print(text.Red + "\n- [Products] Something went wrong, please try again")
            printFinishApplicationMenu()

        if proceed.upper() == "Y":
            # Call add products to account function
            addProducts = add_products_to_account_middleware(abi_id, zone.upper(), environment.upper())
            if addProducts == "success":
                print(text.Green + "\n\n- Products added successfully")
            else:
                print(text.Red + "\n\n- [Products] Something went wrong, please try again")
                printFinishApplicationMenu()
    elif account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        printFinishApplicationMenu()
    else:
        print(text.Red + "\n- [Account] Something went wrong, please try again")
        printFinishApplicationMenu()

# Create Account menu for Zones using MDW
def createAccountMdwMenu():
    zone = printZoneMenu()
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu()
    name = printNameMenu()
    payment_method = printPaymentMethodMenu(zone.upper())
    state = validate_state(zone)

    option_include = input(text.default_text_color + "Do you want to include the minimum order parameter? y/N: ")
    while option_include == "" or validateYesOrNotOption(option_include.upper()) == "false":
        print(text.Red + "\n- Invalid option\n")
        option_include = input(text.default_text_color + "Do you want to include the minimum order parameter? y/N: ")

    if option_include.upper() == "Y":
        minimum_order = printMinimumOrderMenu()
    else:
        minimum_order = None

    # Call create account function
    account = create_account(abi_id, name, zone.upper(), payment_method, environment.upper(), minimum_order, state)

    if account == "success":
        print(text.Green + "\n- Your account has been created! Now register on Web or Mobile applications")
    else:
        print(text.Red + "\n- [Account] Something went wrong, please try again")
        printFinishApplicationMenu()

    # Call add products to account function
    products = add_products_to_account_middleware(abi_id, zone.upper(), environment.upper())

    if products == "success":
        print(text.Green + "\n\n- Products added successfully")
    else:
        print(text.Red + "\n\n- [Products] Something went wrong, please try again")
        printFinishApplicationMenu()

    credit = input(text.default_text_color + "Desire credit (Default 5000): ")
    balance = input(text.default_text_color + "Desire balance (Default 15000): ")

    # Call add credit to account function
    credit = add_credit_to_account(abi_id, zone.upper(), environment.upper(), credit, balance)

    if credit == "success":
        print(text.Green + "\n- Credit added successfully")
    else:
        print(text.Red + "\n- [Credit] Something went wrong, please try again")
        printFinishApplicationMenu()

    # Call add delivery window to account function
    delivery_window = create_delivery_window_middleware(abi_id, zone.upper(), environment.upper())

    if delivery_window == "success":
        print(text.Green + "\n- Delivery window added successfully")
    else:
        print(text.Red + "\n- [DeliveryWindow] Something went wrong, please try again")
        printFinishApplicationMenu()

    printFinishApplicationMenu()

# Create Account menu for Zones using MS
def createAccountMsMenu():
    zone = printZoneMenu("false")
    environment = printEnvironmentMenu()
    abi_id = print_account_id_menu()
    name = printNameMenu()
    payment_method = printPaymentMethodMenu(zone.upper())
    state = validate_state(zone)

    option_include = input(text.default_text_color + "Do you want to include the minimum order parameter? y/N: ")
    while option_include == "" or validateYesOrNotOption(option_include.upper()) == "false":
        print(text.Red + "\n- Invalid option\n")
        option_include = input(text.default_text_color + "Do you want to include the minimum order parameter? y/N: ")

    if option_include.upper() == "Y":
        minimum_order = printMinimumOrderMenu()
    else:
        minimum_order = None

    # Call create account function
    account = create_account_ms(abi_id, name, payment_method, minimum_order, zone.upper(), environment.upper(), state)

    if account == "success":
        print(text.Green + "\n- Your account has been created! Now register on Web or Mobile applications")
    else:
        print(text.Red + "\n- [Account] Something went wrong, please try again")
        printFinishApplicationMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        printFinishApplicationMenu()

    # Call add products to account function
    products = add_products_to_account_microservice(abi_id, zone.upper(), environment.upper(), account[0]['deliveryCenterId'])

    if products == "success":
        print(text.Green + "\n\n- Products added successfully")
    else:
        print(text.Red + "\n\n- [Products] Something went wrong, please try again")
        printFinishApplicationMenu()

    # Validate if it is alternative delivery window
    isAlternativeDeliveryDate = printAlternativeDeliveryDateMenu()

    if isAlternativeDeliveryDate.upper() == "Y":
        isAlternativeDeliveryDate = "true"
    else:
        isAlternativeDeliveryDate = "false"

    # Call add delivery window to account function
    delivery_window = create_delivery_window_microservice(abi_id, zone.upper(), environment.upper(), account[0], isAlternativeDeliveryDate)

    if delivery_window == "success":
        print(text.Green + "\n- Delivery window added successfully")
    else:
        print(text.Red + "\n- [DeliveryWindow] Something went wrong, please try again")

    printFinishApplicationMenu()


# Create User for zones in Microservice
def createUserMsMenu():
    country = printCountryMenuInUserCreation()
    env = printEnvironmentMenuInUserCreation()
    account_id = print_account_id_menu()
    email = print_input_email()
    password = print_input_password()

    account_id_list = user_v2.authenticate_user(env, country, email, password)

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

    status_response = user_v2.create_user(env, country, email, password, account_result[0])
    if status_response == "success":
        print(text.Green + "\n- User created successfully")
    else:
        print(text.Red + "\n- [User] Something went wrong, please try again")
        printFinishApplicationMenu()

    printFinishApplicationMenu()

# Print Finish Menu application
def printFinishApplicationMenu():
    finish = input(text.default_text_color + "\nDo you want to finish the application? y/N: ")
    while validateYesOrNotOption(finish.upper()) == "false":
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

    account_id = print_account_id_menu()
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

# Init
if __name__ == '__main__':
    showMenu()

