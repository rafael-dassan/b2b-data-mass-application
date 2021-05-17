# Standard library imports
import json
from datetime import datetime, timedelta, timezone
from random import randint, randrange

import pkg_resources

from data_mass.classes.text import text
# Local application imports
from data_mass.common import (
    convert_json_to_string,
    get_header_request,
    get_microservice_base_url,
    place_request,
    print_input_text,
    set_to_dictionary,
    update_value_to_json
    )
from data_mass.rewards.rewards_utils import (
    create_product_list_from_zone,
    display_all_challenges_info,
    format_datetime_to_str,
    generate_id,
    get_payload
    )

APP_ADMIN = 'membership'


def create_take_photo_challenge(zone, environment, challenge_id=None, is_expired=False):
    if challenge_id is None:
        challenge_id = generate_id()

    if is_expired is False:
        json_object = create_challenge_payload(challenge_id, 'TAKE_PHOTO')
    else:
        json_object = create_challenge_payload(challenge_id, 'TAKE_PHOTO', None, -30, -1)

    # Create body
    request_body = convert_json_to_string(json_object)

    return put_challenge(challenge_id, request_body, zone, environment)


def create_mark_complete_challenge(zone, environment, challenge_id=None, is_expired=False):
    if challenge_id is None:
        challenge_id = generate_id()

    if is_expired is False:
        json_object = create_challenge_payload(challenge_id, 'MARK_COMPLETE')
    else:
        json_object = create_challenge_payload(challenge_id, 'MARK_COMPLETE', None, -30, -1)

    # Create body
    request_body = convert_json_to_string(json_object)

    return put_challenge(challenge_id, request_body, zone, environment)


def create_purchase_challenge(zone, environment, is_multiple, challenge_id=None, is_expired=False):
    print(text.Yellow + f'\n- [Products] Verifying the list of available products for "{zone}" zone.')
    zone_skus_list = create_product_list_from_zone(zone, environment)

    if zone_skus_list is None:
        return None
    
    if len(zone_skus_list) == 0:
        print(text.Red + f'\n- [Rewards] There are no products available for "{zone}" zone.')
        return None

    if challenge_id is None:
        challenge_id = generate_id()

    execution_method = 'PURCHASE' if is_multiple is False else 'PURCHASE_MULTIPLE'

    if is_expired is False:
        json_object = create_challenge_payload(challenge_id, execution_method, zone_skus_list)
    else:
        json_object = create_challenge_payload(challenge_id, execution_method, zone_skus_list, -30, -1)
    
    # Create body
    request_body = convert_json_to_string(json_object)

    return put_challenge(challenge_id, request_body, zone, environment)


def create_challenge_payload(challenge_id, execution_method, zone_skus_list=None, start_date_timedelta=0, end_date_timedelta=180):
    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/create_rewards_challenges_payload.json"
    )
    json_data = json.loads(content.decode("utf-8"))

    start_date = datetime.now(timezone.utc) + timedelta(days=start_date_timedelta)
    start_date = format_datetime_to_str(start_date)

    end_date = datetime.now(timezone.utc) + timedelta(days=end_date_timedelta)
    end_date = format_datetime_to_str(end_date)

    dict_challenge = {
        'title': 'DM-' + challenge_id + ' (' + execution_method + ')',
        'description': execution_method + ' challenge created by data-mass',
        'points': randrange(500, 5000, 100),
        'startDate': start_date,
        'endDate': end_date,
        'executionMethod': execution_method
    }

    for key in dict_challenge.keys():
        json_object = update_value_to_json(json_data, key, dict_challenge[key])

    if execution_method == 'TAKE_PHOTO':
        good_photo = 'https://b2bstaticwebsagbdev.blob.core.windows.net/challenge-uat/DO/good-examples-photo-challenge/cooler_cerveza_ok.png'
        bad_photo = 'https://b2bstaticwebsagbdev.blob.core.windows.net/challenge-uat/DO/bad-examples-photo-challenge/cooler_cerveza_nok.png'

        set_to_dictionary(json_object, 'goodPhotoSample', good_photo)
        set_to_dictionary(json_object, 'badPhotoSample', bad_photo)

    if execution_method == 'PURCHASE' or execution_method == 'PURCHASE_MULTIPLE':
        sku_count = 4 if len(zone_skus_list) > 4 else len(zone_skus_list)

        challenge_sku_list = list()
        for i in range(sku_count):
            dict_challenge_sku  = {
                'sku' : zone_skus_list[i],
                'quantity' : randint(2, 5)
            }
            challenge_sku_list.append(dict_challenge_sku)

        set_to_dictionary(json_object, 'skus', challenge_sku_list)
    
    return json_object


