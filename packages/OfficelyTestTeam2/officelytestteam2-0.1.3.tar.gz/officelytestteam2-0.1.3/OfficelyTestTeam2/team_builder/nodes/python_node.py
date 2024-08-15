from typing import Dict

from team_builder.nodes.interface import Iinputs
from .node import Node
from .enums import NodeType
import boto3
import json

class PythonNode(Node):
    code:str



    @property
    def type(self) -> NodeType:
        return NodeType.PYTHON

    def execute(self, inputs:Iinputs) -> str | Dict :
        return self.invoke_lambda(inputs.as_dict())

    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls(
            id = kwargs["id"],
            name = kwargs["name"],
            code = kwargs["code"],
        )
    
    def invoke_lambda(self, inputs:Dict) -> Dict | str :
        lambda_client = boto3.client('lambda', region_name='eu-west-1')

        if self.code is None:
            return "Error: No script content provided."
            

        payload = {
            "script": self.code,
            "inputs": inputs,
        }

        response = lambda_client.invoke(
            FunctionName='executePythonScript',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        res = json.load(response['Payload'])
        if res['status_code'] != 200:
            return res
        res['body'] = json.loads(res['body'])
        return res

