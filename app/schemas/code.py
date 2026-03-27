from pydantic import BaseModel
from typing import Optional, List


class GroupCodeOut(BaseModel):
    group_code: str
    group_name: str
    group_desc: Optional[str] = None


class CodeOut(BaseModel):
    group_code: str
    code: int
    code_name: str
    code_desc: Optional[str] = None
    sort_order: Optional[int] = None


class GroupCodeWithCodesOut(BaseModel):
    group_code: str
    group_name: str
    group_desc: Optional[str] = None
    codes: List[CodeOut] = []
