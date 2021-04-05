import os
from os import path
import subprocess
import logging


def log_to_file(request_method, request_url, request_body, request_headers, status_code, response_body):
    """
    Log all requests to a specific file
    Args:
        request_method: e.g., POST, GET, PUT, PATCH, and DELETE
        request_url: resource locator or endpoint
        request_body: data transmitted in the HTTP transaction
        request_headers: e.g., Auth, timezone, trace ID, etc.
        status_code: indicates whether a specific HTTP request has been successfully completed or not
        response_body: response from the service when available
    Returns: Log request to file successfully
    """

    # Create dir and file paths
    dir_project = os.path.abspath(os.path.dirname(__file__))
    file_debug = os.path.join(dir_project, 'debug.log')

    # If the logs directory does not exist, create it
    if not path.exists(dir_project):
        if os.name == 'nt':
            os.makedirs(dir_project)
        else:
            subprocess.call(['mkdir', '-p', dir_project])

    # If the debug.log file does not exist, create it
    if not path.exists(file_debug):
        if os.name == 'nt':
            f = open(file_debug, 'w+')
            f.close()
        else:
            subprocess.call(['touch', file_debug])

    # Log request data to debug.log file
    logging.basicConfig(filename=file_debug, level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('chardet.charsetprober').setLevel(logging.WARNING)

    logging.debug('Starting new HTTPS connection: {} {}'
                  '\nRequest headers: {}'
                  '\nRequest body: {}'
                  '\nResponse code: {}'
                  '\nResponse body: {}\n'.format(request_method, request_url, request_headers, request_body,
                                                 status_code, response_body))
