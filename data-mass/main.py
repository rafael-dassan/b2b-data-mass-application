import os
import sys
import webbrowser

# Custom
from account import create_account, check_account_exists_middleware
from products import *
from credit import add_credit_to_account, add_credit_to_account_microservice
from delivery_window import create_delivery_window_middleware, create_delivery_window_microservice, validateAlternativeDeliveryDate
from account_ms import create_account_ms, check_account_exists_microservice
from discounts_ms import inputDiscountByPaymentMethod, inputDiscountByDeliveryDate, inputDiscountBySku, inputFreeGoodsSelection
from helper import *
from classes.text import text
from random import randint
from combos import *

def showMenu():
    clearTerminal()
    printWelcomeScript()
    selectionStructure = printStructureMenu()
    option = printAvailableOptions(selectionStructure)
    if selectionStructure == '1':
        switcher = {
            '0': finishApplication,
            '1': createAccountMdwMenu,
            '2': inputProductsAccountMdwMenu,
            '3': inputCreditAccountMdwMenu,
            '4': inputDeliveryWindowAccountMdwMenu
        }
    elif selectionStructure == '2':
        switcher = {
            '0': finishApplication,
            '1': createAccountMsMenu,
            '2': inputProductsAccountMicroserviceMenu,
            '3': inputCreditAccountMicroserviceMenu,
            '4': inputDeliveryWindowAccountMicroserviceMenu,
            '5': inputDiscountByPaymentMethodMenu,
            '6': inputDiscountByDeliveryDateMenu,
            '7': inputDiscountBySkuMenu,
            '8': inputFreeGoodsSelectionMenu,
            '9': inputCombosMenu,
        }
    elif selectionStructure == '3':
        switcher = {
            '0': finishApplication,
            '1': openWeb,
        }
    else:
        finishApplication()

    function = switcher.get(option, "")
    if function != '':
        function()
    
    printFinishApplicationMenu()

#Input combos by account
def inputCombosMenu():
    accounts = list()
    abi_id = input(text.White + "Input account ID to apply combos: ")
    zone = printZoneMenu('false')
    environment = printEnvironmentMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())
    if account == 'false':
        print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        printFinishApplicationMenu()
    
    accounts.append(abi_id)
    productOffers = request_get_offers_microservice(abi_id, zone, environment, account[0]['deliveryCenterId'])
    if len(productOffers) == 0:
        print(text.Red + '\n- [Product Offers] The account ' + str(abi_id) + ' has no products available for purchase')
        printFinishApplicationMenu()
    
    typeCombo = input(text.White + "Select which type of combo you want to register (1-Discount, 2-With Free Goods, 3-Only Free Goods): ")
    while (str(typeCombo) != '1') and (str(typeCombo) != '2') and (str(typeCombo) != '3'):
        print(text.Red + '\n- Invalid option')
        typeCombo = input(text.White + "Select which type of combo you want to register (1-Discount, 2-With Free Goods, 3-Only Free Goods): ")

    if (str(typeCombo) == '1'):

        skuCombo = None
        indexOffers = randint(0, (len(productOffers) - 1))
        skuCombo = productOffers[indexOffers]
        response = inputComboDiscount(accounts, zone, environment, skuCombo)
        if response == 'success':
            print(text.Green + '\n- Combo successfully registered.')
        else:
            print(text.Red + '\n- [Combo] Something went wrong, try again. (' + str(response) + ')')
            printFinishApplicationMenu()

    elif (str(typeCombo) == '2'):

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
        if response == 'success':
            print(text.Green + '\n- Combo successfully registered.')
        else:
            print(text.Red + '\n- [Combo] Something went wrong, try again. (' + str(response) + ')')
            printFinishApplicationMenu()
    
    else:

        skusFreeGoods = list()
        auxIndex = 0
        while auxIndex < 3:
            indexOffers = randint(0, (len(productOffers) - 1))
            skusFreeGoods.append(productOffers[indexOffers])
            auxIndex = auxIndex + 1
        
        response = inputComboOnlyFreeGoods(accounts, zone, environment, skusFreeGoods)
        if response == 'success':
            print(text.Green + '\n- Combo successfully registered.')
        else:
            print(text.Red + '\n- [Combo] Something went wrong, try again. (' + str(response) + ')')
            printFinishApplicationMenu()

