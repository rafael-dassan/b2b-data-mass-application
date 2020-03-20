import webbrowser

# Custom
from account import create_account, check_account_exists_middleware, create_account_ms, check_account_exists_microservice
from products import *
from credit import add_credit_to_account, add_credit_to_account_microservice
from delivery_window import create_delivery_window_middleware, create_delivery_window_microservice, validateAlternativeDeliveryDate
from helpers.common import *
from helpers.dependencies_handling import *
from classes.text import text
from random import randint
from combos import *
from deals import *

def showMenu():
    clearTerminal()
    install_dependencies()
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
            "5": inputDealsMenu,
            "6": inputCombosMenu
        }
    elif selectionStructure == "3":
        switcher = {
            "0": finishApplication,
            "1": openWeb
        }
    else:
        finishApplication()

    function = switcher.get(option, "")
    if function != "":
        function()
    
    printFinishApplicationMenu()

# Input Deals to an account
def inputDealsMenu():
    selectionStructure = printDealsMenu()
    zone = printZoneMenu("false")
    environment = printEnvironmentMenu()
    abi_id = printAccountIdMenu(zone.upper())

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

    productOffers = request_get_offers_microservice(abi_id, zone, environment, account[0]['deliveryCenterId'])

    if len(productOffers) == 0:
        print(text.Red + "\n- [Products] The account " + str(abi_id) + " has no available products for purchase")
        printFinishApplicationMenu()

    indexOffers = randint(0, (len(productOffers) - 1))
    deal_sku = productOffers[indexOffers]

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
    zone = printZoneMenu("false")
    environment = printEnvironmentMenu()
    accounts = list()
    abi_id = printAccountIdMenu(zone.upper())
    
    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        printFinishApplicationMenu()
    
    accounts.append(abi_id)
    productOffers = request_get_offers_microservice(abi_id, zone, environment, account[0]['deliveryCenterId'])

    if len(productOffers) == 0:
        print(text.Red + "\n- [ProductOffers] The account " + str(abi_id) + " has no products available for purchase")
        printFinishApplicationMenu()
    
    typeCombo = input(text.White + "Select which type of combo you want to register (1-Discount, 2-With Free Goods, 3-Only Free Goods): ")

    while (str(typeCombo) != "1") and (str(typeCombo) != "2") and (str(typeCombo) != "3"):
        print(text.Red + "\n- Invalid option")
        typeCombo = input(text.White + "Select which type of combo you want to register (1-Discount, 2-With Free Goods, 3-Only Free Goods): ")

    if (str(typeCombo) == "1"):
        skuCombo = None
        indexOffers = randint(0, (len(productOffers) - 1))
        skuCombo = productOffers[indexOffers]
        response = inputComboDiscount(accounts, zone, environment, skuCombo)
        if response == "success":
            print(text.Green + "\n- Combo successfully registered")
        else:
            print(text.Red + "\n- [Combo] Something went wrong, please try again")
            printFinishApplicationMenu()

    elif (str(typeCombo) == "2"):
        skuCombo = None
        indexOffers = randint(0, (len(productOffers) - 1))
        skuCombo = productOffers[indexOffers]

        skusFreeGoods = list()
        auxIndex = 0
        while auxIndex < 3:
            indexOffers = randint(0, (len(productOffers) - 1))
            skusFreeGoods.append(productOffers[indexOffers])
            auxIndex = auxIndex + 1
        
        response = inputComboWithFreeGoods(accounts, zone, environment, skuCombo, skusFreeGoods)
        if response == "success":
            print(text.Green + "\n- Combo successfully registered")
        else:
            print(text.Red + "\n- [Combo] Something went wrong, please try again")
            printFinishApplicationMenu()
    
    else:
        skusFreeGoods = list()
        auxIndex = 0
        while auxIndex < 3:
            indexOffers = randint(0, (len(productOffers) - 1))
            skusFreeGoods.append(productOffers[indexOffers])
            auxIndex = auxIndex + 1
        
        response = inputComboOnlyFreeGoods(accounts, zone, environment, skusFreeGoods)
        if response == "success":
            print(text.Green + "\n- Combo successfully registered")
        else:
            print(text.Red + "\n- [Combo] Something went wrong, please try again")
            printFinishApplicationMenu()

# Input credit account on microservice
def inputCreditAccountMicroserviceMenu():
    zone = printZoneMenu("false")
    environment = printEnvironmentMenu()
    abi_id = printAccountIdMenu(zone.upper())

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        printFinishApplicationMenu()
    
    # Call add credit to account function
    credit = add_credit_to_account_microservice(abi_id, zone.upper(), environment.upper())

    if credit == "success":
        print(text.Green + "\n- Credit added successfully")
    else:
        print(text.Red + "\n- [Credit] Something went wrong, please try again")

    printFinishApplicationMenu()

