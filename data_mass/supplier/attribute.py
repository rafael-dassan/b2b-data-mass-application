import json
import string
from datetime import datetime, timedelta
from random import randint
from typing import Any, Union

from gql import Client, gql
from gql.gql import DocumentNode
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport
from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.common import get_header_request_supplier, get_supplier_base_url
from data_mass.menus.supplier_menu import print_primitive_type
from data_mass.supplier.gql.attributes import (
    create_edit_enum_attribute,
    create_edit_group_attribute,
    create_edit_primitive_attribute,
    create_enum_generic_payload,
    create_group_attribute
)
from data_mass.supplier.gql.attributes import \
    create_legacy_group_attribute as create_legacy_group_attr
from data_mass.supplier.gql.attributes import (
    create_primitive_attribute_payload,
    create_search_all_attribute_payload,
    create_search_all_legacy_attributes_payload,
    create_search_specific_attribute_payload
)


def create_attribute_primitive_type(
        environment: str,
        type_attribute: str) -> Union[bool, str]:
    """
    Create attribute using primitive type.

    Parameters
    ----------
    environment : str
    type_attribute : str

    Returns
    -------
    bool
        `False`, when a `TransportQueryError` occurs.
    str
        The attribute id.

    Raises
    ------
    TransportQueryError
        When a `gql` occurs.
    """
    name = f"DM ATTRIBUTE {type_attribute} {str(randint(1, 100000))}"
    description = f"DM DESCRIPTION to {name}"

    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(
        url=base_url,
        headers=base_header
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    mut = create_primitive_attribute_payload()

    params = {
        "name": name,
        "description": description,
        "attribute_type": type_attribute
    }

    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)

        if json_data:
            json_split = json_data.rsplit()
            id_att = json_split[2]
            id_att1 = id_att.lstrip('"')
            id_att2 = id_att1.rsplit('"', 1)[0]

            return id_att2

    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def create_attribute_enum(
        environment: str,
        type_attribute: str) -> Union[bool, str]:
    """
    Create enum attribute.

    Parameters
    ----------
    environment : str
    type_attribute : str

    Returns
    -------
    bool
        `False`, when a `TransportQueryError` occurs.
    str
        The attribute id.

    Raises
    ------
    TransportQueryError
        When a `gql` occurs.
    """
    random_int = str(randint(1, 100000))
    name = f"DM ATTRIBUTE {str(type_attribute)} {random_int}"
    description = f"DM DESCRIPTION to {name}"

    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(
        url=base_url,
        headers=base_header
    )

    # Create a GraphQL client using the defined transport
    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )
    values = []

    # Provide a GraphQL query
    if type_attribute == 'NUMERIC':
        values.append(str(randint(1, 100000)) + '1')
        values.append(str(randint(1, 100000)) + '2')
        values.append(str(randint(1, 100000)) + '3')
    elif type_attribute == 'DATE':
        time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        time += 'T00:00:00'

        for _ in range(3):
            values.append(time)

    elif type_attribute == 'TEXT':
        values.append(string.ascii_lowercase + 'a')
        values.append(string.ascii_lowercase + 'b')
        values.append(string.ascii_lowercase + 'c')

    mut = create_enum_generic_payload()
    params = {
        "name": name,
        "description": description,
        "values": values,
        "enum_primitive_type": type_attribute
    }

    # Execute the query on the transport
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)
        if len(json_data) != 0:
            json_split = json_data.rsplit()
            id_att = json_split[2]
            id_att1 = id_att.lstrip('"')
            id_att2 = id_att1.rsplit('"', 1)[0]
            return id_att2
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def create_attribute_group(
        environment: str,
        attributes: str) -> Union[bool, str]:
    """
    Creat attribute group.

    Returns
    -------
    bool
        `False`, when a `TransportQueryError` occurs.
    str
        The attribute id.

    Raises
    ------
    TransportQueryError
        When a `gql` occurs.
    """
    name = 'DM ATTRIBUTE GROUP' + str(randint(1, 100000))
    description = 'DM DESCRIPTION to ' + name

    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    mut = create_group_attribute()

    params = {
        "name": name,
        "description": description,
        "values": attributes
    }

    # Execute the query on the transport
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)

        if not json_data:
            json_split = json_data.rsplit()
            id_att = json_split[2]
            id_att1 = id_att.lstrip('"')
            id_att2 = id_att1.rsplit('"', 1)[0]
            return id_att2
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def create_legacy_attributes_by_type(
        environment: str,
        attribute_name_list: list,
        attribute_type: str):
    """
    Create legacy attributes by type.

    Parameters
    ----------
    environment : str
    attribute_name_list : list
    attribute_type : str

    Returns
    -------
    list
        A list with legacy attributes.
    """
    attribute_ids = []

    for name in attribute_name_list:
        attribute_id = create_legacy_attribute_primitive_type(
            environment=environment,
            name=name,
            attribute_type=attribute_type
        )

        attribute_ids.append(attribute_id)

    return attribute_ids