# Input free goods selection by account
def inputFreeGoodsSelectionMenu():
    accounts = list()
    abi_id = input(text.White + "Input account ID to apply free goods selection: ")
    zone = printZoneMenu('false')
    environment = printEnvironmentMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())
    if account == 'false':
        print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        printFinishApplicationMenu()

    accounts.append(abi_id)
    productOffers = request_get_offers_microservice(abi_id, zone, environment, account[0]['deliveryCenterId'])
    if len(productOffers) == 0:
        print(text.Red + '\n- [Product Offers] The account ' + str(abi_id) + ' has no products available for purchase')
        printFinishApplicationMenu()

    minimumProductsPurchase = None
    while True:
        try:
            minimumProductsPurchase = int(input(text.White + "Quantity of the list of products that will result in the free goods selection (Recommended 1): "))
            if minimumProductsPurchase == 0:
                minimumProductsPurchase = 1
            break
        except ValueError:
            print(text.Red + '\n- Invalid value')

    minimumQuantityPurchase = None
    while True:
        try:
            minimumQuantityPurchase = int(input(text.White + "Value of minimum quantity purchase sku (Example: you need to buy 5 items of this sku to grant free goods access): "))
            if minimumQuantityPurchase == 0:
                minimumQuantityPurchase = 1
            break
        except ValueError:
            print(text.Red + '\n- Invalid value')
    
    quantitySkusChoice = None
    while True:
        try:
            quantitySkusChoice = int(input(text.White + "Define how many skus will be displayed for choosing free goods (Example: you can select from 4 different skus): "))
            if quantitySkusChoice == 0:
                quantitySkusChoice = 1
            break
        except ValueError:
            print(text.Red + '\n- Invalid value')
    
    quantitySkusEarn = None
    while True:
        try:
            quantitySkusEarn = int(input(text.White + "Define how many skus you will earn in the bonus (Example: you can earn and choose 3 skus): "))
            if quantitySkusEarn == 0:
                quantitySkusEarn = 1
            break
        except ValueError:
            print(text.Red + '\n- Invalid value')

    quantityMultiplierSku = None
    while True:
        try:
            quantityMultiplierSku = int(input(text.White + "Set the bonus gain multiplier (Example: for every 10 skus on the cart you can choose 1 sku): "))
            if quantityMultiplierSku == 0:
                quantityMultiplierSku = 1
            break
        except ValueError:
            print(text.Red + '\n- Invalid value')
    
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
    if response == 'success':
        print(text.Green + '\n- Rule of discount applied successfully.')
    else:
        print(text.Red + '\n- [Discount] Something went wrong, try again. (' + str(response) + ')')
        printFinishApplicationMenu()


