import os
import sys
import webbrowser

# Custom
from account import create_account, check_account_exists_middleware, create_account_ms, check_account_exists_microservice
from products import *
from credit import add_credit_to_account, add_credit_to_account_microservice
from delivery_window import create_delivery_window_middleware, create_delivery_window_microservice, validateAlternativeDeliveryDate
from discounts_ms import inputDiscountByPaymentMethod, inputDiscountByDeliveryDate, inputDiscountBySku, inputFreeGoodsSelection, inputSteppedDiscount, inputSteppedFreeGood
from helper import *
from classes.text import text
from random import randint
from combos import *

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
            "5": inputDiscountByPaymentMethodMenu,
            "6": inputDiscountByDeliveryDateMenu,
            "7": inputDiscountBySkuMenu,
            "8": inputFreeGoodsSelectionMenu,
            "9": inputSteppedDiscountMenu,
            "10": inputSteppedFreeGoodMenu,
            "11": inputCombosMenu 
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

# Input free goods selection by account
def inputFreeGoodsSelectionMenu():
    zone = printZoneMenu('false')
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

    minimumProductsPurchase = None
    while True:
        try:
            minimumProductsPurchase = int(input(text.White + "Quantity of products that will result in the free goods selection (Recommended 1): "))
            if minimumProductsPurchase == 0:
                minimumProductsPurchase = 1
            break
        except ValueError:
            print(text.Red + "\n- Invalid value")

    minimumQuantityPurchase = None
    while True:
        try:
            minimumQuantityPurchase = int(input(text.White + "Minimum quantity value (Example: you need to buy 5 items of this sku to grant free good access): "))
            if minimumQuantityPurchase == 0:
                minimumQuantityPurchase = 1
            break
        except ValueError:
            print(text.Red + "\n- Invalid value")
    
    quantitySkusChoice = None
    while True:
        try:
            quantitySkusChoice = int(input(text.White + "Define how many skus will be displayed for choosing free goods (Example: you can select from 4 different skus): "))
            if quantitySkusChoice == 0:
                quantitySkusChoice = 1
            break
        except ValueError:
            print(text.Red + "\n- Invalid value")
    
    quantitySkusEarn = None
    while True:
        try:
            quantitySkusEarn = int(input(text.White + "Define how many skus you will earn in the bonus (Example: you can earn and choose 3 skus): "))
            if quantitySkusEarn == 0:
                quantitySkusEarn = 1
            break
        except ValueError:
            print(text.Red + "\n- Invalid value")

    quantityMultiplierSku = None
    while True:
        try:
            quantityMultiplierSku = int(input(text.White + "Set the bonus gain multiplier (Example: for every 10 skus on the cart you can choose 1 sku): "))
            if quantityMultiplierSku == 0:
                quantityMultiplierSku = 1
            break
        except ValueError:
            print(text.Red + "\n- Invalid value")
    
    paymentMethod = printPaymentMethodMenu(zone.upper())

    skusPurchase = list()
    auxIndex = 0
    while auxIndex < minimumProductsPurchase:
        indexOffers = randint(0, (len(productOffers) - 1))
        skusPurchase.append(productOffers[indexOffers])
        auxIndex = auxIndex + 1
    
    skusFreeGoods = list()
    auxIndex = 0
    while auxIndex < quantitySkusChoice:
        indexOffers = randint(0, (len(productOffers) - 1))
        skusFreeGoods.append(productOffers[indexOffers])
        auxIndex = auxIndex + 1
    
    response = inputFreeGoodsSelection(accounts, zone.upper(), environment.upper(), int(minimumQuantityPurchase), int(quantitySkusEarn), int(quantityMultiplierSku), skusPurchase, skusFreeGoods, paymentMethod)
    if response == "success":
        print(text.Green + "\n- Rule of discount applied successfully")
    else:
        print(text.Red + "\n- [Discount] Something went wrong, please try again")
        printFinishApplicationMenu()

# Input stepped discount
def inputSteppedDiscountMenu():
    zone = printZoneMenu("false")
    environment = printEnvironmentMenu()
    accounts = list()
    skus = list()
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

    skuDiscount = None
    indexOffers = randint(0, (len(productOffers) - 1))
    skuDiscount = productOffers[indexOffers]
    skus.append(skuDiscount)

    response = inputSteppedDiscount(accounts, zone, environment, skus)
    if response == "success":
        print(text.Green + "\n- Stepped discount successfully registered")
    else:
        print(text.Red + "\n- [Discount] Something went wrong, please try again")
        printFinishApplicationMenu()

