from gql import gql
from gql.gql import DocumentNode


def create_sub_category_payload() -> DocumentNode:
    """
    Create sub category payload.

    Returns
    -------
    DocumentNode
        The `gql` response.
    """
    return gql(
        """
        mutation createCategory(
            $name: String!,
            $description: String!,
            $parent: ID
        ) {
            createCategory(
                input:{
                    name: $name,
                    helpText: $description,
                    description: "Create Category",
                    parentId: $parent
                }
            ){
                id
                name
                helpText
                description
            }
        }
        """
    )


def create_root_category_payload() -> DocumentNode:
    """
    Create root category payload

    Returns
    -------
    DocumentNode
        The `gql` response.
    """
    return gql(
        """
        mutation createCategory(
            $name: String!,
            $description: String!
        ){
            createCategory(
                input:{
                    name: $name,
                    helpText: $description,
                    description: "Create Category"
                }
            ) {
                id
                name
                helpText
                description
            }
        }
    """)


def create_search_specific_category_payload() -> DocumentNode:
    """
    Create search specific category payload.

    Returns
    -------
    DocumentNode
        The `gql` response.
    """
    return gql(
        """
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
                        attributeModel{
                            id
                            semanticId
                        }
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
        """)


def search_all_category_payload() -> DocumentNode:
    """
    Search all categories payload.

    Returns
    -------
    DocumentNode
        The payload.
    """
    return gql(
        """
        query categories($page: NonNegativeInt){
            categories(
                input: {
                    page: $page,
                    size: 50
                }
            ) {
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
        """)


def create_association_payload() -> DocumentNode:
    """
    Create association payload.

    Returns
    -------
    DocumentNode
        The `gql` response.
    """
    return gql(
        """
        mutation associateAttribute(
            $attribute_id: ID!,
            $category_id: ID!,
            $min_cardinality: NonNegativeInt!,
            $max_cardinality: NonNegativeInt!
        ) {
            associateAttribute(
                input:{
                    attributeModelId: $attribute_id
                    taxonomyNodeId: $category_id
                    minCardinality: $min_cardinality
                    maxCardinality: $max_cardinality
                    }
            ) {
                id
                minCardinality
                maxCardinality
                taxonomyNode{
                    id
                    name
                    children{
                        id
                        name
                    }
                }
                attributeModel{
                    id
                    name
                }
            }
        }
    """)