# Input discount by sku
def inputDiscountBySkuMenu():
    accounts = list()
    abi_id = input(text.White + "Input account ID to apply discount by sku: ")
    zone = printZoneMenu('false')
    environment = printEnvironmentMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())
    if account == 'false':
        print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        printFinishApplicationMenu()

    accounts.append(abi_id)    
    productOffers = request_get_offers_microservice(abi_id, zone, environment, account[0]['deliveryCenterId'])
    if len(productOffers) == 0:
        print(text.Red + '\n- [Product Offers] The account ' + str(abi_id) + ' has no products available for purchase')
        printFinishApplicationMenu()
    
    listOffers = list()
    listSkuOffers = list()
    indexOffers = 0
    indexLineOffers = 0
    lineSku = ''
    print(text.White + 'List product offers')
    while (indexOffers < len(productOffers)):
        lineSku = lineSku + ' -- Sku: ' + productOffers[indexOffers] + ' -- '
        listSkuOffers.append(productOffers[indexOffers])
        indexOffers = indexOffers + 1
        indexLineOffers = indexLineOffers + 1        
        if indexLineOffers == 3:
            indexLineOffers = 0
            print(lineSku)
            print('\n')
            lineSku = ''
    
    sku = input(text.White + "Choose the sku to apply discount (enter one at a time): ")
    while validateSkuChosen(sku, listSkuOffers) == 'false':
        print(text.Red + '\n- The sku ' + str(sku) + ' it is invalid.')
        sku = input(text.White + "Choose the sku to apply discount (enter one at a time): ")

    listOffers.append(sku)
    moreSkus = input(text.White + "Do you want to apply this same rule to another sku: y/N ")
    while moreSkus.upper() != 'N':
        print(text.White + 'List product offers')
        while (indexOffers < len(productOffers)):
            lineSku = lineSku + ' -- Sku: ' + productOffers[indexOffers] + ' -- '
            indexOffers = indexOffers + 1
            indexLineOffers = indexLineOffers + 1
            listSkuOffers.append(productOffers[indexOffers])
            if indexLineOffers == 3:
                indexLineOffers = 0
                print(lineSku)
                print('\n')
                lineSku = ''
        
        sku = input(text.White + "Choose the sku to apply discount (enter one at a time): ")
        while validateSkuChosen(sku, listSkuOffers) == 'false':
            print(text.Red + '\n- The sku ' + str(sku) + ' it is invalid.')
            sku = input(text.White + "Choose the sku to apply discount (enter one at a time): ")

        listOffers.append(sku)
        moreSkus = input(text.White + "Do you want to apply this same rule to another sku: y/N ")
    
    typeDiscount = input(text.White + "What kind of discount do you want to apply (1- Percentage, 2- Fixed amount): ")
    while (int(typeDiscount) != 1 and int(typeDiscount) != 2):
        print(text.Red + '\n- Invalid option')
        typeDiscount = input(text.White + "What kind of discount do you want to apply (1- Percentage, 2- Fixed amount): ")

    valueDiscount = None
    if int(typeDiscount) == 1:
        while True:
            try:
                valueDiscount = float(input(text.White + "Value of percentage discount: "))
                break
            except ValueError:
                print(text.Red + '\n- Invalid value')
    else:
        while True:
            try:
                valueDiscount = float(input(text.White + "Value of amount: "))
                break
            except ValueError:
                print(text.Red + '\n- Invalid value')
    
    response = inputDiscountBySku(accounts, zone.upper(), environment.upper(), listOffers, int(typeDiscount), float(valueDiscount))
    if response == 'success':
        print(text.Green + '\n- Rule of discount applied successfully.')
    else:
        print(text.Red + '\n- [Discount] Something went wrong, try again. (' + str(response) + ')')
        printFinishApplicationMenu()

# Input discount account by delivery date
def inputDiscountByDeliveryDateMenu():
    accounts = list()
    abi_id = input(text.White + "Input account ID to apply discount by delivery date: ")
    zone = printZoneMenu('false')
    environment = printEnvironmentMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())
    if account == 'false':
        print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        printFinishApplicationMenu()

    accounts.append(abi_id)
    moreAccounts = input(text.White + "Do you want to apply this same rule to another account: y/N ")
    while moreAccounts.upper() != 'N':
        abi_id = input(text.White + "Input account ID to apply discount by payment method: ")
        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())
        if account == 'false':
            print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        else:
            accounts.append(abi_id)

        moreAccounts = input(text.White + "Do you want to apply this same rule to another account: y/N ")

    listDates = printDeliveryDateMenu()
    typeDiscount = input(text.White + "What kind of discount do you want to apply (1- Percentage, 2- Fixed amount): ")
    while (int(typeDiscount) != 1 and int(typeDiscount) != 2):
        print(text.Red + '\n- Invalid option')
        typeDiscount = input(text.White + "What kind of discount do you want to apply (1- Percentage, 2- Fixed amount): ")

    valueDiscount = None
    if int(typeDiscount) == 1:
        while True:
            try:
                valueDiscount = float(input(text.White + "Value of percentage discount: "))
                break
            except ValueError:
                print(text.Red + '\n- Invalid value')
    else:
        while True:
            try:
                valueDiscount = float(input(text.White + "Value of amount: "))
                break
            except ValueError:
                print(text.Red + '\n- Invalid value')

    response = inputDiscountByDeliveryDate(accounts, zone.upper(), environment.upper(), listDates[0], int(typeDiscount), float(valueDiscount))
    if response == 'success':
        print(text.Green + '\n- Rule of discount applied successfully.')
    else:
        print(text.Red + '\n- [Discount] Something went wrong, try again. (' + str(response) + ')')
        printFinishApplicationMenu()

