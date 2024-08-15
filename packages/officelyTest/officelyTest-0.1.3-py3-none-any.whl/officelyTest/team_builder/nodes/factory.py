
from team_builder.nodes.filter.filter_node import FilterNode
from team_builder.nodes.jump import JumpNode
from team_builder.nodes.python_node import PythonNode
from .enums import  EmbeddingModel, NodeType
from .llm_node import LLMNode
from .retriver_node import RetriverNode
from .text_node import TextNode



def factory_node(node_type:NodeType, **kwargs):
    """
    This is the factory_node method.
    It creates a new instance of the Node class based on the specified NodeType.
    """
    kwargs['name'] = kwargs['name'] if kwargs['name'] else kwargs['id']

    match node_type.lower():
        case NodeType.FILTER:
            return FilterNode.from_kwargs(**kwargs)
        case NodeType.LLM:
            return LLMNode.from_kwargs(**kwargs)
        case NodeType.RETRIVER:
            return RetriverNode.from_kwargs(**kwargs)
        case NodeType.PYTHON:
            return PythonNode.from_kwargs(**kwargs)
        case NodeType.TEXT:
            return TextNode.from_kwargs(**kwargs)
        case NodeType.JUMP:
            return JumpNode.from_kwargs(**kwargs)
        case _:
            raise ValueError(f"Invalid NodeType: {node_type}")
        
