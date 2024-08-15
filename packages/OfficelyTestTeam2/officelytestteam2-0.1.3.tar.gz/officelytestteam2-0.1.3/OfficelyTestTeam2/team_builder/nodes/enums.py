from enum import Enum

class NodeType(str, Enum):
    LLM = 'llm'
    RETRIVER = 'retriver'
    FILTER = 'filter'
    PYTHON = 'python',
    TEXT = 'text' 
    JUMP = 'jump'
    ########## for DictInputsType
    QUESTION = "question"
    HISTORY = "history"



class SchemaType(str, Enum):
    STRING = "string"
    BOOL = "boolean"
    NUMBER = "number"
    FLOAT = "float"

# class DictInputsType(str, Enum):
#     TEXT = "text"
#     HISTORY = "history"

    
# class MessageType(str, Enum):
#     AI_OUTBOUND = "ai-outbound"
#     OUTBOUND = "outbound"
#     HUMAN = "human"
#     AI = "ai"

class EmbeddingModel(str, Enum):
    AZURE = "AZURE",
    ADA2 = "text-embedding-ada-002",
    OPEN_AI_SMALL = "text-embedding-3-small"
    TITAN_1 = "amazon.titan-embed-text-v1",
    TITAN_2 = "amazon.titan-embed-text-v2:0",
    COHERE_MULTY = "cohere.embed-multilingual-v3"

class MessageType(str, Enum):
    OUTBOUND = "outbound"
    INBOUND = "inbound"

