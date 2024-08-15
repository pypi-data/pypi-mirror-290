from typing import Dict

from team_builder.nodes.enums import NodeType
from .node import Node
from .interface import Iinputs

class JumpNode(Node):
    jump_to_id:str
    jump_to_name:str

    @property
    def type(self) -> NodeType:
       return NodeType.JUMP
        
    def execute(self, inputs:Iinputs) -> str :
        return ""

    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls(
            id = kwargs["id"],
            name = kwargs["name"],
            jump_to_id = kwargs["jump_to_id"],
            jump_to_name = kwargs["jump_to_name"],
        )
