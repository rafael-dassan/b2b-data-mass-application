from json import loads
from random import randint, randrange
from typing import Union

import pkg_resources
from requests import Response

from data_mass.classes.text import text
from data_mass.common import (
    convert_json_to_string,
    get_header_request,
    get_microservice_base_url,
    place_request,
    print_input_number,
    print_input_text,
    set_to_dictionary,
    update_value_to_json
)
from data_mass.rewards.utils import (
    build_request_url_with_projection_query,
    create_product_list_from_zone,
    display_all_programs_info,
    get_dt_combos_from_zone,
    print_input_combo_qty,
    print_input_decision
)

APP_ADMIN = "adminportal"
BASE_URL_IMAGE = "https://cdn-b2b-abi.global.ssl.fastly.net"


def create_new_program(
        zone: str,
        environment: str) -> Union[None, Response]:
    """
    Create Rewards Program on the microservice.

    Parameters
    ----------
    zone : str
    environment : str

    Returns
    -------
    None or Response
        `None` if a http error accours, else, the http response.
    """
    # Verify if the zone already have a reward program created
    response_all_programs = get_all_programs(
        zone,
        environment,
        {"DEFAULT"}
    )

    if response_all_programs is None:
        return None

    response_list_json = loads(response_all_programs.text)
    dm_program = get_dm_rewards_program_for_zone(
        response_list_json
    )

    if dm_program is not None:
        dm_program_id = dm_program["id"]

        print(
            f'{text.Yellow}\n'
            '- [Rewards] This zone already have a reward program created '
            f'- Program ID: "{dm_program_id}"'
        )

        return None

    response_zone_dt_combos = get_dt_combos_from_zone(
        zone,
        environment
    )

    # Verify if the zone has combos available
    if response_zone_dt_combos is None:
        return None

    product_list_from_zone = create_product_list_from_zone(
        zone=zone,
        environment=environment
    )

    # Verify if the zone has at least 20 SKUs available
    if product_list_from_zone is None:
        return None

    if len(product_list_from_zone) < 20:
        print(
            f'{text.Red}\n'
            '- [Rewards] The zone must have at least 20 products to proceed'
        )

        return None

    # Generates the new Program ID
    new_program_id = f"DM-REWARDS-{randint(100, 900)}"

    balance = print_input_decision(
        "Do you want to create the program with initial balance (20.000): "
    )

    if balance == "Y":
        initial_balance = 20000
    else:
        initial_balance = 0

    zone_dt_combos = loads(response_zone_dt_combos.text)

    premium_rule_skus = product_list_from_zone[0:10]
    core_rule_skus = product_list_from_zone[10:20]

    # Getting all the basic information for the Program to be created
    generated_combos = generate_combos_information(zone_dt_combos)
    categories = generate_categories_information(zone)
    terms = generate_terms_information(zone)

    print(
        f"{text.default_text_color}\n"
        f"Creating new Rewards program in {zone} -"
        f"{environment}. Please wait..."
    )

    # get data from Data Mass files
    content: bytes = pkg_resources.resource_string(
        "data_mass",
        "data/create_rewards_program_payload.json"
    )
    json_data = loads(content.decode("utf-8"))

    dict_values = {
        "name": new_program_id,
        "rules[0].moneySpentSkuRule.skus": premium_rule_skus,
        "rules[1].moneySpentSkuRule.skus": core_rule_skus,
        "combos": generated_combos,
        "initialBalance": initial_balance,
        "categories[0].categoryId": categories[0],
        "categories[0].categoryIdWeb": categories[1],
        "categories[0].description": categories[2],
        "categories[0].buttonLabel": categories[3],
        "categories[0].image": categories[4],
        "categories[0].title": "Premium",
        "categories[0].subtitle": categories[2],
        "categories[0].headerImage": (
            f"{BASE_URL_IMAGE}"
            "/sit/images/br/redesign/premium"
            "/img-premium-chopp-brahma-logo@2x.png"
        ),
        "categories[0].brands": [{
            "brandId": "123",
            "title": "premium brand",
            "image": (
                f"{BASE_URL_IMAGE}"
                "/uat/images/do/premium/img_puntos_20.png"
            ),
        }],
        "categories[1].categoryId": categories[5],
        "categories[1].categoryIdWeb": categories[6],
        "categories[1].description": categories[7],
        "categories[1].buttonLabel": categories[8],
        "categories[1].image": categories[9],
        "categories[1].title": 'Core',
        "categories[1].subtitle": categories[7],
        "categories[1].headerImage": (
            f"{BASE_URL_IMAGE}"
            "/sit/images/br/redesign/core/img-core-brahmachopp-logo@2x.png"
        ),
        "categories[1].brands": [{
            "brandId": "321",
            "title": "core brand",
            "image": (
                f"{BASE_URL_IMAGE}"
                "/uat/images/do/core/img_punto_1.png"
            ),
        }],
        "termsAndConditions[0].documentURL": terms[0],
        "termsAndConditions[0].changeLog": terms[1]
    }

    for key in dict_values.keys():
        json_object = update_value_to_json(
            json_data,
            key, dict_values[key]
        )

    request_body = convert_json_to_string(json_object)

    return put_programs(
        program_id=new_program_id,
        zone=zone,
        environment=environment,
        request_body=request_body
    )


