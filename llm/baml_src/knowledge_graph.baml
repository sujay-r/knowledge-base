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
    name string @description("Name of the attribute")
    value string @description("Value of the attribute")
    data_type DataType
}

class EntityBase {
    name string
    type string
}

class Entity {
    base EntityBase
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


function ExtractEntityBases(chunk: string) -> EntityBase[] {
    client GPT4o
    prompt #"####INSTRUCTIONS####
You are an expert in linguistics and have over 20+ years of experience applying linguistic research to real world engineering problems.
Your task is to identify entities from a chunk of text that will be given to you, which will later be added to a knowledge graph that you will be maintaining.

For this task, an entity is defined as any distinct and contextually relevant concept, object or abstraction that:
- Is Identifiable: Can be named, described or uniquely distinguished within the context.
- Has Meaning or Significance: Carries meaning that is useful towards the purpose of understanding the given piece of information and building a high level overview of all the underlying concepts at play.
- Is Relational: Can have relationships with other 'entities'.
- Has Contextual Integrity: Exists as a distinct concept in the specific domain or textual context.

Entities are also generally linguistically denoted by (but are not limited to) nouns and noun-phrases within a text. You MUST identify and extract all the entities from the chunk of text given to you, as well as determine what type of entity it is (like entity labels in Neo4j).

####

Here is the piece of text:
{{ chunk }}

####

{{ ctx.output_format }}
"#
}


function ExtractEntityAttributes(entity: EntityBase, chunk: string) -> Attribute[]{
    client GPT4o
    prompt #"####INSTRUCTIONS####
You are an expert in linguistics and have over 20+ years of experience applying linguistic research to real world engineering problems.
Your task is to identify all the attributes of an entity that will be provided to you, from a given chunk of text.

For this task, an attribute is defined as a descriptive characteristic or qualifier that provides additional context about an entity but:
- Cannot independently exist as a standalone concept within the domain.
- Does not form a relationship with other entities.
- Is contextually bound to its associated entity, enhancing its meaning or specificity.

Attributes are also linguistically denoted by (but are not limited to) adjectives, and adjective phrases within a text. They are also generally strong quantified/qualified descriptors of their entities. Attributes also cannot be entire phrases and are generally primitive data types. If a string is required to denote the value of an attribute, it MUST be just one or two words.

Please note that all the extracted attributes MUST STRICTLY be from the given chunk of text only. If there are no attributes present for the given entity in the provided text, the output must correspondingly be blank (while following the structure provided).

####

Here is the entity that you need to find all the attributes for:
{{ entity }}

Here is the chunk of text in which the entity appears:
{{ chunk }}

####

{{ ctx.output_format }}
"#
}
