from dotenv import load_dotenv

from ingestors.preprocessing import chunk
from ingestors.readers import read_text_file


load_dotenv()

from llm.baml_client import b


corpus = read_text_file("./docs/bees.txt")
chunks = chunk(corpus)

sample_chunk = chunks[0]
print(sample_chunk)

kg_output = b.ExtractEntities(sample_chunk)
print(kg_output)
