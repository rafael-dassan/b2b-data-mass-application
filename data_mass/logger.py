import subprocess
import logging

from time import time
from os import makedirs, name
from os.path import abspath, dirname, exists, join


def log_to_file(
        request_method: str,
        request_url: str,
        request_body: str,
        request_headers: str,
        status_code: str,
        response_body: str):
    """
    Log all requests to a specific file.

    Parameters
    ----------
    request_method : str
        http methods (e.g. POST, GET, PUT, PATCH, and DELETE).
    request_url : str
        Resource locator or endpoint.
    request_body : str
        Data transmitted in the HTTP transaction.
    request_headers : str
        e.g., Auth, timezone, trace ID, etc.
    status_code : str
        Indicates whether a specific HTTP request has been successfully
        completed or not.
    response_body : str
        Response from the service when available.
    """
    log_directory = join(abspath(dirname("__main__")), "data_mass/logs")
    log_file = join(log_directory, f"{int(time())}.log")

    if not exists(log_directory):
        if name == "nt":
            makedirs(log_directory)
        else:
            subprocess.call(["mkdir", "-p", log_directory])

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s:%(levelname)s:%(message)s"
    )

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("chardet.charsetprober").setLevel(logging.WARNING)

    logging.debug((
        f"Starting new HTTPS connection: {request_method} {request_url}\n"
        f"Request headers: {request_headers}\n"
        f"Request body: {request_body}\n"
        f"Response code: {status_code}\n"
        f"Response body: {response_body}\n"
    ))