def update_program_dt_combos(
        zone: str,
        environment: str) -> Union[None, Response]:
    """
    Update Program DT Combos on the microservice.

    Parameters
    ----------
    zone : str
    environment : str

    None or Response
        `None` if a http error accours, else, the http response.
    """
    all_programs = get_all_programs(zone, environment, ["COMBOS"])

    if all_programs is None:
        return None

    json_all_programs = loads(all_programs.text)
    display_all_programs_info(json_all_programs)

    selected_program = None
    while selected_program is None:
        program_id = print_input_text('\n- Please inform the Program ID')

        for program in json_all_programs:
            if program['id'].upper() == program_id.upper():
                selected_program = program
                break

        if selected_program is None:
            print(f'{text.Red}\n- Program "{program_id}" not found!!')

    # Get all the DT combos of the specified zone
    response_combos_from_zone = get_dt_combos_from_zone(zone, environment)

    if response_combos_from_zone is None:
        return None

    json_combos_from_zone = loads(response_combos_from_zone.text)
    zone_dt_combos = json_combos_from_zone["combos"]

    program_dt_combos = selected_program["combos"]

    diff_combos_list = diff_combos_program_and_zone(
        program_dt_combos=program_dt_combos,
        zone_dt_combos=zone_dt_combos,
        reason="inclusion"
    )

    if not diff_combos_list:
        return None

    update_program_combos = print_input_decision(
        "Do you want to update the program "
        "configuration to include the missing DT combos: "
    )

    if update_program_combos == "Y":
        dt_combos_qty = print_input_combo_qty(
            "Number of DT combos to include",
            len(diff_combos_list)
        )

        diff_combos_list = diff_combos_list[0:dt_combos_qty]
        patch_combos_list = []

        for combo_id in diff_combos_list:
            dict_combo = {
                "comboId": combo_id,
                "points": randrange(500, 5000, 100)
            }
            patch_combos_list.append(dict_combo)

        dict_patch_program_combos = set_to_dictionary(
            {},
            "combos",
            patch_combos_list
        )

        request_body = convert_json_to_string(dict_patch_program_combos)

        return patch_program_combos(
            program_id=selected_program["id"],
            zone=zone,
            environment=environment,
            request_body=request_body
        )

    return None


