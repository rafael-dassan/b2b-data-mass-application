"""Request tools for Data Mass use."""
import json
import os
from io import FileIO
from time import time
from typing import List, Optional, Union
from uuid import uuid1

import jwt
from requests import Response, request
from requests.exceptions import RequestException

from data_mass.classes.text import text
from data_mass.tools.logger import log_to_file
from data_mass.tools.utils import (
    finish_application,
    set_to_dictionary,
    update_value_to_json
)


def place_request(
        request_method: str,
        request_url: str,
        request_body: Union[
            dict,
            List[tuple],
            bytes,
            str,
            FileIO
        ],
        request_headers: dict) -> Response:
    """
    Place generic request.

    Parameters
    ----------
    request_method : str
    request_url : str
    request_body : dict, list of tuple, bytes, str or file-like

    Returns
    -------
    Response
        The http response.
    """
    try:
        response = request(
            request_method,
            request_url,
            data=request_body,
            headers=request_headers
        )
    except RequestException as error:
        print(f"\n{text.Red}{str(error)}")
        finish_application()

    log_to_file(
        request_method=request_method,
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers,
        status_code=response.status_code,
        response_body=response.text,
    )

    return response


def get_header_request(
        zone: str,
        use_jwt_auth: Optional[bool] = False,
        use_root_auth: Optional[bool] = False,
        use_inclusion_auth: Optional[bool] = False,
        sku_product: Optional[bool] = False,
        account_id: Optional[str] = None,
        jwt_app_claim: Optional[str] = None) -> dict:
    """
    Get JWT header request.

    Parameters
    ----------
    zone : str
    use_jwt_auth : bool
        Default to False.
    use_root_auth : bool
        Default to False.
    use_inclusion_auth : bool
        Default to False.
    sku_product : bool
        Default to False.
    account_id : str
        Default to None.
    jwt_app_claim : str
        Default to None.

    Returns
    -------
    dict
        The header formatted.
    """
    switcher = {
        "AR": "America/Buenos_Aires",
        "BR": "America/Sao_Paulo",
        "CA": "America/Toronto",
        "CO": "America/Bogota",
        "DO": "America/Santo_Domingo",
        "EC": "America/Guayaquil",
        "MX": "America/Mexico_City",
        "PA": "America/Panama",
        "PE": "America/Lima",
        "PY": "America/Asuncion",
        "ZA": "Africa/Johannesburg"
    }
    timezone = switcher.get(zone, False)

    header = {
        "User-Agent": "BEES - Data Mass Framework",
        "Content-Type": "application/json",
        "country": zone,
        "requestTraceId": str(uuid1()),
        "x-timestamp": str(int(round(time() * 1000))),
        "cache-control": "no-cache",
        "timezone": timezone
    }

    if use_jwt_auth:
        header["Authorization"] = generate_hmac_jwt(account_id, jwt_app_claim)
    elif use_root_auth:
        header["Authorization"] = "Basic cm9vdDpyb290"
    elif use_inclusion_auth:
        header["Authorization"] = "Basic cmVsYXk6TVVRd3JENVplSEtB"
    else:
        header["Authorization"] = "Basic cmVsYXk6cmVsYXk="

    if sku_product:
        header["skuId"] = sku_product

    return header


def get_microservice_base_url(
        environment: str,
        is_v1: Optional[bool] = True):
    """
    Get base URL for Microservice.

    Parameters
    ----------
    environment : str
    is_v1 : Optional[bool]
        Default to `True`.

    Returns
    -------
    str
        The formatted string.
    """
    if environment == "DEV":
        if is_v1:
            return "https://bees-services-dev.eastus2.cloudapp.azure.com/v1"

        return "https://bees-services-dev.eastus2.cloudapp.azure.com/api"

    if environment not in ["UAT", "SIT"]:
        env_name = "SIT"
    else:
        env_name = environment

    context = "v1" if is_v1 else "api"

    return (
        f"https://services-{env_name.lower()}.bees-platform.dev/"
        f"{context}"
    )


