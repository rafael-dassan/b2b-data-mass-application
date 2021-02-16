# Standard library imports
import json
from json import loads
import os
from random import randint
from datetime import timedelta, datetime
from time import time

# Third party imports
from tabulate import tabulate

# Local application imports
from common import get_header_request, get_microservice_base_url, convert_json_to_string, place_request
from classes.text import text
from rewards.rewards_programs import get_DM_program_for_zone, get_specific_program


# Input transactions to a account
def input_transactions_to_account(account_id, zone, environment):

    # Define headers
    request_headers = get_header_request(zone, 'true', 'false', 'false', 'false', account_id)

    # Check if the zone already have a reward program created
    program_found = get_DM_program_for_zone(zone, environment)

    if program_found == 'false':
        return 'pgm_not_found'
    else:
         # Define url request
        request_url_offer = get_microservice_base_url(environment) + '/rewards-service/rewards/' + account_id + '/transaction/rewards-offer'
        request_url_redemption = get_microservice_base_url(environment) + '/rewards-service/rewards/' + account_id + '/transaction/redemption'

        body_offer = {
            "points": 1500,
            "campaignId": "BRZ8635",
            "description": "Bonus for customers signing up to Rewards Program from 5/1 to 31/1; Braze campaign ID BRZ8635"          
        }

        body_redemption = {
            "combos": [
                        {
                            "comboId": "DT_01",
                            "quantity": 5
                        }
                    ],
            "orderId": "546A456"
        }

        #Create bodys
        request_body_offer = convert_json_to_string(body_offer)
        request_body_redemption = convert_json_to_string(body_redemption)

        response_offer = place_request('POST', request_url_offer, request_body_offer, request_headers)
        response_redemption = place_request('POST', request_url_redemption, request_body_redemption, request_headers)

        if response_offer.status_code != 201:
             print(text.Red + '\n- [Rewards Service] Failure when input a offer transaction to account. Response Status: '
                            + str(response_offer.status_code) + '. Response message ' + response_offer.text)

        if response_redemption.status_code != 200:
             print(text.Red + '\n- [Rewards Service] Failure when input a redemption transaction to account. Response Status: '
                            + str(response_redemption.status_code) + '. Response message ' + response_redemption.text)   
        
        return 201 if response_offer.status_code == 201 and response_redemption.status_code == 200 else 'post_error'