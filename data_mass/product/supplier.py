import json
from datetime import datetime, timedelta
from random import randint
from gql import gql, Client
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport
import string
from tabulate import tabulate

from data_mass.attribute_supplier import create_attribute_primitive_type
from data_mass.classes.text import text
from data_mass.common import get_supplier_base_url, get_header_request_supplier
from data_mass.menus.supplier_menu import print_primitive_type
from data_mass.supplier_category import create_root_category, \
    create_association_attribute_with_category


def create_product_supplier(environment):
    name = 'DM PRODUCT ' + str(randint(1, 100000))
    description = 'DM DESCRIPTION to ' + name
    var_name = 'DM VARIANT ' + str(randint(1, 100000))
    att_type_option = 'TEXT'

    att1 = create_attribute_primitive_type(environment, att_type_option)
    att2 = create_attribute_primitive_type(environment, att_type_option)

    category = create_root_category(environment)

    abs1 = create_association_attribute_with_category(environment, att1, category, 1, 1)
    abs2 = create_association_attribute_with_category(environment, att2, category, 1, 1)

    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mut = create_product_payload()

    params = {'name': name, 'description': description, 'category': category, 'abstractAttributeId1': abs1,
              'abstractAttributeId2': abs2, 'varName': var_name}
    # Execute the query on the transport
    try:
        response = client.execute(mut, variable_values=params)
        json_data = json.dumps(response)
        if len(json_data) != 0:
            json_split = json_data.rsplit()
            product_id = json_split[2]
            product_id1 = product_id.lstrip('"')
            product_id2 = product_id1.rsplit('"', 1)[0]
            return product_id2
    except TransportQueryError as e:
        print(text.Red + str(e))
        return False


def create_product_payload():
    return gql(
        '''
        mutation createProduct(
              $name: String!
              $description: String!
              $category: ID!
              $varName: String!
              $abstractAttributeId1: ID!
              $abstractAttributeId2: ID!
            ) {
              createProduct(
                input: {
                  name: $name
                  description: $description
                  categoryId: $category
                  country: "BR"
                  images: ["http://test.com/1"]
                  vendorId: "e437c69f-2f6e-4412-b78b-1845c8ac8838"
                  manufacturerId: "0c2e96b5-26ea-4698-80a7-86d658656572"
                  attributes: [
                    { abstractAttributeId: $abstractAttributeId1, values: ["1"] }
                  ]
                  variants: [
                    {
                      name: $varName
                      images: ["http://testVariant.com/1"]
                      skus: ["123"]
                      attributes: [
                        { abstractAttributeId: $abstractAttributeId2, values: ["2"] }
                      ]
                    }
                  ]
                }
              ) {
                id
              }
            }
        '''
    )

