from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.code import GroupCodeOut, GroupCodeWithCodesOut
from app.crud import code as crud

router = APIRouter()


@router.get("", response_model=List[GroupCodeOut], summary="코드 그룹 목록 조회")
async def list_group_codes():
    return await crud.get_group_code_list()


@router.get("/{group_code}", response_model=GroupCodeWithCodesOut, summary="특정 코드 그룹 + 코드 목록 조회")
async def get_group_codes(group_code: str):
    result = await crud.get_group_code_with_codes(group_code)
    if result is None:
        raise HTTPException(status_code=404, detail="코드 그룹을 찾을 수 없습니다.")
    return result
