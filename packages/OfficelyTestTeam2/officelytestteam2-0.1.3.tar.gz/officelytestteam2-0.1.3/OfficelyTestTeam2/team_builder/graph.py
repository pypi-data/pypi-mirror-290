from typing import Dict, List, Optional, Sequence, cast, Any
from pydantic.v1 import BaseModel, Field, root_validator
from colorama import Fore, Style
from team_builder.nodes.enums import NodeType
from OfficelyTestTeam2.generator import ThreadedGenerator
from team_builder.nodes.filter.filter_node import FilterNode
from team_builder.nodes.interface import Iinputs, InputItem
from team_builder.nodes.jump import JumpNode
from team_builder.nodes.llm_node import LLMNode
from .nodes.node import Node
from .llms import Tokenizer

class Edge(BaseModel):
    source: str
    target: str

class Graph(BaseModel):
    nodes: Sequence[Node]
    edges: List[Edge]
    tokenizer:Optional[Tokenizer]=None
    g:Optional[ThreadedGenerator] = None
    verbose:bool = True
    inputs: Iinputs = Field(default_factory=lambda: Iinputs())
    current_node:Optional[str] =  ""


    @root_validator(pre=True)
    def set_inputs_verbose(cls, values):
        verbose = values.get('verbose', True)
        values['inputs'] = Iinputs(verbose=verbose)
        return values




    def __send_verbose(self, key:str, answer:Any, _type:NodeType):
        if _type in {NodeType.HISTORY, NodeType.QUESTION}:
            return

        color_mapping = {
            NodeType.LLM: "#5B61EB",
            NodeType.PYTHON: "green",
            NodeType.RETRIVER: "#B9B9B9",
            NodeType.JUMP: "purple",
        }
        default_color = "black"

        color = color_mapping.get(_type, default_color)
        if self.g:
            self.g.send(f"<code style='color:{color}'>{key}: {answer}</code>\n\n", False) 

    def __add_input(self, key:str, answer:Any, _type:NodeType, print_verbose:bool=True):
        new_input = InputItem(key=key, value=answer, type=_type)
        self.inputs[key] = new_input # pylint: disable=unsupported-assignment-operation
        if self.verbose and print_verbose:
            print(Fore.MAGENTA + ("----------" * 3))
            print(Fore.GREEN + f"{key} - {answer}" + Style.RESET_ALL)
            # if not last_node:
            #     self.__send_verbose(key, answer, _type)

    def run(self, query:str, chat_history:List[Dict]):
        self.__add_input("question", query, NodeType.QUESTION, False)
        self.__add_input("chat_history", chat_history, NodeType.HISTORY, False)
        node = self.__run_node()
        return self.inputs.get_value(node.name)

    def __run_node(self):
        try:
            next_node = self.__next_node()
            while next_node is not None:
                node = next_node
                self.current_node = node.id  # Correctly use the property
                next_node = self.__next_node()
                match node.type:
                    case NodeType.LLM:
                        llm_node = cast(LLMNode, node)
                        llm_node.g = self.g
                        llm_node.tokenizer = self.tokenizer
                        if next_node is None  and llm_node.g:
                            llm_node.g.is_answer = True
                    case NodeType.FILTER:
                        filter_node = cast(FilterNode, node)
                        filter_node.childs = [item for item in self.nodes if item.id in self.get_edge_child(node)]
                        next_node = filter_node.execute(self.inputs, self.g if self.verbose else None)
                        continue
                    case NodeType.JUMP:
                        jump_node = cast(JumpNode, node)
                        next_node = self.find_node(jump_node.jump_to_id)
                        if next_node is None:
                            raise ValueError(f"Jump node '{jump_node.name}' not found")
                        self.__add_input(jump_node.name, f" => {next_node.name}", jump_node.type, print_verbose=(next_node is not None))
                        continue
                res_node = node.execute(self.inputs)
                self.__add_input(node.name, res_node, node.type, print_verbose=(next_node is not None))
            return node
        except Exception as e:
            if node:    
                err = f"Error in **{node.name}**: {e}"
            else: 
                err = str(e) 
            raise Exception(err) 
        
    def find_node(self, node_id:str):
        return next((item for item in self.nodes if item.id == node_id), None)

    def __next_node(self, node_id:Optional[str]=None) -> Node | None:
        if node_id:
            return self.find_node(node_id)
        if not self.current_node:
            return self.get_start_node()
        try:
            edge:Edge = next((item for item in self.edges if item.source == self.current_node))
        except StopIteration:
            return None
        return next((item for item in self.nodes if item.id == edge.target))

    def get_edge_child(self, node:Node):
        return [x.target for x in self.edges if x.source == node.id]
    
    def get_start_node(self):
        for node in self.nodes:
            if not any(edge.target == node.id for edge in self.edges):
                return node
        raise ValueError("Graph has no start node")


