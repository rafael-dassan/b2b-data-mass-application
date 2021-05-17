import logging
import re
import subprocess
from datetime import datetime
from os import makedirs, name
from os.path import abspath, dirname, exists, join

PROJECT = "/b2b-data-mass-application"


def log_to_file(
        request_method: str,
        request_url: str,
        request_body: str,
        request_headers: str,
        status_code: int,
        response_body: str):
    """
    Log all requests to a specific file named
     following year-month-day-hour pattern.

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
    log_directory = create_today_directory()

    log_file = join(
        log_directory, f"{datetime.now().strftime('%H-%M-%S')}.log"
    )

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s:%(levelname)s:%(message)s"
    )

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("chardet.charsetprober").setLevel(logging.WARNING)

    logging.debug(
        f"Starting new HTTPS connection: {request_method} {request_url}\n"
        f"Request headers: {request_headers}\n"
        f"Request body: {request_body}\n"
        f"Response code: {status_code}\n"
        f"Response body: {response_body}\n"
    )


def create_today_directory() -> str:
    """
    Create a log folder with today's date name.

    Returns
    -------
    str
        The path for the today directory.
    """
    # Problem: since the project is a library, the logs directory
    # will be created in the path of the Python site-package
    # (i.e. /lib/site-packages).
    # Solution: it must use the path to the project, and after that,
    # manually define the rest.
    current_dir = abspath(dirname(__file__))
    project_dir = re.match(rf"^.*?\{PROJECT}", current_dir)
    log_path = "data_mass/logs"

    if project_dir is None:
        project_dir = join(abspath(dirname("__main__")), log_path)
    else:
        project_dir = project_dir.group(0)

    today = datetime.today().strftime("%Y-%m-%d")
    today_dir_path = join(project_dir, f"{log_path}/{today}")

    if not exists(today_dir_path):
        if name == "nt":
            makedirs(today_dir_path)
        else:
            subprocess.call(["mkdir", "-p", today_dir_path])

    return today_dir_path