def create_legacy_root_attribute(environment: str):
    """
    Create legacy root attribute.

    Parameters
    ----------
    environment : str
    """
    text_attributes = ["Classification", "Brand ID", "Brand", "Sub Brand Name"]
    attribute_type_text = "TEXT"
    create_legacy_attributes_by_type(
        environment=environment,
        attribute_name_list=text_attributes,
        attribute_type=attribute_type_text
    )

    boolean_attributes = ["Is Alcoholic", "Is Narcotic", "Hidden"]
    attribute_type_boolean = "BOOLEAN"
    create_legacy_attributes_by_type(
        environment=environment,
        attribute_name_list=boolean_attributes,
        attribute_type=attribute_type_boolean
    )

    numeric_attributes = [
        "Sales Ranking",
        "Pallet Quantity",
        "Minimum Order Quantity"
    ]
    attribute_type_numeric = "NUMERIC"
    create_legacy_attributes_by_type(
        environment=environment,
        attribute_name_list=numeric_attributes,
        attribute_type=attribute_type_numeric
    )


def create_legacy_attribute_package(environment: str) -> Union[bool, str]:
    """
    Create legacy attribute packge.

    Parameters
    ----------
    environment : str

    Returns
    -------
    bool
        `False`, when a `TransportQueryError` occurs.
    str
        The attribute id.
    """
    numeric_attributes = ["Unit Count", "Item Count"]
    attribute_type_numeric = "NUMERIC"
    sub_attributes_ids = create_legacy_attributes_by_type(
        environment=environment,
        attribute_name_list=numeric_attributes,
        attribute_type=attribute_type_numeric
    )

    text_attributes = [
        "Package ID",
        "Package Name",
        "Pack",
        "Pack Material Type"
    ]
    attribute_type_text = "TEXT"
    sub_attributes_ids.extend(
        create_legacy_attributes_by_type(
            environment=environment,
            attribute_name_list=text_attributes,
            attribute_type=attribute_type_text
        )
    )

    name = "Package"
    attribute_id = create_legacy_group_attribute(
        environment=environment,
        name=name,
        attributes=sub_attributes_ids
    )

    return attribute_id


def create_legacy_attribute_container(
        environment: str) -> Union[bool, str]:
    """
    Create legacy attribute container.

    Parameters
    ----------
    environment : str

    Returns
    -------
    bool
        `False`, when a `TransportQueryError` occurs.
    str
        The attribute id.
    """
    numeric_attributes = ["Size"]
    attribute_type_numeric = "NUMERIC"
    sub_attributes_ids = create_legacy_attributes_by_type(
        environment,
        numeric_attributes,
        attribute_type_numeric
    )

    text_attributes = ["Container Name", "Container Material"]
    attribute_type_text = "TEXT"
    sub_attributes_ids.extend(
        create_legacy_attributes_by_type(
            environment,
            text_attributes,
            attribute_type_text
        )
    )

    boolean_attributes = ["Returnable"]
    attribute_type_boolean = 'BOOLEAN'
    sub_attributes_ids.extend(
        create_legacy_attributes_by_type(
            environment,
            boolean_attributes,
            attribute_type_boolean
        )
    )

    unit_of_measurement_name = "Unit of Measurement"
    unit_of_measurement_values = [
        "G",
        "GR",
        "Gal",
        "L",
        "ML",
        "OZ",
        "Litro",
        "Onz"
    ]
    unit_of_measurement_enum_type = "TEXT"
    sub_attributes_ids.append(
        create_legacy_attribute_enum_type(
            environment,
            unit_of_measurement_name,
            unit_of_measurement_values,
            unit_of_measurement_enum_type
        )
    )

    name = "Container"
    attribute_id = create_legacy_group_attribute(
        environment=environment,
        name=name,
        attributes=sub_attributes_ids
    )

    return attribute_id


