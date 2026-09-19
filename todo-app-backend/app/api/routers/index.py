from fastapi import APIRouter

from app.schemas.index import BookSchema, book

router = APIRouter()


@router.get("/")
def read_base_page():
    return {"message": f"Любимая книга {book}"}


@router.post("/")
def set_book(payload: BookSchema):
    global book
    book = payload.book
    return {"message": f"Любимая книга {book}"}
