from pydantic import BaseModel
from typing import Optional, Any, List


class ExamListOut(BaseModel):
    exam_key: int
    exam_year: str
    exam_type: str
    round: Optional[int] = None
    tpk_level: Optional[str] = None
    section: str


class ExamQuestionOut(BaseModel):
    exam_key: int
    question_no: int
    section: Optional[str] = None
    question_type: Optional[str] = None
    struct_type: Optional[str] = None
    question_json: Optional[Any] = None
    score: Optional[int] = None
    difficulty: Optional[str] = None


class ExamAnswerOut(BaseModel):
    exam_key: int
    question_no: int
    feedback_json: Optional[Any] = None


class ExamInstructionOut(BaseModel):
    exam_key: int
    ins_no: int
    ins_json: Optional[Any] = None


class ExamFileOut(BaseModel):
    pdf_key: int
    exam_key: int
    file_name: str
    file_path: str
    file_size: Optional[int] = None
    sort_order: Optional[int] = None


class ExamDetailOut(BaseModel):
    exam_key: int
    exam_year: str
    exam_type: str
    round: Optional[int] = None
    tpk_level: Optional[str] = None
    section: str
    questions: List[ExamQuestionOut] = []
    instructions: List[ExamInstructionOut] = []
    files: List[ExamFileOut] = []
