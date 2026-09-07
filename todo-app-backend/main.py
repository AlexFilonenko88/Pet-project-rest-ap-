from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

tasks = list[TaskSchema] = []


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: str


@app.get('/')
def read_base_page():
    return {'message': 'Hello World'}


@app.get('/tasks')
def read_tasks():
    return tasks


@app.post('/task')
def create_task(payload):
    new_task = TaskSchema
    tasks.append(new_task)