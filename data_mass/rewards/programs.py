import concurrent.futures
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

    # get data from Rewards Data Mass files
    categories_content: bytes = pkg_resources.resource_string(
        "data_mass",
        f"rewards/data/{zone.upper()}/program_categories.json"
    )
    categories_json_data = loads(categories_content.decode("utf-8"))

    # get data from Rewards Data Mass files
    terms_content: bytes = pkg_resources.resource_string(
        "data_mass",
        f"rewards/data/{zone.upper()}/program_terms.json"
    )
    terms_json_data = loads(terms_content.decode("utf-8"))

    print(
        f"{text.default_text_color}\n"
        f"Creating new Rewards program in {zone} - "
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
        "rules[0].skus": premium_rule_skus,
        "rules[1].skus": core_rule_skus,
        "combos": generated_combos,
        "initialBalance": initial_balance,
        "categories": categories_json_data,
        "termsAndConditions": terms_json_data
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

        results = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    put_program_combos,
                    program_id=selected_program["id"],
                    combo_id=combo_id,
                    zone=zone,
                    environment=environment,
                    request_body=convert_json_to_string(
                        {
                            "points": randrange(500, 5000, 100)
                        }
                    )
                )
                for combo_id in diff_combos_list
            ]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        print(
            f'{text.Green}\n'
            f'- DT combos included: {results.count(True)} / failed: {results.count(False)} '
            f'for Rewards program "{selected_program["id"]}".'
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


def put_program_combos(
        program_id: str,
        combo_id: str,
        zone: str,
        environment: str,
        request_body: str) -> Response:
    """
    Insert/Update a DT combo into the rewards program on the microservice.

    Parameters
    ----------
    program_id : str
    combo_id: str
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
    request_url = f"{base_url}/rewards-service/programs/{program_id}/combos/{combo_id}"

    response = place_request(
        request_method="PUT",
        request_url=request_url,
        request_body=request_body,
        request_headers=request_headers
    )

    if response.status_code == 200:
        return True        
    elif response.status_code == 404:
        print(
            f'{text.Red}\n'
            f'- [Rewards] The Rewards program "{program_id}" does not exist.'
        )
    else:
        print(
            f'{text.Red}\n'
            f'- [Rewards] Failure when including the DT combo "{combo_id}" '
            f'for Rewards program "{program_id}".\n'
            f'- Response Status: "{response.status_code}".\n'
            f'- Response message "{response.text}".'
        )

    return False


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