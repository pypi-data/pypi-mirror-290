from sys import api_version
from typing import Dict, List, Tuple, Optional

from pydantic.v1 import root_validator, validator
from OfficelyTestTeam2.stream_handler import StreamHandler
from .llm import LLM
from langchain_openai import AzureChatOpenAI
import os
from OfficelyTestTeam2.CustomException import RootValidatorException



class AzureLLM(LLM):
    azure_deployment_name: Optional[str]
    streaming:bool = True


    @root_validator(pre=True)
    def check_azure_deployment_name(cls, values):
        if not values.get('azure_deployment_name'):
            raise RootValidatorException("Missing Azure Deployment Name")
        return values



    @property
    def base(self):
        callbacks = []
        if self.tokenizer:
            self.tokenizer.model = self.model
            callbacks.append(self.tokenizer)
        is_answer = False
        if self.g:
            callbacks.append(StreamHandler(gen=self.g, with_final=False))
            is_answer = self.g.is_answer
            
        api_version = "2024-05-01-preview"

        return AzureChatOpenAI(
            azure_deployment=self.azure_deployment_name,
            api_version=api_version,
            temperature=self.temperature,
            streaming=is_answer and self.streaming, 
            callbacks=callbacks
        )
            
    def with_schema(self, prompt:List[Tuple[str, str]], schema:Dict, name:str):
        self.streaming = False
        return self.base.with_structured_output(schema).with_config({"run_name":name}).invoke(prompt)
    
