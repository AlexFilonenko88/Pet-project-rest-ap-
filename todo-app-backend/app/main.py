import logging
from contextlib import asynccontextmanager
from time import perf_counter

from app.api.routers.category import router as category_router
from app.api.routers.index import router as index_router
from app.api.routers.task import router as task_router
from app.core.logging import configure_logging
from app.db.session import engine
from app.models.base import Base

# from sqlalchemy.orm import Mapped, mapped_column
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     Base.metadata.create_all(bind=engine)
#     yield

configure_logging()

# app = FastAPI(lifespan=lifespan)
app = FastAPI()
logger = logging.getLogger("app.middleware")

app.state.request_count = 0

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def count_requests(request: Request, call_next) -> Response:
    request.app.state.request_count += 1
    current_number = request.app.state.request_count

    response: Response = await call_next(request)
    response.headers["X-Request-Number"] = str(current_number)
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    started_at = perf_counter()
    try:
        response: Response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


app.include_router(router=index_router)
app.include_router(router=task_router)
app.include_router(router=category_router)
