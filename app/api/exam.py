from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.exam import (
    ExamListOut,
    ExamDetailOut,
    ExamQuestionOut,
    ExamAnswerOut,
    ExamInstructionOut,
    ExamFileOut,
)
from app.core.deps import get_current_user
from app.crud import exam as crud

router = APIRouter()


@router.get("", response_model=List[ExamListOut], summary="시험 목록 조회")
async def list_exams(
    exam_year: Optional[str] = Query(None, description="시험 연도 (예: 2024)"),
    exam_type: Optional[str] = Query(None, description="시험 유형 (예: TOPIK1, TOPIK2)"),
    tpk_level: Optional[str] = Query(None, description="토픽 레벨"),
    section: Optional[str] = Query(None, description="영역 코드"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    return await crud.get_exam_list(exam_year, exam_type, tpk_level, section, skip, limit)


@router.get("/{exam_key}", response_model=ExamDetailOut, summary="시험 상세 조회")
async def get_exam(exam_key: int):
    result = await crud.get_exam_detail(exam_key)
    if result is None:
        raise HTTPException(status_code=404, detail="시험을 찾을 수 없습니다.")
    return result


@router.get("/{exam_key}/questions", response_model=List[ExamQuestionOut], summary="시험 문제 목록")
async def list_exam_questions(exam_key: int):
    return await crud.get_exam_questions(exam_key)


@router.get("/{exam_key}/questions/{question_no}", response_model=ExamQuestionOut, summary="시험 문제 개별 조회")
async def get_exam_question(exam_key: int, question_no: int):
    result = await crud.get_exam_question(exam_key, question_no)
    if result is None:
        raise HTTPException(status_code=404, detail="문제를 찾을 수 없습니다.")
    return result


@router.get("/{exam_key}/answers", response_model=List[ExamAnswerOut], summary="시험 전체 정답 조회")
async def get_exam_answers(
    exam_key: int,
    user_key: int = Depends(get_current_user),
):
    return await crud.get_exam_answers(exam_key)


@router.get("/{exam_key}/answers/{question_no}", response_model=ExamAnswerOut, summary="시험 문제 정답 조회")
async def get_exam_answer(
    exam_key: int,
    question_no: int,
    user_key: int = Depends(get_current_user),
):
    result = await crud.get_exam_answer(exam_key, question_no)
    if result is None:
        raise HTTPException(status_code=404, detail="정답을 찾을 수 없습니다.")
    return result


@router.get("/{exam_key}/instructions", response_model=List[ExamInstructionOut], summary="시험 지시문 조회")
async def get_exam_instructions(exam_key: int):
    return await crud.get_exam_instructions(exam_key)


@router.get("/{exam_key}/files", response_model=List[ExamFileOut], summary="시험 PDF 파일 목록")
async def get_exam_files(exam_key: int):
    return await crud.get_exam_files(exam_key)
