from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from app.services.parser import parse_code, to_markdown

router = APIRouter()

class CodeIn(BaseModel):
    code: str
    filename: str = "main.py"

@router.post("/parse")
def parse_code_endpoint(data: CodeIn):
    result = parse_code(data.code, data.filename)
    return result

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8", errors="ignore")
    return parse_code(content, file.filename)

@router.post("/export")
def export_md(data: CodeIn):
    result = parse_code(data.code, data.filename)
    return {"markdown": to_markdown(result), "filename": data.filename}
