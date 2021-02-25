import json
from datetime import datetime, timedelta
from random import randint
from gql import gql, Client
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport
import string

from tabulate import tabulate

from classes.text import text
from common import get_supplier_base_url, get_header_request_supplier


def create_attribute_primitive_type(environment, type_attribute):
    name = 'DM ATTRIBUTE ' + str(type_attribute) + ' ' + str(randint(1, 100000))
    description = 'DM DESCRIPTION to ' + name

    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    # Provide a GraphQL query
    if type_attribute == 'NUMERIC':
        mut = create_numeric_payload()
    elif type_attribute == 'DATE':
        mut = create_date_payload()
    elif type_attribute == 'TEXT':
        mut = create_text_payload()

    params = {'name': name, 'description': description}

    # Execute the query on the transport
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)
        if len(json_data) != 0:
            json_split = json_data.rsplit()
            id_att = json_split[2]
            return id_att
    except TransportQueryError as e:
        print(text.Red + str(e))
        return 'false'


def create_attribute_enum(environment, type_attribute):
    name = 'DM ATTRIBUTE ' + str(type_attribute) + ' ' + str(randint(1, 100000))
    description = 'DM DESCRIPTION to ' + name

    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)
    values = list()
    # Provide a GraphQL query
    if type_attribute == 'NUMERIC':
        mut = create_enum_numeric_payload()
        values.append(str(randint(1, 100000)) + '1')
        values.append(str(randint(1, 100000)) + '2')
        values.append(str(randint(1, 100000)) + '3')
    elif type_attribute == 'DATE':
        mut = create_enum_date_payload()
        values.append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') + 'T00:00:00')
        values.append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') + 'T00:00:00')
        values.append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') + 'T00:00:00')
    elif type_attribute == 'TEXT':
        mut = create_enum_text_payload()
        values.append(string.ascii_lowercase + 'a')
        values.append(string.ascii_lowercase + 'b')
        values.append(string.ascii_lowercase + 'c')

    params = {'name': name, 'description': description, 'values': values}

    # Execute the query on the transport
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)
        if len(json_data) != 0:
            json_split = json_data.rsplit()
            id_att = json_split[2]
            return id_att
    except TransportQueryError as e:
        print(text.Red + str(e))
        return 'false'


def create_attribute_group(environment, attributes):
    name = 'DM ATTRIBUTE GROUP' + str(randint(1, 100000))
    description = 'DM DESCRIPTION to ' + name

    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mut = gql(
        """
        mutation createAttributeModel($name: String!, $description: String!, $values: [ID!]){
            createAttributeModel(input: {
                name: $name,
                description: $description,
                helpText: "This is an attribute to help you in your test",
                attributeType: GROUP,
                metadata: {
                    subAttributes: $values
                }
            }){
                id
                name
                description
                helpText
                attributeType
                metadata {
                     ... on GroupAttributeModelMetadata {
                            subAttributes{
                                id
                            }
                    }
                }
                createdAt
                }
            }
        """
    )

    params = {'name': name, 'description': description, 'values': attributes}

    # Execute the query on the transport
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)
        if len(json_data) != 0:
            json_split = json_data.rsplit()
            id_att = json_split[2]
            return id_att
    except TransportQueryError as e:
        print(text.Red + str(e))
        return 'false'


def create_numeric_payload():
    return gql(
        """
        mutation createAttributeModel($name: String!, $description: String!) {
            createAttributeModel(input: {
                name: $name,
                description: $description,
                helpText: "This is an attribute to help you in your test",
                attributeType: NUMERIC
        }){
            id
            attributeType
        }
    }
    """
    )


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


def create_date_payload():
    return gql(
        """
        mutation createAttributeModel($name: String!, $description: String!) {
            createAttributeModel(input: {
                name: $name,
                description: $description,
                helpText: "This is an attribute to help you in your test",
                attributeType: DATE
        }){
            id
            attributeType
        }
    }
    """
    )


