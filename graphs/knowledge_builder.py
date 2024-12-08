from operator import add
from typing import Annotated

from typing_extensions import TypedDict


# TODO: Step 1 - Create a workflow that first extracts neo4j entity labels from given chunk.
# Once it does, we create a new enum for BAML using those labels so that we can
# effectively maintain some sort of data integrity while creating entity types.
# Maybe after a v0, we can also have the workflow query the already existing labels
# so that our knowledge builder workflow is able to leverage that information as well.

# TODO: Step 2 - Utilise the extracted (and pre-existing) labels to extract
# entities and relationships from the current chunk.

# TODO: Step 3 - Update the graph database using the newly extracted entities
# and relationships.


class KnowledgeState(TypedDict):
    labels: Annotated[list[str], add]
    entities: Annotated[list[dict], add]
    relationships: Annotated[list[dict], add]