def create_legacy_group_attribute(
        environment: str,
        name: str,
        attributes: list) -> Union[bool, str]:
    """
    Create legacy group attribute.

    Parameters
    ----------
    environment : str
    name : str
    attributes : list

    Returns
    -------
    bool
        `False`, when a `TransportQueryError` occurs.
    str
        The attribute id.

    Raises
    ------
    TransportQueryError
        When a `gql` occurs.
    """
    description = f"DESCRIPTION OF {name}"

    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(
        url=base_url,
        headers=base_header
    )

    # Create a GraphQL client using the defined transport
    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    mut = create_legacy_group_attr()

    params = {
        "name": name,
        "description": description,
        "values": attributes
    }

    # Execute the query on the transport
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)

        if json_data:
            json_split = json_data.rsplit()
            id_att = json_split[2]
            id_att1 = id_att.lstrip('"')
            id_att2 = id_att1.rsplit('"', 1)[0]

            return id_att2
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def check_if_attribute_exist(
        environment: str,
        attribute: str) -> Union[bool, str]:
    """
    Check if attribute exist.

    Parameters
    ----------
    environment : str
    attribute : str

    Returns
    -------
    bool
        `False`, when a `TransportQueryError` occurs.
    str
        The response.

    Raises
    ------
    TransportQueryError
        When a `gql` occurs.
    """
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(
        url=base_url,
        headers=base_header
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    mut = gql(
        """
        query attributeModel($id: ID!){
            attributeModel(id: $id) {
                id
            }
        }
        """
    )

    params = {"id": attribute}

    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)

        return json_data
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def delete_attribute_supplier(
        environment: str,
        attribute: str) -> Union[str, bool]:
    """
    Delete attribute supplier.

    Parameters
    ----------
    environment : str
    attribute : str

    Returns
    -------
    bool
        `False`, when a `TransportQueryError` occurs.
    str
        The response.
    """
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(
        url=base_url,
        headers=base_header
    )

    # Create a GraphQL client using the defined transport
    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    mut = gql(
        """
        mutation deleteAttributeModel($id: ID!){
            deleteAttributeModel(id: $id)
        }
        """
    )

    params = {"id": attribute}
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)

        return json_data
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def search_specific_attribute(
        environment: str,
        attribute: list) -> Union[bool, str]:
    """
    Search specific attribute.

    Parameters
    ----------
    environment : str
    attribute : list

    Returns
    -------
    bool
        `False`, when a `TransportQueryError` occurs.
    str
        The response.
    """
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(
        url=base_url,
        headers=base_header
    )

    # Create a GraphQL client using the defined transport
    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    mut = create_search_specific_attribute_payload()

    params = {"id": attribute}
    try:
        response = client.execute(
            document=mut,
            variable_values=params
        )
        json_data = json.dumps(response)

        return json_data
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def search_all_attribute(
        environment: str,
        page_number: int) -> Union[bool, str]:
    """
    Search all attribute.

    Parameters
    ----------
    environment : str
    page_number : int

    Returns
    -------
    bool
        `False`, when a `TransportQueryError` occurs.
    str
        The response.
    """
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mut = create_search_all_attribute_payload()
    params = {"page": page_number}
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)

        return json_data
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def search_all_legacy_attributes(
        environment: str,
        page_number: int) -> Union[DocumentNode, bool]:
    """
    Search all legacy attributes.

    Parameters
    ----------
    environment : str
    page_number : int

    Returns
    -------
    DocumentNode
        The `gql` DocumentNode.
    bool:
        Does not contains any legacy attribute.
    """
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(
        url=base_url,
        headers=base_header
    )

    # Create a GraphQL client using the defined transport
    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    mut = create_search_all_legacy_attributes_payload()
    params = {"page": page_number}
    try:
        response = client.execute(mut, variable_values=params)

        return response
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def get_all_legacy_attributes(environment: str) -> tuple:
    """
    Get all legacy attributes.

    Parameters
    ----------
    environment : str

    Returns
    -------
    tuple
        The `semantic_id_and_id` as `dict` and \
        `has_all_attributes` as `bool`.
    """
    all_attributes = [
        "classification",
        "brand-id",
        "brand",
        "sub-brand-name",
        "minimum-order-quantity",
        "is-alcoholic",
        "is-narcotic",
        "hidden",
        "sales-ranking",
        "pallet-quantity",
        "unit-count",
        "item-count",
        "package-id",
        "package-name",
        "pack",
        "pack-material-type",
        "package",
        "size",
        "container-name",
        "unit-of-measurement",
        "container-material",
        "returnable",
        "container"
    ]

    semantic_id_and_id = {}
    has_all_attributes = False
    page_number = 0

    while not has_all_attributes and page_number < 50:
        result = search_all_legacy_attributes(environment, page_number)

        for attribute_model in result['attributeModels']:
            populate_attributes(
                all_attributes=all_attributes,
                attribute_model=attribute_model,
                semantic_id_and_id=semantic_id_and_id,
            )

        has_all_attributes = validate_if_contains_all_legacy_attributes(
            all_attributes=all_attributes,
            has_all_attributes=has_all_attributes,
            semantic_id_and_id=semantic_id_and_id
        )

        page_number += 1

    return semantic_id_and_id, has_all_attributes