def remove_program_dt_combos(zone: str, environment: str) -> None:
    """
    Remove Program DT Combos from microservice.

    Parameters
    ----------
    zone : str
    environment : str

    Returns
    -------
    None
        If there's no program to be removed.

    Note
    -----
        If Program DT Combos exists, this is a no-op function.
    """
    all_programs = get_all_programs(
        zone=zone,
        environment=environment,
        projections=["COMBOS"]
    )

    if all_programs is None:
        return None

    json_all_programs = loads(all_programs.text)
    display_all_programs_info(json_all_programs)

    selected_program = None
    while selected_program is None:
        program_id = print_input_text('\nPlease inform the Program ID')

        for program in json_all_programs:
            if program["id"].upper() == program_id.upper():
                selected_program = program
                break

        if selected_program is None:
            print(
                f'{text.Red}\n'
                f'- Program "{program_id}" not found!!'
            )

    # Get all the DT combos of the specified zone
    response_combos_from_zone = get_dt_combos_from_zone(zone, environment)

    if response_combos_from_zone is None:
        return None

    json_combos_from_zone = loads(response_combos_from_zone.text)
    zone_dt_combos = json_combos_from_zone["combos"]

    # Get the DT combos configured in the rewards program
    program_dt_combos = selected_program["combos"]

    diff_combos_list = diff_combos_program_and_zone(
        program_dt_combos=program_dt_combos,
        zone_dt_combos=zone_dt_combos,
        reason='exclusion'
    )

    if not diff_combos_list:
        return None

    remove_program_combos = print_input_decision(
        "Do you want to remove ALL nonexistent DT combos "
        "from the program configuration"
    )

    if remove_program_combos.upper() == 'Y':
        for combo_id in diff_combos_list:
            delete_program_combo(
                program_id=selected_program['id'],
                combo_id=combo_id,
                zone=zone,
                environment=environment
            )

    return None


def patch_program_root_field(
        zone: str,
        environment: str,
        field: str) -> Union[None, Response]:
    """
    Patches the selected program root field.

    Parameters
    ----------
    zone : str
    environment : str
    field : str

    Returns
    -------
    None or Response
        `None` if a http error accours, else, the http response.
    """
    all_programs = get_all_programs(zone, environment, ["DEFAULT"])

    if all_programs is not None:
        initial_balance = True if field == "initial_balance" else False
        redeem_limit = True if field == "redeem_limit" else False

        json_all_programs = loads(all_programs.text)
        display_all_programs_info(
            list_all_programs=json_all_programs,
            show_initial_balance=initial_balance,
            show_redeem_limit=redeem_limit
        )

        program_id = print_input_text('\nPlease inform the Program ID')
        dict_values_patch_program = {}

        if initial_balance:
            new_balance = print_input_number(
                "\nPlease inform the new balance amount "
                "(greater or equal zero)"
            )

            while int(new_balance) < 0:
                print(
                    f'{text.Red}\n'
                    'Invalid value!! Must be greater or equal zero!!'
                )

                new_balance = print_input_number(
                    "\nPlease inform the new balance amount "
                    "(greater or equal zero)"
                )

            set_to_dictionary(
                dict_values_patch_program,
                "initialBalance",
                int(new_balance)
            )

        elif redeem_limit:
            new_redeem_limit = print_input_number(
                "\nPlease inform the new redeem limit value "
                "(greater than zero)"
            )

            while int(new_redeem_limit) <= 0:
                print(
                    f'{text.Red}\n'
                    'Invalid value!! Must be greater than zero!!'
                )

                new_redeem_limit = print_input_number(
                    "\nPlease inform the new redeem limit value "
                    "(greater than zero)"
                )

            set_to_dictionary(
                dict_values_patch_program,
                "redeemLimit",
                int(new_redeem_limit)
            )

        request_body = convert_json_to_string(dict_values_patch_program)

        return patch_program(
            program_id=program_id,
            zone=zone,
            environment=environment,
            request_body=request_body
        )

    return None


def get_dm_rewards_program_for_zone(
        zone_programs_list: list) -> Union[None, str]:
    """
    Check if DM Rewards program exists for the zone.

    Parameters
    ----------
    zone_programs_list : list

    Returns
    -------
    None or str
        None is DM Rewards does not exissts, else, \
        the `DM-REWARDS` property.
    """
    dm_rewards_program = None

    for program in zone_programs_list:
        prefix_program_id = program['id'][0:9]

        if prefix_program_id == 'DM-REWARD':
            dm_rewards_program = program
            break

    return dm_rewards_program


