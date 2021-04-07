# Standard library imports
from random import randint

# Third party imports
from requests import request

# Local application imports
from data_mass.classes.text import text
from data_mass.common import get_header_request, \
    get_microservice_base_url, set_to_dictionary, \
    remove_from_dictionary
from data_mass.logger import log_to_file


def create_file_api(zone, environment, account_id, purpose, data):
    """
    Create file through the File Management Service
    Args:
        zone: e.g., ZA, BR
        environment: e.g., DEV, SIT, UAT
        account_id: POC unique identifier
        purpose: e.g., invoice, bank-slip, credit-statement
        data: specific file data according to the purpose

    Returns: `false` in case of failure
    """
    file = {'file': ('random-file.pdf', open('data/files/random-file.pdf', 'rb'), 'application/pdf')}
    file_id = str(randint(1, 100000))
    metadata = get_file_metadata(account_id, purpose, data)
    title = '{file_id}-{purpose}-{account_id}'.format(file_id=file_id, purpose=purpose, account_id=account_id)

    # Define headers
    request_headers = get_header_request(zone, True, False, False, False, account_id)
    set_to_dictionary(request_headers, 'linkExpirationTime', str(-1))
    set_to_dictionary(request_headers, 'metadata', metadata)
    set_to_dictionary(request_headers, 'purpose', purpose)
    set_to_dictionary(request_headers, 'title', title)
    set_to_dictionary(request_headers, 'expiresAt', '')
    remove_from_dictionary(request_headers, 'Content-Type')

    # Define url request
    request_url = get_microservice_base_url(environment) + '/files/upload'

    # Send request
    response = request('POST', request_url, files=file, headers=request_headers)
    log_to_file(
        request_method='POST',
        request_url=request_url,
        request_body='random-file.pdf',
        request_headers=request_headers,
        status_code=response.status_code,
        response_body=response.text,
    )

    if response.status_code == 200:
        return 'success'
    else:
        print(text.Red + '\n- [File Management Service] Failure to create file. Response Status: '
                         '{response_status}. Response message: {response_message}'
              .format(response_status=response.status_code, response_message=response.text))
        return False


def get_file_metadata(account_id, purpose, data):
    metadata = {
        'invoice': 'accountId:{account_id}, invoiceId:{invoice_id}'
            .format(account_id=account_id, invoice_id=data.get('invoice_id')),
        'bank-slip': 'accountId:{account_id}, invoiceId:{invoice_id}'
            .format(account_id=account_id, invoice_id=data.get('invoice_id')),
        'credit-statement': 'accountId:{account_id}, date:{month}/{year}, creditBalance:123.05'
            .format(account_id=account_id, month=data.get('month'), year=data.get('year'))
    }

    return metadata[purpose]