def create_enum_numeric_payload():
    return gql(
        """
        mutation createAttributeModel($name: String!, $description: String!, $values: [String!]!) {
            createAttributeModel(input: {
                name: $name,
                description: $description,
                helpText: "This is an attribute to help you in your test",
                attributeType: ENUM,
                metadata: {
                    enumPrimitiveType: NUMERIC,
                    enumValues: $values
                }
        }){
            id
            }
        }
    """
    )


def create_enum_text_payload():
    return gql(
        """
        mutation createAttributeModel($name: String!, $description: String!, $values: [String!]!) {
            createAttributeModel(input: {
                name: $name,
                description: $description,
                helpText: "This is an attribute to help you in your test",
                attributeType: ENUM,
                metadata: {
                    enumPrimitiveType: TEXT,
                    enumValues: $values
                }
        }){
            id            
            }
        }
    """
    )


def create_enum_date_payload():
    return gql(
        """
        mutation createAttributeModel($name: String!, $description: String!, $values: [String!]!) {
            createAttributeModel(input: {
                name: $name,
                description: $description,
                helpText: "This is an attribute to help you in your test",
                attributeType: ENUM,
                metadata: {
                    enumPrimitiveType: DATE,
                    enumValues: $values
                }
        }){
            id
            }
        }
    """
    )


def check_if_attribute_exist(environment, attribute):
    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mut = gql("""
        query attributeModel($id: ID!){  
            attributeModel(id: $id) {
                id
                  }
            }
    """)

    params = {"id": attribute}
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)
        return json_data
    except TransportQueryError as e:
        print(text.Red + str(e))
        return 'false'


def delete_attribute_supplier(environment, attribute):
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mut = gql("""
            mutation deleteAttributeModel($id: ID!){
            deleteAttributeModel(id: $id)
          }
        """)

    params = {"id": attribute}
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)
        return json_data
    except TransportQueryError as e:
        print(text.Red + str(e))
        return 'false'


def search_specific_attribute(environment, attribute):
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mut = create_search_specific_attribute_payload()

    params = {"id": attribute}
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)
        return json_data
    except TransportQueryError as e:
        print(text.Red + str(e))
        return 'false'


def search_all_attribute(environment, page_number):
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
        return 'false'


def display_specific_attribute(attribute):
    attribute_model = json.loads(attribute)
    info = attribute_model['attributeModel']
    info_attribute = {
        'Name': info['name'],
        'Description': info['description'],
        'Attribute Type': info['attributeType']
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


def display_all_attribute(attributes):
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


def create_search_specific_attribute_payload():
    return gql(
        """
        query attributeModel($id: ID!){  
            attributeModel(id: $id) {
                id
                name
                semanticId
                description
                attributeType
                metadata {
                    ... on EnumAttributeModelNumericMetadata {
                        primitiveType
                        values
                    }
                    ... on EnumAttributeModelStringMetadata {
                        primitiveType
                        values
                    }
                    ... on EnumAttributeModelDateMetadata {
                        primitiveType
                        values
                    }
                    ... on GroupAttributeModelMetadata {
                        subAttributes{
                            id
                            name
                            attributeType
                        }
                    }
                }
            }
        }
    """
    )


def create_search_all_attribute_payload():
    return gql(
        '''
        query attributeModels($page: NonNegativeInt) {
            attributeModels(input:  {
                page: $page
                size: 50
                }){
                    id
                    name
                    semanticId
                    description
                    helpText
                    attributeType 
                    createdAt 
                    metadata {
                        ... on EnumAttributeModelNumericMetadata {
                            primitiveType
                            values
                        }
                        ... on EnumAttributeModelStringMetadata {
                            primitiveType
                            values
                        }
                        ... on EnumAttributeModelDateMetadata {
                            primitiveType
                            values
                        }
                        ... on GroupAttributeModelMetadata {
                            subAttributes{
                                id
                                name
                                attributeType
                            }
                        }
                    }   
                }
        }
        '''
    )
