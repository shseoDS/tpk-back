from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.practice import (
    PracticeQuestionOut,
    PracticeAnswerOut,
    PracticeQuestionWithAnswerOut,
)
from app.core.deps import get_current_user
from app.crud import practice as crud

router = APIRouter()


@router.get("/questions", response_model=List[PracticeQuestionOut], summary="연습 문제 목록 조회")
async def list_practice_questions(
    section: Optional[str] = Query(None, description="영역 (듣기, 읽기, 쓰기)"),
    question_type: Optional[str] = Query(None, description="문제 유형"),
    difficulty: Optional[str] = Query(None, description="난이도"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    return await crud.get_practice_questions(section, question_type, difficulty, skip, limit)


@router.get("/questions/{question_no}", response_model=PracticeQuestionOut, summary="연습 문제 개별 조회")
async def get_practice_question(question_no: int):
    result = await crud.get_practice_question(question_no)
    if result is None:
        raise HTTPException(status_code=404, detail="문제를 찾을 수 없습니다.")
    return result


@router.get("/questions/{question_no}/answer", response_model=PracticeAnswerOut, summary="연습 문제 정답 조회")
async def get_practice_answer(
    question_no: int,
    user_key: int = Depends(get_current_user),
):
    result = await crud.get_practice_answer(question_no)
    if result is None:
        raise HTTPException(status_code=404, detail="정답을 찾을 수 없습니다.")
    return result


@router.get("/questions/{question_no}/with-answer", response_model=PracticeQuestionWithAnswerOut, summary="연습 문제 + 정답 함께 조회")
async def get_practice_question_with_answer(
    question_no: int,
    user_key: int = Depends(get_current_user),
):
    result = await crud.get_practice_question_with_answer(question_no)
    if result is None:
        raise HTTPException(status_code=404, detail="문제를 찾을 수 없습니다.")
    return result
