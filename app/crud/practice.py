import json
from typing import Optional, List
from app.db.database import database
from app.schemas.practice import (
    PracticeQuestionOut,
    PracticeAnswerOut,
    PracticeQuestionWithAnswerOut,
)


def _parse_json(value):
    if value is None:
        return None
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value


async def get_practice_questions(
    section: Optional[str],
    question_type: Optional[str],
    difficulty: Optional[str],
    skip: int,
    limit: int,
) -> List[PracticeQuestionOut]:
    conditions = ["del_yn = 'N'", "confirm_yn = 'Y'"]
    values: dict = {}

    if section:
        conditions.append("section = :section")
        values["section"] = section
    if question_type:
        conditions.append("question_type = :question_type")
        values["question_type"] = question_type
    if difficulty:
        conditions.append("difficulty = :difficulty")
        values["difficulty"] = difficulty

    where = " AND ".join(conditions)
    query = f"""
        SELECT question_no, section, question_type, struct_type,
               question_json, score, difficulty, confirm_yn
        FROM tb_practice_question
        WHERE {where}
        ORDER BY question_no DESC
        LIMIT :limit OFFSET :skip
    """
    values["limit"] = limit
    values["skip"] = skip

    rows = await database.fetch_all(query, values=values)
    return [
        PracticeQuestionOut(**{**dict(r), "question_json": _parse_json(r["question_json"])})
        for r in rows
    ]


async def get_practice_question(question_no: int) -> Optional[PracticeQuestionOut]:
    query = """
        SELECT question_no, section, question_type, struct_type,
               question_json, score, difficulty, confirm_yn
        FROM tb_practice_question
        WHERE question_no = :question_no AND del_yn = 'N'
    """
    row = await database.fetch_one(query, values={"question_no": question_no})
    if row is None:
        return None
    return PracticeQuestionOut(**{**dict(row), "question_json": _parse_json(row["question_json"])})


async def get_practice_answer(question_no: int) -> Optional[PracticeAnswerOut]:
    query = """
        SELECT question_no, feedback_json
        FROM tb_practice_answer
        WHERE question_no = :question_no AND del_yn = 'N'
    """
    row = await database.fetch_one(query, values={"question_no": question_no})
    if row is None:
        return None
    return PracticeAnswerOut(**{**dict(row), "feedback_json": _parse_json(row["feedback_json"])})


async def get_practice_question_with_answer(question_no: int) -> Optional[PracticeQuestionWithAnswerOut]:
    question = await get_practice_question(question_no)
    if question is None:
        return None
    answer = await get_practice_answer(question_no)
    return PracticeQuestionWithAnswerOut(**question.model_dump(), answer=answer)
