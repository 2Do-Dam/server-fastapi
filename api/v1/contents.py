from fastapi import APIRouter
from domain.contents.schemas import ContentCreate, Content
from typing import List
from domain.contents.services import list_contents, create_content

router = APIRouter()

@router.get("/", response_model=List[Content])
def list_contents_api():
    return list_contents()

@router.post("/", response_model=Content)
def create_content_api(content: ContentCreate):
    return create_content(content)
