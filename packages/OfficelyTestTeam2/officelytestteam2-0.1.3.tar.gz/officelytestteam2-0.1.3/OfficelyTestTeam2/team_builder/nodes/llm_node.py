
import base64
from typing import Any, Dict, List, Optional, Tuple
import base64
import httpx
from langchain_core.output_parsers import StrOutputParser

from OfficelyTestTeam2.generator import ThreadedGenerator
from team_builder.llms import LLMType, factory_llm, is_openAI, is_anthropic
from team_builder.llms.tokenizer import Tokenizer
from .enums import NodeType
from .interface import ISchema, Iinputs
from .node import Node





class LLMNode(Node):
    """this node use langchain """
    model:LLMType
    system_prompt:str
    prompt:str
    with_schema:bool
    map_model:str
    llm_map:bool
    temperature:Optional[float] = None
    schema_data:Optional[List[ISchema]] = None
    g:Optional[ThreadedGenerator] = None
    tokenizer:Optional[Tokenizer] = None
    extra_kwargs:Dict[str, Any]



    @property
    def type(self):
        return NodeType.LLM
    
    @property
    def Allowed_schema(self):
        return self.model in [LLMType.GPT4, LLMType.GPT_4_TURBO, LLMType.GPT4_O, LLMType.GPT4_O_MINI, LLMType.AZURE,
            LLMType.COMMAND_R_PLUS, LLMType.COMMAND_R, LLMType.COMMAND, LLMType.COMMAND_LIGHT
        ]

    
    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls(
            id = kwargs["id"],
            name = kwargs["name"],
            model = LLMType[kwargs["model"]],
            system_prompt = kwargs.get("system_prompt", ""),
            prompt = kwargs["prompt"],
            with_schema = kwargs.get("with_schema", False),
            description = kwargs.get("description"),
            temperature = kwargs.get("temperature", 0),
            schema_data = kwargs.get("schema"),
            map_model = str(kwargs.get("model_string", '')).strip(),
            llm_map = kwargs.get("llm_map", False),
            extra_kwargs = cls.get_extra_kwargs(**kwargs)
        )
    
    @classmethod
    def get_extra_kwargs(cls, **kwargs):
        return {
            "azure_deployment_name":kwargs.get("azureDeploymentName", None),
            "own_bedrock":kwargs.get("ownBedrock", False),
            "togther_model":kwargs.get("togtherModel", ""),
        }
    
    def is_valid_model(self, model: str) -> bool:
        return model in LLMType.__members__.values()

    def get_llm(self, inputs:Iinputs):
        if self.llm_map:
            model = self.convert_varibales(self.map_model, inputs)
            if self.is_valid_model(model):
                model = LLMType(model)
            else:
                err = f"model <b>{model}</b> is not valid you need to choose one of: <br><br> {'<br>'.join(LLMType.__members__.values())}"
                err += f"<br><br> from node <b>{self.name}<b>"
                raise ValueError(err)
        else:
            model = self.model
        return factory_llm(model, g=self.g, tokenizer=self.tokenizer, **self.extra_kwargs)


    def execute(self, inputs:Iinputs):
        if self.with_schema and self.Allowed_schema:
            return self.run_schema(inputs)
        return self.run(inputs)
    
    def run(self, inputs:Iinputs) -> str:
        llm = self.get_llm(inputs)
        PROMPT = self.create_messages(inputs)
        chain = llm.base | StrOutputParser()
        return chain.with_config({"run_name":self.name}).invoke(PROMPT) 
    
    def create_messages(self, inputs:Iinputs) -> List[Tuple[str, str]]:
        system = self.convert_varibales(self.system_prompt, inputs)
        messages = []
        if system:
            messages.append(("system", system))
        messages.append(("human", self.convert_varibales(self.prompt, inputs)))
        return messages
    








    

    


    def run_schema(self, inputs:Iinputs):
        llm = self.get_llm(inputs)
        _schema =  self.create_schema()
        PROMPT = self.create_messages(inputs)
        answer = llm.with_schema(PROMPT, _schema, self.name)
        return answer


    def create_schema(self) -> Dict:
        if not self.schema_data:
            raise ValueError("schema_dict is empty")

        schema = {
            "name":self.name,
            "description":"use this schema to create structured output and return object",
            "parameters":{
                "type":"object",    
                "properties":{},
                "required":[]
            },
        }

        for s in self.schema_data:
            obj_prop = {
                "type":s.type,
                "description":s.description,
            }
            if s.is_enum:
                obj_prop["enum"] = s.enums

            schema["parameters"]["properties"][s.key] = obj_prop

            if s.required:
                schema["parameters"]["required"].append(s.key)
        return schema
        
        