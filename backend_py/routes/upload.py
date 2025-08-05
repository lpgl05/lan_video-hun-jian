from fastapi import APIRouter

router = APIRouter()

@router.post("/api/upload")
def upload_file():
    # TODO: 处理文件上传
    return {"msg": "文件上传成功"}

# ...可继续补充其他上传相关接口...