def get_magento_base_url(environment: str, country: str) -> str:
    """
    Get base URL for Magento.

    Parameters
    ----------
    environment : str
    country : str

    Returns
    -------
    str
        The base url according to environment and country.
    """
    magento_url = {
        "DT": {
            "AR": "https://qa-dt-las-ar.abi-sandbox.net/",
            "BR": "https://qa-dt-br.abi-sandbox.net",
            "CA": "https://qa-dt-ca.abi-sandbox.net/",
            "CO": "https://qa-dt-copec-co.abi-sandbox.net",
            "DO": "https://qa-dt-dr.abi-sandbox.net",
            "MX": "https://qa-dt-mx.abi-sandbox.net",
            "ZA": "https://qa-dt-za.abi-sandbox.net"
        },
        "QA": {
            "AR": "https://qa-ma-las.abi-sandbox.net",
            "BR": "https://qa-ma-br.abi-sandbox.net",
            "CO": "https://qa-m3-copec-co.abi-sandbox.net",
            "DO": "https://qa-ma-dr.abi-sandbox.net",
            "EC": "https://qa-m1-ec.abi-sandbox.net",
            "MX": "https://qa-se-mx.abi-sandbox.net",
            "PE": "https://qa-m1-pe.abi-sandbox.net",
            "ZA": "https://qa-ma-za.abi-sandbox.net"
        },
        "SIT": {
            "AR": "https://ar.sit.bees-platform.dev",
            "BR": "https://br.sit.bees-platform.dev",
            "CA": "https://ca.sit.bees-platform.dev",
            "CO": "https://co.sit.bees-platform.dev",
            "DO": "https://do.sit.bees-platform.dev",
            "EC": "https://ec.sit.bees-platform.dev",
            "MX": "https://mx.sit.bees-platform.dev",
            "PA": "https://pa.sit.bees-platform.dev",
            "PE": "https://pe.sit.bees-platform.dev",
            "PY": "https://py.sit.bees-platform.dev",
            "ZA": "https://za.sit.bees-platform.dev"
        },
        "UAT": {
            "AR": "https://ar.uat.bees-platform.dev",
            "BR": "https://br.uat.bees-platform.dev",
            "CA": "https://ca.uat.bees-platform.dev",
            "CO": "https://co.uat.bees-platform.dev",
            "DO": "https://do.uat.bees-platform.dev",
            "EC": "https://ec.uat.bees-platform.dev",
            "MX": "https://mx.uat.bees-platform.dev",
            "PA": "https://pa.uat.bees-platform.dev",
            "PE": "https://pe.uat.bees-platform.dev",
            "PY": "https://py.uat.bees-platform.dev",
            "ZA": "https://za.uat.bees-platform.dev"
        }
    }

    return magento_url.get(environment).get(country)