def get_all_programs(
        zone: str,
        environment: str,
        projections: Union[set, list]) -> Union[None, Response]:
    """
    Get all reward program for the zone.

    Parameters
    ----------
    zone : str
    environment : str
    projections : set or list

    Returns
    -------
    None or Response
        `None` if a http error accours, else, the http response.
    """
    if projections is None:
        projections = set()

    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        jwt_app_claim=APP_ADMIN
    )

    # Define url request
    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/rewards-service/programs"
    request_url = build_request_url_with_projection_query(
        request_url=request_url,
        projections=projections
    )

    # Send request
    response = place_request(
        request_method="GET",
        request_url=request_url,
        request_body="",
        request_headers=request_headers
    )

    if response.status_code == 200:
        json_data = loads(response.text)

        if json_data:
            return response
        else:
            print(
                f'{text.Red}\n'
                '- [Rewards] There are no Reward '
                f'programs available in "{zone}" zone.'
            )
    else:
        print(
            f'{text.Red}\n'
            '- [Rewards] Failure when getting all '
            f'programs in "{zone}" zone.\n'
            f'- Response Status: "{response.status_code}".\n'
            f'- Response message "{response.text}".'
        )

    return None


def get_specific_program(
        program_id: str,
        zone: str,
        environment: str,
        projections: set) -> Union[None, Response]:
    """
    Get an specific reward program for the zone.

    Parameters
    ----------
    program_id : str
    zone : str
    environment : str

    Returns
    -------
    None or Response
        `None` if the specific program does not exits, else,\
        the http response.
    """
    if projections is None:
        projections = set()

    header_request = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        jwt_app_claim=APP_ADMIN
    )

    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/rewards-service/programs/{program_id}"
    request_url = build_request_url_with_projection_query(
        request_url,
        projections
    )

    response = place_request(
        request_method="GET",
        request_url=request_url,
        request_body="",
        request_headers=header_request
    )

    if response.status_code == 200:
        return response

    elif response.status_code == 404:
        print(
            f'{text.Red}\n'
            f'- [Rewards] The Rewards program "{program_id}" does not exist.'
        )
    else:
        print(
            f'{text.Red}\n'
            '- [Rewards] Failure when getting the program '
            f'"{program_id}" information.\n'
            f'- Response Status: "{response.status_code}".\n'
            f'- Response message "{response.text}".'
        )

    return None

# NOTE: According to the Rewards team,
# the `PUT` method is being used for the same purposes as`POST`,
# therefore, there is no endpoint for creation (`POST`) so far.
# It is worth remembering that pylint is accusing the methods of
# `patch_program` and` put_programs` as duplicate code,
# and thus, evading good practice guidelines.

# TODO: Keep up to date with the Rewards team on the creation and/or
# alteration of your endpoints. Once the endpoints are defined,
# evaluate the unification of the methods below and make
# them as generic as possible.


def patch_program(
        program_id: str,
        zone: str,
        environment: str,
        request_body: str) -> Response:
    """
    Update a program on the microservice.

    Paramters
    ---------
    program_id : str
    zone : str
    environment : str
    request_body : str

    Returns
    -------
    Response
        The http response.
    """
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        jwt_app_claim=APP_ADMIN
    )

    # Define url request to patch the Rewards program selected
    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/rewards-service/programs/{program_id}"

    response = place_request(
        request_method="PATCH",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 200:
        print(
            f'{text.Green}\n'
            f'- [Rewards] The Rewards program "{program_id}" has been '
            'successfully updated.'
        )

    elif response.status_code == 404:
        print(
            f'{text.Red}\n'
            f'- [Rewards] The Rewards program "{program_id}" does not exist.'
        )
    else:
        print(
            f'{text.Red}\n'
            '- [Rewards] Failure when updating the program '
            f'"{program_id}" configuration.\n'
            f'- Response Status: "{response.status_code}".\n'
            f'- Response message "{response.text}".'
        )

    return response


def put_programs(
        program_id: str,
        zone: str,
        environment: str,
        request_body: str) -> Response:
    """
    Create Programs on the microservice.

    Parameters
    ----------
    program_id : str
    zone : str
    environment : str
    request_body : str

    Returns
    -------
    Response
        The http response.
    """
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        jwt_app_claim=APP_ADMIN
    )

    # Define url request to patch the Rewards program selected
    base_url = get_microservice_base_url(environment, False)
    request_url = f'{base_url}/rewards-service/programs/{program_id}'

    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 200:
        print(
            f'{text.Green}\n'
            f'- [Rewards] The Rewards program "{program_id}" '
            'has been successfully created.'
        )
    else:
        print(
            f'{text.Red}\n'
            f'- [Rewards] Failure when creating the program "{program_id}".\n'
            f'- Response Status: "{response.status_code}".\n'
            f'- Response message "{response.text}".'
        )

    return response


