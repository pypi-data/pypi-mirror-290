from enum import Enum
from typing import List, Any, Union, Dict, Iterator
from pydantic.v1 import BaseModel

from team_builder.nodes.enums import MessageType, NodeType, SchemaType
import re


class ISchema(BaseModel):
    key: str
    type: SchemaType
    description: str
    required: bool = True
    is_enum: bool = False
    enums: List[str] = []



class InputItem(BaseModel):
    key: str
    value: Any
    type: NodeType

class IHistory(BaseModel):
    text: str
    type: MessageType

class Iinputs(BaseModel):
    data: Dict[str, InputItem] = {}
    verbose: bool = True



    def __setitem__(self, key: str, item: InputItem) -> None:
        self.data[key] = item  # Use the data attribute directly

    def __getitem__(self, key: str) -> InputItem:
        return self.data[key]
    
    def get_value(self, key: str) -> str:
        """Returns the InputItem associated with the given key."""
        return str(self.data[key].value)

    def __iter__(self) -> Iterator[str]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def as_dict(self) -> Dict[str, Any]:
        def serialize_value(value: Any) -> Any:
            if isinstance(value, BaseModel):
                return value.dict()  # Pydantic model, use its dict() method
            elif isinstance(value, list):
                return [serialize_value(item) for item in value]  # Recursively handle lists
            elif isinstance(value, Enum):  # Handle Enums by converting to their value
                return value.value
            else:
                return value  # Return the value as-is for other types

        return {k: serialize_value(v.value) for k, v in self.data.items()}
    
    def as_full_dict(self) -> Dict[str, Any]:
        return {k: {"value": v.value, "type":v.type} for k, v in self.data.items()}
    
    def as_dict_str(self) -> Dict[str, Union[str, Any]]:
        return {k: self.format_string(v) for k, v in self.data.items()}
    
    def format_string(self, inputs:InputItem) -> str | Dict:
        match inputs.type:
            case NodeType.HISTORY:
                return self.format_history(inputs.value)
            # case NodeType.RETRIVER:
            #     return self.get_doc_string(inputs.value)
            case _:
                return inputs.value
            
        
        



    def format_history(self, history:List[IHistory]) -> str:
        cleaned_history = []
        for item in history:
            text = item.text
            if self.verbose:
                text = re.sub(r'<(code|pre).*?>.*?</\1>', '', text, flags=re.DOTALL).strip()

            if MessageType.OUTBOUND:
                cleaned_history.append(f"AI: {text}")
            else:
                cleaned_history.append(f"Human: {text}")

        return "\n".join(cleaned_history)

       
















