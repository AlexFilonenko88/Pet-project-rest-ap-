from pydantic import BaseModel


class BookSchema(BaseModel):
    book: str


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None
