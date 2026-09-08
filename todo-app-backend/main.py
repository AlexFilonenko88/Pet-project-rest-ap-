from uuid import uuid4
from uuid import UUID

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreateSchema(BaseModel):
    title: str   


class BookSchema(BaseModel):
    book: str


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


tasks: list[TaskSchema] = []
book: str = ''


@app.get('/')
def read_base_page():
    return {'message': f'Любимая книга {book}'}


@app.post('/')
def set_book(payload: BookSchema):
    global book
    book = payload.book
    return {'message': f'Любимая книга {book}'}


@app.get('/tasks')
def read_tasks() -> list[TaskSchema]:
    return tasks


@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(
                        id=str(uuid4()),
                        title=payload.title,
                        completed=False
                        )
    tasks.append(new_task)

    return new_task


@app.patch('/tasks/{task_id}')
def update_task(task_id: str, payload: TaskUpdateSchema):
    for task in tasks:
        if task.id == task_id:
            if payload.title:
                task.title = payload.title 
            if payload.completed is not None:
                task.completed = payload.completed

            return task       


@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)     
def delete_task(task_id):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)