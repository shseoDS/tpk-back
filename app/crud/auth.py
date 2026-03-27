from typing import Optional
from app.db.database import database
from app.schemas.user import UserOut, SocialLoginRequest


async def get_user_by_provider(provider_id: str, provider_type: str) -> Optional[UserOut]:
    query = """
        SELECT user_key, email, provider_type, ins_date
        FROM tb_user
        WHERE provider_id = :provider_id
          AND provider_type = :provider_type
          AND del_yn = 'N'
    """
    row = await database.fetch_one(
        query,
        values={"provider_id": provider_id, "provider_type": provider_type},
    )
    return UserOut(**dict(row)) if row else None


async def create_user(body: SocialLoginRequest) -> UserOut:
    query = """
        INSERT INTO tb_user (email, provider_id, provider_type)
        VALUES (:email, :provider_id, :provider_type)
        RETURNING user_key, email, provider_type, ins_date
    """
    row = await database.fetch_one(
        query,
        values={
            "email": body.email,
            "provider_id": body.provider_id,
            "provider_type": body.provider_type,
        },
    )
    return UserOut(**dict(row))


async def get_user_by_key(user_key: int) -> Optional[UserOut]:
    query = """
        SELECT user_key, email, provider_type, ins_date
        FROM tb_user
        WHERE user_key = :user_key AND del_yn = 'N'
    """
    row = await database.fetch_one(query, values={"user_key": user_key})
    return UserOut(**dict(row)) if row else None


async def soft_delete_user(user_key: int) -> None:
    query = """
        UPDATE tb_user
        SET del_yn = 'Y', upd_date = CURRENT_TIMESTAMP
        WHERE user_key = :user_key
    """
    await database.execute(query, values={"user_key": user_key})
