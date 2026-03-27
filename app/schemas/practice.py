from pydantic import BaseModel
from typing import Optional, Any


class PracticeQuestionOut(BaseModel):
    question_no: int
    section: Optional[str] = None
    question_type: Optional[str] = None
    struct_type: Optional[str] = None
    question_json: Optional[Any] = None
    score: Optional[int] = None
    difficulty: Optional[str] = None
    confirm_yn: Optional[str] = None


class PracticeAnswerOut(BaseModel):
    question_no: int
    feedback_json: Optional[Any] = None


class PracticeQuestionWithAnswerOut(PracticeQuestionOut):
    answer: Optional[PracticeAnswerOut] = None
