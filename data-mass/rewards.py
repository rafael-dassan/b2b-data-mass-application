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

    balance = input(text.Yellow + '\nDo you want to create the program with initial balance ($20.000)? y/N: ')
    balance = balance.upper()

    if balance == 'Y':
        initial_balance = 20000
    else:
        initial_balance = 0

    # Generates the new Program ID
    reward_id = 'DM-REWARDS-' + str(randint(100,900))

    # Define url request
    request_url = get_microservice_base_url(environment) + '/rewards-service/programs/' + reward_id

    deals = request_get_dt_combos(zone, environment, request_headers)

    # Verify if the zone has combos available
    if len(deals) > 0:

        sku_rules = generate_skus_for_rules(zone, environment)

        # Verify if the zone has at least 20 SKUs available
        if len(sku_rules) >= 20:

            print(text.default_text_color + '\nCreating new Rewards program in ' + zone + ' - ' + environment + '. Please wait...')
            
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
                print(text.Green + '\n- [Rewards] The new program has been created successfully. ID: ' + reward_id + ' - Initial balance = ' + str(initial_balance))
                return 'true'
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


# Add Reward challenges to a zone
def input_challenge_to_zone(abi_id, zone, environment):

    # Gets the account's SKUs to use only for challenge type = PURCHASE
    product_offers = request_get_products_by_account_microservice(abi_id, zone, environment)
    
    # Verify if the account has at least 10 SKUs inside for PURCHASE type
    if len(product_offers) > 10:
        sku_list = list()
        counter_offers = 0
        while counter_offers < len(product_offers):
            sku_list.append(product_offers[counter_offers]['sku'])
            counter_offers += 1

        if counter_offers > 0:
            offers_flag = 'true'
        else:
            offers_flag = 'false'
    else:
        offers_flag = 'false'  

    # Generates six challenges - two of each type (take_photo, mark_complete and purchase)
    i = 1
    error_flag = 'false'
    while i <= 9:
        # Generates the new Program ID
        challenge_id = 'DM-CHALLENGE-' + str(randint(100,900))

        # Getting all the basic information to create the challenges
        if i == 1:
            generated_challenges = challenge_details(1)
        elif i == 4:
            generated_challenges = challenge_details(2)
        elif i == 7 and offers_flag == 'true':
            generated_challenges = challenge_details(3, sku_list)

        # Create file path
        path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(path, 'data/create_rewards_challenges.json')

        # Load JSON file
        with open(file_path) as file:
            json_data = json.load(file)

        if i == 1 or i == 4:
            dict_values  = {
                'title' : challenge_id,
                'description' : generated_challenges[0],
                'detailedDescription' : generated_challenges[1],
                'startDate' : generated_challenges[2],
                'endDate' : generated_challenges[3],
                'image' : generated_challenges[4],
                'executionMethod' : generated_challenges[5],
                'goodPhotoSample' : generated_challenges[6],
                'badPhotoSample' : generated_challenges[7]
            }
        elif i == 2 or i == 5:
            dict_values  = {
                'title' : challenge_id,
                'description' : generated_challenges[8],
                'detailedDescription' : generated_challenges[9],
                'startDate' : generated_challenges[10],
                'endDate' : generated_challenges[11],
                'image' : generated_challenges[12],
                'executionMethod' : generated_challenges[13],
                'goodPhotoSample' : generated_challenges[14],
                'badPhotoSample' : generated_challenges[15]
            }
        elif i == 3 or i == 6:
            dict_values  = {
                'title' : challenge_id,
                'description' : generated_challenges[16],
                'detailedDescription' : generated_challenges[17],
                'startDate' : generated_challenges[18],
                'endDate' : generated_challenges[19],
                'image' : generated_challenges[20],
                'executionMethod' : generated_challenges[21],
                'goodPhotoSample' : generated_challenges[22],
                'badPhotoSample' : generated_challenges[23]
            }   
        elif i == 7 and offers_flag == 'true':
            dict_values  = {
                'title' : challenge_id,
                'description' : generated_challenges[0],
                'detailedDescription' : generated_challenges[1],
                'startDate' : generated_challenges[2],
                'endDate' : generated_challenges[3],
                'image' : generated_challenges[4],
                'executionMethod' : generated_challenges[5],
                'goodPhotoSample' : generated_challenges[6],
                'badPhotoSample' : generated_challenges[7],
                'skus' : generated_challenges[8]
            }
        elif i == 8 and offers_flag == 'true':
            dict_values  = {
                'title' : challenge_id,
                'description' : generated_challenges[9],
                'detailedDescription' : generated_challenges[10],
                'startDate' : generated_challenges[11],
                'endDate' : generated_challenges[12],
                'image' : generated_challenges[13],
                'executionMethod' : generated_challenges[14],
                'goodPhotoSample' : generated_challenges[15],
                'badPhotoSample' : generated_challenges[16],
                'skus' : generated_challenges[17]
            }
        elif i == 9 and offers_flag == 'true':
            dict_values  = {
                'title' : challenge_id,
                'description' : generated_challenges[18],
                'detailedDescription' : generated_challenges[19],
                'startDate' : generated_challenges[20],
                'endDate' : generated_challenges[21],
                'image' : generated_challenges[22],
                'executionMethod' : generated_challenges[23],
                'goodPhotoSample' : generated_challenges[24],
                'badPhotoSample' : generated_challenges[25],
                'skus' : generated_challenges[26]
            }

        for key in dict_values.keys():
            json_object = update_value_to_json(json_data, key, dict_values[key])

        #Create body
        request_body = convert_json_to_string(json_object)

        # Define headers
        request_headers = get_header_request(zone, 'true', 'false', 'false', 'false')

        # Define url request
        request_url = get_microservice_base_url(environment) + '/rewards-service/challenges/' + challenge_id

        # Verify if the challenge is PURCHASE and the account has at least 10 SKUs inside
        if i <= 6 or (i >= 7 and offers_flag == 'true'):
            # Send request
            response = place_request('PUT', request_url, request_body, request_headers)

            if response.status_code == 200:
                print(text.Green + '\n- [Rewards] The new challenge has been created successfully. ID: ' + challenge_id)
            else:
                error_flag = 'true'

        i += 1

    if offers_flag == 'false':
        print(text.Yellow + '\n- [Rewards] The PURCHASE challenges could not be created. The specified account needs at least 10 SKUs inside for that')

    # Verify if all challenges were created succesfully or if some failed
    if error_flag == 'true':
        return 'false'
    else:
        return 'true'


