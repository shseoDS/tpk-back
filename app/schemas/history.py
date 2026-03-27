from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class HistoryExamCreate(BaseModel):
    exam_key: int
    question_no: int
    history_type: Optional[str] = None  # submit, bookmark 등
    result_json: Optional[Any] = None
    duration: Optional[int] = None      # 풀이 소요 시간(초)


class HistoryExamOut(BaseModel):
    history_key: int
    user_key: int
    exam_key: int
    question_no: int
    history_type: Optional[str] = None
    result_json: Optional[Any] = None
    duration: Optional[int] = None
    ins_date: datetime


class HistoryPracticeCreate(BaseModel):
    question_no: int
    history_type: Optional[str] = None
    result_json: Optional[Any] = None
    duration: Optional[int] = None


class HistoryPracticeOut(BaseModel):
    history_key: int
    user_key: int
    question_no: int
    history_type: Optional[str] = None
    result_json: Optional[Any] = None
    duration: Optional[int] = None
    ins_date: datetime
