import json
from random import randint
from typing import Any, Union

from gql import Client, gql
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport
from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.common import get_header_request_supplier, get_supplier_base_url, set_to_dictionary
from data_mass.supplier.attribute import (
    create_legacy_attribute_container,
    create_legacy_attribute_package,
    create_legacy_root_attribute,
    get_all_legacy_attributes,
    search_specific_attribute
)
from data_mass.supplier.gql.categories import (
    create_association_payload,
    create_root_category_payload,
    create_search_specific_category_payload,
    create_sub_category_payload,
    search_all_category_payload
)


def create_root_category(
        environment: str,
        name: str = None) -> Union[str, bool]:
    """
    Create root category.

    Parameters
    ----------
    environment : str
    name : str, optional
        The name, by default None.

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
    if name is None:
        name = 'DM CATEGORY ROOT ' + str(randint(1, 100000))

    description = 'DM DESCRIPTION to ' + name

    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mut = create_root_category_payload()
    params = {'name': name, 'description': description}

    # Execute the query on the transport
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)

        if len(json_data) != 0:
            json_split = json_data.rsplit()
            id_cat = json_split[2]
            id_cat1 = id_cat.lstrip('"')
            id_cat2 = id_cat1.rsplit('"', 1)[0]

            return id_cat2
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def create_sub_category_supplier(
        environment: str,
        parent: str) -> Union[str, bool]:
    """
    Create sub category supplier.

    Parameters
    ----------
    environment : str
    parent : str

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
    rand_int = str(randint(1, 100000))
    name = f"DM SUBCATEGORY {rand_int}"
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

    mut = create_sub_category_payload()
    params = {
        "name": name,
        "description": description,
        "parent": parent
    }

    # Execute the query on the transport
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)

        if len(json_data) != 0:
            json_split = json_data.rsplit()
            id_cat = json_split[2]
            id_cat1 = id_cat.lstrip('"')
            id_cat2 = id_cat1.rsplit('"', 1)[0]

            return id_cat2
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def check_if_supplier_category_exist(
        environment: str,
        category: str) -> Union[bool, str]:
    """
    Check if supplier category exists.

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

    mut = gql(
        """
        query category(
            $id: ID!
        ) {
            category(id: $id){
                id
            }
        }
    """)

    params = {"id": category}
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)

        return json_data
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def create_association_attribute_with_category(
        environment: str,
        attribute_id: str,
        category_id: str,
        min_cardinality: int,
        max_cardinality: int,
        metadata_values: list = None) -> Union[bool, str]:
    """
    Create association attribute with category.

    Parameters
    ----------
    environment : str
    attribute_id : str
    category_id : str
    min_cardinality : int
    max_cardinality : int
    metadata_values : list

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

    mut = create_association_payload()

    params = {
        "attribute_id": attribute_id,
        "category_id": category_id,
        "min_cardinality": min_cardinality,
        "max_cardinality": max_cardinality,
        "metadata_values": metadata_values
    }

    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)
        if len(json_data) != 0:
            json_split = json_data.rsplit()
            id_abs = json_split[2]
            id_abs1 = id_abs.lstrip('"')
            id_abs2 = id_abs1.rsplit('"', 1)[0]

            return id_abs2
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def search_specific_category(
        environment: str,
        category: str) -> Union[bool, str]:
    """
    Search specific category.

    Parameters
    ----------
    environment : str
    category : str

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

    mut = create_search_specific_category_payload()

    params = {"id": category}
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)

        return json_data
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def display_specific_category(category: Any):
    """
    Display specific category.

    Paramters
    ---------
    category: Any
    """
    category_model = json.loads(category)
    info = category_model['category']
    info_category = {
        'Name': info['name'],
        'Description': info['description'],
    }

    parent = info['parent']
    if parent is None:
        parent_info = {
            'Parent': 'None'
        }
    else:
        parent_info = {
            'Parent Id': parent['id'],
            'Parent Name': parent['name']
        }

    ancestors = info['ancestors']
    ancestors_list = []

    if len(ancestors) == 0:
        ancestors_info = {
            "Ancestors": "None"
        }
        ancestors_list.append(ancestors_info)
    else:
        for i in range(len(ancestors)):
            ancestors_info = {
                "Ancestor Id": ancestors[i]["id"],
                "Ancestor Name": ancestors[i]["name"]
            }
            ancestors_list.append(ancestors_info)

    attributes = info["attributes"]
    attributes_list = []

    if len(attributes) == 0:
        attributes_info = {"Attributes": "None"}
        attributes_list.append(attributes_info)
    for a in range(len(attributes)):
        if attributes[a]['__typename'] == 'AbstractAttribute':
            attributes_info = {
                'Attribute Type': 'AbstractAttribute',
                'Attribute Id': attributes[a]['id'],
                'Attribute Min. Cardinality': attributes[a]['minCardinality'],
                'Attribute Max. Cardinality': attributes[a]['maxCardinality']
            }
            attributes_list.append(attributes_info)
        elif attributes[a]['__typename'] == 'ConcreteAttribute':
            attributes_info = {
                'Attribute Type': 'ConcreteAttribute',
                'Attribute Id': attributes[a]['id'],
                'Attribute Values': attributes[a]['values'],

            }
            attributes_list.append(attributes_info)

    print(text.default_text_color + '\nCategory - General Information')
    print(tabulate([info_category], headers='keys', tablefmt='fancy_grid'))

    print(text.default_text_color + '\nCategory - Parent Information')
    print(tabulate([parent_info], headers='keys', tablefmt='fancy_grid'))

    print(text.default_text_color + '\nCategory - Ancestor Information')
    print(tabulate(ancestors_list, headers='keys', tablefmt='fancy_grid'))

    print(text.default_text_color + '\nCategory - Attribute Information')
    print(tabulate(attributes_list, headers='keys', tablefmt='fancy_grid'))


def search_all_category(
        environment: str,
        page_number: int) -> Union[bool, str]:
    """
    Search all categories

    Parameters
    ----------
    environment : str
    page_number : int

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

    mut = search_all_category_payload()
    params = {"page": page_number}

    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)

        return json_data
    except TransportQueryError as e:
        print(text.Red + str(e))

        return False