def challenge_details(challenge_type, sku_ids = None):

    # Sets the format of the challenge's start date (current date and time)
    start_date = datetime.now()
    start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S')
    start_date = start_date + 'Z'

    # Sets the format of the challenge's end date with expiration within 30 days
    end_date_one = datetime.now() + timedelta(days=30)
    end_date_one = end_date_one.strftime('%Y-%m-%dT%H:%M:%S')
    end_date_one = end_date_one + 'Z'

    # Sets the format of the challenge's end date with expiration within 60 days
    end_date_two = datetime.now() + timedelta(days=60)
    end_date_two = end_date_two.strftime('%Y-%m-%dT%H:%M:%S')
    end_date_two = end_date_two + 'Z'

    # Sets the format of the challenge's past start date (for expired challenges)
    expired_start_date = datetime.now() - timedelta(days=60)
    expired_start_date = expired_start_date.strftime('%Y-%m-%dT%H:%M:%S')
    expired_start_date = expired_start_date + 'Z'

    # Sets the format of the challenge's end date already expired (for expired challenges)
    expired_end_date = datetime.now() - timedelta(days=30)
    expired_end_date = expired_end_date.strftime('%Y-%m-%dT%H:%M:%S')
    expired_end_date = expired_end_date + 'Z'

    challenge_details = list()

    if challenge_type == 1:
        # Details of the take photo #1 (expiration within 30 days)
        challenge_details.append('TAKE A PHOTO')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(start_date)
        challenge_details.append(end_date_one)
        challenge_details.append('https://b2bfilemgmtsagbtest.blob.core.windows.net/files-do/rewards-admin_challenge-image.png?sig=IzFb2Eo16gb61Y92j3qry%2BiC61kqijYPkAZxuqf4ESI%3D&se=3019-06-23T15%3A38%3A29Z&sv=2015-04-05&sp=r&sr=b')
        challenge_details.append('TAKE_PHOTO')
        challenge_details.append('https://b2bstaticwebsagbdev.blob.core.windows.net/digitaltrade/uat/images/br/challenges/1659/photo_of_cooler_ok.jpg')
        challenge_details.append('https://b2bstaticwebsagbdev.blob.core.windows.net/digitaltrade/uat/images/br/challenges/1659/photo_of_cooler_nok.jpg')
        
        # Details of the take photo #2 (expiration within 60 days)
        challenge_details.append('TAKE A PHOTO')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(start_date)
        challenge_details.append(end_date_two)
        challenge_details.append('https://b2bfilemgmtsagbtest.blob.core.windows.net/files-do/rewards-admin_challenge-image.png?sig=IzFb2Eo16gb61Y92j3qry%2BiC61kqijYPkAZxuqf4ESI%3D&se=3019-06-23T15%3A38%3A29Z&sv=2015-04-05&sp=r&sr=b')
        challenge_details.append('TAKE_PHOTO')
        challenge_details.append('https://b2bstaticwebsagbdev.blob.core.windows.net/digitaltrade/uat/images/br/challenges/1659/photo_of_cooler_ok.jpg')
        challenge_details.append('https://b2bstaticwebsagbdev.blob.core.windows.net/digitaltrade/uat/images/br/challenges/1659/photo_of_cooler_nok.jpg')

       # Details of the take photo #3 (already expired)
        challenge_details.append('TAKE A PHOTO')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(expired_start_date)
        challenge_details.append(expired_end_date)
        challenge_details.append('https://b2bfilemgmtsagbtest.blob.core.windows.net/files-do/rewards-admin_challenge-image.png?sig=IzFb2Eo16gb61Y92j3qry%2BiC61kqijYPkAZxuqf4ESI%3D&se=3019-06-23T15%3A38%3A29Z&sv=2015-04-05&sp=r&sr=b')
        challenge_details.append('TAKE_PHOTO')
        challenge_details.append('https://b2bstaticwebsagbdev.blob.core.windows.net/digitaltrade/uat/images/br/challenges/1659/photo_of_cooler_ok.jpg')
        challenge_details.append('https://b2bstaticwebsagbdev.blob.core.windows.net/digitaltrade/uat/images/br/challenges/1659/photo_of_cooler_nok.jpg')
    elif challenge_type == 2:
        # Details of the mark complete #1 (expiration within 30 days)
        challenge_details.append('MARK COMPLETE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(start_date)
        challenge_details.append(end_date_one)
        challenge_details.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/br/challenges/1661/execution_2nd_display.jpg')
        challenge_details.append('MARK_COMPLETE')
        challenge_details.append('')
        challenge_details.append('')
        
        # Details of the mark complete #2 (expiration within 60 days)
        challenge_details.append('MARK COMPLETE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(start_date)
        challenge_details.append(end_date_two)
        challenge_details.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/br/challenges/1661/execution_2nd_display.jpg')
        challenge_details.append('MARK_COMPLETE')
        challenge_details.append('')
        challenge_details.append('')

        # Details of the mark complete #3 (already expired)
        challenge_details.append('MARK COMPLETE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(expired_start_date)
        challenge_details.append(expired_end_date)
        challenge_details.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/br/challenges/1661/execution_2nd_display.jpg')
        challenge_details.append('MARK_COMPLETE')
        challenge_details.append('')
        challenge_details.append('')
    elif challenge_type == 3:
        if len(sku_ids) >= 10:
            dict_values_purchase = [
                {
                    'sku' : sku_ids[0],
                    'quantity' : 2
                },
                {
                    'sku' : sku_ids[1],
                    'quantity' : 2,
                },
                {
                    'sku' : sku_ids[2],
                    'quantity' : 2,
                },
                {
                    'sku' : sku_ids[3],
                    'quantity' : 2,
                },
                {
                    'sku' : sku_ids[4],
                    'quantity' : 2,
                },
                {
                    'sku' : sku_ids[5],
                    'quantity' : 2,
                },
                {
                    'sku' : sku_ids[6],
                    'quantity' : 2,
                },
                {
                    'sku' : sku_ids[7],
                    'quantity' : 2,
                },
                {
                    'sku' : sku_ids[8],
                    'quantity' : 2,
                },
                {
                    'sku' : sku_ids[9],
                    'quantity' : 2,
                }
            ]
        else:
            dict_values_purchase = None

        # Details of the purchase #1 (expiration within 30 days)
        challenge_details.append('PURCHASE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(start_date)
        challenge_details.append(end_date_one)
        challenge_details.append('https://b2bstaticwebsagbprod.blob.core.windows.net/challenge/DO/images/afiche_12oz_PTE.jpg')
        challenge_details.append('PURCHASE')
        challenge_details.append('')
        challenge_details.append('')
        challenge_details.append(dict_values_purchase)

        # Details of the purchase #2 (expiration within 60 days)
        challenge_details.append('PURCHASE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(start_date)
        challenge_details.append(end_date_two)
        challenge_details.append('https://b2bstaticwebsagbprod.blob.core.windows.net/challenge/DO/images/afiche_12oz_PTE.jpg')
        challenge_details.append('PURCHASE')
        challenge_details.append('')
        challenge_details.append('')
        challenge_details.append(dict_values_purchase)

        # Details of the purchase #3 (already expired)
        challenge_details.append('PURCHASE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(expired_start_date)
        challenge_details.append(expired_end_date)
        challenge_details.append('https://b2bstaticwebsagbprod.blob.core.windows.net/challenge/DO/images/afiche_12oz_PTE.jpg')
        challenge_details.append('PURCHASE')
        challenge_details.append('')
        challenge_details.append('')
        challenge_details.append(dict_values_purchase)

    return challenge_details

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


# Retrieve Digital Trade combos (DT Combos) for the specified zone
def request_get_dt_combos(zone, environment, header_request):

    # Define url request
    request_url = get_microservice_base_url(environment) + '/combos/?types=DT&includeDeleted=false&includeDisabled=false'
    
    # Send request
    response = place_request('GET', request_url, '', header_request)
    
    dt_combos_list = loads(response.text)

    return dt_combos_list


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