def populate_attributes(
        all_attributes: list,
        attribute_model: dict,
        semantic_id_and_id: dict):
    """
    Populate attributes.

    Parameters
    ----------
    all_attributes : list
    attribute_model : dict
    semantic_id_and_id : dict
    """
    if attribute_model['semanticId'] in all_attributes:
        semantic_id = attribute_model['semanticId']
        semantic_id_and_id[semantic_id] = attribute_model['id']

        if attribute_model['attributeType'] == 'GROUP':
            populate_sub_attributes(
                all_attributes=all_attributes,
                attribute_model=attribute_model,
                semantic_id_and_id=semantic_id_and_id
            )


def populate_sub_attributes(
        all_attributes: list,
        attribute_model: dict,
        semantic_id_and_id: dict):
    """
    Poulate sub attributes.

    Parameters
    ----------
    all_attributes : list
    attribute_model : dict
    semantic_id_and_id : dict
    """
    for sub_attribute in attribute_model['metadata']['subAttributes']:
        if sub_attribute['semanticId'] in all_attributes:
            semantic_id = sub_attribute['semanticId']
            semantic_id_and_id[semantic_id] = sub_attribute['id']


def validate_if_contains_all_legacy_attributes(
        all_attributes: list,
        has_all_attributes: bool,
        semantic_id_and_id: dict) -> bool:
    """
    Validate if contains all legacy attributes.

    Parameters
    ----------
    all_attributes : list
    has_all_attributes : bool
    semantic_id_and_id : dict

    Returns
    -------
    bool
        Whenever contains the attribute.
    """
    for attribute in all_attributes:
        if attribute not in semantic_id_and_id.keys():
            has_all_attributes = False
            break

        has_all_attributes = True

    return has_all_attributes


def populate_package_attribute_payload(
        abstract_package_attribute_id: str,
        all_attributes: list) -> dict:
    """
    Populate package attribute payload.

    Parameters
    ----------
    abstract_package_attribute_id : str
    all_attributes : list

    Returns
    -------
    dict
        The payload as `dict`.
    """
    payload = {
        "abstractAttributeId": abstract_package_attribute_id,
        "values": [
            [
                {
                    "id": all_attributes['unit-count'],
                    "value": 1
                },
                {
                    "id": all_attributes['item-count'],
                    "value": 10
                },
                {
                    "id": all_attributes['package-id'],
                    "value": "pack_id"
                },
                {
                    "id": all_attributes['package-name'],
                    "value": "pack_name"
                },
                {
                    "id": all_attributes['pack'],
                    "value": "pack"
                },
                {
                    "id": all_attributes['pack-material-type'],
                    "value": "pack_material_type"
                }
            ]
        ]
    }

    return payload


