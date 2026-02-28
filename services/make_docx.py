from .ai import generate_json
from .make_docx_from_json import make_docx_from_json


async def make_docx(request: str, user_id: int, num: int = 0) -> str:
    json_data = await generate_json(request=request)
    filename = make_docx_from_json(json_data, user_id, num)

    return filename