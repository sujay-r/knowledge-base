from typing import Any, List

from dotenv import load_dotenv


load_dotenv()
from .baml_client import b
from .baml_client.types import Attribute, DataType, EntityBase


datatype2func = {
    DataType.STR: str,
    DataType.INT: int,
    DataType.FLOAT: float,
    DataType.BOOL: bool,
}


def extract_entities_from_text(text: str) -> List[dict]:
    kg_output = b.ExtractEntities(text)
    entities = [process_entity(entity) for entity in kg_output.entities]

    return entities


def extract_entity_bases_from_text(text: str) -> List[EntityBase]:
    entity_bases = b.ExtractEntityBases(text)
    return entity_bases


def extract_attributes_of_entity_from_text(
    entity: EntityBase, text: str
) -> List[dict]:
    extracted_attributes = b.ExtractEntityAttributes(entity, text)
    attributes = [
        process_attribute(attribute) for attribute in extracted_attributes
    ]
    return attributes


def process_attribute(attr: Attribute) -> dict:
    return {
        "name": attr.name,
        "value": map_value_to_data_type(attr.value, attr.data_type),
    }


def map_value_to_data_type(value: Any, data_type: DataType) -> Any:
    conversion_function = datatype2func[data_type]
    return conversion_function(value)
