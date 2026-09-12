from contextlib import asynccontextmanager
# from sqlalchemy.orm import Mapped, mapped_column
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.base import Base
from app.db.session import engine

from app.api.routers.task import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

book: str = ''

@app.get('/')
def read_base_page():
    return {'message': f'Любимая книга {book}'}


# @app.post('/')
# def set_book(payload: BookSchema):
#     global book
#     book = payload.book
#     return {'message': f'Любимая книга {book}'}



# endpoints /category



# class CategoryORM(Base):
#     __tablename__ = "categories"

#     name: Mapped[str]


# class CategorySchema(BaseModel):
#     id: str
#     name: str | None = Field(max_length=25, min_length=3, default=None)


# class CategoryCreateSchema(BaseModel):
#     name: str


# class CategoryUpdateSchema(BaseModel):
#     name: str | None = Field(max_length=25, min_length=3, default=None)


# # categories: list[TaskSchema] = []


# def categ_ory_orm_to_model(category_orm:CategoryORM) -> CategorySchema:
#     return CategorySchema(
#         id=category_orm.id,
#         name=category_orm.name,
#     )


# @app.get('/categories')
# def read_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
#     categories_from_db = db.scalars(select(CategoryORM)).all()
#     return [categ_ory_orm_to_model(category) for category in categories_from_db]


# @app.post('/categories', status_code=status.HTTP_201_CREATED)
# def create_categories(payload: CategoryCreateSchema, db: Session = Depends(get_db)) -> CategorySchema:
#     new_category = CategoryORM(
#                                 name=payload.name
#                                 )

#     db.add(new_category)
#     db.commit()

#     return categ_ory_orm_to_model(new_category)


# @app.patch('/categories/{id}')
# def update_category(id: str, payload: CategoryUpdateSchema, db: Session = Depends(get_db)) -> CategorySchema:
#     category_for_update = db.get(CategoryORM, id)

#     if payload.name:
#         category_for_update.name = payload.name

#     db.commit()

#     return categ_ory_orm_to_model(category_for_update)


# @app.delete('/categories/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_category(id: str, db: Session = Depends(get_db)):
#     category_for_delete = db.get(CategoryORM, id)

#     db.delete(category_for_delete)
#     db.commit()

#     return {"msg": "Category deleted"}
