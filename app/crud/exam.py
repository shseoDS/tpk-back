import json
from typing import Optional, List
from app.db.database import database
from app.schemas.exam import (
    ExamListOut,
    ExamDetailOut,
    ExamQuestionOut,
    ExamAnswerOut,
    ExamInstructionOut,
    ExamFileOut,
)


def _parse_json(value):
    if value is None:
        return None
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value


async def get_exam_list(
    exam_year: Optional[str],
    exam_type: Optional[str],
    tpk_level: Optional[str],
    section: Optional[str],
    skip: int,
    limit: int,
) -> List[ExamListOut]:
    conditions = ["del_yn = 'N'"]
    values: dict = {}

    if exam_year:
        conditions.append("exam_year = :exam_year")
        values["exam_year"] = exam_year
    if exam_type:
        conditions.append("exam_type = :exam_type")
        values["exam_type"] = exam_type
    if tpk_level:
        conditions.append("tpk_level = :tpk_level")
        values["tpk_level"] = tpk_level
    if section:
        conditions.append("section = :section")
        values["section"] = section

    where = " AND ".join(conditions)
    query = f"""
        SELECT exam_key, exam_year, exam_type, round, tpk_level, section
        FROM tb_exam_list
        WHERE {where}
        ORDER BY exam_year DESC, round DESC
        LIMIT :limit OFFSET :skip
    """
    values["limit"] = limit
    values["skip"] = skip

    rows = await database.fetch_all(query, values=values)
    return [ExamListOut(**dict(r)) for r in rows]


async def get_exam_detail(exam_key: int) -> Optional[ExamDetailOut]:
    exam_query = """
        SELECT exam_key, exam_year, exam_type, round, tpk_level, section
        FROM tb_exam_list
        WHERE exam_key = :exam_key AND del_yn = 'N'
    """
    exam_row = await database.fetch_one(exam_query, values={"exam_key": exam_key})
    if exam_row is None:
        return None

    questions = await get_exam_questions(exam_key)
    instructions = await get_exam_instructions(exam_key)
    files = await get_exam_files(exam_key)

    return ExamDetailOut(
        **dict(exam_row),
        questions=questions,
        instructions=instructions,
        files=files,
    )


async def get_exam_questions(exam_key: int) -> List[ExamQuestionOut]:
    query = """
        SELECT exam_key, question_no, section, question_type, struct_type,
               question_json, score, difficulty
        FROM tb_exam_question
        WHERE exam_key = :exam_key AND del_yn = 'N'
        ORDER BY question_no
    """
    rows = await database.fetch_all(query, values={"exam_key": exam_key})
    return [
        ExamQuestionOut(**{**dict(r), "question_json": _parse_json(r["question_json"])})
        for r in rows
    ]


async def get_exam_question(exam_key: int, question_no: int) -> Optional[ExamQuestionOut]:
    query = """
        SELECT exam_key, question_no, section, question_type, struct_type,
               question_json, score, difficulty
        FROM tb_exam_question
        WHERE exam_key = :exam_key AND question_no = :question_no AND del_yn = 'N'
    """
    row = await database.fetch_one(
        query, values={"exam_key": exam_key, "question_no": question_no}
    )
    if row is None:
        return None
    return ExamQuestionOut(**{**dict(row), "question_json": _parse_json(row["question_json"])})


async def get_exam_answers(exam_key: int) -> List[ExamAnswerOut]:
    query = """
        SELECT exam_key, question_no, feedback_json
        FROM tb_exam_answer
        WHERE exam_key = :exam_key AND del_yn = 'N'
        ORDER BY question_no
    """
    rows = await database.fetch_all(query, values={"exam_key": exam_key})
    return [
        ExamAnswerOut(**{**dict(r), "feedback_json": _parse_json(r["feedback_json"])})
        for r in rows
    ]


async def get_exam_answer(exam_key: int, question_no: int) -> Optional[ExamAnswerOut]:
    query = """
        SELECT exam_key, question_no, feedback_json
        FROM tb_exam_answer
        WHERE exam_key = :exam_key AND question_no = :question_no AND del_yn = 'N'
    """
    row = await database.fetch_one(
        query, values={"exam_key": exam_key, "question_no": question_no}
    )
    if row is None:
        return None
    return ExamAnswerOut(**{**dict(row), "feedback_json": _parse_json(row["feedback_json"])})


async def get_exam_instructions(exam_key: int) -> List[ExamInstructionOut]:
    query = """
        SELECT exam_key, ins_no, ins_json
        FROM tb_exam_instruction
        WHERE exam_key = :exam_key AND del_yn = 'N'
        ORDER BY ins_no
    """
    rows = await database.fetch_all(query, values={"exam_key": exam_key})
    return [
        ExamInstructionOut(**{**dict(r), "ins_json": _parse_json(r["ins_json"])})
        for r in rows
    ]


async def get_exam_files(exam_key: int) -> List[ExamFileOut]:
    query = """
        SELECT pdf_key, exam_key, file_name, file_path, file_size, sort_order
        FROM tb_exam_file
        WHERE exam_key = :exam_key AND del_yn = 'N'
        ORDER BY sort_order
    """
    rows = await database.fetch_all(query, values={"exam_key": exam_key})
    return [ExamFileOut(**dict(r)) for r in rows]