def get_magento_user_registration_access_token(
        environment: str,
        country: str) -> str:
    """
    Get Magento User Registration Integration Access Token.

    Parameters
    ----------
    environment : str
    country : str

    Returns
    -------
    str
        Magento User Registration Integration Access Token.
    """
    access_token = {
        "DT": {
            "AR": "0pj40segd3h67zjn68z9oj18xyx5yib8",
            "BR": "qq8t0w0tvz7nbn4gxo5jh9u62gohvjrw",
            "CO": "2z0re32n00z159oui0az2j2dr42bx8m5",
            "DO": "56jqtzzto7tw9uox8nr3eckoeup53dt2",
            "MX": "40qrmhwv93ixeysxsw5hxrvjn6dstdim",
            "ZA": "y4u1xqitth7k8y50ei5nlfm538sblk6j"
        },
        "QA": {
            "AR": "30lqki06nbdegugcmdb0ttm9yppnmoec",
            "BR": "qq8t0w0tvz7nbn4gxo5jh9u62gohvjrw",
            "CO": "8mh6b9b6ft6m1cr5k7zm2jh4aljq4slx",
            "DO": "56jqtzzto7tw9uox8nr3eckoeup53dt2",
            "EC": "kyhzpszn0bswbf17mlb409ldg14j58uv",
            "MX": "w0mi88cajh0jbq0zrive3ht4eywc8xlm",
            "PE": "hwv67q9d3zyy2u500n2x0r5g7mr2j5is",
            "ZA": "yq2ed2ygbuiuysimjuir7cr86lbo3b90"
        },
        "SIT": {
            "AR": "30lqki06nbdegugcmdb0ttm9yppnmoec",
            "BR": "qq8t0w0tvz7nbn4gxo5jh9u62gohvjrw",
            "CA": "nhdzq8d4c59q1ofzsrpzlm2o7e2vdonf",
            "CO": "walt5dp3keiq2du0f30kir21v13f3u0v",
            "DO": "56jqtzzto7tw9uox8nr3eckoeup53dt2",
            "EC": "kyhzpszn0bswbf17mlb409ldg14j58uv",
            "MX": "w0mi88cajh0jbq0zrive3ht4eywc8xlm",
            "PA": "28bfo54x45h9xajalu3hvl0a33dmo4z3",
            "PE": "hwv67q9d3zyy2u500n2x0r5g7mr2j5is",
            "PY": "03ijjunt2djravu3kin3siirfdah0u7j",
            "ZA": "nmvvuk58lc425a7p5l55orrkgh0jprr2"
        },
        "UAT": {
            "AR": "30lqki06nbdegugcmdb0ttm9yppnmoec",
            "BR": "qq8t0w0tvz7nbn4gxo5jh9u62gohvjrw",
            "CA": "1nb7d81mmwmsyd0i6n01fgrkyhmpj6k8",
            "CO": "8mh6b9b6ft6m1cr5k7zm2jh4aljq4slx",
            "DO": "56jqtzzto7tw9uox8nr3eckoeup53dt2",
            "EC": "awtm7d9as0n9k1o5zi9fi90rtukxdmqh",
            "MX": "kcsn7y80vvo2by9fluw2vq4r2a6pucfs",
            "PA": "ovdnr3wfoh6nf0uh6h9ppoicp8jb15y0",
            "PE": "4z0crqq6yb6t5mip43i63tgntdll09vc",
            "PY": "z3l3d1l09hxd9wy0jmnphfwj09o8iefn",
            "ZA": "31pdb0yht5kn3eld7gum021f6k984jh9"
        }
    }

    return access_token.get(environment).get(country)


def get_magento_datamass_access_token(environment: str, country: str) -> str:
    """
    Get Magento Datamass Application Access Token.

    Parameters
    ----------
    environment : str
    country : str

    Returns
    -------
    str
        Magento Datamass Application Access Token.
    """
    access_token = {
        "UAT": {
            "AR": "a34o213zgisn67efeg0zbq04sqg667qk",
            "BR": "8z2z3y523hoqkcqci8q58afuoue81bns",
            "CA": "kz18zssktxjrns2jyq1lbj7mufs3mj2h",
            "CO": "meqei3q5ztreebdpb5vyej378mt2o8qy",
            "DO": "js4gd8y9wkqogf7eo2s4uy6oys15lfkf",
            "EC": "w9pphbvskd35206otky7cv1dobn0p1yb",
            "MX": "lsnudq7uujr3svcbn0g0uxlt6vjqe9yj",
            "PA": "t1l4tdhvzrsk54qgm9b7wg0nty1ia0jr",
            "PE": "xcgb5m0rl5pto116q4gxe1msd3zselq6",
            "PY": "nju63hy7j5nhfzgaeah2y077anlpzs6o",
            "ZA": "0seca4btewbr3e1opma4je2x8ftj57wx"
        },
        "SIT": {
            "AR": "hzp6hw65oqiyeyv8ozfzunex0nc1rff8",
            "BR": "q6yti2dxmhp0e2xjgyvtt72nziss6ptp",
            "CA": "93slxvujwumdkbpzb1qg4jf0zwrew1ud",
            "CO": "new189lnml9xmcr3m9gc0j6oji6w2izr",
            "DO": "tgqnjlqpfupf0i4zxcs2doqx409k1hyq",
            "EC": "ybyiars1mhm5e4jyaq94s5csj1e77knp",
            "MX": "86pg36lug4ivrx3xh5b5qnemzy1gw6v8",
            "PA": "3bs7q1f5wtegt7vrgxumcv1plhjatf1d",
            "PE": "lda0mjri507oqrm8xfofk6weifajn8cm",
            "PY": "bgfrp38faxbpwnad7uoc2vqlprmv5nck",
            "ZA": "fde80w10jbbaed1mrz6yg0pwy1vzfo48"
        }
    }

    return access_token.get(environment).get(country)


