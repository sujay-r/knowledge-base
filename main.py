import json

from dotenv import load_dotenv

from ingestors.preprocessing import chunk
from ingestors.readers import read_text_file
from llm import extract_attributes_of_entity_from_text
from llm.baml_client.types import EntityBase


load_dotenv()


corpus = read_text_file("./docs/bees.txt")
chunks = chunk(corpus)

sample_chunk = chunks[0]
print(sample_chunk)

# entities = extract_entity_bases_from_text(sample_chunk)
# print(json.dumps(entities, indent=2))

entity_dict = {"name": "Bees", "type": "Insect"}
entity = EntityBase(name=entity_dict["name"], type=entity_dict["type"])
attributes = extract_attributes_of_entity_from_text(entity, sample_chunk)

print(json.dumps(attributes, indent=2))
