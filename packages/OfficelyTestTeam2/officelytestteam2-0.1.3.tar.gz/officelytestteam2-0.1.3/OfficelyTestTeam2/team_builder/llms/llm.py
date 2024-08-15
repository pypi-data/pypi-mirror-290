from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic.v1 import BaseModel, Field

from OfficelyTestTeam2.generator import ThreadedGenerator
from team_builder.nodes.interface import ISchema
from .enums import LLMType
from .tokenizer import Tokenizer
from langchain_core.prompt_values import PromptValue


class LLM(BaseModel, ABC):
    """
    This is the LLM class.
    It is a subclass of BaseModel and ABC.
    """
    model:LLMType
    temperature:float = 0
    g: Optional[ThreadedGenerator] = Field(default=None)
    tokenizer: Optional[Tokenizer] = Field(default=None) 




    @property
    @abstractmethod
    def base(self):
        """
        This is the base method.
        It serves as a placeholder and does not perform any specific functionality.
        """
    


    @abstractmethod
    def with_schema(self, prompt:str, schema:List[ISchema], name:str):
        """
        This is the with_structured_output method.
        It takes in a schema and returns a response.
        """





