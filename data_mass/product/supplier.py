import json
from datetime import datetime, timedelta
from random import randint
from gql import gql, Client
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport
import string
from tabulate import tabulate

from data_mass.attribute_supplier import get_all_legacy_attributes, populate_package_attribute_payload, \
    populate_container_attribute_payload, create_root_attribute_payload
from data_mass.classes.text import text
from data_mass.common import get_supplier_base_url, get_header_request_supplier
from data_mass.supplier_category import associate_all_legacy_attributes


def create_product_supplier(environment, category_id):
    name = 'DM PRODUCT ' + str(randint(1, 100000))
    description = 'DM DESCRIPTION to ' + name
    var_name = 'DM VARIANT ' + str(randint(1, 100000))

    all_attributes = get_all_legacy_attributes(environment)

    root_abstract_attribute_ids_dictionary, package_abstract_attribute_id, container_abstract_attribute_id = \
        associate_all_legacy_attributes(environment, category_id, all_attributes)

    package_group_payload = populate_package_attribute_payload(package_abstract_attribute_id, all_attributes)
    container_group_payload = populate_container_attribute_payload(container_abstract_attribute_id, all_attributes)

    attributes = create_root_attribute_payload(root_abstract_attribute_ids_dictionary)
    attributes.append(package_group_payload)
    attributes.append(container_group_payload)

    # Select your transport with a defined url endpoint
    base_url = get_supplier_base_url(environment)
    base_header = get_header_request_supplier()
    transport = RequestsHTTPTransport(url=base_url, headers=base_header)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mut = create_product_payload()

    params = {'name': name, 'description': description, 'category': category_id,
              'attributes': attributes, 'varName': var_name}

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
              $attributes: [ConcreteAttributeInput!]!
            ) {
              createProduct(
                input: {
                  name: $name
                  description: $description
                  categoryId: $category
                  country: "BR"
                  images: ["http://test.com/1"]
                  attributes: 
                    $attributes
                  variants: [
                    {
                      name: $varName
                      images: ["http://testVariant.com/1"]
                      skus: ["123"]
                      vendorId: "e437c69f-2f6e-4412-b78b-1845c8ac8838"
                      manufacturerId: "0c2e96b5-26ea-4698-80a7-86d658656572"
                      attributes: []
                    }
                  ]
                }
              ) {
                id
              }
            }
        '''
    )

