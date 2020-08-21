import time
from products import *
from json import loads


def create_all_recommendations(zone, environment, abi_id, products):
    # Get responses
    quick_order_response = request_quick_order(zone, environment, abi_id, products)
    sell_up_response = request_sell_up(zone, environment, abi_id, products)
    forgotten_items_response = request_forgotten_items(zone, environment, abi_id, products)

    if quick_order_response == 'success' and sell_up_response == 'success' and forgotten_items_response == 'success':
        return 'success'
    else:
        responses_list = [quick_order_response, sell_up_response, forgotten_items_response]
        for x in range(len(responses_list)):
            if responses_list[x].status_code != 202:
                print(text.Red + '\n- [Recommendation Relay Service] Failure to add recommendations. Response Status: '
                      + str(responses_list[x].status_code) + '. Response message ' + responses_list[x].text)
        return 'false'


# Define JSON to submmit QUICK ORDER recommendation type
def create_quick_order_payload(abi_id, zone, product_list):
    if zone == 'DO' or zone == 'CL' or zone == 'AR' or zone == 'CO':
        language = 'es'
        text = 'Pedido Facil'
        text_description = 'Productos que ordenaste anteriormente <link>Anadir todo al camion</link>'
    elif zone == 'BR':
        language = 'pt'
        text = 'Pedido Facil'
        text_description = 'Produtos comprados anteriormente <link>Adicionar todos itens ao carrinho</link>'
    else:
        language = 'en'
        text = 'Quick Order'
        text_description = 'Products ordered before <link>Add all items to cart</link>'

    # Retrieve the first ten SKUs of the account
    sku = list()
    aux_index = 0
    while aux_index <= 9:
        sku.append(product_list[aux_index])
        aux_index = aux_index + 1
    
    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_beer_recommender_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values  = {
        'recommendationId': 'DM-' + str(randint(1, 100000)),
        'useCase': 'QUICK_ORDER',
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

    return request_body


# Define JSON to submmit FORGOTTEN ITEMS recommendation type
def create_forgotten_items_payload(abi_id, zone, product_list):
    if zone == 'DO' or zone == 'CL' or zone == 'AR' or zone == 'CO':
        language = 'es'
        text = 'Productos Populares para Negocios como el tuyo'
        text_description = ''
    elif zone == 'BR':
        language = 'pt'
        text = 'Produtos Populares para Negocios como o seu'
        text_description = ''
    else:
        language = 'en'
        text = 'Popular Products for Businesses like yours'
        text_description = ''

    # Retrieve the first ten SKUs after the eleven one of the account
    sku = list()
    aux_index = 10
    while aux_index <= 19:
        sku.append(product_list[aux_index])
        aux_index = aux_index + 1
    
    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_beer_recommender_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values  = {
        'recommendationId': 'DM-' + str(randint(1, 100000)),
        'useCase': 'FORGOTTEN_ITEMS',
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

    return request_body


# Define JSON to submmit UP SELL recommendation type
def create_upsell_payload(abi_id, zone, product_list):
    if zone == 'DO' or zone == 'CL' or zone == 'AR' or zone == 'CO':
        language = 'es'
        text = 'Productos Populares para Negocios como el tuyo'
        text_description = 'Los Productos mas Vendidos en tu Zona'
    elif zone == 'BR':
        language = 'pt'
        text = 'Produtos Populares para Negocios como o seu'
        text_description = 'Os Produtos mais Vendidos em tua região'
    else:
        language = 'en'
        text = 'Popular Products for Businesses like yours'
        text_description = 'The Best Selling Products in your zone'
    
    # Retrieve the first five SKUs after the twenty one of the account
    sku = list()
    aux_index = 20
    while aux_index <= 24:
        sku.append(product_list[aux_index])
        aux_index = aux_index + 1
    
    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, 'data/create_beer_recommender_sell_up_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values  = {
        'recommendationId': 'DM-' + str(randint(1, 100000)),
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

    return request_body


def request_quick_order(zone, environment, abi_id, products):
    # Define headers
    request_headers = get_header_request_recommender(zone, environment)

    # Define url request 
    request_url = get_microservice_base_url(environment) + '/global-recommendation-relay'

    # Get body
    request_body = create_quick_order_payload(abi_id, zone, products)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)
    
    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Recommendation Relay Service] Failure to add recommendation. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def request_forgotten_items(zone, environment, abi_id, products):
    # Define headers
    request_headers = get_header_request_recommender(zone, environment)

    # Define url request
    request_url = get_microservice_base_url(environment) + '/global-recommendation-relay'

    # Get body
    request_body = create_forgotten_items_payload(abi_id, zone, products)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Recommendation Relay Service] Failure to add recommendation. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def request_sell_up(zone, environment, abi_id, products):
    # Define headers
    request_headers = get_header_request_recommender(zone, environment)

    # Define url request
    request_url = get_microservice_base_url(environment) + '/global-recommendation-relay'

    # Get body
    request_body = create_upsell_payload(abi_id, zone, products)

    # Send request
    response = place_request('POST', request_url, request_body, request_headers)

    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Recommendation Relay Service] Failure to add recommendation. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


