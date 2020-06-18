import sys
from json import dumps
import time
from datetime import date, datetime, timedelta
import calendar
from products import *
from deals import *
from random import *

# Create Rewards Program
def create_new_program(zone, environment):

    # Generates the Program ID
    reward_id = 'DM-REWARDS-' + str(randint(100,900))

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Define url request
    request_url = get_microservice_base_url(environment) + '/rewards-service/programs/' + reward_id

    deals = request_get_deals_promo_fusion_service(zone, environment)

    # Verify if the zone has at least 5 combos available
    if len(deals) >= 5:
        
        print(text.default_text_color + '\nCreating new Rewards program in ' + zone + ' - ' + environment + '. Please wait...')

        sku_rules = generate_skus_for_rules(zone, environment)

        # Verify if the zone has at least 20 SKUs available
        if len(sku_rules) >= 20:
            sku_rules_premium = list()
            sku_rules_core = list()
            i = 0

            while i <= 9:
                # Getting 10 SKUs for premium rule
                sku_rules_premium.append(sku_rules[i])

                # Getting 10 SKUs for core rule
                sku_rules_core.append(sku_rules[i+10])
                i += 1

            # Getting all the basic information for the Program to be created
            generated_combos = generate_combos_information(deals)
            generated_potentials = generate_potential_information()
            generated_segments = generate_segment_information()
            generated_subsegments = generate_subsegment_information()
            categories = generate_categories_information(zone)
            terms = generate_terms_information(zone)

            # Create file path
            path = os.path.abspath(os.path.dirname(__file__))
            file_path = os.path.join(path, 'data/create_rewards_program.json')

            # Load JSON file
            with open(file_path) as file:
                json_data = json.load(file)

            dict_values  = {
                'name': reward_id,
                'rules[0].moneySpentSkuRule.skus': sku_rules_premium,
                'rules[1].moneySpentSkuRule.skus': sku_rules_core,
                'combos[0].comboId': generated_combos[0],
                'combos[1].comboId': generated_combos[1],
                'combos[2].comboId': generated_combos[2],
                'combos[3].comboId': generated_combos[3],
                'combos[4].comboId': generated_combos[4],
                'filter.potential': generated_potentials,
                'filter.segment': generated_segments,
                'filter.subsegment': generated_subsegments,
                'categories[0].description' : categories[0],
                'categories[0].buttonLabel' : categories[1],
                'categories[0].image' : categories[2],
                'categories[1].description' : categories[3],
                'categories[1].buttonLabel' : categories[4],
                'categories[1].image' : categories[5],
                'termsAndConditions[0].documentURL' : terms[0],
                'termsAndConditions[0].changeLog' : terms[1]
            }

            for key in dict_values.keys():
                json_object = update_value_to_json(json_data, key, dict_values[key])

            #Create body
            request_body = convert_json_to_string(json_object)

            # Send request
            response = place_request('PUT', request_url, request_body, request_headers)

            if response.status_code == 200:
                return reward_id
            else:
                return 'false'
        else:
            return 'error_len_sku'
    else:
        return 'error_len_combo'


# Generates the SKUs for the rules for Rewards program
def generate_skus_for_rules(zone, environment):
    products = request_get_products_microservice(zone, environment)

    sku_rules = list()
    for i in range(len(products)):
        sku_rules.append(products[i]['sku'])

    return sku_rules


# Generates the Combos for Rewards program
def generate_combos_information(deals_list):
    combos = deals_list['combos']
    combos_id = list()

    for i in range(len(combos)):
        combos_id.append(combos[i]['id'])

    return combos_id


# Generates the Potentials for Rewards program
def generate_potential_information():
    potential_id = list()
    
    i = 1
    while i <= 3:
        potential_id.append('DM-POT-' + str(randint(100,900)))
        i += 1

    return potential_id


# Generates the Segments for Rewards program
def generate_segment_information():
    segment_id = list()
    
    i = 1
    while i <= 3:
        segment_id.append('DM-SEG-' + str(randint(100,900)))
        i += 1

    return segment_id


# Generates the Sub-Segments for Rewards program
def generate_subsegment_information():
    subsegment_id = list()
    
    i = 1
    while i <= 3:
        subsegment_id.append('DM-SUBSEG-' + str(randint(100,900)))
        i += 1

    return subsegment_id


# Generates the Categories for Rewards program
def generate_categories_information(zone):
    category_info = list()
    
    if zone == 'DO' or zone == 'CO' or zone == 'AR':
        category_info.append('Gana 100 puntos por cada RD $1000 pesos de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png')
    
        category_info.append('Gana 50 puntos por cada RD $1000 pesos de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png')
    elif zone == 'BR':
        category_info.append('Ganhe 100 pontos para cada R$1000,00 gastos em compras e troque por produtos gratis.')
        category_info.append('COMPRAR AGORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/br/premium/img-premium-br-rules-2.png')

        category_info.append('Ganhe 50 pontos para cada R$1000,00 gastos em compras e troque por produtos gratis.')
        category_info.append('COMPRAR AGORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/br/premium/img-premium-br-rules-2.png')

    return category_info


# Generates the Terms and Conditions for Rewards program
def generate_terms_information(zone):
    terms_info = list()
    
    if zone == 'DO' or zone == 'CO' or zone == 'AR':
        terms_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/terms/terms-co.html')
        terms_info.append('Términos iniciales introducidos al programa')
    elif zone == 'BR':
        terms_info.append('https://b2bstaticwebsagbdev.blob.core.windows.net/digitaltrade/terms/terms-br.html')
        terms_info.append('Termos iniciais introduzidos ao programa')

    return terms_info