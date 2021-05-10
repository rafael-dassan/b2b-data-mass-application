from gql import gql
from gql.gql import DocumentNode


def create_product_payload() -> DocumentNode:
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