# Input stepped free good
def inputSteppedFreeGoodMenu():
    zone = printZoneMenu("false")
    environment = printEnvironmentMenu()
    accounts = list()
    skus = list()
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

    skuDiscount = None
    indexOffers = randint(0, (len(productOffers) - 1))
    skuDiscount = productOffers[indexOffers]
    skus.append(skuDiscount)

    response = inputSteppedFreeGood(accounts, zone, environment, skus)

    if response == "success":
        print(text.Green + "\n- Stepped free good successfully registered")
    else:
        print(text.Red + "\n- [Discount] Something went wrong, please try again")
        printFinishApplicationMenu()

# Input discount by sku
def inputDiscountBySkuMenu():
    accounts = list()
    zone = printZoneMenu("false")
    environment = printEnvironmentMenu()
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
    
    listOffers = list()
    listSkuOffers = list()
    indexOffers = 0
    indexLineOffers = 0
    lineSku = ""
    print(text.White + "List product offers")
    while (indexOffers < len(productOffers)):
        lineSku = lineSku + " -- Sku: " + productOffers[indexOffers] + " -- "
        listSkuOffers.append(productOffers[indexOffers])
        indexOffers = indexOffers + 1
        indexLineOffers = indexLineOffers + 1        
        if indexLineOffers == 3:
            indexLineOffers = 0
            print(lineSku)
            print("\n")
            lineSku = ""
    
    sku = input(text.White + "Choose the sku to apply discount (enter one at a time): ")
    while validateSkuChosen(sku, listSkuOffers) == "false":
        print(text.Red + "\n- The sku " + str(sku) + " is invalid")
        sku = input(text.White + "Choose the sku to apply discount (enter one at a time): ")

    listOffers.append(sku)
    moreSkus = input(text.White + "Do you want to apply this same rule to another sku? y/N: ")
    while moreSkus.upper() != "N":
        print(text.White + "List product offers")
        while (indexOffers < len(productOffers)):
            lineSku = lineSku + " -- Sku: " + productOffers[indexOffers] + " -- "
            indexOffers = indexOffers + 1
            indexLineOffers = indexLineOffers + 1
            listSkuOffers.append(productOffers[indexOffers])
            if indexLineOffers == 3:
                indexLineOffers = 0
                print(lineSku)
                print("\n")
                lineSku = ""
        
        sku = input(text.White + "Choose the sku to apply discount (enter one at a time): ")
        while validateSkuChosen(sku, listSkuOffers) == "false":
            print(text.Red + "\n- The sku " + str(sku) + " is invalid")
            sku = input(text.White + "Choose the sku to apply discount (enter one at a time): ")

        listOffers.append(sku)
        moreSkus = input(text.White + "Do you want to apply this same rule to another sku? y/N: ")
    
    typeDiscount = input(text.White + "What kind of discount do you want to apply (1- Percentage, 2- Fixed amount): ")
    while (int(typeDiscount) != 1 and int(typeDiscount) != 2):
        print(text.Red + "\n- Invalid option")
        typeDiscount = input(text.White + "What kind of discount do you want to apply (1- Percentage, 2- Fixed amount): ")

    valueDiscount = None
    if int(typeDiscount) == 1:
        while True:
            try:
                valueDiscount = float(input(text.White + "Value of discount percentage (%): "))
                break
            except ValueError:
                print(text.Red + "\n- Invalid value")
    else:
        while True:
            try:
                valueDiscount = float(input(text.White + "Value of discount amount: "))
                break
            except ValueError:
                print(text.Red + "\n- Invalid value")
    
    response = inputDiscountBySku(accounts, zone.upper(), environment.upper(), listOffers, int(typeDiscount), float(valueDiscount))
    if response == "success":
        print(text.Green + "\n- Rule of discount applied successfully")
    else:
        print(text.Red + "\n- [Discount] Something went wrong, please try again")
        printFinishApplicationMenu()

# Input discount account by delivery date
def inputDiscountByDeliveryDateMenu():
    accounts = list()
    zone = printZoneMenu("false")
    environment = printEnvironmentMenu()
    abi_id = printAccountIdMenu(zone.upper())

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account == "false":
        print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        printFinishApplicationMenu()

    accounts.append(abi_id)
    moreAccounts = input(text.White + "Do you want to apply this same rule to another account? y/N: ")
    while moreAccounts.upper() != "N":
        abi_id = printAccountIdMenu(zone.upper())
        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())
        if account == "false":
            print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        else:
            accounts.append(abi_id)

        moreAccounts = input(text.White + "Do you want to apply this same rule to another account? y/N: ")

    listDates = printDeliveryDateMenu()
    typeDiscount = input(text.White + "What kind of discount do you want to apply (1- Percentage, 2- Fixed amount): ")
    while (int(typeDiscount) != 1 and int(typeDiscount) != 2):
        print(text.Red + "\n- Invalid option")
        typeDiscount = input(text.White + "What kind of discount do you want to apply (1- Percentage, 2- Fixed amount): ")

    valueDiscount = None
    if int(typeDiscount) == 1:
        while True:
            try:
                valueDiscount = float(input(text.White + "Value of discount percentage (%): "))
                break
            except ValueError:
                print(text.Red + "\n- Invalid value")
    else:
        while True:
            try:
                valueDiscount = float(input(text.White + "Value of discount amount: "))
                break
            except ValueError:
                print(text.Red + "\n- Invalid value")

    response = inputDiscountByDeliveryDate(accounts, zone.upper(), environment.upper(), listDates[0], int(typeDiscount), float(valueDiscount))
    if response == "success":
        print(text.Green + "\n- Rule of discount applied successfully")
    else:
        print(text.Red + "\n- [Discount] Something went wrong, please try again")
        printFinishApplicationMenu()

