import requests, sys, random, json

from random import randint

def generate_random_array(items_num, requests_num):
    return random.sample(range(1, 10000000), items_num*requests_num)

def generate_request(start, end, random_array):
    aux_array = []

    unique_body = {
        "accountId": "",
        "deliveryPlant": "DEPOT001",
        "itemId": "SKU001",
        "location": "CO",
        "action": "SAV",
        "subchannel": "TEST"
    }

    for i in range(start, end):
        unique_body = {
            "accountId": str(random_array[i]),
            "deliveryPlant": "DEPOT001",
            "itemId": "SKU001",
            "location": "CO",
            "action": "SAV",
            "subchannel": "TEST"
        }
        aux_array.append(unique_body)

    return aux_array

def send_requests(requests_num, items_num, headers, url, random_array):
    for i in range(0, requests_num):

        request_body = json.dumps(generate_request(i*items_num, (i+1)*items_num, random_array))

        response = requests.request(
            "POST",
            url,
            data=request_body,
            headers=headers
        )

        print response

if __name__ == '__main__':
    # Argument 1: number of items on each requests
    # Argument 2: number of requests to be send

    items_num = int(sys.argv[1])
    requests_num = int(sys.argv[2])

    headers = {
        "requestTraceId": "12341234",
        "Content-Type": "application/json",
        "Authorization": "Basic cm9vdDpyb290"
    }

    url = "https://abi-b2b-co-api-qa.azurewebsites.net/api/v5/CO/productexclusions"

    send_requests(requests_num, items_num, headers, url, generate_random_array(items_num, requests_num))
