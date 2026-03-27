from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import SocialLoginRequest, LoginResponse, UserOut
from app.core.security import create_access_token
from app.core.deps import get_current_user
from app.crud import auth as crud

router = APIRouter()


@router.post("/social-login", response_model=LoginResponse, summary="소셜 로그인")
async def social_login(body: SocialLoginRequest):
    """
    소셜 로그인 (Google, Apple, Kakao 등).
    프론트에서 OAuth 인증 후 provider_id + provider_type + email 전달.
    신규 유저면 자동 생성, 기존 유저면 조회 후 JWT 반환.
    """
    user = await crud.get_user_by_provider(body.provider_id, body.provider_type)
    if user is None:
        user = await crud.create_user(body)

    token = create_access_token(user.user_key)
    return LoginResponse(access_token=token, user=user)


@router.get("/me", response_model=UserOut, summary="내 정보 조회")
async def get_me(user_key: int = Depends(get_current_user)):
    user = await crud.get_user_by_key(user_key)
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user


@router.delete("/me", summary="회원 탈퇴")
async def delete_me(user_key: int = Depends(get_current_user)):
    await crud.soft_delete_user(user_key)
    return {"message": "탈퇴 처리되었습니다."}
