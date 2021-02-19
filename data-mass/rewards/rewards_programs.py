# Standard library imports
import json
from json import loads
import os
from random import randint

# Local application imports
from common import get_header_request, get_microservice_base_url, update_value_to_json, convert_json_to_string, \
    place_request, print_input_number, print_input_text, set_to_dictionary
from classes.text import text
from rewards.rewards_utils import display_all_programs_info, build_request_url_with_projection_query, get_dt_combos_from_zone, \
    create_product_list_from_zone


# Create Rewards Program
def create_new_program(zone, environment):

    # Verify if the zone already have a reward program created
    DM_program = get_DM_program_for_zone(zone, environment)

    if DM_program != None:
        program_id = DM_program['id']
        print(text.Yellow + '\n- [Rewards] This zone already have a reward program created - Program ID: "{}"'.format(program_id))
        return None

    response_zone_dt_combos = get_dt_combos_from_zone(zone, environment)

    # Verify if the zone has combos available
    if response_zone_dt_combos == None: return None
        
    product_list_from_zone = create_product_list_from_zone(zone, environment)

    # Verify if the zone has at least 20 SKUs available
    if len(product_list_from_zone) < 20:
        print(text.Red + '\n- [Rewards] The zone must have at least 20 products to proceed')
        return None

    # Generates the new Program ID
    new_program_id = 'DM-REWARDS-' + str(randint(100,900))

    balance = input(text.Yellow + '\nDo you want to create the program with initial balance (20.000)? y/N: ')
    balance = balance.upper()

    if balance == 'Y':
        initial_balance = 20000
    else:
        initial_balance = 0
    
    print(text.default_text_color + '\nCreating new Rewards program in ' + zone + ' - ' + environment + '. Please wait...')

    zone_dt_combos = loads(response_zone_dt_combos.text)
    
    premium_rule_skus = list()
    core_rule_skus = list()
    i = 0

    while i <= 9:
        # Getting 10 SKUs for premium rule
        premium_rule_skus.append(product_list_from_zone[i])

        # Getting 10 SKUs for core rule
        core_rule_skus.append(product_list_from_zone[i+10])
        i += 1

    # Getting all the basic information for the Program to be created
    generated_combos = generate_combos_information(zone_dt_combos)
    categories = generate_categories_information(zone)
    terms = generate_terms_information(zone)

    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, '../data/create_rewards_program_payload.json')

    # Load JSON file
    with open(file_path) as file:
        json_data = json.load(file)

    dict_values  = {
        'name' : new_program_id,
        'rules[0].moneySpentSkuRule.skus' : premium_rule_skus,
        'rules[1].moneySpentSkuRule.skus' : core_rule_skus,
        'combos' : generated_combos,
        'initialBalance' : initial_balance,
        'categories[0].categoryId' : categories[0],
        'categories[0].categoryIdWeb' : categories[1],
        'categories[0].description' : categories[2],
        'categories[0].buttonLabel' : categories[3],
        'categories[0].image' : categories[4],
        'categories[0].title' : 'Premium',
        'categories[0].subtitle' : categories[2],
        'categories[0].headerImage' : "https://cdn-b2b-abi.global.ssl.fastly.net/sit/images/br/redesign/premium/img-premium-chopp-brahma-logo@2x.png",
        'categories[0].brands' : [{
            "brandId": "123",
            "title": "premium brand",
            "image": "https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/premium/img_puntos_20.png"
        }],
        'categories[1].categoryId' : categories[5],
        'categories[1].categoryIdWeb' : categories[6],
        'categories[1].description' : categories[7],
        'categories[1].buttonLabel' : categories[8],
        'categories[1].image' : categories[9],
        'categories[1].title' : 'Core',
        'categories[1].subtitle' : categories[7],
        'categories[1].headerImage' : "https://cdn-b2b-abi.global.ssl.fastly.net/sit/images/br/redesign/core/img-core-brahmachopp-logo@2x.png",
        'categories[1].brands' : [{
            "brandId": "321",
            "title": "core brand",
            "image": "https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png"
        }],
        'termsAndConditions[0].documentURL' : terms[0],
        'termsAndConditions[0].changeLog' : terms[1]
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(json_data, key, dict_values[key])

    #Create body
    request_body = convert_json_to_string(json_object)

    # Send request
    return put_programs(new_program_id, zone, environment, request_body)


def update_dt_combos_rewards(zone, environment):

    all_programs = get_all_programs(zone, environment, set(["COMBOS"]))

    if all_programs == None: return None

    json_all_programs = loads(all_programs.text)
    display_all_programs_info(json_all_programs)

    selected_program = None
    while selected_program == None:
    
        program_id = print_input_text('\nPlease inform the Program ID')

        for program in json_all_programs:
            if program['id'].upper() == program_id.upper():
                selected_program = program
                break
        
        if selected_program == None: print(text.Red + '\n- Program "{}" not found!!'.format(program_id))

    # Get all the DT combos of the specified zone
    response_combos_from_zone = get_dt_combos_from_zone(zone, environment)

    if response_combos_from_zone == None: return None

    json_combos_from_zone = loads(response_combos_from_zone.text)
    zone_dt_combos = json_combos_from_zone['combos']

    # Get the DT combos configured in the rewards program
    program_dt_combos = selected_program['combos']

    missing_combos_list = missing_dt_combos_to_include(program_dt_combos, zone_dt_combos)

    if len(missing_combos_list) == 0:
        print("\nThere is nothing to update, please insert a DT combo first")
        return None
    
    update_program_combos = input(text.Yellow + '\n- Do you want to update the program configuration to include "{}" DT combos? y/N: '
        .format(str(len(missing_combos_list))))

    while update_program_combos.upper() != 'Y' and update_program_combos.upper() != 'N':
        print(text.Red + '\n- Invalid option!!')
        update_program_combos = input(text.Yellow + '\n- Do you want to update the program configuration to include "{}" DT combos? y/N: '
            .format(str(len(missing_combos_list)))) 
    
    if update_program_combos.upper() == 'Y':

        patch_combos_list = list()
        for j in range(len(missing_combos_list)):
            dict_combo = {
                'comboId': missing_combos_list[j],
                'points': 500
            }
            patch_combos_list.append(dict_combo)
        
        dict_patch_program_combos = set_to_dictionary(dict(), 'combos', patch_combos_list)

        request_body = convert_json_to_string(dict_patch_program_combos)

        return patch_program_combos(selected_program['id'], zone, environment, request_body)

    else:
        return None


# Patches the selected program root field
def patch_program_root_field(zone, environment, field):

    all_programs = get_all_programs(zone, environment, set(["DEFAULT"]))

    if all_programs != None:

        initial_balance = True if field == 'initial_balance' else False
        redeem_limit = True if field == 'redeem_limit' else False

        json_all_programs = loads(all_programs.text)
        display_all_programs_info(json_all_programs, initial_balance, redeem_limit)

        program_id = print_input_text('\nPlease inform the Program ID')

        dict_values_patch_program = dict()

        if initial_balance:
            new_balance = print_input_number('\nPlease inform the new balance amount (greater or equal zero)')
            while int(new_balance) < 0:
                print(text.Red + '\nInvalid value!! Must be greater or equal zero!!')
                new_balance = print_input_number('\nPlease inform the new balance amount (greater or equal zero)')
            
            set_to_dictionary(dict_values_patch_program, 'initialBalance', int(new_balance))
        
        elif redeem_limit:
            new_redeem_limit = print_input_number('\nPlease inform the new redeem limit value (greater than zero)')
            while int(new_redeem_limit) <= 0:
                print(text.Red + '\nInvalid value!! Must be greater than zero!!')
                new_redeem_limit = print_input_number('\nPlease inform the new redeem limit value (greater than zero)')
            
            set_to_dictionary(dict_values_patch_program, 'redeemLimit', int(new_redeem_limit))
       
        request_body = convert_json_to_string(dict_values_patch_program)

        return patch_program(program_id, zone, environment, request_body)

    else:
        return None


# Check if DM Rewards program exists for the zone
def get_DM_program_for_zone(zone, environment):

    DM_program = None

    # Send request
    response = get_all_programs(zone, environment, set(["DEFAULT"]))
    
    if response != None:

        program_list = loads(response.text)
        for i in range(len(program_list)):
            program_id = program_list[i]['id']
            preffix_program_id = program_id[0:9]

            if preffix_program_id == 'DM-REWARD':
                DM_program = program_list[i]
                break
    
    return DM_program


# Get all reward program for the zone
def get_all_programs(zone, environment, projections=set()):

    header_request = get_header_request(zone, 'true', 'false', 'false', 'false')
    
    # Define url request
    request_url = get_microservice_base_url(environment, 'false') + '/rewards-service/programs'

    request_url = build_request_url_with_projection_query(request_url, projections)
    
    # Send request
    response = place_request('GET', request_url, '', header_request)

    if response.status_code == 200:
        json_data = loads(response.text)
        if len(json_data) > 0:
            return response
        else:
            print(text.Red + '\n- [Rewards] There are no Reward programs available in "{}" zone.'.format(zone))

    else:
        print(text.Red + '\n- [Rewards] Failure when getting all programs in "{}" zone. \n- Response Status: "{}". \n- Response message "{}".'
                .format(zone, str(response.status_code), response.text))
    
    return None


# Get an specific reward program for the zone
def get_specific_program(program_id, zone, environment, projections=set()):

    header_request = get_header_request(zone, 'true', 'false', 'false', 'false')
    
    # Define url request
    request_url = get_microservice_base_url(environment, 'false') + '/rewards-service/programs/' + program_id

    request_url = build_request_url_with_projection_query(request_url, projections)
    
    # Send request
    response = place_request('GET', request_url, '', header_request)

    if response.status_code == 200:
        return response
    
    elif response.status_code == 404:
        print(text.Red + '\n- [Rewards] The Rewards program "{}" does not exist.'.format(program_id))

    else:
        print(text.Red + '\n- [Rewards] Failure when getting the program "{}" information. \n- Response Status: "{}". \n- Response message "{}".'
                .format(program_id, str(response.status_code), response.text))

    return None


def patch_program(program_id, zone, environment, request_body):

    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Define url request to patch the Rewards program selected
    request_url = get_microservice_base_url(environment, 'false') + '/rewards-service/programs/' + program_id

    # Send request
    response = place_request('PATCH', request_url, request_body, request_headers)

    if response.status_code == 200:
        print(text.Green + '\n- [Rewards] The Rewards program "{}" has been successfully updated.'.format(program_id))

    elif response.status_code == 404:
        print(text.Red + '\n- [Rewards] The Rewards program "{}" does not exist.'.format(program_id))

    else:
        print(text.Red + '\n- [Rewards] Failure when updating the program "{}" configuration. \n- Response Status: "{}". \n- Response message "{}".'
                .format(program_id, str(response.status_code), response.text))

    return response


def put_programs(program_id, zone, environment, request_body):

    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Define url request to patch the Rewards program selected
    request_url = get_microservice_base_url(environment, 'false') + '/rewards-service/programs/' + program_id

    # Send request
    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 200:
        print(text.Green + '\n- [Rewards] The Rewards program "{}" has been successfully created.'.format(program_id))

    else:
        print(text.Red + '\n- [Rewards] Failure when creating the program "{}". \n- Response Status: "{}". \n- Response message "{}".'
                .format(program_id, str(response.status_code), response.text))

    return response


def missing_dt_combos_to_include(program_dt_combos, zone_dt_combos):

    program_combos_list = list()
    for combo in program_dt_combos:
        program_combos_list.append(combo.get('comboId'))

    print(text.Yellow + '\n- Found "{}" DT combos configured for rewards program.'.format(str(len(program_dt_combos))))

    zone_combos_list = list()
    for combo in zone_dt_combos:
        zone_combos_list.append(combo.get('id'))

    print(text.Yellow + '\n- Found "{}" DT combos configured for the zone.'.format(str(len(zone_dt_combos))))

    missing_combos_list = list(set(zone_combos_list) - set(program_combos_list))
    
    print(text.Yellow + '\n- Found "{}" DT combos missing in the program configuration.'.format(str(len(missing_combos_list))))

    return missing_combos_list


def patch_program_combos(program_id, zone, environment, request_body):

    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Define url request to patch the Rewards program selected
    request_url = get_microservice_base_url(environment, 'false') + '/rewards-service/programs/' + program_id + '/combos'

    # Send request
    response = place_request('PATCH', request_url, request_body, request_headers)

    if response.status_code == 200:
        print(text.Green + '\n- [Rewards] The combos for Rewards program "{}" have been successfully updated.'.format(program_id))

    elif response.status_code == 404:
        print(text.Red + '\n- [Rewards] The Rewards program "{}" does not exist.'.format(program_id))

    else:
        print(text.Red + '\n- [Rewards] Failure when updating the program "{}" combos configuration. \n- Response Status: "{}". \n- Response message "{}".'
                .format(program_id, str(response.status_code), response.text))

    return response


# Generates the Combos for Rewards program
def generate_combos_information(zone_dt_combos):
    zone_dt_combos = zone_dt_combos['combos']
    combos_list = list()

    for i in range(len(zone_dt_combos)):
        points = i + 1

        dic_combos  = {
            'comboId' : zone_dt_combos[i]['id'],
            'points' : points * 250
        }

        combos_list.append(dic_combos)

    return combos_list


# Generates the Categories for Rewards program
def generate_categories_information(zone):
    category_info = list()
    
    if zone == 'DO':
        # Premium category
        category_info.append('96')
        category_info.append('94')
        category_info.append('Gana 100 puntos por cada RD $1000 pesos de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png')
        
        # Core category
        category_info.append('95')
        category_info.append('93')
        category_info.append('Gana 50 puntos por cada RD $1000 pesos de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png')
    elif zone == 'CO':
        # Premium category
        category_info.append('124')
        category_info.append('304')
        category_info.append('Gana 100 puntos por cada RD $1000 pesos de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png')
    
        # Core category
        category_info.append('123')
        category_info.append('261')
        category_info.append('Gana 50 puntos por cada RD $1000 pesos de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png')
    elif zone == 'AR':
        # Premium category
        category_info.append('582')
        category_info.append('494')
        category_info.append('Gana 100 puntos por cada RD $1000 pesos de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png')

        # Core category
        category_info.append('581')
        category_info.append('493')
        category_info.append('Gana 50 puntos por cada RD $1000 pesos de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/do/core/img_punto_1.png')
    elif zone == 'BR':
        # Premium category
        category_info.append('262')
        category_info.append('226')
        category_info.append('Ganhe 100 pontos para cada R$1000,00 gastos em compras e troque por produtos gratis.')
        category_info.append('COMPRAR AGORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/br/premium/img-premium-br-rules-2.png')

        # Core category
        category_info.append('272')
        category_info.append('236')
        category_info.append('Ganhe 50 pontos para cada R$1000,00 gastos em compras e troque por produtos gratis.')
        category_info.append('COMPRAR AGORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/br/premium/img-premium-br-rules-2.png')
    elif zone == 'ZA':
        # Premium category
        category_info.append('217')
        category_info.append('214')
        category_info.append('Earn 1 point for each R100 spent on quarts products.')
        category_info.append('BUY NOW')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/za/quarts-brands.png')

        # Core category
        category_info.append('219')
        category_info.append('216')
        category_info.append('Earn 10 points for each R100 spent on bonus products.')
        category_info.append('BUY NOW')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/za/bonus-brands.png')
    elif zone == 'MX':
        # Premium category
        category_info.append('9')
        category_info.append('1')
        category_info.append('Gana 1 punto por cada $10 de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/mx/core-brands.png')

        # Core category
        category_info.append('12')
        category_info.append('2')
        category_info.append('Gana 3 puntos por cada $10 de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/mx/premium-brands.png')
    elif zone == 'EC':
        # Premium category
        category_info.append('129')
        category_info.append('115')
        category_info.append('Gana 4 puntos por cada $1 de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/sit/images/ec/premium-brands.png')

        # Core category
        category_info.append('127')
        category_info.append('113')
        category_info.append('Gana 1 punto por cada $1 de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/ec/core-brands.png')
    elif zone == 'PE':
        # Premium category
        category_info.append('premium')
        category_info.append('premium')
        category_info.append('Gana 2 puntos por cada S/ 1.00 de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/pe/premium-brands.png')

        # Core category
        category_info.append('core')
        category_info.append('core')
        category_info.append('Gana 1 punto por cada S/ 1.00 de compra en estos productos')
        category_info.append('COMPRA AHORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/pe/core-brands.png')


    return category_info


# Generates the Terms and Conditions for Rewards program
def generate_terms_information(zone):
    terms_info = list()
    
    if zone == 'DO' or zone == 'CO' or zone == 'AR' or zone == 'MX' or zone == 'EC' or zone == 'PE':
        terms_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/terms/terms-co.html')
        terms_info.append('Términos iniciales introducidos al programa')
    elif zone == 'BR':
        terms_info.append('https://b2bstaticwebsagbdev.blob.core.windows.net/digitaltrade/terms/terms-br.html')
        terms_info.append('Termos iniciais introduzidos ao programa')
    elif zone == 'ZA':
        terms_info.append('https://cdn-b2b-abi-prod.global.ssl.fastly.net/prod/terms/terms-za.html')
        terms_info.append('Initial terms added to the program')

    return terms_info    