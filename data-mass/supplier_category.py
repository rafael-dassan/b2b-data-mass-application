import json
from random import randint
from gql import gql, Client
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport

from classes.text import text
from common import get_supplier_base_url, get_header_request_supplier


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
            return id_cat
    except TransportQueryError as e:
        print(text.Red + str(e))
        return 'false'


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
            return id_cat
    except TransportQueryError as e:
        print(text.Red + str(e))
        return 'false'


def create_text_payload():
    return gql(
        """
        mutation createAttributeModel($name: String!, $description: String!) {
            createAttributeModel(input: {
                name: $name,
                description: $description,
                helpText: "This is an attribute to help you in your test",
                attributeType: TEXT
        }){
            id
            attributeType
        }
    }
    """
    )


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
        return 'false'


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
            id_cat = json_split[2]
            return id_cat
    except TransportQueryError as e:
        print(text.Red + str(e))
        return 'false'


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
