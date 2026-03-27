import json
from typing import Optional, List
from app.db.database import database
from app.schemas.history import (
    HistoryExamCreate,
    HistoryExamOut,
    HistoryPracticeCreate,
    HistoryPracticeOut,
)


def _parse_json(value):
    if value is None:
        return None
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value


def _dump_json(value) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


async def create_exam_history(user_key: int, body: HistoryExamCreate) -> HistoryExamOut:
    query = """
        INSERT INTO tb_history_exam
            (user_key, exam_key, question_no, history_type, result_json, duration)
        VALUES
            (:user_key, :exam_key, :question_no, :history_type, :result_json, :duration)
        RETURNING history_key, user_key, exam_key, question_no,
                  history_type, result_json, duration, ins_date
    """
    row = await database.fetch_one(
        query,
        values={
            "user_key": user_key,
            "exam_key": body.exam_key,
            "question_no": body.question_no,
            "history_type": body.history_type,
            "result_json": _dump_json(body.result_json),
            "duration": body.duration,
        },
    )
    return HistoryExamOut(**{**dict(row), "result_json": _parse_json(row["result_json"])})


async def get_exam_history_list(
    user_key: int,
    exam_key: Optional[int],
    skip: int,
    limit: int,
) -> List[HistoryExamOut]:
    conditions = ["del_yn = 'N'", "user_key = :user_key"]
    values: dict = {"user_key": user_key}

    if exam_key is not None:
        conditions.append("exam_key = :exam_key")
        values["exam_key"] = exam_key

    where = " AND ".join(conditions)
    query = f"""
        SELECT history_key, user_key, exam_key, question_no,
               history_type, result_json, duration, ins_date
        FROM tb_history_exam
        WHERE {where}
        ORDER BY ins_date DESC
        LIMIT :limit OFFSET :skip
    """
    values["limit"] = limit
    values["skip"] = skip

    rows = await database.fetch_all(query, values=values)
    return [
        HistoryExamOut(**{**dict(r), "result_json": _parse_json(r["result_json"])})
        for r in rows
    ]


async def create_practice_history(user_key: int, body: HistoryPracticeCreate) -> HistoryPracticeOut:
    query = """
        INSERT INTO tb_history_practice
            (user_key, question_no, history_type, result_json, duration)
        VALUES
            (:user_key, :question_no, :history_type, :result_json, :duration)
        RETURNING history_key, user_key, question_no,
                  history_type, result_json, duration, ins_date
    """
    row = await database.fetch_one(
        query,
        values={
            "user_key": user_key,
            "question_no": body.question_no,
            "history_type": body.history_type,
            "result_json": _dump_json(body.result_json),
            "duration": body.duration,
        },
    )
    return HistoryPracticeOut(**{**dict(row), "result_json": _parse_json(row["result_json"])})


async def get_practice_history_list(
    user_key: int,
    skip: int,
    limit: int,
) -> List[HistoryPracticeOut]:
    query = """
        SELECT history_key, user_key, question_no,
               history_type, result_json, duration, ins_date
        FROM tb_history_practice
        WHERE del_yn = 'N' AND user_key = :user_key
        ORDER BY ins_date DESC
        LIMIT :limit OFFSET :skip
    """
    rows = await database.fetch_all(
        query, values={"user_key": user_key, "limit": limit, "skip": skip}
    )
    return [
        HistoryPracticeOut(**{**dict(r), "result_json": _parse_json(r["result_json"])})
        for r in rows
    ]
