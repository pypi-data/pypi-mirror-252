import json

from fastapi import status
from fastapi.responses import JSONResponse
from beanie import Document, PydanticObjectId


async def return_response(data=None, message=None, code=None, page_no=None, total_num=None, page_size=None,
                          status_code=status.HTTP_200_OK):
    def _serialize(data):
        if isinstance(data, Document) and isinstance(data.id, PydanticObjectId):
            data = json.loads(data.to_json())
        return data

    ret = {}
    if isinstance(data, list):
        data = [_serialize(d) for d in data]
    else:
        data = _serialize(data)

    if code:
        ret['code'] = code

    if message:
        ret['message'] = message

    if page_no and total_num and page_size:
        ret['data'] = {
            'page_no': page_no,
            'total_num': total_num,
            'page_size': page_size,
            'page_data': data
        }
    else:
        ret['data'] = data

    return JSONResponse(status_code=status_code, content=ret)