def diff_combos_program_and_zone(
        program_dt_combos: list,
        zone_dt_combos: list,
        reason: str) -> list:
    """
    Get differences between two combos.

    Parameters
    ----------
    program_dt_combos : list
    zone_dt_combos : list
    reason : str

    Returns
    -------
    list
        The difference between two combos.
    """
    program_combos_list = [combo["comboId"] for combo in program_dt_combos]

    print(
        f'{text.Yellow}\n'
        f'- Found "{len(program_combos_list)}" DT combos '
        'configured for rewards program.'
    )

    zone_combos_list = [combo["id"] for combo in zone_dt_combos]
    print(
        f'{text.Yellow}\n'
        f'- Found "{len(zone_combos_list)}" DT combos configured for the zone.'
    )

    if reason == "inclusion":
        diff_combos_list = set(zone_combos_list) - set(program_combos_list)
        diff_combos_list = list(diff_combos_list)

        print(
            f'{text.Yellow}\n'
            f'- Found "{len(diff_combos_list)}" DT combos missing in the '
            'program configuration.'
        )
    else:
        diff_combos_list = set(program_combos_list) - set(zone_combos_list)
        diff_combos_list = list(diff_combos_list)

        print(
            f'{text.Yellow}\n'
            f'- Found "{len(diff_combos_list)}" nonexistent DT combos in the '
            'program configuration.'
        )

    return diff_combos_list