def populate_container_attribute_payload(
        abstract_container_attribute_id: str,
        all_attributes: list) -> dict:
    """
    Populate container attribute payload.

    Parameters
    ----------
    abstract_container_attribute_id : str
    all_attributes : list

    Returns
    -------
    dict
        The payload as `dict`.
    """
    payload = {
        "abstractAttributeId": abstract_container_attribute_id,
        "values": [
            [
                {
                    "id": all_attributes['size'],
                    "value": 15
                },
                {
                    "id": all_attributes['container-name'],
                    "value": "container-name"
                },
                {
                    "id": all_attributes['unit-of-measurement'],
                    "value": "ML"
                },
                {
                    "id": all_attributes['container-material'],
                    "value": "container-material"
                },
                {
                    "id": all_attributes['returnable'],
                    "value": True
                }
            ]
        ]
    }

    return payload


def create_root_attribute_payload(root_abs_attr_ids: dict) -> list:
    """
    Create a root attribute payload.

    Parameters
    ----------
    root_abs_attr_ids : dict
        The root abstract attribute ids.

    Returns
    -------
    list
        The payload with the attributes.
    """
    payload = [
        {
            "abstractAttributeId": root_abs_attr_ids['classification'],
            "values": ["classification"]
        },
        {
            "abstractAttributeId": root_abs_attr_ids['brand-id'],
            "values": ["brand-id"]
        },
        {
            "abstractAttributeId": root_abs_attr_ids['brand'],
            "values": ["skol"]
        },
        {
            "abstractAttributeId": root_abs_attr_ids['sub-brand-name'],
            "values": ["sub-skol"]
        },
        {
            "abstractAttributeId": root_abs_attr_ids['minimum-order-quantity'],
            "values": [1]
        },
        {
            "abstractAttributeId": root_abs_attr_ids['is-alcoholic'],
            "values": [True]
        },
        {
            "abstractAttributeId": root_abs_attr_ids['is-narcotic'],
            "values": [False]
        },
        {
            "abstractAttributeId": root_abs_attr_ids['hidden'],
            "values": [False]
        },
        {
            "abstractAttributeId": root_abs_attr_ids['sales-ranking'],
            "values": [1]
        },
        {
            "abstractAttributeId": root_abs_attr_ids['pallet-quantity'],
            "values": [10]
        }]
    return payload


def display_specific_attribute(attribute: str):
    """
    Display specific attribute.

    Parameters
    ----------
    attribute : str
    """
    attribute_model = json.loads(attribute)
    info = attribute_model["attributeModel"]
    info_attribute = {
        "Name": info["name"],
        "Description": info["description"],
        "Attribute Type": info["attributeType"]
    }

    metadata_att = info['metadata']
    metadata = list()
    if metadata_att is None:
        metadata_info = {
            'Metadata': 'None'
        }
        metadata.append(metadata_info)
    elif info['attributeType'] == 'ENUM':
        metadata_info = {
            'Type': metadata_att['primitiveType'],
            'Value': metadata_att['values']
        }
        metadata.append(metadata_info)
    elif info['attributeType'] == 'GROUP':
        for i in range(len(metadata_att)):
            sub_attributes = metadata_att['subAttributes']
            for sub_attribute in sub_attributes:
                metadata_info = {
                    'Attribute ID': sub_attribute['id'],
                    'Attribute Name': sub_attribute['name'],
                    'Attribute Type': sub_attribute['attributeType']
                }
                metadata.append(metadata_info)

    print(text.default_text_color + '\nAttribute - General Information')
    print(tabulate([info_attribute], headers='keys', tablefmt='grid'))

    print(text.default_text_color + '\nAttribute - Metadata Information')
    print(tabulate(metadata, headers='keys', tablefmt='grid'))


def display_all_attribute(attributes: Any):
    """
    Display all attributes.

    Parameters
    ----------
    attributes : Any
    """
    attribute_model = json.loads(attributes)
    info = attribute_model['attributeModels']
    information_att = list()

    if len(info) == 0:
        info_attribute = {
            'Attribute Info': 'None'
        }
        information_att.append(info_attribute)
    else:
        for i in range(len(info)):
            metadata_att = info[i]['metadata']
            if metadata_att is None:
                metadata_info = {
                    'None'
                }
            elif info[i]['attributeType'] == 'ENUM':
                metadata_info = {
                    'Type': metadata_att['primitiveType'],
                    'Value': metadata_att['values']
                }
            elif info[i]['attributeType'] == 'GROUP':
                for x in range(len(metadata_att)):
                    sub_attributes = metadata_att['subAttributes']
                    for sub_attribute in sub_attributes:
                        metadata_info = {
                            'Attribute ID': sub_attribute['id'],
                            'Attribute Name': sub_attribute['name'],
                            'Attribute Type': sub_attribute['attributeType']
                        }
            metadata = metadata_info
            info_attribute = {
                'ID': info[i]['id'],
                'Name': info[i]['name'],
                'Attribute Type': info[i]['attributeType'],
                'Metadata': metadata
            }
            information_att.append(info_attribute)

    print(text.default_text_color + '\nAttribute - General Information')
    print(tabulate(information_att, headers='keys', tablefmt='grid'))


