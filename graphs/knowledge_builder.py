from operator import add
from typing import Annotated, List, Set

from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

from llm import (
    EntityBase,
    extract_attributes_of_entity_from_text,
    extract_entity_bases_from_text,
)


# TODO: Step 1 - Create a workflow that first extracts neo4j entity labels from given chunk.
# Once it does, we create a new enum for BAML using those labels so that we can
# effectively maintain some sort of data integrity while creating entity types.
# Maybe after a v0, we can also have the workflow query the already existing labels
# so that our knowledge builder workflow is able to leverage that information as well.

# TODO: Step 2 - Utilise the extracted (and pre-existing) labels to extract
# entities and relationships from the current chunk.

# TODO: Step 3 - Update the graph database using the newly extracted entities
# and relationships.


def set_union_reducer(current_state: set, new_state: set) -> set:
    return current_state.union(new_state)


class KnowledgeState(TypedDict):
    chunk: str
    entity_types: Annotated[Set[str], set_union_reducer]
    entity_bases: Annotated[List[EntityBase], add]
    final_entities: Annotated[List[dict], add]
    # relationships: Annotated[list[dict], add]


def entity_identifier(state: KnowledgeState):
    print("Entered entity identifier")
    entity_bases = extract_entity_bases_from_text(state["chunk"])
    entity_types = {entity.type for entity in entity_bases}

    return {"entity_types": entity_types, "entity_bases": entity_bases}


# TODO: Pass the previously extracted attributes to the LLM to maintain some
# integrity of created attributes. Or introduce an attribute "normalization"
# stage after the attribute identification.
def entity_attribute_identifier(state: KnowledgeState):
    print("Entered attribute identifier")
    entities = []
    for entity_base in state["entity_bases"]:
        attributes = extract_attributes_of_entity_from_text(
            entity_base, state["chunk"]
        )
        entities.append(
            {
                "name": entity_base.name,
                "type": entity_base.type,
                "attributes": attributes,
            }
        )

    return {"final_entities": entities}


def create_knowledge_builder():
    graph_builder = StateGraph(KnowledgeState)

    # Node definitions
    graph_builder.add_node("entity_identifier", entity_identifier)
    graph_builder.add_node(
        "entity_attribute_identifier", entity_attribute_identifier
    )

    # Edge definitions
    graph_builder.add_edge(START, "entity_identifier")
    graph_builder.add_edge("entity_identifier", "entity_attribute_identifier")
    graph_builder.add_edge("entity_attribute_identifier", END)

    knowledge_builder_agent = graph_builder.compile()
    return knowledge_builder_agent