def patch_program_combos(
        program_id: str,
        zone: str,
        environment: str,
        request_body: str) -> Response:
    """
    Update program combos on the microservice.

    Parameters
    ----------
    program_id : str
    zone : str
    environment : str
    request_body : str

    Returns
    -------
    Response
        The http response.
    """
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        jwt_app_claim=APP_ADMIN
    )

    base_url = get_microservice_base_url(environment, False)
    request_url = f"{base_url}/rewards-service/programs/{program_id}/combos"

    response = place_request(
        request_method="PATCH",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 200:
        print(
            f'{text.Green}\n'
            f'- [Rewards] The combos for Rewards program "{program_id}" '
            'have been successfully updated.'
        )

    elif response.status_code == 404:
        print(
            f'{text.Red}\n'
            f'- [Rewards] The Rewards program "{program_id}" does not exist.'
        )
    else:
        print(
            f'{text.Red}\n'
            f'- [Rewards] Failure when updating the program "{program_id}" '
            'combos configuration.\n'
            f'- Response Status: "{response.status_code}".\n'
            f'- Response message "{response.text}".'
        )

    return response


def delete_program_combo(
        program_id: str,
        combo_id: str,
        zone: str,
        environment: str) -> Response:
    """
    Delete a program combo from microservice.

    Parameters
    ----------
    program_id : str
    combo_id : str
    zone : str
    environment : str

    Returns
    -------
    Response
        The http response.
    """
    request_headers = get_header_request(
        zone=zone,
        use_jwt_auth=True,
        jwt_app_claim=APP_ADMIN
    )

    # Define url request to delete the Rewards program combo
    base_url = get_microservice_base_url(environment, False)
    request_url = (
        f"{base_url}/rewards-service"
        f"/programs/{program_id}/combos/{combo_id}"
    )

    response = place_request(
        request_method="DELETE",
        request_url=request_url,
        request_body="",
        request_headers=request_headers
    )

    if response.status_code == 204:
        print(
            f'{text.Green}\n'
            f'- [Rewards] The combo "{combo_id}" have been '
            'successfully deleted '
            f'from Rewards program "{program_id}".'
        )

    elif response.status_code == 404:
        print(
            f'{text.Red}\n'
            f'- [Rewards] The combo "{combo_id}" does not exist '
            f'in Rewards program "{program_id}".'
        )

    else:
        print(
            f'{text.Red}\n'
            f'- [Rewards] Failure when deleting the combo "{combo_id}" '
            f'from Rewards program "{program_id}".\n'
            f'- Response Status: "{response.status_code}".\n'
            f'- Response message "{response.text}".'
        )

    return response


def generate_combos_information(zone_dt_combos: list) -> list:
    """
    Generates the Combos for Rewards program.

    Parameters
    ----------
    zone_dt_combos : list

    Returns
    -------
    list
        The combo list.
    """
    zone_dt_combos = zone_dt_combos["combos"]

    dt_combos_qty = print_input_combo_qty(
        "Number of DT combos to include in the program",
        len(zone_dt_combos)
    )

    zone_dt_combos = zone_dt_combos[0:dt_combos_qty]
    combos_list = []

    for dt_combo in zone_dt_combos:
        dic_combos = {
            "comboId": dt_combo["id"],
            "points": randrange(500, 5000, 100)
        }

        combos_list.append(dic_combos)

    return combos_list


def generate_categories_information(zone: str) -> list:
    """
    Generates the Categories for Rewards program.

    Parameters
    ----------
    zone : str

    Returns
    -------
    list
        The Categories for Rewards list.
    """
    category_info = []

    if zone == "DO":
        # Premium category
        category_info.append("96")
        category_info.append("94")
        category_info.append(
            "Gana 100 puntos por cada RD $1000 pesos "
            "de compra en estos productos"
        )
        category_info.append("COMPRA AHORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/do/core/img_punto_1.png"
        )

        # Core category
        category_info.append("95")
        category_info.append("93")
        category_info.append(
            "Gana 50 puntos por cada RD $1000 pesos "
            "de compra en estos productos"
        )
        category_info.append("COMPRA AHORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/do/core/img_punto_1.png"
        )
    elif zone == "CO":
        # Premium category
        category_info.append("124")
        category_info.append("304")
        category_info.append(
            "Gana 100 puntos por cada RD $1000 pesos de "
            "compra en estos productos"
        )
        category_info.append("COMPRA AHORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/do/core/img_punto_1.png"
        )

        # Core category
        category_info.append("123")
        category_info.append("261")
        category_info.append(
            "Gana 50 puntos por cada RD $1000 pesos de "
            "compra en estos productos"
        )
        category_info.append("COMPRA AHORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/do/core/img_punto_1.png"
        )
    elif zone == "AR":
        # Premium category
        category_info.append("582")
        category_info.append("494")
        category_info.append(
            "Gana 100 puntos por cada RD $1000 pesos de "
            "compra en estos productos"
        )
        category_info.append("COMPRA AHORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/do/core/img_punto_1.png"
        )

        # Core category
        category_info.append("581")
        category_info.append("493")
        category_info.append(
            "Gana 50 puntos por cada RD $1000 pesos de "
            "compra en estos productos"
        )
        category_info.append("COMPRA AHORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/do/core/img_punto_1.png"
        )
    elif zone == "BR":
        # Premium category
        category_info.append("262")
        category_info.append("226")
        category_info.append(
            "Ganhe 100 pontos para cada R$1000,00 gastos em compras "
            "e troque por produtos gratis."
        )
        category_info.append("COMPRAR AGORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/br/premium/img-premium-br-rules-2.png"
        )

        # Core category
        category_info.append("272")
        category_info.append("236")
        category_info.append(
            "Ganhe 50 pontos para cada R$1000,00 gastos em compras "
            "e troque por produtos gratis."
        )
        category_info.append("COMPRAR AGORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/br/premium/img-premium-br-rules-2.png"
        )
    elif zone == "ZA":
        # Premium category
        category_info.append("217")
        category_info.append("214")
        category_info.append(
            "Earn 1 point for each R100 spent on "
            "quarts products."
        )
        category_info.append("BUY NOW")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/za/quarts-brands.png"
        )

        # Core category
        category_info.append("219")
        category_info.append("216")
        category_info.append(
            "Earn 10 points for each R100 spent on "
            "bonus products."
        )
        category_info.append("BUY NOW")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/za/bonus-brands.png"
        )
    elif zone == "MX":
        # Premium category
        category_info.append("9")
        category_info.append("1")
        category_info.append(
            "Gana 1 punto por cada $10 de "
            "compra en estos productos"
        )
        category_info.append("COMPRA AHORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/mx/core-brands.png"
        )

        # Core category
        category_info.append("12")
        category_info.append("2")
        category_info.append(
            "Gana 3 puntos por cada $10 de "
            "compra en estos productos"
        )
        category_info.append("COMPRA AHORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/mx/premium-brands.png"
        )
    elif zone == "EC":
        # Premium category
        category_info.append("129")
        category_info.append("115")
        category_info.append(
            "Gana 4 puntos por cada $1 de "
            "compra en estos productos"
        )
        category_info.append("COMPRA AHORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/sit/images/ec/premium-brands.png"
        )

        # Core category
        category_info.append("127")
        category_info.append("113")
        category_info.append(
            "Gana 1 punto por cada $1 de "
            "compra en estos productos"
        )
        category_info.append("COMPRA AHORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/ec/core-brands.png"
        )
    elif zone == "PE":
        # Premium category
        category_info.append("premium")
        category_info.append("premium")
        category_info.append(
            "Gana 2 puntos por cada S/ 1.00 de "
            "compra en estos productos"
        )
        category_info.append("COMPRA AHORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/pe/premium-brands.png"
        )

        # Core category
        category_info.append("core")
        category_info.append("core")
        category_info.append(
            "Gana 1 punto por cada S/ 1.00 "
            "de compra en estos productos"
        )
        category_info.append("COMPRA AHORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/pe/core-brands.png"
        )

    elif zone == 'PY':
        # Premium category
        category_info.append("168")
        category_info.append("11")
        category_info.append(
            "Gana 10 puntos por cada Gs.100.00 de "
            "compra en estos productos"
        )
        category_info.append("COMPRA AHORA")
        category_info.append(
            f"{BASE_URL_IMAGE}/"
            "uat/images/py/premium-brands.png"
        )

        # Core category
        category_info.append("167")
        category_info.append("4")
        category_info.append(
            "Gana 1 punto por cada Gs.1.00 de "
            "compra en estos productos"
        )
        category_info.append("COMPRA AHORA")
        category_info.append(
            f"{BASE_URL_IMAGE}"
            "/uat/images/py/core-brands.png"
        )

    return category_info


def generate_terms_information(zone: str) -> list:
    """
    Generates the Terms and Conditions for Rewards program.

    Parameters
    ----------
    zone : str

    Returns
    -------
    list
        Terms and Conditions list.
    """
    terms_info = []

    if zone in ["DO", "CO", "AR", "MX", "EC", "PE", "PY"]:
        terms_info.append(
            f"{BASE_URL_IMAGE}"
            "/terms/terms-co.html"
        )
        terms_info.append("Términos iniciales introducidos al programa")
    elif zone == "BR":
        terms_info.append(
            "https://b2bstaticwebsagbdev.blob.core.windows.net"
            "/digitaltrade/terms/terms-br.html"
        )
        terms_info.append("Termos iniciais introduzidos ao programa")
    elif zone == "ZA":
        terms_info.append(
            "https://cdn-b2b-abi-prod.global.ssl.fastly.net"
            "/prod/terms/terms-za.html"
        )
        terms_info.append("Initial terms added to the program")

    return terms_info
