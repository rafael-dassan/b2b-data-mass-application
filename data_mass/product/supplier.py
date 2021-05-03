import json
from datetime import datetime, timedelta
from random import randint

from gql import Client, gql
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport

from data_mass.attribute_supplier import (
    create_root_attribute_payload,
    get_all_legacy_attributes,
    populate_container_attribute_payload,
    populate_package_attribute_payload
    )
from data_mass.classes.text import text
from data_mass.common import get_header_request_supplier, get_supplier_base_url
from data_mass.supplier_category import (
    associate_all_legacy_attributes,
    search_specific_category,
    verify_if_category_has_all_legacy_category
    )


def create_product_supplier(environment, category_id, country):
    name = 'DM PRODUCT ' + str(randint(1, 100000))
    description = 'DM DESCRIPTION to ' + name
    var_name = 'DM VARIANT ' + str(randint(1, 100000))
    skus = ['DM-SKU-' + str(randint(1, 100000))]

    all_attributes, has_all_attributes = get_all_legacy_attributes(environment)

    category = search_specific_category(environment, category_id)
    if category is False:
        return False
    else:
        category_model = json.loads(category)
        info = category_model['category']
        has_all_legacy_attribute = verify_if_category_has_all_legacy_category(environment, category_id)

        root_abstract_attribute_id = {}
        package_abstract_attribute_id = None
        container_abstract_attribute_id = None
        attributes_info = info['attributes']

        if has_all_legacy_attribute is True:
            for i in range(len(attributes_info)):
                attribute_model = attributes_info[i]['attributeModel']
                attribute_semantic_id = attribute_model['semanticId']
                if attribute_semantic_id == 'package':
                    package_abstract_attribute_id = attributes_info[i]['id']
                elif attribute_semantic_id == 'container':
                    container_abstract_attribute_id = attributes_info[i]['id']
                else:
                    root_abstract_attribute_id[attribute_semantic_id] = attributes_info[i]['id']

            package_group_payload = populate_package_attribute_payload(package_abstract_attribute_id, all_attributes)
            container_group_payload = populate_container_attribute_payload(container_abstract_attribute_id,
                                                                           all_attributes)

            attributes = create_root_attribute_payload(root_abstract_attribute_id)
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
                      'attributes': attributes, 'varName': var_name, 'skus': skus, 'country': country}

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
        else:
            print(text.Red + "\n [Category] - This category doesn't have all the legacy attributes or has more"
                             " attributes than the item contract")
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
              $skus: [String!]!
              $country: String!
            ) {
              createProduct(
                input: {
                  name: $name
                  description: $description
                  categoryId: $category
                  country: $country
                  images: ["http://test.com/1"]
                  attributes: 
                    $attributes
                  variants: [
                    {
                      name: $varName
                      images: ["http://testVariant.com/1"]
                      skus: $skus
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
