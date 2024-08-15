
from typing import List, Optional
from pydantic import BaseModel

from officelyTest.team_builder.nodes.filter.enums import OperatorValue
from officelyTest.team_builder.nodes.filter.enums import DataType






class IOperatorInfo(BaseModel):
    label: OperatorValue
    dataType: DataType

    # class Config:
    #     arbitrary_types_allowed = True

class ICondition(BaseModel):
    field: str
    operator: IOperatorInfo
    value: str
    logicalOperator:Optional[str] = None


    # class Config:
    #     arbitrary_types_allowed = True



class IGroupCondtions(BaseModel):
    id: str
    conditions: List[ICondition]

    # class Config:
    #     arbitrary_types_allowed = True

class IFilterObject(BaseModel):
    groups: List[IGroupCondtions]
    elseID:str

    # class Config:
    #     arbitrary_types_allowed = True
