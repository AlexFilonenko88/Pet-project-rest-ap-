from contextlib import asynccontextmanager
# from sqlalchemy.orm import Mapped, mapped_column
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.base import Base
from app.db.session import engine

from app.api.routers.task import router as task_router
from app.api.routers.index import router as index_router
from app.api.routers.category import router as category_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=index_router)
app.include_router(router=task_router)
app.include_router(router=category_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)





# endpoints /category


# # categories: list[TaskSchema] = []


# def categ_ory_orm_to_model(category_orm:CategoryORM) -> CategorySchema:
#     return CategorySchema(
#         id=category_orm.id,
#         name=category_orm.name,
#     )
