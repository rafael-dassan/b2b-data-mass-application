import sys
from json import dumps
import time
from datetime import date, datetime, timedelta
import calendar
from products import *


#Custom
#from helpers.common import *


# Create beer recommender in microservice
def create_beer_recommender_microservice(accountId, zone, environment, deliveryCenterId):
    # Define headers
    request_headers = get_header_request(zone, 'false', 'true')

    # Define url request
    request_url = get_microservice_base_url(environment) + "/global-recommendation-relay"

    # Retrieve all SKUs of the specified Account and DeliveryCenter IDs
    productOffers = request_get_offers_microservice(accountId, zone, environment, deliveryCenterId)

    # Check if the account has at least 25 SKUs added to it
    if len(productOffers) >= 25:

        print('\nAdding beer recommenders. Please wait...')

        # Get body request for Quick Order
        request_body_quick_order = create_file_request_quick_order(request_url, request_headers, accountId, zone, productOffers)

        # Get body request for Forgotten Items
        request_body_forgotten_items = create_file_request_forgotten_items(request_url, request_headers, accountId, zone, productOffers)

        # Get body request Sell Up
        request_body_sell_up = create_file_request_sell_up(request_url, request_headers, accountId, zone, productOffers)


        if (request_body_quick_order.status_code == 202 and request_body_quick_order.text != "[]"):
                quick_order = "true"
                print("\nQuick Order Items added successfull...")
        else:
                quick_order = "false"
                print(text.Red + "\n- [BeerRecommender] Failed to add Quick Order Items")

        if (request_body_forgotten_items.status_code == 202 and request_body_forgotten_items.text != "[]"):
                forgotten_items = "true"
                print("\nForgotten Items added successfull...")
        else:
                forgotten_items = "false"
                print(text.Red + "\n- [BeerRecommender] Failed to add Forgotten Items")

        if (request_body_sell_up.status_code == 202 and request_body_sell_up.text != "[]"):
                sell_up = "true"
                print("\nSell Up Items added successfull...")
        else:
                sell_up = "false"
                print(text.Red + "\n- [BeerRecommender] Failed to add Sell Up Items")

        if (quick_order == "true") and (forgotten_items == "true") and (sell_up == "true"):
            return "true"
        else:
            return "false"
    else:
        return "error25"


# Define JSON to submmit QUICK ORDER recommendation type
def create_file_request_quick_order(url, headers, abi_id, zone, productList):
    if (zone == "DO") or (zone == "CL") or (zone == "AR"):
        language = "es"
        text = "Pedido Facil"
        text_description = "Productos que ordenaste anteriormente.<link>Anadir todo al camion</link>"
    elif (zone == "BR"):
        language = "pt"
        text = "Pedido Facil"
        text_description = "Produtos comprados anteriormente"
    else:
        language = "en"
        text = "Quick Order"
        text_description = "Products ordered before"


    # Retrieve the first ten SKUs of the account
    sku = []
    auxIndex = 0
    while auxIndex <= 9:
        sku.append(productList[auxIndex])
        auxIndex = auxIndex + 1
    
    
    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "data/create_beer_recommender_payload.json")

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values  = {
        'recommendationId': "QUICK ORDER RECOMMENDATION FOR ACCOUNT " + str(abi_id),
        'useCase': "QUICK_ORDER",
        'useCaseId': abi_id,
        'items[0].sku': sku[0],
        'items[1].sku': sku[1],
        'items[2].sku': sku[2],
        'items[3].sku': sku[3],
        'items[4].sku': sku[4],
        'items[5].sku': sku[5],
        'items[6].sku': sku[6],
        'items[7].sku': sku[7],
        'items[8].sku': sku[8],
        'items[9].sku': sku[9],
        'descriptions[0].language': language,
        'descriptions[0].text': text,
        'descriptions[0].description': text_description
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])


    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    # Send request
    response = place_request("POST", url, request_body, headers)

    return response


# Define JSON to submmit FORGOTTEN ITEMS recommendation type
def create_file_request_forgotten_items(url, headers, abi_id, zone, productList):
    if (zone == "DO") or (zone == "CL") or (zone == "AR"):
        language = "es"
        text = "Productos Populares para Negocios como el tuyo"
        text_description = ""
    elif (zone == "BR"):
        language = "pt"
        text = "Produtos Populares para Negocios como o seu"
        text_description = ""
    else:
        language = "en"
        text = "Popular Products for Businesses like yours"
        text_description = ""


    #Retrieve the first ten SKUs after the eleven one of the account
    sku = []
    auxIndex = 10
    while auxIndex <= 19:
        sku.append(productList[auxIndex])
        auxIndex = auxIndex + 1
    
    
    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "data/create_beer_recommender_payload.json")

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values  = {
        'recommendationId': "FORGOTTEN ITEMS RECOMMENDATION FOR ACCOUNT " + str(abi_id),
        'useCase': "FORGOTTEN_ITEMS",
        'useCaseId': abi_id,
        'items[0].sku': sku[0],
        'items[1].sku': sku[1],
        'items[2].sku': sku[2],
        'items[3].sku': sku[3],
        'items[4].sku': sku[4],
        'items[5].sku': sku[5],
        'items[6].sku': sku[6],
        'items[7].sku': sku[7],
        'items[8].sku': sku[8],
        'items[9].sku': sku[9],
        'descriptions[0].language': language,
        'descriptions[0].text': text,
        'descriptions[0].description': text_description
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])


    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    # Send request
    response = place_request("POST", url, request_body, headers)

    return response

# Define JSON to submmit SELL UP recommendation type
def create_file_request_sell_up(url, headers, abi_id, zone, productList):
    if (zone == "DO") or (zone == "CL") or (zone == "AR"):
        language = "es"
        text = "Productos Populares para Negocios como el tuyo"
        text_description = "Los Productos mas Vendidos en tu Zona"
    elif (zone == "BR"):
        language = "pt"
        text = "Produtos Populares para Negocios como o seu"
        text_description = "Os Produtos mais Vendidos em tua região"
    else:
        language = "en"
        text = "Popular Products for Businesses like yours"
        text_description = "The Best Selling Products in your zone"
    

    #Retrieve the first five SKUs after the twenty one of the account
    sku = []
    auxIndex = 20
    while auxIndex <= 24:
        sku.append(productList[auxIndex])
        auxIndex = auxIndex + 1
    

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "data/create_beer_recommender_sell_up_payload.json")

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)


    dict_values  = {
        'recommendationId': "SELL UP RECOMMENDATION FOR ACCOUNT " + str(abi_id),
        'descriptions[0].language': language,
        'descriptions[0].text': text,
        'descriptions[0].description': text_description,
        'useCaseId': abi_id,
        'items[0].sku': sku[0],
        'items[1].sku': sku[1],
        'items[2].sku': sku[2],
        'items[3].sku': sku[3],
        'items[4].sku': sku[4]
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])


    # Create body
    list_dict_values = create_list(json_object)
    request_body = convert_json_to_string(list_dict_values)

    # Send request
    response = place_request("POST", url, request_body, headers)

    return response