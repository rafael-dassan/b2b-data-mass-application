# Standard library imports
import json
from json import loads
import os
from datetime import timedelta, datetime
from time import time

# Local application imports
from common import get_header_request, get_microservice_base_url, update_value_to_json, convert_json_to_string, \
    place_request
from products import request_get_products_by_account_microservice
from classes.text import text
from rewards.rewards_programs import get_rewards_program_for_zone
from rewards.rewards_utils import generate_id


# Add Reward challenges to a zone
def input_challenge_to_zone(abi_id, zone, environment):
    # Verify if the zone already have a reward program created
    rewards_program = get_rewards_program_for_zone(zone, environment)
    if rewards_program is None:
        return None

    # Gets the account's SKUs to use only for challenge type = PURCHASE
    product_offers = request_get_products_by_account_microservice(abi_id, zone, environment)
    
    # Verify if the account has at least 10 SKUs inside for PURCHASE type
    if len(product_offers) > 10:
        offers_flag = 'true'
    else:
        offers_flag = 'false'  

    # Generates challenges - two of each type (take_photo, mark_complete, purchase and purchase_multiple)
    i = 1
    error_flag = 'false'
    while i <= 8:
        # Generates the new Program ID

        challenge_id = 'DM-CHALLENGE-' + generate_id()

        # Getting all the basic information to create the challenges
        if i == 1:
            generated_challenges = challenge_details(1)
        elif i == 3:
            generated_challenges = challenge_details(2)
        elif i == 5 and offers_flag == 'true':
            generated_challenges = challenge_details(3, product_offers)
        elif i == 7 and offers_flag == 'true':
            generated_challenges = challenge_details(4, product_offers)

        # Create file path
        path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(path, '../data/create_rewards_challenges_payload.json')

        # Load JSON file
        with open(file_path) as file:
            json_data = json.load(file)

        if i == 1 or i == 3:
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
        elif i == 2 or i == 4:
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
        elif (i == 5 or i == 7) and offers_flag == 'true':
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
        elif (i == 6 or i == 8) and offers_flag == 'true':
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
                print(text.Green + '\n- [Rewards] The new challenge has been successfully created. ID: ' + challenge_id)
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