def put_challenge(challenge_id, request_body, zone, environment):
    # Define headers
    request_headers = get_header_request(zone, True, False, False, False, None, APP_ADMIN + '-' + zone.lower())

    # Define url request
    request_url = get_microservice_base_url(environment, False) + '/rewards-service/challenges/' + challenge_id

    response = place_request('PUT', request_url, request_body, request_headers)

    if response.status_code == 200:
        print(text.Green + f'\n- [Rewards] The challenge "{challenge_id}" was successfully created.')

    else:
        print(text.Red + '\n- [Rewards] Failure when creating the challenge "{}".  \n- Response Status: "{}". \n- Response message "{}".'
                .format(challenge_id, str(response.status_code), response.text))

    return response


def remove_challenge(zone, environment):

    response_all_challenges = get_all_challenges(zone, environment)

    if response_all_challenges is None: return None

    json_all_challenges = json.loads(response_all_challenges.text)
    display_all_challenges_info(json_all_challenges)

    challenge_id = print_input_text('\nPlease inform the Challenge ID')
    return delete_challenge(challenge_id, zone, environment)


def delete_challenge(challenge_id, zone, environment):
    # Define headers
    request_headers = get_header_request(zone, True, False, False, False, None, APP_ADMIN + '-' + zone.lower())

    # Define url request
    request_url = get_microservice_base_url(environment, False) + '/rewards-service/challenges/' + challenge_id

    response = place_request('DELETE', request_url, '', request_headers)

    if response.status_code == 204:
        print(text.Green + f'\n- [Rewards] The challenge "{challenge_id}" was successfully deleted.')

    elif response.status_code == 404:
        print(text.Red + f'\n- [Rewards] The challenge "{challenge_id}" was not found.')

    else:
        print(text.Red + '\n- [Rewards] Failure when deleting the challenge "{}".  \n- Response Status: "{}". \n- Response message "{}".'
                .format(challenge_id, str(response.status_code), response.text))

    return response


# Get all challenges for the zone
def get_all_challenges(zone, environment):
    header_request = get_header_request(zone, True, False, False, False, None, APP_ADMIN + '-' + zone.lower())
    
    # Define url request
    request_url = get_microservice_base_url(environment, False) + '/rewards-service/challenges'
    
    # Send request
    response = place_request('GET', request_url, '', header_request)

    if response.status_code == 200:
        json_data = json.loads(response.text)
        if len(json_data) > 0:
            return response
        else:
            print(text.Red + f'\n- [Rewards] There are no challenges available in "{zone}" zone.')

    else:
        print(text.Red + '\n- [Rewards] Failure when getting all challenges in "{}" zone. \n- Response Status: "{}". \n- Response message '
                         '"{}".'.format(zone, str(response.status_code), response.text))
    
    return None


# Get an specific challenge for the zone
def get_specific_challenge(challenge_id, zone, environment):

    header_request = get_header_request(zone, True, False, False, False, None, APP_ADMIN + '-' + zone.lower())
    
    # Define url request
    request_url = get_microservice_base_url(environment, False) + '/rewards-service/challenges/' + challenge_id
    
    # Send request
    response = place_request('GET', request_url, '', header_request)

    if response.status_code == 200:
        return response
    
    elif response.status_code == 404:
        print(text.Red + f'\n- [Rewards] The challenge "{challenge_id}" was not found.')

    else:
        print(text.Red + '\n- [Rewards] Failure when getting the challenge "{}" information. \n- Response Status: "{}". \n- Response message "{}".'
                .format(challenge_id, str(response.status_code), response.text))

    return None