# Define an exclusive header for Recommended Products
def get_header_request_recommender(zone, environment):
    # Define headers
    if environment == 'SIT':
        request_headers = get_header_request(zone, 'false', 'true')
    elif environment == 'UAT':
        switcher = {
            'ZA': 'UTC',
            'AR': 'America/Buenos_Aires',
            'DO': 'America/Santo_Domingo',
            'BR': 'America/Sao_Paulo',
            'CO': 'America/Bogota',
            'PE': 'America/Lima',
            'CL': 'America/Santiago',
            'MX': 'UTC'
        }

        timezone = switcher.get(zone, 'false')

        request_headers = {
            'Content-Type': 'application/json',
            'country': zone,
            'requestTraceId': str(uuid1()),
            'x-timestamp': str(int(round(time() * 1000))),
            'cache-control': 'no-cache',
            'timezone': timezone,
            'Authorization': 'Basic ZGV4dGVyOktZTVU5MndHUjNZaENlRHI='
        }
        
    return request_headers


def get_recommendation_by_account(abi_id, zone, environment, use_case):
    headers = get_header_request(zone, 'true')

    request_url = get_microservice_base_url(environment, 'true') + '/global-recommendation/?useCase=' + use_case + \
                  '&useCaseId=' + abi_id + '&useCaseType=ACCOUNT'

    response = place_request('GET', request_url, '', headers)

    recommendation_data = loads(response.text)

    if response.status_code == 200:
        content = recommendation_data['content']
        if len(content) != 0:
            return recommendation_data
        elif len(content) == 0:
            print(text.Yellow + '\n- [Global Recommendation Service] The account ' + abi_id
                  + ' does not have recommendation type ' + use_case)
            return 'not_found'
    else:
        print(text.Red + '\n- [Global Recommendation Service] Failure to retrieve a recommendation. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def delete_recommendation_by_id(environment, recommendation_data):
    recommendation_id = recommendation_data['content'][0]['id']

    headers = {
        'requestTraceId': str(uuid1()),
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3Nlc'
                         'nZpY2VzIiwiZXhwIjoxNjE2MjM5MDIyLCJpYXQiOjE1MTYyMzkwMjIsInVwZGF0ZWRfYXQiOjExMTExMTEsIm5hbWUiOi'
                         'J1c2VyQGFiLWluYmV2LmNvbSIsImFjY291bnRJRCI6IiIsInVzZXJJRCI6IjIxMTgiLCJyb2xlcyI6WyJST0xFX0FETUl'
                         'OIl19.Hpthi-Joez6m2lNiOpC6y1hfPOT5nvMtYdNnp5NqVTM'
    }

    request_url = get_microservice_base_url(environment, 'true') + '/global-recommendation/' + recommendation_id

    response = place_request('DELETE', request_url, '', headers)

    if response.status_code == 202:
        return 'success'
    else:
        print(text.Red + '\n- [Global Recommendation Service] Failure to delete a recommendation. Response Status: '
              + str(response.status_code) + '. Response message ' + response.text)
        return 'false'


def display_recommendations_by_account(zone, environment, abi_id):
    case_id = 'QUICK_ORDER&useCase=FORGOTTEN_ITEMS&useCase=CROSS_SELL_UP_SELL'
    data = get_recommendation_by_account(abi_id, zone, environment, case_id)
    recommender_list = list()
    if data == 'false' or data == 'not_found':
        dict_value = {
            'Quick Order': 'None',
            'Forgotten Items': 'None',
            'Up Sell Contextual Model': 'None'
        }
        recommender_list.append(dict_value)
        print(text.default_text_color + '\nRecommendations Information By Account')
        print(tabulate(recommender_list, headers='keys', tablefmt='grid'))
    else:
        recommendations = data['content']
        items_list = list()
        combo_list = list()
        for i in range(len(recommendations)):
            dict_value = {
                'Name': recommendations[i]['recommendationId'],
                'Use Case': recommendations[i]['useCase'],
                'Created Date': recommendations[i]['createdDate'],
                'Update Date': recommendations[i]['updatedDate']
            }
            recommender_list.append(dict_value)
            items = recommendations[i]['items']
            combos = recommendations[i]['combos']
            if len(items) == 0:
                items_value = {
                    'Recommendation': recommendations[i]['useCase'],
                    'Items': 'None'
                }
                items_list.append(items_value)
            else:
                for x in range(len(items)):
                    items_value = {
                        'Recommendation': recommendations[i]['useCase'],
                        'SKU': items[x]['sku'],
                        'Quantity': items[x]['quantity'],
                        'Score': items[x]['score']
                    }
                    items_list.append(items_value)
            if len(combos) == 0:
                combos_value = {
                    'Recommendation': recommendations[i]['useCase'],
                    'Combos': 'None'
                }
                combo_list.append(combos_value)
            else:
                for z in range(len(combos)):
                    combos_value = {
                        'Recommendation': recommendations[i]['useCase'],
                        'ID Combo': combos[z]['id'],
                        'Quantity': combos[z]['quantity'],
                        'Score': combos[z]['score'],
                        'Type': combos[z]['type']
                    }
                    combo_list.append(combos_value)

        print(text.default_text_color + '\nRecommendations Information By Account')
        print(tabulate(recommender_list, headers='keys', tablefmt='grid'))

        print(text.default_text_color + '\nItems Recommendations Information By Account')
        print(tabulate(items_list, headers='keys', tablefmt='grid'))

        print(text.default_text_color + '\nCombos Recommendations Information By Account')
        print(tabulate(combo_list, headers='keys', tablefmt='grid'))