def display_all_category(category: Any):
    """
    Display all categories.

    Parameters
    ----------
    category : Any
    """
    category_model = json.loads(category)
    info = category_model["categories"]
    information_cat = []

    if not info:
        category_info = {"Category Info": "None"}
        information_cat.append(category_info)
    else:
        for a in range(len(info)):
            parent = info[a]["parent"]
            if parent is None:
                parent_info = {
                    "None"
                }
            else:
                parent_info = {
                    "Id": parent["id"],
                    "Name": parent["name"]
                }

            category_info = {
                "Id": info[a]["id"],
                "Name": info[a]["name"],
                "Parent": parent_info
            }
            information_cat.append(category_info)

    print(text.default_text_color + '\nCategory - General Information')
    print(tabulate(information_cat, headers='keys', tablefmt='fancy_grid'))


def associate_all_legacy_attributes(
        environment: str,
        category_id: str,
        all_attributes: dict) -> tuple:
    """
    Associate all legacy attributes.

    Parameters
    ----------
    environment : str
    category_id : str
    all_attributes : dict

    Returns
    -------
    tuple
        A tuple with `root_abs_att_id`,\
        `package_abs_att_id` and `container_abs_att_id`.
    """
    attributes_to_be_associated = [
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
        "package",
        "container"
    ]

    root_abs_att_id = {}
    package_abs_att_id = None
    container_abs_att_id = None

    for attribute in attributes_to_be_associated:
        if attribute == "package":
            package_abs_att_id = \
                create_association_attribute_with_category(
                    environment=environment,
                    attribute_id=all_attributes[attribute],
                    category_id=category_id,
                    min_cardinality=0,
                    max_cardinality=1,
                    metadata_values=get_group_sub_attributes_metadata(environment=environment, attribute_id=all_attributes[attribute])
                )
        elif attribute == "container":
            container_abs_att_id = \
                create_association_attribute_with_category(
                    environment=environment,
                    attribute_id=all_attributes[attribute],
                    category_id=category_id,
                    min_cardinality=0,
                    max_cardinality=1,
                    metadata_values=get_group_sub_attributes_metadata(environment=environment, attribute_id=all_attributes[attribute])
                )
        else:
            if attribute == "brand-id":
                abstract_attribute_id = \
                    create_association_attribute_with_category(
                        environment=environment,
                        attribute_id=all_attributes[attribute],
                        category_id=category_id,
                        min_cardinality=1,
                        max_cardinality=1
                    )
            else:
                abstract_attribute_id = \
                    create_association_attribute_with_category(
                        environment=environment,
                        attribute_id=all_attributes[attribute],
                        category_id=category_id,
                        min_cardinality=0,
                        max_cardinality=1
                    )

            root_abs_att_id[attribute] = abstract_attribute_id

    return root_abs_att_id, package_abs_att_id, container_abs_att_id


