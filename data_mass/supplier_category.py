import json
from random import randint
from gql import gql, Client
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport
from tabulate import tabulate

from data_mass.classes.text import text
from data_mass.tools.requests import (
    get_header_request_supplier,
    get_supplier_base_url,
)


def create_root_category(environment):
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


def create_sub_category_supplier(environment, parent):
    name = 'DM SUBCATEGORY ' + str(randint(1, 100000))
    description = 'DM DESCRIPTION to ' + name

    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mut = create_sub_category_payload()
    params = {'name': name, 'description': description, 'parent': parent}

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


def create_sub_category_payload():
    return gql(
        """
             mutation createCategory($name: String!, $description: String!, $parent: ID) {
                  createCategory(input: {
                        name: $name, 
                        helpText: $description, 
                        description: "Create Category"
                        parentId: $parent
                        }) {
                            id
                            name
                            helpText
                             description
                        }}
        """
    )


def create_root_category_payload():
    return gql(
        """
            mutation createCategory($name: String!, $description: String!) {
                createCategory(input: {
                    name: $name, 
                    helpText: $description, 
                    description: "Create Category"
                    }) {
                        id
                        name
                        helpText
                        description
                    }}
    """
    )


def check_if_supplier_category_exist(environment, category):
    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mut = gql("""
        query category($id: ID!){  
            category(id: $id) {
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


def create_association_attribute_with_category(environment, attribute_id, category_id, min_cardinality,
                                               max_cardinality):
    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mut = create_association_payload()

    params = {"attribute_id": attribute_id, "category_id": category_id, "min_cardinality": min_cardinality,
              "max_cardinality": max_cardinality}
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


def create_association_payload():
    return gql(
        """
               mutation associateAttribute($attribute_id: ID!, $category_id: ID!, $min_cardinality: NonNegativeInt!, $max_cardinality: NonNegativeInt!) { 
                  associateAttribute(
                    input: {
                      attributeModelId: $attribute_id
                      taxonomyNodeId: $category_id
                      minCardinality: $min_cardinality
                      maxCardinality: $max_cardinality
                    }
                  ) {
                    id
                    minCardinality
                    maxCardinality
                    taxonomyNode {
                      id
                      name
                      children{
                            id
                            name
                        }
                    }
                    attributeModel {
                      id
                      name
                    }
                  }
                }
    """
    )


def search_specific_category(environment, category):
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mut = create_search_specific_category_payload()

    params = {"id": category}
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)
        return json_data
    except TransportQueryError as e:
        print(text.Red + str(e))
        return False


def create_search_specific_category_payload():
    return gql(
        '''
             query category($id: ID!){
              category(id: $id) {
                name
                description
                parent {
                  id
                  name
                }
                children {
                  id
                  name
                }
                ancestors {
                  id
                  name
                }
               attributes {
                        ... on AbstractAttribute {
                            id
                            minCardinality
              	            maxCardinality
                            __typename
                        }
                        ... on ConcreteAttribute {
                            id
                            values
                            __typename
                        }
                    }
                createdAt
              }
            }
        '''

    )


def display_specific_category(category):
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
    ancestors_list = list()
    if len(ancestors) == 0:
        ancestors_info = {
            'Ancestors': 'None'
        }
        ancestors_list.append(ancestors_info)
    else:
        for i in range(len(ancestors)):
            ancestors_info = {
                'Ancestor Id': ancestors[i]['id'],
                'Ancestor Name': ancestors[i]['name']
            }
            ancestors_list.append(ancestors_info)

    attributes = info['attributes']
    attributes_list = list()
    if len(attributes) == 0:
        attributes_info = {
            'Attributes': 'None'
        }
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
    print(tabulate([info_category], headers='keys', tablefmt='grid'))

    print(text.default_text_color + '\nCategory - Parent Information')
    print(tabulate([parent_info], headers='keys', tablefmt='grid'))

    print(text.default_text_color + '\nCategory - Ancestor Information')
    print(tabulate(ancestors_list, headers='keys', tablefmt='grid'))

    print(text.default_text_color + '\nCategory - Attribute Information')
    print(tabulate(attributes_list, headers='keys', tablefmt='grid'))


def search_all_category(environment, page_number):
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mut = search_all_category_payload()
    params = {"page": page_number}
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)
        return json_data
    except TransportQueryError as e:
        print(text.Red + str(e))
        return False


def search_all_category_payload():
    return gql(
        '''
            query categories($page: NonNegativeInt){
                categories(input: { page: $page, size: 50 }) {
                    id
                    name
                    description
                    helpText
                    parent {
                      id
                      name
                    }
                    children {
                      id
                      name
                    }
                    ancestors {
                      id
                      name
                    }
                    attributes {
                      ... on AbstractAttribute {
                        id
                        minCardinality
                        maxCardinality
                        __typename
                      }
                      ... on ConcreteAttribute {
                        id
                        values
                        __typename
                      }
                    }
                    createdAt
                    }
                }
        '''
    )


def display_all_category(category):
    category_model = json.loads(category)
    info = category_model['categories']
    information_cat = list()

    if len(info) == 0:
        category_info = {
            'Category Info': 'None'
        }
        information_cat.append(category_info)
    else:
        for a in range(len(info)):
            parent = info[a]['parent']
            if parent is None:
                parent_info = {
                    'None'
                }
            else:
                parent_info = {
                    'Id': parent['id'],
                    'Name': parent['name']
                }

            category_info = {
                'Id': info[a]['id'],
                'Name': info[a]['name'],
                'Parent': parent_info
            }
            information_cat.append(category_info)

    print(text.default_text_color + '\nCategory - General Information')
    print(tabulate(information_cat, headers='keys', tablefmt='grid'))