def edit_attribute_type(
        environment: str,
        attribute_id: str,
        attribute_type: str,
        values: list) -> Union[bool, str]:
    """
    Edit attribute type.

    Parameters
    ----------
    environment : str
    attribute_id : str
    attribute_type : str
    values : list

    Returns
    -------
    str
        The id of the category.
    bool
        Whenever a `gql` occours.

    Raises
    ------
    TransportQueryError
        When a `gql` error occours.
    """
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(
        url=base_url,
        headers=base_header
    )

    # Create a GraphQL client using the defined transport
    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    if attribute_type == '1':
        primitive_type = print_primitive_type()
        if primitive_type == '1':
            type_prim = 'NUMERIC'
        elif primitive_type == '2':
            type_prim = 'TEXT'
        elif primitive_type == '3':
            type_prim = 'DATE'

        mut = create_edit_primitive_attribute()
        params = {
            "id": attribute_id,
            "type": type_prim
        }

    elif attribute_type == '2':
        primitive_type = print_primitive_type()
        if primitive_type == '1':
            type_prim = 'NUMERIC'
        elif primitive_type == '2':
            type_prim = 'TEXT'
        elif primitive_type == '3':
            type_prim = 'DATE'
        mut = create_edit_enum_attribute()

        values = []
        value1 = input(text.default_text_color + 'Insert the first value: ')
        value2 = input(text.default_text_color + 'Insert the second value: ')
        values.append(value1)
        values.append(value2)

        params = {
            "id": attribute_id,
            "values": values,
            "enum_primitive_type": type_prim
        }

    elif attribute_type == '3':
        mut = create_edit_group_attribute()

        params = {
            "id": attribute_id,
            "values": values
        }

    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)

        return json_data
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def create_legacy_attribute_primitive_type(
        environment: str,
        name: str,
        attribute_type: str) -> Union[bool, str]:
    """
    Create legacy attribute primitive type.

    Parameters
    ----------
    environment : str
    name : str
    attribute_type : str

    Returns
    -------
    str
        The id of the category.
    bool
        Whenever a `gql` occours.

    Raises
    ------
    TransportQueryError
        When a `gql` error occours.
    """
    description = f"DESCRIPTION OF {name} ATTRIBUTE"

    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(
        url=base_url,
        headers=base_header
    )

    # Create a GraphQL client using the defined transport
    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    mut = create_primitive_attribute_payload()

    params = {
        "name": name,
        "description": description,
        "attribute_type": attribute_type
    }

    # Execute the query on the transport
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)

        if len(json_data) != 0:
            json_split = json_data.rsplit()
            id_att = json_split[2]
            id_att1 = id_att.lstrip('"')
            id_att2 = id_att1.rsplit('"', 1)[0]

            return id_att2

    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def create_legacy_attribute_enum_type(
        environment: str,
        name: str,
        values: list,
        type_prim: str):
    """
    Create legacy attribute enum type.

    Parameters
    ----------
    environment : str
    name : str
    values : str
    type_prim : str

    Returns
    -------
    str
        The id of the category.
    bool
        Whenever a `gql` occours.

    Raises
    ------
    TransportQueryError
        When a `gql` error occours.
    """
    description = f"DESCRIPTION OF {name} ATTRIBUTE"

    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    mut = create_enum_generic_payload()

    params = {
        "name": name,
        "description": description,
        "values": values,
        "enum_primitive_type": type_prim
    }

    # Execute the query on the transport
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)
        if len(json_data) != 0:
            json_split = json_data.rsplit()
            id_att = json_split[2]
            id_att1 = id_att.lstrip('"')
            id_att2 = id_att1.rsplit('"', 1)[0]

            return id_att2

    except TransportQueryError as e:
        print(text.Red + str(e))

        return False
