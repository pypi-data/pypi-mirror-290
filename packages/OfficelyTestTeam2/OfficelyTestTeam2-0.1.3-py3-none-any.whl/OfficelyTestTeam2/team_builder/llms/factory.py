from typing import Optional

from OfficelyTestTeam2.generator import ThreadedGenerator
#from models.agents import agent
from .cohere import CohereLLM
from .google import GoogleLLM
from .tokenizer import Tokenizer
from .enums import LLMType
from .bedrock import BedrockLLM
from .openai import OpenAILLM
from .azure import AzureLLM
from .together import TogtherLLM
from OfficelyTestTeam2.CustomException import RootValidatorException




def factory_llm(
        llm_type:LLMType,
        temperature:float=0, 
        g: Optional[ThreadedGenerator]=None, 
        tokenizer:Optional[Tokenizer]=None,
        **kwargs
    ):
    """
    This is the factory_llm method.
    It creates a new instance of the LLM class based on the specified LLMType.
    """

    try:
        if is_openAI(llm_type):
            return OpenAILLM(model=llm_type, temperature=temperature, g=g, tokenizer=tokenizer)
        elif is_cohere(llm_type):
            return CohereLLM(model=llm_type, temperature=temperature, g=g, tokenizer=tokenizer)
        elif is_google(llm_type):
            return GoogleLLM(model=llm_type, temperature=temperature, g=g, tokenizer=tokenizer)
        elif llm_type == LLMType.AZURE:
            return AzureLLM(model=llm_type, temperature=temperature, g=g, tokenizer=tokenizer, **kwargs)
        elif llm_type == LLMType.TOGETHER:
            return TogtherLLM(model=llm_type, temperature=temperature, g=g, tokenizer=tokenizer, **kwargs)
        return BedrockLLM(model=llm_type, temperature=temperature, g=g, tokenizer=tokenizer, **kwargs)
    except RootValidatorException as e:
        raise e

def is_openAI(llm_type:LLMType):
    return llm_type.lower().startswith("gpt")

def is_anthropic(llm_type:LLMType):
    return llm_type.startswith("anthropic")

def is_google(llm_type:LLMType):
    return llm_type.startswith("gemini")


def is_cohere(llm_type:LLMType):
    return llm_type.startswith("command")

