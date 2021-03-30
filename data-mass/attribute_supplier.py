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
from menus.supplier_menu import print_primitive_type


def create_attribute_primitive_type(environment, type_attribute):
    name = 'DM ATTRIBUTE ' + str(type_attribute) + ' ' + str(randint(1, 100000))
    description = 'DM DESCRIPTION to ' + name

    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mut = create_primitive_attribute_payload()

    params = {'name': name, 'description': description, 'attribute_type': type_attribute}

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
        values.append(str(randint(1, 100000)) + '1')
        values.append(str(randint(1, 100000)) + '2')
        values.append(str(randint(1, 100000)) + '3')
    elif type_attribute == 'DATE':
        values.append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') + 'T00:00:00')
        values.append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') + 'T00:00:00')
        values.append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') + 'T00:00:00')
    elif type_attribute == 'TEXT':
        values.append(string.ascii_lowercase + 'a')
        values.append(string.ascii_lowercase + 'b')
        values.append(string.ascii_lowercase + 'c')

    mut = create_enum_generic_payload()
    params = {'name': name, 'description': description, 'values': values, 'enum_primitive_type': type_attribute }

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
            id_att1 = id_att.lstrip('"')
            id_att2 = id_att1.rsplit('"', 1)[0]
            return id_att2
    except TransportQueryError as e:
        print(text.Red + str(e))
        return False


def create_primitive_attribute_payload():
    return gql(
        """
        mutation createAttributeModel($name: String!, $description: String!, $attribute_type: AttributeType!) {
            createAttributeModel(input: {
                name: $name,
                description: $description,
                helpText: "This is an attribute to help you in your test",
                attributeType: $attribute_type
        }){
            id
            attributeType
        }
    }
    """
    )


def create_enum_generic_payload():
    return gql(
        """
        mutation createAttributeModel($name: String!, $description: String!, $values: [String!]!, 
            $enum_primitive_type: AttributePrimitiveType) {
            createAttributeModel(input: {
                name: $name,
                description: $description,
                helpText: "This is an attribute to help you in your test",
                attributeType: ENUM,
                metadata: {
                    enumPrimitiveType: $enum_primitive_type,
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
        return False


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
        return False


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
        return False


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
        return False


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


def edit_attribute_type(environment, attribute_id, type, values):
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    if type == '1':
        primitive_type = print_primitive_type()
        if primitive_type == '1':
            type_prim = 'NUMERIC'
        elif primitive_type == '2':
            type_prim = 'TEXT'
        elif primitive_type == '3':
            type_prim = 'DATE'

        mut = create_edit_primitive_attribute()
        params = {"id": attribute_id, "type": type_prim}

    elif type == '2':
        primitive_type = print_primitive_type()
        if primitive_type == '1':
            type_prim = 'NUMERIC'
        elif primitive_type == '2':
            type_prim = 'TEXT'
        elif primitive_type == '3':
            type_prim = 'DATE'
        mut = create_edit_enum_attribute()

        values = list()
        value1 = input(text.default_text_color + 'Insert the first value: ')
        value2 = input(text.default_text_color + 'Insert the second value: ')
        values.append(value1)
        values.append(value2)

        params = {'id': attribute_id, 'values': values, 'enum_primitive_type': type_prim}

    elif type == '3':
        mut = create_edit_group_attribute()
        params = {"id": attribute_id, "values": values}

    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)
        return json_data
    except TransportQueryError as e:
        print(text.Red + str(e))
        return False


def create_edit_primitive_attribute():
    return gql(
        '''
        mutation updateAttribute($id: ID!, $type: AttributeType){
            updateAttributeModel(id: $id,
                input: {
                    attributeType: $type
                }
            ) {
                id
                attributeType
            }
        }
        '''
    )


def create_edit_enum_attribute():
    return gql(
        '''
        mutation updateAttribute($id: ID!, $values: [String!]!, $enum_primitive_type: AttributePrimitiveType) {
    updateAttributeModel(id: $id,
        input: {
            attributeType: ENUM,
            metadata: {
                enumPrimitiveType: $enum_primitive_type,
                enumValues: $values
            }
        }
    ) {
        id
        }
    }
        '''
    )


def create_edit_group_attribute():
    return gql(
        '''
        mutation updateAttribute($id: ID!, $values: [ID!] ){
            updateAttributeModel(id: $id,
                input: {
                    attributeType: GROUP,
                    metadata: {
                        subAttributes: $values
                }
                }
            ) {
                id
                attributeType
                metadata {
                    ... on GroupAttributeModelMetadata {
                        subAttributes {
                            id
                        }
                    }
                }
            }
        }
        '''
    )
