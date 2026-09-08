from uuid import uuid4
from uuid import UUID

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


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



# endpoints /category



class CategorySchema(BaseModel):
    id: str
    name: str | None = Field(max_length=25, min_length=3, default=None)


class CategoryCreateSchema(BaseModel):
    name: str   


class CategoryUpdateSchema(BaseModel):
    name: str | None = Field(max_length=25, min_length=3, default=None)


categories: list[TaskSchema] = []


@app.get('/categories')
def read_categories() -> list[CategorySchema]:
    return categories


@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_categories(payload: CategoryCreateSchema) -> CategorySchema:
    new_category = CategorySchema(
                        id=str(uuid4()),
                        name=payload.name
                        )
    
    categories.append(new_category)

    return new_category


@app.patch('/categories/{id}')
def update_category(id: str, payload: CategoryUpdateSchema):
    for category in categories:
        if category.id == id:
            if payload.name:
                category.name = payload.name 

            return category               


@app.delete('/categories/{id}', status_code=status.HTTP_204_NO_CONTENT)     
def delete_category(id):
    for category in categories:
        if category.id == id:
            categories.remove(category)        