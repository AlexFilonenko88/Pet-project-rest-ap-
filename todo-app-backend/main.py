from contextlib import asynccontextmanager
from unicodedata import category
from uuid import uuid4

from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))


class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


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


book: str = ''


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


def task_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(
        id=task_orm.id,
        title=task_orm.title,
        completed=task_orm.completed,
    )


@app.get('/')
def read_base_page():
    return {'message': f'Любимая книга {book}'}


@app.post('/')
def set_book(payload: BookSchema):
    global book
    book = payload.book
    return {'message': f'Любимая книга {book}'}


@app.get('/tasks')
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_to_model(task) for task in tasks_from_db]


@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskORM(
                        title=payload.title,
                        completed=False
                        )
    db.add(new_task)
    db.commit()

    return task_to_model(new_task)


@app.patch('/tasks/{task_id}')
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    task_for_update = db.get(TaskORM, task_id)

    if payload.title:
        task_for_update.title = payload.title
    if payload.completed is not None:
        task_for_update.completed = payload.completed

    db.commit()

    return task_to_model(task_for_update)


@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id, db: Session = Depends(get_db)) -> None:
    task_for_delete = db.get(TaskORM, task_id)

    db.delete(task_for_delete)
    db.commit()

    return {"msg": "Task deleted"}



# endpoints /category



class CategoryORM(Base):
    __tablename__ = "categories"

    name: Mapped[str]


class CategorySchema(BaseModel):
    id: str
    name: str | None = Field(max_length=25, min_length=3, default=None)


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str | None = Field(max_length=25, min_length=3, default=None)


# categories: list[TaskSchema] = []


def category_to_model(category_orm:CategoryORM) -> CategorySchema:
    return CategorySchema(
        id=category_orm.id,
        name=category_orm.name,
    )


@app.get('/categories')
def read_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
    categories_from_db = db.scalars(select(CategoryORM)).all()
    return [category_to_model(category) for category in categories_from_db]


@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_categories(payload: CategoryCreateSchema, db: Session = Depends(get_db)) -> CategorySchema:
    new_category = CategoryORM(
                                name=payload.name
                                )

    db.add(new_category)
    db.commit()

    return category_to_model(new_category)


@app.patch('/categories/{id}')
def update_category(id: str, payload: CategoryUpdateSchema, db: Session = Depends(get_db)) -> CategorySchema:
    category_for_update = db.get(CategoryORM, id)

    if payload.name:
        category_for_update.name = payload.name

    db.commit()

    return category_to_model(category_for_update)


@app.delete('/categories/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: str, db: Session = Depends(get_db)):
    category_for_delete = db.get(CategoryORM, id)

    db.delete(category_for_delete)
    db.commit()

    return {"msg": "Category deleted"}
