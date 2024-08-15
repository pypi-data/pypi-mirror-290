from typing import Dict, List, Tuple
import boto3
from langchain_aws import ChatBedrock, BedrockLLM as Bedrock 

from OfficelyTestTeam2.stream_handler import StreamHandler
from team_builder.llms.enums import LLMType

from .llm import LLM





class BedrockLLM(LLM):
    region:str = "us-east-1"



    @property
    def Client(self):
        kwargs = {}


        kwargs.update({
            "service_name":'bedrock-runtime',
            "region_name": self.region
        })
        return boto3.client(**kwargs)

    
    @property
    def bedrock_chat_kwargs(self):
        callbacks = []
        if self.tokenizer:
            self.tokenizer.model = self.model
            callbacks.append(self.tokenizer)
        is_answer = False
        if self.g:
            callbacks.append(StreamHandler(gen=self.g, with_final=False))
            is_answer = self.g.is_answer
        return {
            "model_id": self.model,
            "model_kwargs": {"temperature": self.temperature},
            "client": self.Client,
            "callbacks": callbacks,
            "streaming": is_answer,

        }

    @property
    def base(self):
        if self.model in [LLMType.COMMAND_R_PLUS, LLMType.COMMAND_R, LLMType.COMMAND, LLMType.COMMAND_LIGHT]:
            return Bedrock(**self.bedrock_chat_kwargs)
        return ChatBedrock(**self.bedrock_chat_kwargs)

    
    
    def with_schema(self, prompt:List[Tuple[str, str]], schema:Dict, name:str):
        pass




    