def inputProductsAccountMicroserviceMenu():
    zone = printZoneMenu("false")
    environment = printEnvironmentMenu()
    abi_id = printAccountIdMenu(zone.upper())
    
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
    abi_id = printAccountIdMenu(zone.upper())

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
    abi_id = printAccountIdMenu(zone.upper())

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
    abi_id = printAccountIdMenu(zone.upper())
    
    # Call check account exists function
    account = check_account_exists_middleware(abi_id, zone.upper(), environment.upper())

    if account == "success":
        # Call add credit to account function
        credit = add_credit_to_account(abi_id, zone.upper(), environment.upper())
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
    abi_id = printAccountIdMenu(zone.upper())

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
    abi_id = printAccountIdMenu(zone.upper())
    name = printNameMenu()
    payment_method = printPaymentMethodMenu(zone.upper())

    option_include = input(text.White + "Do you want to include the minimum order parameter? y/N: ")
    while option_include == "" or validateYesOrNotOption(option_include.upper()) == "false":
        print(text.Red + "\n- Invalid option\n")
        option_include = input(text.White + "Do you want to include the minimum order parameter? y/N: ")

    if option_include.upper() == "Y":
        minimum_order = printMinimumOrderMenu()
    else:
        minimum_order = None

    # Call create account function
    account = create_account(abi_id, name, zone.upper(), payment_method, environment.upper(), minimum_order)

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

    # Call add credit to account function
    credit = add_credit_to_account(abi_id, zone.upper(), environment.upper())

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
    abi_id = printAccountIdMenu(zone.upper())
    name = printNameMenu()
    payment_method = printPaymentMethodMenu(zone.upper())

    option_include = input(text.White + "Do you want to include the minimum order parameter? y/N: ")
    while option_include == "" or validateYesOrNotOption(option_include.upper()) == "false":
        print(text.Red + "\n- Invalid option\n")
        option_include = input(text.White + "Do you want to include the minimum order parameter? y/N: ")

    if option_include.upper() == "Y":
        minimum_order = printMinimumOrderMenu()
    else:
        minimum_order = None

    # Call create account function
    account = create_account_ms(abi_id, name, payment_method, minimum_order, zone.upper(), environment.upper())

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
    
    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
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

# Open browser with correct environment
def openWeb():
    zone = printZoneMenu('false')
    environment = printEnvironmentMenu()
    if environment.upper() == "UAT":
        environment = "test"
        if zone.upper() == "AR":
            zone = "las-ar"
        elif zone.upper() == "CL":
            zone = "conv-cl-mitienda"
        elif zone.upper() == "DO":
            zone = "conv-micerveceria"
        elif zone.upper() == "ZA":
            zone = "conv-sabconnect"

    elif environment.upper() == "QA":
        environment = "qa-se"
        if zone.upper() == "AR":
            zone = "las-ar"
        elif zone.upper() == "CL":
            zone = "las-ch"
        elif zone.upper() == "DO":
            zone = "dr"

    url = "https://" + environment + "-" + zone.lower() + ".abi-sandbox.net"
    webbrowser.open(url)

# Print Finish Menu application
def printFinishApplicationMenu():
    finish = input(text.White + "\nDo you want to finish the application? y/N: ")
    while validateYesOrNotOption(finish.upper()) == "false":
        print(text.Red + "\n- Invalid option")
        finish = input(text.White + "\nDo you want to finish the application? y/N: ")

    if finish.upper() == "Y":
        finishApplication()
    else:
        showMenu()

# Print alternative delivery date menu application
def printAlternativeDeliveryDateMenu():
    isAlternativeDeliveryDate = input(text.White + "\nDo you want to register an alternative delivery date? y/N: ")
    while validateAlternativeDeliveryDate(isAlternativeDeliveryDate.upper()) == "false":
        print(text.Red + "\n- Invalid option")
        isAlternativeDeliveryDate = input(text.White + "\nDo you want to register an alternative delivery date? y/N: ")

    return isAlternativeDeliveryDate

# Validate if chosen sku is valid
def validateSkuChosen(sku, listSkuOffers):
    countItems = 0
    while countItems < len(listSkuOffers):
        if listSkuOffers[countItems] == sku:
            return "true"
        
        countItems = countItems + 1

    return "false"


# Init
if __name__ == '__main__':
    showMenu()