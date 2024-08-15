
from typing import List, Optional
from pydantic.v1 import BaseModel

from .enums import OperatorValue
from team_builder.nodes.filter.enums import DataType






class IOperatorInfo(BaseModel):
    label: OperatorValue
    dataType: DataType

class ICondition(BaseModel):
    field: str
    operator: IOperatorInfo
    value: str
    logicalOperator:Optional[str] = None



class IGroupCondtions(BaseModel):
    id: str
    conditions: List[ICondition]

class IFilterObject(BaseModel):
    groups: List[IGroupCondtions]
    elseID:str