def create_legacy_category(
        environment: str,
        category_name: str) -> Union[bool, str]:
    """
    Create legacy category.

    Parameters
    ----------
    environment : str
    category_name : str

    Returns
    -------
    str
        The id of the category.
    bool
        Whenever a `gql` occours.
    """
    category_id = create_root_category(environment, category_name)

    if category_id is False:
        return False

    all_attributes, has_all_attributes = \
        get_all_legacy_attributes(environment)

    if not has_all_attributes:
        create_legacy_root_attribute(environment)
        create_legacy_attribute_package(environment)
        create_legacy_attribute_container(environment)

    all_attributes_2, has_all_attributes = \
        get_all_legacy_attributes(environment)

    associate_all_legacy_attributes(
        environment=environment,
        category_id=category_id,
        all_attributes=all_attributes_2
    )

    return category_id


def verify_if_category_has_all_legacy_category(
        environment: str,
        category: str):
    """
    Verify if a categor has all legacy categories.

    Parameters
    ----------
    environment : str
    category : str

    Returns
    -------
    bool
        Whenever a category has all legacy categories.
    """
    all_attributes = [
        'classification',
        'brand-id',
        'brand',
        'sub-brand-name',
        'minimum-order-quantity',
        'is-alcoholic',
        'is-narcotic',
        'hidden',
        'sales-ranking',
        'pallet-quantity',
        'unit-count',
        'item-count',
        'package-id',
        'package-name',
        'pack',
        'pack-material-type',
        'package',
        'size',
        'container-name',
        'unit-of-measurement',
        'container-material',
        'returnable',
        'container'
    ]

    result = search_specific_category(environment, category)
    category_result = json.loads(result)

    attribute_semantic_id = []
    info = category_result['category']
    attributes_info = info['attributes']

    for i in range(len(attributes_info)):
        attribute_model = attributes_info[i]['attributeModel']
        attribute_semantic_id = attribute_model['semanticId']

    if attribute_semantic_id in all_attributes:
        return True

    return False


def get_group_sub_attributes_metadata(environment, attribute_id):
    attribute = search_specific_attribute(environment, attribute_id)
    attribute_model = json.loads(attribute)
    info = attribute_model["attributeModel"]
    metadata_att = info['metadata']
    attr_metadata_dicts = list()

    required_attrs = [
        "Container Name",
        "Size",
        "Returnable",
        "Unit of Measurement",
        "Unit Count",
        "Package ID",
        "Package Name"
    ]
    optional_attrs = [
        "Container Material",
        "Item Count",
        "Pack Material Type",
        "Pack"
    ]

    for i in range(len(metadata_att)):
        sub_attributes = metadata_att['subAttributes']

        for sub_attribute in sub_attributes:
            metadata_info = dict()
            sub_attr_name = sub_attribute['name']
            if sub_attr_name in required_attrs:
                metadata_info = {
                    'subAttributeId': sub_attribute['id'],
                    'minCardinality': 1,
                    'maxCardinality': 1
                }

            elif sub_attr_name in optional_attrs:
                metadata_info = {
                    'subAttributeId': sub_attribute['id'],
                    'minCardinality': 0,
                    'maxCardinality': 1
                }

            attr_metadata_dicts.append(metadata_info)

    return attr_metadata_dicts