# Input discount account by payment method
def inputDiscountByPaymentMethodMenu():
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
    moreAccounts = input(text.White + "Do you want to apply this same rule to another account? y/N: ")
    while moreAccounts.upper() != "N":
        abi_id = printAccountIdMenu(zone.upper())
        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())
        if account == "false":
            print(text.Red + "\n- [Account] The account " + str(abi_id) + " does not exist")
        else:
            accounts.append(abi_id)
        
        moreAccounts = input(text.White + "Do you want to apply this same rule to another account? y/N: ")
    
    paymentMethod = printPaymentMethodMenu(zone.upper())
    typeDiscount = input(text.White + "What kind of discount do you want to apply (1- Percentage, 2- Fixed amount): ")
    while (int(typeDiscount) != 1 and int(typeDiscount) != 2):
        print(text.Red + "\n- Invalid option")
        typeDiscount = input(text.White + "What kind of discount do you want to apply (1- Percentage, 2- Fixed amount): ")
    
    valueDiscount = None
    if int(typeDiscount) == 1:
        while True:
            try:
                valueDiscount = float(input(text.White + "Value of discount percentage (%): "))
                break
            except ValueError:
                print(text.Red + "\n- Invalid value")
    else:
        while True:
            try:
                valueDiscount = float(input(text.White + "Value of discount amount: "))
                break
            except ValueError:
                print(text.Red + "\n- Invalid value")
    
    response = inputDiscountByPaymentMethod(accounts, zone.upper(), environment.upper(), paymentMethod.upper(), int(typeDiscount), float(valueDiscount))
    if response == "success":
        print(text.Green + "\n- Rule of discount applied successfully")
    else:
        print(text.Red + "\n- [Discount] Something went wrong, please try again")
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
            print(text.Green + "\n- Products added successfully")
        else:
            print(text.Red + "\n- [Products] Something went wrong, please try again")
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
                print(text.Green + "\n- Products added successfully")
            else:
                print(text.Red + "\n- [Products] Something went wrong, please try again")
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

    # Call create account function
    account = create_account(abi_id, name, zone.upper(), environment.upper())

    if account == "success":
        print(text.Green + "\n- Your account has been created! Now register on Web or Mobile applications")
    else:
        print(text.Red + "\n- [Account] Something went wrong, please try again")
        printFinishApplicationMenu()

    # Call add products to account function
    products = add_products_to_account_middleware(abi_id, zone.upper(), environment.upper())

    if products == "success":
        print(text.Green + "\n- Products added successfully")
    else:
        print(text.Red + "\n- [Products] Something went wrong, please try again")
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

    # Call create account function
    account = create_account_ms(abi_id, name, zone.upper(), environment.upper())

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
        print(text.Green + "\n- Products added successfully")
    else:
        print(text.Red + "\n- [Products] Something went wrong, please try again")
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
    finish = input(
        text.White + "Do you want to finish the application? y/N: ")
    while validateYesOrNotOption(finish.upper()) == "false":
        print(text.Red + "\n- Invalid option")
        finish = input(text.White + "Do you want to finish the application? y/N: ")

    if finish.upper() == "Y":
        finishApplication()
    else:
        showMenu()

# Validate the option to finish application
def validateYesOrNotOption(option):
    if option == "Y" or option == "N":
        return "true"
    else:
        return "false"

# Print alternative delivery date menu application
def printAlternativeDeliveryDateMenu():
    isAlternativeDeliveryDate = input(text.White + "Do you want to register an alternative delivery date? y/N: ")
    while validateAlternativeDeliveryDate(isAlternativeDeliveryDate.upper()) == "false":
        print(text.Red + "\n- Invalid option")
        isAlternativeDeliveryDate = input(text.White + "Want to register an alternative delivery date? y/N: ")

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
showMenu()