def challenge_details(challenge_type, products = None):
    # Sets the format of the challenge's start date (current date and time)
    start_date = datetime.now()
    start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S')
    start_date = start_date + 'Z'

    # Sets the format of the challenge's end date with expiration within 5 days
    end_date_one = datetime.now() + timedelta(days=1)
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
    expired_end_date = datetime.now() - timedelta(days=1)
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

       # Details of the take photo #2 (already expired)
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

        # Details of the mark complete #2 (already expired)
        challenge_details.append('MARK COMPLETE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(expired_start_date)
        challenge_details.append(expired_end_date)
        challenge_details.append('https://cdn-b2b-abi.global.ssl.fastly.net/uat/images/br/challenges/1661/execution_2nd_display.jpg')
        challenge_details.append('MARK_COMPLETE')
        challenge_details.append('')
        challenge_details.append('')
    elif challenge_type == 3:
        if len(products) >= 10:
            dict_values_purchase = [
                {
                    'sku' : products[0]['sku'],
                    'quantity' : 2
                },
                {
                    'sku' : products[1]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[2]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[3]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[4]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[5]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[6]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[7]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[8]['sku'],
                    'quantity' : 2,
                },
                {
                    'sku' : products[9]['sku'],
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

        # Details of the purchase #2 (already expired)
        challenge_details.append('PURCHASE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(expired_start_date)
        challenge_details.append(expired_end_date)
        challenge_details.append('https://b2bstaticwebsagbprod.blob.core.windows.net/challenge/DO/images/afiche_12oz_PTE.jpg')
        challenge_details.append('PURCHASE')
        challenge_details.append('')
        challenge_details.append('')
        challenge_details.append(dict_values_purchase)

    elif challenge_type == 4:
        if len(products) >= 10:
            dict_values_purchase = [
                {
                    'sku' : products[0]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 0,
                    'itemImage': products[0]['itemImage'],
                    'itemName': products[0]['itemName'],
                    'price': products[0]['price'],
                    'container' : products[0]['container'],
                    'package': products[0]['package'],
                },
                {
                    'sku' : products[1]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 1,
                    'itemImage': products[1]['itemImage'],
                    'itemName': products[1]['itemName'],
                    'price': products[1]['price'],
                    'container' : products[1]['container'],
                    'package': products[1]['package'],
                },
                {
                    'sku' : products[2]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 2,
                    'itemImage': products[2]['itemImage'],
                    'itemName': products[2]['itemName'],
                    'price': products[2]['price'],
                    'container' : products[2]['container'],
                    'package': products[2]['package'],
                },
                {
                    'sku' : products[3]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 3,
                    'itemImage': products[3]['itemImage'],
                    'itemName': products[3]['itemName'],
                    'price': products[3]['price'],
                    'container' : products[3]['container'],
                    'package': products[3]['package'],
                },
                {
                    'sku' : products[4]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 4,
                    'itemImage': products[4]['itemImage'],
                    'itemName': products[4]['itemName'],
                    'price': products[4]['price'],
                    'container' : products[4]['container'],
                    'package': products[4]['package'],
                },
                {
                    'sku' : products[5]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 5,
                    'itemImage': products[5]['itemImage'],
                    'itemName': products[5]['itemName'],
                    'price': products[5]['price'],
                    'container' : products[5]['container'],
                    'package': products[5]['package'],
                },
                {
                    'sku' : products[6]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 6,
                    'itemImage': products[6]['itemImage'],
                    'itemName': products[6]['itemName'],
                    'price': products[6]['price'],
                    'container' : products[6]['container'],
                    'package': products[6]['package'],
                },
                {
                    'sku' : products[7]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 7,
                    'itemImage': products[7]['itemImage'],
                    'itemName': products[7]['itemName'],
                    'price': products[7]['price'],
                    'container' : products[7]['container'],
                    'package': products[7]['package'],
                },
                {
                    'sku' : products[8]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 8,
                    'itemImage': products[8]['itemImage'],
                    'itemName': products[8]['itemName'],
                    'price': products[8]['price'],
                    'container' : products[8]['container'],
                    'package': products[8]['package'],
                },
                {
                    'sku' : products[9]['sku'],
                    'quantity' : 2,
                    'quantityPurchased' : 9,
                    'itemImage': products[9]['itemImage'],
                    'itemName': products[9]['itemName'],
                    'price': products[9]['price'],
                    'container' : products[9]['container'],
                    'package': products[9]['package'],
                }
            ]
        else:
            dict_values_purchase = None

        # Details of the multiple purchase #1 (expiration within 30 days)
        challenge_details.append('MULTIPLE PURCHASE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(start_date)
        challenge_details.append(end_date_one)
        challenge_details.append('https://b2bstaticwebsagbprod.blob.core.windows.net/challenge/DO/images/afiche_12oz_PTE.jpg')
        challenge_details.append('PURCHASE_MULTIPLE')
        challenge_details.append('')
        challenge_details.append('')
        challenge_details.append(dict_values_purchase)

        # Details of the multiple purchase #2 (already expired)
        challenge_details.append('MULTIPLE PURCHASE')
        challenge_details.append('Complete this challenge and receive extra points')
        challenge_details.append(expired_start_date)
        challenge_details.append(expired_end_date)
        challenge_details.append('https://b2bstaticwebsagbprod.blob.core.windows.net/challenge/DO/images/afiche_12oz_PTE.jpg')
        challenge_details.append('PURCHASE_MULTIPLE')
        challenge_details.append('')
        challenge_details.append('')
        challenge_details.append(dict_values_purchase)

    return challenge_details