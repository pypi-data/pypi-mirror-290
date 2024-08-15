from typing import Dict

from team_builder.nodes.enums import NodeType
from .node import Node
from .interface import Iinputs

class TextNode(Node):
    text:str

    @property
    def type(self) -> NodeType:
       return NodeType.TEXT
        
    def execute(self, inputs:Iinputs) -> str :
        return self.convert_varibales(self.text, inputs)

    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls(
            id = kwargs["id"],
            name = kwargs["name"],
            text = kwargs["text"],
        )
