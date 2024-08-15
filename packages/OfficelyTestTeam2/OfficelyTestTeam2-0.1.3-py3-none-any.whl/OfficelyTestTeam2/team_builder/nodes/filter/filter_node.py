
from typing import Dict, List, Optional

from OfficelyTestTeam2.generator import ThreadedGenerator
from .enums import OperatorValue
from team_builder.nodes.enums import NodeType
from team_builder.nodes.filter.interfaces import ICondition, IFilterObject
from team_builder.nodes.interface import Iinputs
from team_builder.nodes.node import Node

from team_builder.nodes.filter.enums import DataType




class FilterNode(Node):
    """this node use filter the childs """
    childs: List["Node"] = []
    filter_object: IFilterObject




    @property
    def type(self):
        return NodeType.FILTER

    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls(
            id = kwargs["id"],
            name = "Filter",
            filter_object = kwargs['filterObject']
        )

    def execute(self, inputs:Iinputs, g:Optional[ThreadedGenerator] = None):
        next_child = None
        for group in self.filter_object.groups:
            _bool = False
            temp_bool = False
            conditions = group.conditions
            for i, con in enumerate(conditions):
                field, value = self.convert_varibales(con.field, inputs), self.convert_varibales(con.value, inputs)
                if not field and not value:
                    field = None
                try:
                    field, value = self.convert_data_type(str(field), value, con)
                except ValueError:
                    continue
                temp_bool = self.logical_by_operator(field, value, con.operator.label)
                if i != 0:
                    if conditions[i - 1].logicalOperator == "AND":
                        _bool = _bool and temp_bool
                    else:
                        _bool = _bool or temp_bool
                else:
                    _bool = temp_bool
            if _bool:
                next_child = self.__next_child(group.id)
                self.send_verbose(self.name, next_child.name, g)
                break
        else:
            next_child = self.__next_child(self.filter_object.elseID)
            self.send_verbose(self.name, next_child.name, g)
        return next_child


    def __next_child(self, _id:str):
        return next((item for item in self.childs if item.id == _id ))
    
    def send_verbose(self, parent:str, child:str, g:ThreadedGenerator=None):
        if g:
            g.send(f"<code style='color:red'>{parent} -> {child}</code>\n\n", False)
        
    

    def convert_data_type(self, field:str, value:str, condition:ICondition):
        try:
            data_type = condition.operator.dataType
            match data_type:
                case DataType.TEXT:
                    new_field, new_value = str(field).strip(), str(value).strip()
                case DataType.NUMBER:
                    new_field, new_value = float(field), float(value)
                case DataType.BASIC:
                    if field == condition.field:
                        new_field = None
                case _:
                    raise ValueError(f"DataType {data_type} not supported")
        except ValueError as e:
            raise e
        else:
            return new_field, new_value
        
    def logical_by_operator(self, field, value, operator:OperatorValue):
        match operator:
            case OperatorValue.EQUAL.value:  # done
                return field == value
            case OperatorValue.EQUAL_INSENSETIVE.value:  # done
                return str(field).lower() == str(value).lower()
            case OperatorValue.NOT_EQUAL.value:  # done
                return field != value
            case OperatorValue.NOT_EQUAL_INSENSETIVE.value:  # done
                return str(field).lower() != str(value).lower()
            case OperatorValue.GREATER_THAN.value:
                return field > value
            case OperatorValue.LESS_THAN.value:
                return field < value
            case OperatorValue.GREATER_THAN_OR_EQUAL_TO.value:
                return field >= value
            case OperatorValue.LESS_THAN_OR_EQUAL_TO.value:
                return field <= value
            case OperatorValue.STARTS_WITH.value:
                return str(field).startswith(value)
            case OperatorValue.STARTS_WITH_INSENSETIVE.value:
                return str(field).lower().startswith(str(value).lower())
            case OperatorValue.NOT_STARTS_WITH.value:
                return not str(field).startswith(value)
            case OperatorValue.NOT_STARTS_WITH_INSENSETIVE.value:
                return not str(field).lower().startswith(str(value).lower())
            case OperatorValue.ENDS_WITH.value:
                return str(field).endswith(value)
            case OperatorValue.ENDS_WITH_INSENSETIVE.value:
                return str(field).lower().endswith(str(value).lower())
            case OperatorValue.NOT_ENDS_WITH.value:
                return not str(field).endswith(value)
            case OperatorValue.NOT_ENDS_WITH_INSENSETIVE.value:
                return not str(field).lower().endswith(str(value).lower())
            case OperatorValue.CONTAINS.value:
                return value in field
            case OperatorValue.CONTAINS_INSENSETIVE.value:
                return str(value).lower() in str(field).lower()
            case OperatorValue.NOT_CONTAINS.value:
                return value not in field
            case OperatorValue.NOT_CONTAINS_INSENSETIVE.value:
                return str(value).lower() not in str(field).lower()
            case OperatorValue.EXISTS.value:
                return field is not None
            case OperatorValue.NOT_EXISTS.value:
                return field is None
        return False
        


        
        