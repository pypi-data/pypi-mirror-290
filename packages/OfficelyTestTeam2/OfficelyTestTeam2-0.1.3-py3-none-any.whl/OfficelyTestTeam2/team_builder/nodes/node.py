from typing import Dict, Optional, List
from abc import ABC, abstractmethod
import re
from pydantic.v1 import BaseModel


from team_builder.nodes.interface import Iinputs

from .enums import NodeType


class Node(BaseModel, ABC):
    id:str
    name:str
    description:Optional[str] = None
    _answer:Optional[str] = None


    @property
    @abstractmethod
    def type(self) -> NodeType:
        """return the type of the node"""
        
    @abstractmethod
    def execute(self, inputs:Iinputs) -> str | Dict :
        """execute the node""" 

    @classmethod
    @abstractmethod
    def from_kwargs(cls):
        """create the node from kwargs"""



    def validate_placeholders(self, template:str, data:dict):
        def get_nested_data(data, keys):
            for key in keys:
                try:
                    data = data[key]
                except (TypeError, KeyError):
                    return None
            return data
        
        #placeholders = re.findall(r'\{(.*?)\}', template)
        placeholders = re.findall(r'\{\{(.*?)\}\}', template)
        missing = []

        # Process each placeholder
        for placeholder in placeholders:
            keys = placeholder.split('.')
            result = get_nested_data(data, keys)
            # Check if the result is None or if it is still a placeholder
            if result is None:
                missing.append(placeholder)

        if missing:
            raise ValueError(f"Missing placeholders: {', '.join(missing)} in Node: {self.name}")

    def convert_varibales(self, text:str, inputs:Iinputs) -> str:
        self.validate_placeholders(text, inputs.as_dict())
        _inputs = inputs.as_dict_str()

        def find_value(keys:List, value:Dict):
            try:
                for key in keys:
                    if "[" in key:
                        key, index = key[:-1].split("[")
                        value = value[key][int(index)]
                    else:
                        value = value[key]
                return value
            except (KeyError, IndexError, ValueError):
                return None
            
        def replace_placeholders_with_symbol(text: str, data: Dict, symbol: str):
            placeholders = re.findall(rf"\{symbol}(\w+)", text)
            for placeholder in placeholders:
                if placeholder in data:
                    text = text.replace(
                        f"{symbol}{placeholder}", str(data[placeholder])
                    )
            return text
        
        text = replace_placeholders_with_symbol(text, _inputs, "$")
        while matches := list(re.finditer(r"\{\{([\w\.\[\]]+)\}\}", text)):
            for match in reversed(matches):
                key_str = match.group(1)
                keys = key_str.split(".")
                value = find_value(keys, _inputs)
                if value is not None:
                    text = text[:match.start()] + str(value) + text[match.end():]
                else:
                    text = text[:match.start()] + text[match.end():]
        return text