# Input discount account by payment method
def inputDiscountByPaymentMethodMenu():
    accounts = list()
    abi_id = input(text.White + "Input account ID to apply discount by payment method: ")
    zone = printZoneMenu('false')
    environment = printEnvironmentMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())
    if account == 'false':
        print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        printFinishApplicationMenu()
    
    accounts.append(abi_id)
    moreAccounts = input(text.White + "Do you want to apply this same rule to another account: y/N ")
    while moreAccounts.upper() != 'N':
        abi_id = input(text.White + "Input account ID to apply discount by payment method: ")
        # Call check account exists function
        account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())
        if account == 'false':
            print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        else:
            accounts.append(abi_id)
        
        moreAccounts = input(text.White + "Do you want to apply this same rule to another account: y/N ")
    
    paymentMethod = printPaymentMethodMenu(zone.upper())
    typeDiscount = input(text.White + "What kind of discount do you want to apply (1- Percentage, 2- Fixed amount): ")
    while (int(typeDiscount) != 1 and int(typeDiscount) != 2):
        print(text.Red + '\n- Invalid option')
        typeDiscount = input(text.White + "What kind of discount do you want to apply (1- Percentage, 2- Fixed amount): ")
    
    valueDiscount = None
    if int(typeDiscount) == 1:
        while True:
            try:
                valueDiscount = float(input(text.White + "Value of percentage discount: "))
                break
            except ValueError:
                print(text.Red + '\n- Invalid value')
    else:
        while True:
            try:
                valueDiscount = float(input(text.White + "Value of amount: "))
                break
            except ValueError:
                print(text.Red + '\n- Invalid value')
    
    response = inputDiscountByPaymentMethod(accounts, zone.upper(), environment.upper(), paymentMethod.upper(), int(typeDiscount), float(valueDiscount))
    if response == 'success':
        print(text.Green + '\n- Rule of discount applied successfully.')
    else:
        print(text.Red + '\n- [Discount] Something went wrong, try again. (' + str(response) + ')')
        printFinishApplicationMenu()


#Input credit account on microservice
def inputCreditAccountMicroserviceMenu():
    abi_id = input("ID Account: ")
    zone = printZoneMenu('false')
    environment = printEnvironmentMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())
    if account == 'false':
        print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        printFinishApplicationMenu()
    
    # Call add credit to account function
    credit = add_credit_to_account_microservice(abi_id, zone.upper(), environment.upper())
    if credit == 'success':
        print(text.Green + '\n- Credit added successfully.')
    else:
        print(text.Red + '\n- [Credit] Something went wrong, try again. (' + str(credit) + ')')

    printFinishApplicationMenu()

def inputProductsAccountMicroserviceMenu():
    abi_id = input("ID Account: ")
    zone = printZoneMenu('false')
    environment = printEnvironmentMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())
    if account == 'false':
        print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        printFinishApplicationMenu()
    
    products = check_products_account_exists_microservice(abi_id, zone.upper(), environment.upper())
    proceed = "n"
    if products == 'success':
        proceed = input(text.Green + '\n- [Account] The account ' + str(abi_id) + ' already have products, do you want to proceed? (y/N):')
        if proceed == "":
            proceed = "n"
    elif products == 'false':
        proceed = "y"
    else:
        print(text.Red + '\n- [Products] Something went wrong, try again.')
        printFinishApplicationMenu()

    if proceed.upper() == "Y":
        # Call add products to account function
        addProducts = add_products_to_account_microservice(abi_id, zone.upper(), environment.upper(), account[0]['deliveryCenterId'])
        if addProducts == 'success':
            print(text.Green + '\n- Products added successfully.')
        else:
            print(text.Red + '\n- [Products] Something went wrong, try again.')
            printFinishApplicationMenu()

