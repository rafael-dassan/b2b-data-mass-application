"""Supplier Atribute GQL Documents handler."""
from gql import gql
from gql.gql import DocumentNode


def create_primitive_attribute_payload():
    """
    Create primitive attribute payload.

    Returns
    -------
    DocumentNode
        The `gql` DocumentNode.
    """
    return gql(
        """
        mutation createAttributeModel(
            $name: String!,
            $description: String!,
            $attribute_type: AttributeType!
        ) {
            createAttributeModel(
                input: {
                    name: $name,
                    description: $description,
                    helpText: "This is an attribute to help you in your test",
                    attributeType: $attribute_type
                }
            ){
                id
                attributeType
            }
        }
        """
    )


def create_enum_generic_payload() -> DocumentNode:
    """
    Create enum generic payload.

    Returns
    -------
    DocumentNode
        The `gql` DocumentNode.
    """
    return gql(
        """
        mutation createAttributeModel(
            $name: String!,
            $description: String!,
            $values: [String!]!,
            $enum_primitive_type: AttributePrimitiveType
        ) {
            createAttributeModel(
                input: {
                    name: $name,
                    description: $description,
                    helpText: "This is an attribute to help you in your test",
                    attributeType: ENUM,
                    metadata: {
                        enumPrimitiveType: $enum_primitive_type,
                        enumValues: $values
                    }
                }
            ){
                id
            }
        }
        """
    )


def create_search_specific_attribute_payload() -> DocumentNode:
    """
    Create a search for a specific attribute payload.

    Returns
    -------
    DocumentNode
        The gql `DocumentNode`.
    """
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


def create_search_all_attribute_payload() -> DocumentNode:
    """
    Create a search for all attribute payload.

    Returns
    -------
    DocumentNode
        The gql `DocumentNode`.
    """
    return gql(
        """
        query attributeModels($page: NonNegativeInt) {
            attributeModels(input:  {
                page: $page
                size: 50
                }
            ){
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
                        subAttributes {
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


def create_search_all_legacy_attributes_payload() -> DocumentNode:
    """
    Create a search for all legacy attribute payload.

    Returns
    -------
    DocumentNode
        The gql `DocumentNode`.
    """
    return gql(
        """
        query attributeModels($page: NonNegativeInt) {
            attributeModels(
                input: {
                    page: $page
                    size: 50
                }
            ){
                id
                semanticId
                attributeType
                metadata {
                    ... on GroupAttributeModelMetadata {
                        subAttributes{
                            id
                            semanticId
                        }
                    }
                }
            }
        }
        """
    )


def create_edit_primitive_attribute() -> DocumentNode:
    """
    Create edit primitive attribute.

    Returns
    -------
    DocumentNode
        The gql `DocumentNode`.
    """
    return gql(
        """
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
        """
    )


def create_edit_enum_attribute() -> DocumentNode:
    """
    Create edit enum attribute.

    Returns
    -------
    DocumentNode
        The gql `DocumentNode`.
    """
    return gql(
        """
        mutation updateAttribute(
            $id: ID!,
            $values: [String!]!,
            $enum_primitive_type: AttributePrimitiveType
        ) {
            updateAttributeModel(
                id: $id,
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
        """
    )


def create_edit_group_attribute() -> DocumentNode:
    """
    Create edit group attribute.

    Returns
    -------
    DocumentNode
        The gql `DocumentNode`.
    """
    return gql(
        """
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
        """
    )


def create_group_attribute() -> DocumentNode:
    """
    Create group attribute.

    Returns
    -------
    DocumentNode
        The gql `DocumentNode`.
    """
    return gql(
        """
        mutation createAttributeModel(
            $name: String!,
            $description: String!,
            $values: [ID!]
        ){
            createAttributeModel(
                input: {
                    name: $name,
                    description: $description,
                    helpText: "This is an attribute to help you in your test",
                    attributeType: GROUP,
                    metadata: {
                        subAttributes: $values
                    }
                }
            ){
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


def create_legacy_group_attribute() -> DocumentNode:
    """
    Create legacy group attribute.

    Returns
    -------
    DocumentNode
        The gql `DocumentNode`.
    """
    return gql(
        """
        mutation createAttributeModel(
            $name: String!,
            $description: String!,
            $values: [ID!]
        ){
            createAttributeModel(
                input: {
                    name: $name,
                    description: $description,
                    helpText: "This is an attribute to help you in your test",
                    attributeType: GROUP,
                    metadata: {
                        subAttributes: $values
                    }
                }
            ){
                id
                name
                description
                helpText
                attributeType
                metadata {
                    ... on GroupAttributeModelMetadata {
                         subAttributes {
                             id
                        }
                    }
                }
                createdAt
            }
        }
        """
    )
