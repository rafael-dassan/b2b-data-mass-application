from json import dumps
import time
from datetime import date, datetime, timedelta
from products import *
from deals import *
from account import create_account_ms, check_account_exists_microservice, display_account_information
from random import *

# Create Rewards Program
def create_new_program(zone, environment):

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Verify if the zone already have a reward program created
    program_found = locate_program_for_zone(zone, environment, request_headers)

    if program_found != 'false':
        print(text.Yellow + '\n- [Rewards] This zone already have a reward program created - ID: ' + program_found)
        return 'error_found'

    print(text.default_text_color + '\nCreating new Rewards program in ' + zone + ' - ' + environment + '. Please wait...')

    # Generates the new Program ID
    reward_id = 'DM-REWARDS-' + str(randint(100,900))

    # Define url request
    request_url = get_microservice_base_url(environment) + '/rewards-service/programs/' + reward_id

    deals = request_get_deals_promo_fusion_service(zone, environment)

    # Verify if the zone has combos available
    if len(deals) > 0:

        balance = input(text.Yellow + '\nDo you want to create the program with an initial balance? y/N: ')
        balance = balance.upper()

        if balance == 'Y':
            initial_balance = 20000
        else:
            initial_balance = 0

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
            categories = generate_categories_information(zone)
            terms = generate_terms_information(zone)

            # Create file path
            path = os.path.abspath(os.path.dirname(__file__))
            file_path = os.path.join(path, 'data/create_rewards_program.json')

            # Load JSON file
            with open(file_path) as file:
                json_data = json.load(file)

            dict_values  = {
                'name' : reward_id,
                'rules[0].moneySpentSkuRule.skus' : sku_rules_premium,
                'rules[1].moneySpentSkuRule.skus' : sku_rules_core,
                'combos[0].comboId' : generated_combos[0],
                'combos[1].comboId' : generated_combos[1],
                'combos[2].comboId' : generated_combos[2],
                'combos[3].comboId' : generated_combos[3],
                'combos[4].comboId' : generated_combos[4],
                'initialBalance' : initial_balance,
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


# Enroll POC to a zone's reward program
def enroll_poc_to_program(account_id, zone, environment):

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

    # Check if the zone already have a reward program created
    program_found = locate_program_for_zone(zone, environment, request_headers)

    if program_found != 'false':

        # Define url request
        request_url = get_microservice_base_url(environment) + '/loyalty-business-service/rewards'

        dict_values  = {
            'accountId' : account_id
        }

        #Create body
        request_body = convert_json_to_string(dict_values)

        # Send request
        response = place_request('POST', request_url, request_body, request_headers)

        if response.status_code == 201:
            enroll_response = loads(response.text)
            print(text.Green + '\n- [Rewards] The account has been successfully enrolled to the program "' + enroll_response['programId'] + '"')
            return 'true'
        elif response.status_code == 406:
            turn_eligible = input(text.Yellow + '\nThis account is not eligible to any Reward program. Do you want to make it eligible now? y/N: ')
            turn_eligible = turn_eligible.upper()

            if turn_eligible == 'Y':
                account_eligible = make_account_eligible(account_id, zone, environment, request_headers)

                if account_eligible == 'true':
                    print(text.Green + '\n- [Rewards] The account is now eligible. Back to menu option "2" to resume the enrollment process')
                    return 'true'
                else:
                    return 'false'
        elif response.status_code == 409:
            print(text.Red + '\n- [Rewards] This account already have a Reward program enrolled to it')
            return 'true'
        else:
            return 'false'
    else:
        print(text.Red + '\n- [Rewards] This zone does not have a program created. Please use the menu option "1" to create it')
        return 'true'


# Make an account eligible to a Reward program
def make_account_eligible(abi_id, zone, environment, header_request):

    # Call check account exists function
    account = check_account_exists_microservice(abi_id, zone.upper(), environment.upper())

    if account != 'false':

        # Update the account's information with the right values to associate to a Reward program
        json_object = update_value_to_json(account, '[0][potential]', 'DM-POTENT')
        json_object = update_value_to_json(account, '[0][segment]', 'DM-SEG')
        json_object = update_value_to_json(account, '[0][subSegment]', 'DM-SUBSEG')

        # Get header request
        request_headers = get_header_request(zone, 'false', 'true', 'false', 'false')

        # Get base URL
        request_url = get_microservice_base_url(environment) + '/account-relay/'

        # Create body
        request_body = convert_json_to_string(json_object)

        # Place request
        response = place_request('POST', request_url, request_body, request_headers)

        if response.status_code == 202:
            return 'true'
        else:
            return 'false'


# Locate Rewards program previously created in the zone
def locate_program_for_zone(zone, environment, header_request):

    # Define url request
    request_url = get_microservice_base_url(environment) + '/rewards-service/programs/'
    
    # Send request
    response = place_request('GET', request_url, '', header_request)
    
    program_list = loads(response.text)

    program_found = 'false'

    for i in range(len(program_list)):
        program_id = program_list[i]['id']
        program_id = program_id[0:9]

        if program_id == 'DM-REWARD':
            program_found = program_list[i]['id']
            break
    
    return program_found


# Generates the Combos for Rewards program
def generate_combos_information(deals_list):
    combos = deals_list['combos']
    combos_id = list()

    for i in range(len(combos)):
        combos_id.append(combos[i]['id'])

    return combos_id


# Generates the SKUs for the rules for Rewards program
def generate_skus_for_rules(zone, environment):
    products = request_get_products_microservice(zone, environment)

    sku_rules = list()
    for i in range(len(products)):
        sku_rules.append(products[i]['sku'])

    return sku_rules


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
        category_info.append('0')
        category_info.append('0')
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
        category_info.append('272')
        category_info.append('236')
        category_info.append('Ganhe 100 pontos para cada R$1000,00 gastos em compras e troque por produtos gratis.')
        category_info.append('COMPRAR AGORA')
        category_info.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/br/premium/img-premium-br-rules-2.png')

        # Core category
        category_info.append('262')
        category_info.append('226')
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