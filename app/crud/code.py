from typing import Optional, List
from app.db.database import database
from app.schemas.code import GroupCodeOut, CodeOut, GroupCodeWithCodesOut


async def get_group_code_list() -> List[GroupCodeOut]:
    query = """
        SELECT group_code, group_name, group_desc
        FROM tb_group_code
        WHERE del_yn = 'N'
        ORDER BY group_code
    """
    rows = await database.fetch_all(query)
    return [GroupCodeOut(**dict(r)) for r in rows]


async def get_group_code_with_codes(group_code: str) -> Optional[GroupCodeWithCodesOut]:
    group_query = """
        SELECT group_code, group_name, group_desc
        FROM tb_group_code
        WHERE group_code = :group_code AND del_yn = 'N'
    """
    group_row = await database.fetch_one(group_query, values={"group_code": group_code})
    if group_row is None:
        return None

    codes_query = """
        SELECT group_code, code, code_name, code_desc, sort_order
        FROM tb_code
        WHERE group_code = :group_code AND del_yn = 'N'
        ORDER BY sort_order, code
    """
    code_rows = await database.fetch_all(codes_query, values={"group_code": group_code})

    return GroupCodeWithCodesOut(
        **dict(group_row),
        codes=[CodeOut(**dict(r)) for r in code_rows],
    )
