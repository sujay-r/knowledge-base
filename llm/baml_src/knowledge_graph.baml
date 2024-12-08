client<llm> GPT4o {
    provider "openai"
    options {
        model "gpt-4o"
        api_key env.OPENAI_API_KEY
        supports_streaming false
    }
}

enum DataType {
    INT @description("Integer type data")
    FLOAT @description("Floating point data")
    STR @description("Arbitrary string data")
    BOOL @description("Boolean type data")
}

class Attribute {
    name string @description("Name of the attribute. Please note that attributes cannot be relationships, they have to be individual qualities of the entity that the attribute belongs to.")
    value string @description("Value of the attribute")
    data_type DataType
}

class Entity {
    name string
    type string
    attributes Attribute[]
}

class KGOutput {
    entities Entity[]
}

function ExtractEntities(chunk: string) -> KGOutput {
    client GPT4o
    prompt #"####INSTRUCTION####
You are an expert state of the art knowledge graph agent.
Your task is to identify entities and their relationships from a given piece of text.
 
####

Here is the piece of text:
{{ chunk }}

####

{{ ctx.output_format }}
"#
}