def inputDeliveryWindowAccountMicroserviceMenu():
    abi_id = input("ID Account: ")
    zone = printZoneMenu('false')
    environment = printEnvironmentMenu()

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())
    if account == 'false':
        print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        printFinishApplicationMenu()
    
    # Validate if is alternative delivery window
    isAlternativeDeliveryDate = printAlternativeDeliveryDateMenu()
    if isAlternativeDeliveryDate.upper() == 'Y':
        isAlternativeDeliveryDate = 'true'
    else:
        isAlternativeDeliveryDate = 'false'
    
    # Call add delivery window to account function
    delivery_window = create_delivery_window_microservice(abi_id, zone.upper(), environment.upper(), account[0], isAlternativeDeliveryDate)
    if delivery_window == 'success':
        print(text.Green + '\n- Delivery window added successfully.')
    else:
        print(text.Red + '\n- [DeliveryWindow] Something went wrong, try again. (' + str(delivery_window) + ')')

    printFinishApplicationMenu()

def inputDeliveryWindowAccountMdwMenu():
    abi_id = input("ID Account: ")
    zone = printZoneMenu()
    environment = printEnvironmentMenu()

    # Call check account exists function
    account = check_account_exists_middleware(abi_id, zone.upper(), environment.upper())
    if account == 'success':
        # Call add delivery window to account function
        delivery_window = create_delivery_window_middleware(abi_id, zone.upper(), environment.upper())
        if delivery_window == 'success':
            print(text.Green + '\n- Delivery window added successfully.')
        else:
            print(text.Red + '\n- [DeliveryWindow] Something went wrong, try again. (' + str(delivery_window) + ')')
            printFinishApplicationMenu()

    elif account == 'false':
        print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        printFinishApplicationMenu()

    else:
        print(text.Red + '\n- [Account] Something went wrong, try again. (' + str(account) + ')')
        printFinishApplicationMenu()

def inputCreditAccountMdwMenu():
    abi_id = input("ID Account: ")
    zone = printZoneMenu()
    environment = printEnvironmentMenu()

    # Call check account exists function
    account = check_account_exists_middleware(abi_id, zone.upper(), environment.upper())
    if account == 'success':
        # Call add credit to account function
        credit = add_credit_to_account(abi_id, zone.upper(), environment.upper())
        if credit == 'success':
            print(text.Green + '\n- Credit added successfully.')
        else:
            print(text.Red + '\n- [Credit] Something went wrong, try again. (' + str(credit) + ')')
            printFinishApplicationMenu()

    elif account == 'false':
        print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        printFinishApplicationMenu()

    else:
        print(text.Red + '\n- [Account] Something went wrong, try again. (' + str(account) + ')')
        printFinishApplicationMenu()

def inputProductsAccountMdwMenu():
    abi_id = input("ID Account: ")
    zone = printZoneMenu()
    environment = printEnvironmentMenu()

    # Call check account exists function
    account = check_account_exists_middleware(abi_id, zone.upper(), environment.upper())
    if account == 'success':
        products = check_products_account_exists_middleware(abi_id, zone.upper(), environment.upper())
        proceed = "n"
        if products == 'success':
            proceed = input(text.Green + '\n- [Account] The account ' + str(abi_id) + ' already have products, do you want to proceed? (y/N):')
            if proceed == "":
                proceed = "n"
        elif products == 'false':
            proceed = "y"
        else:
            print(text.Red + '\n- [Products] Something went wrong, try again.')
            printFinishApplicationMenu()

        if proceed.upper() == "Y":
            # Call add products to account function
            addProducts = add_products_to_account_middleware(abi_id, zone.upper(), environment.upper())
            if addProducts == 'success':
                print(text.Green + '\n- Products added successfully.')
            else:
                print(text.Red + '\n- [Products] Something went wrong, try again.')
                printFinishApplicationMenu()

    elif account == 'false':
        print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        printFinishApplicationMenu()

    else:
        print(text.Red + '\n- [Account] Something went wrong, try again. (' + str(account) + ')')
        printFinishApplicationMenu()

