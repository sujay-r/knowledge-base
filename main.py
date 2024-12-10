import json

from dotenv import load_dotenv

from graphs.knowledge_builder import create_knowledge_builder
from ingestors.preprocessing import chunk
from ingestors.readers import read_text_file


load_dotenv()


corpus = read_text_file("./docs/bees.txt")
chunks = chunk(corpus)

sample_chunk = chunks[0]
print(f"Selected chunk: { sample_chunk }")

knowledge_builder_agent = create_knowledge_builder()
result = knowledge_builder_agent.invoke({"chunk": sample_chunk})

print(json.dumps(result["final_entities"], indent=2))