def generate_hmac_jwt(
        account_id: str,
        app_claim: Optional[str] = None,
        expire_months: Optional[int] = 1) -> str:
    """
    Generate HMAC JWT.

    Parameters
    ----------
    account_id : str
    app_claim : str
        Default to None.
    expire_months : int
        Default to int.

    Returns
    -------
    str
        The HMAC JWT.
    """
    now = int(time())
    expire_in = now + (2592000 * expire_months)

    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, "../data/create_jwt_payload.json")

    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        "exp": expire_in,
        "iat": now,
        "accounts": [account_id]
    }

    for key, value in dict_values.items():
        json_object = update_value_to_json(
            json_data,
            key,
            value
        )

    if app_claim is not None:
        set_to_dictionary(json_object, "app", app_claim)

    encoded = jwt.encode(
        json_object,
        "20735d31-46b5-411d-af02-47897a01c0c9",
        algorithm="HS256"
    )

    return f"Bearer {encoded}"


def generate_erp_token(expire_months: Optional[int] = 1) -> str:
    """
    Generate ERP token.

    Parameters
    ----------
    expire_months : int
        Default to 1.

    Returns
    -------
    str
        The ERP token.
    """
    now = int(time())
    expire_in = now + (2592000 * expire_months)

    abs_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(abs_path, "../data/create_erp_token_payload.json")

    with open(file_path) as file:
        json_data = json.load(file)

    dict_values = {
        "exp": expire_in,
        "iat": now
    }

    for key, value in dict_values.items():
        json_object = update_value_to_json(
            json_data,
            key,
            value,
        )

    encoded = jwt.encode(
        json_object,
        "20735d31-46b5-411d-af02-47897a01c0c9",
        algorithm="HS256"
    )

    return f"Bearer {encoded}"


def get_supplier_base_url(environment: str) -> str:
    """
    Get base URL for Supplier.

    Parameters
    ----------
    environment : str

    Returns
    -------
    str
        Supplier base url.
    """
    if environment == "LOCAL":
        return "http://localhost:8080/graphql"

    return (
        f"https://services-{environment.lower()}.bees-platform.dev"
        "/api/product-taxonomy-service/graphql"
    )


def get_header_request_supplier() -> dict:
    """
    Get header request supplier.

    Returns
    -------
    dict
        The header itself.
    """
    header = {
       "Authorization": (
           "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
           "eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3Nlcn"
           "ZpY2VzIiwiZXhwIjoxODkzNDU2MDAwLCJpYXQiOjE1MTYyMzkwMj"
           "IsInVwZGF0ZWRfYXQiOjExMTExMTEsInJvbGVzIjpbIlJPTEVfQ1"
           "VTVE9NRVIiXX0.oDALscasXTa2Zt209Hjmydk9GT7ErsdxI4c1D4q9kNA"
       )
    }

    return header