def createAccountMdwMenu():
    abi_id = printAccountIdMenu()
    name = printNameMenu()
    zone = printZoneMenu()
    environment = printEnvironmentMenu()

    # Call create account function
    account = create_account(abi_id, name, zone.upper(), environment.upper())

    if account == 'success':
        print(text.Green + '\n- Your account has been created! Now register on web or mobile application.')
    else:
        print(text.Red + '\n- [Account] Something went wrong, try again. (' + str(account) + ')')
        printFinishApplicationMenu()
    
    print('\n')

    # Call add products to account function
    products = add_products_to_account_middleware(abi_id, zone.upper(), environment.upper())

    if products == 'success':
        print(text.Green + '\n- Products added successfully.')
    else:
        print(text.Red + '\n- [Products] Something went wrong, try again.')
        printFinishApplicationMenu()
    
    print('\n')

    # Call add credit to account function
    credit = add_credit_to_account(abi_id, zone.upper(), environment.upper())

    if credit == 'success':
        print(text.Green + '\n- Credit added successfully.')
    else:
        print(text.Red + '\n- [Credit] Something went wrong, try again. (' + str(credit) + ')')
        printFinishApplicationMenu()
    
    print('\n')

    # Call add delivery window to account function
    delivery_window = create_delivery_window_middleware(abi_id, zone.upper(), environment.upper())

    if delivery_window == 'success':
        print(text.Green + '\n- Delivery window added successfully.')
    else:
        print(text.Red + '\n- [DeliveryWindow] Something went wrong, try again. (' + str(delivery_window) + ')')
        printFinishApplicationMenu()
    
    print ('\n')
    printFinishApplicationMenu()

def createAccountMsMenu():
    abi_id = printAccountIdMenu()
    name = printNameMenu()
    zone = printZoneMenu('false')
    environment = printEnvironmentMenu()

    # Call create account function
    account = create_account_ms(abi_id, name, zone.upper(), environment.upper())

    if account == 'success':
        print(text.Green + '\n- Your account has been created! Now register on web or mobile application.')
    else:
        print(text.Red + '\n- [Account] Something went wrong, try again. (' + str(account) + ')')
        printFinishApplicationMenu()

    print ('\n')

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())
    if account == 'false':
        print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        printFinishApplicationMenu()

    # Call add products to account function
    products = add_products_to_account_microservice(abi_id, zone.upper(), environment.upper(), account[0]['deliveryCenterId'])

    if products == 'success':
        print(text.Green + '\n- Products added successfully.')
    else:
        print(text.Red + '\n- [Products] Something went wrong, try again.')
        printFinishApplicationMenu()
    
    print('\n')
    
    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())
    if account == 'false':
        print(text.Red + '\n- [Account] The account ' + str(abi_id) + ' not exists')
        printFinishApplicationMenu()

    # Validate if is alternative delivery window
    isAlternativeDeliveryDate = printAlternativeDeliveryDateMenu()
    if isAlternativeDeliveryDate.upper() == 'Y':
        isAlternativeDeliveryDate = 'true'
    else:
        isAlternativeDeliveryDate = 'false'

    # Call add delivery window to account function
    delivery_window = create_delivery_window_microservice(abi_id, zone.upper(), environment.upper(), account[0], isAlternativeDeliveryDate)
    if delivery_window == 'success':
        print(text.Green + '\n- Delivery window added successfully.')
    else:
        print(text.Red + '\n- [DeliveryWindow] Something went wrong, try again. (' + str(delivery_window) + ')')

    print('\n')
    printFinishApplicationMenu()

# Open browse with correct environment
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

# Print finish menu application
def printFinishApplicationMenu():
    finish = input(
        text.White + "Desire finish the application n/Y: ")
    while validateYesOrNotOption(finish.upper()) == 'false':
        print(text.Red + '\n- Invalid option')
        finish = input(text.White + "Desire finish the application n/Y: ")

    if finish.upper() == 'Y':
        finishApplication()
    else:
        showMenu()

# Validate option to finish application
def validateYesOrNotOption(option):
    if option == 'Y' or option == 'N':
        return 'true'
    else:
        return 'false'

# Print alternative delivery date menu application
def printAlternativeDeliveryDateMenu():
    isAlternativeDeliveryDate = input("Want to register an alternative delivery date? (y/N)? ")
    while validateAlternativeDeliveryDate(isAlternativeDeliveryDate.upper()) == 'false':
        print(text.Red + '\n- Invalid option')
        isAlternativeDeliveryDate = input("Want to register an alternative delivery date? (y/N)? ")

    return isAlternativeDeliveryDate

# Validate if sku chosen it's valid
def validateSkuChosen(sku, listSkuOffers):
    countItems = 0
    while countItems < len(listSkuOffers):
        if listSkuOffers[countItems] == sku:
            return 'true'
        
        countItems = countItems + 1

    return 'false'

# Init 
showMenu()
