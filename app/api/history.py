from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from app.schemas.history import (
    HistoryExamCreate,
    HistoryExamOut,
    HistoryPracticeCreate,
    HistoryPracticeOut,
)
from app.core.deps import get_current_user
from app.crud import history as crud

router = APIRouter()


@router.post("/exam", response_model=HistoryExamOut, summary="시험 풀이 결과 저장")
async def save_exam_history(
    body: HistoryExamCreate,
    user_key: int = Depends(get_current_user),
):
    return await crud.create_exam_history(user_key, body)


@router.get("/exam", response_model=List[HistoryExamOut], summary="내 시험 풀이 히스토리 조회")
async def list_exam_history(
    exam_key: Optional[int] = Query(None, description="특정 시험으로 필터"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_key: int = Depends(get_current_user),
):
    return await crud.get_exam_history_list(user_key, exam_key, skip, limit)


@router.post("/practice", response_model=HistoryPracticeOut, summary="연습 풀이 결과 저장")
async def save_practice_history(
    body: HistoryPracticeCreate,
    user_key: int = Depends(get_current_user),
):
    return await crud.create_practice_history(user_key, body)


@router.get("/practice", response_model=List[HistoryPracticeOut], summary="내 연습 풀이 히스토리 조회")
async def list_practice_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_key: int = Depends(get_current_user),
):
    return await crud.get_practice_history_list(user_key, skip, limit)
